# coding=utf-8
"""
声明清理 Pass

移除未使用的变量声明。
"""
from __future__ import annotations

from typing import Dict, Set

from dovetail.core.compile_config import CompileConfig
from dovetail.core.enums import OptimizationLevel
from dovetail.core.enums.types import ValueType
from dovetail.core.instructions import *
from dovetail.core.ir_builder import IRBuilder
from dovetail.core.optimize.base import IROptimizationPass
from dovetail.core.optimize.pass_metadata import PassMetadata, PassPhase
from dovetail.core.optimize.pass_registry import register_pass
from dovetail.core.symbols import Reference


@register_pass(PassMetadata(
    name="declare_cleanup",
    display_name="声明清理",
    description="移除未使用的变量声明",
    level=OptimizationLevel.O1,
    phase=PassPhase.CLEANUP,
    provided_features=("cleaned_declarations",)
))
class DeclareCleanupPass(IROptimizationPass):
    """声明清理优化 Pass

    Attributes:
        scope_tree (Dict[str, Optional[str]]): 作用域树结构，键为作用域名称，值为父作用域
        var_scopes (Dict[str, str]): 变量到其声明作用域的映射，key 格式为 "scope::var"
        var_references (Dict[str, int]): 变量引用计数映射，key 格式为 "scope::var"
        root_vars (Set[str]): 根变量集合，格式为 "scope::var"
        scope_instructions (Dict[str, list]): 每个作用域中的指令列表
        _changed (bool): 标记优化过程中是否发生了变化
    """

    def __init__(self, builder: IRBuilder, config: CompileConfig):
        super().__init__(builder, config)
        self.scope_tree: Dict[str, Optional[str]] = {}
        self.var_scopes: Dict[str, str] = {}
        self.var_references: Dict[str, int] = {}
        self.root_vars: Set[str] = set()
        self.scope_instructions: Dict[str, list] = {}
        self._changed: bool = False

    # ------------------------------------------------------------------ #
    #  内部工具：统一 key 格式                                              #
    # ------------------------------------------------------------------ #

    @staticmethod
    def _key(scope: str, var_name: str) -> str:
        """生成带作用域前缀的变量 key，避免不同作用域同名变量互相污染"""
        return f"{scope}::{var_name}"

    def _ref_add(self, scope: str, var_name: str, delta: int = 1) -> None:
        k = self._key(scope, var_name)
        self.var_references[k] = self.var_references.get(k, 0) + delta

    def _ref_init(self, scope: str, var_name: str) -> None:
        """确保变量存在于引用表中，但不增加计数（用于 target 侧）"""
        k = self._key(scope, var_name)
        if k not in self.var_references:
            self.var_references[k] = 0

    def _ref_get(self, scope: str, var_name: str) -> int:
        return self.var_references.get(self._key(scope, var_name), 0)

    # ------------------------------------------------------------------ #

    def execute(self) -> bool:
        self._changed = False
        self._build_scope_tree()
        self._analyze_variable_usage()
        self._remove_dead_declarations()
        return self._changed

    def _build_scope_tree(self) -> None:
        """构建作用域树结构"""
        iterator = self.builder.__iter__()
        scope_stack = []

        while True:
            try:
                instr = next(iterator)
            except StopIteration:
                break

            if instr.opcode == IROpCode.SCOPE_BEGIN:
                scope_name = instr.get_operands()[0]
                parent = scope_stack[-1] if scope_stack else None
                self.scope_tree[scope_name] = parent
                scope_stack.append(scope_name)

            elif instr.opcode == IROpCode.SCOPE_END:
                if scope_stack:
                    scope_stack.pop()

    def _analyze_variable_usage(self) -> None:
        """分析变量使用，以 scope::var 为 key 隔离不同作用域的同名变量"""
        iterator = self.builder.__iter__()
        scope_stack = []
        current_scope = "global"

        while True:
            try:
                instr = next(iterator)
            except StopIteration:
                break

            if instr.opcode == IROpCode.SCOPE_BEGIN:
                scope_name = instr.get_operands()[0]
                scope_stack.append(scope_name)
                current_scope = scope_name
                self.scope_instructions[scope_name] = []

            elif instr.opcode == IROpCode.SCOPE_END:
                if scope_stack:
                    scope_stack.pop()
                    current_scope = scope_stack[-1] if scope_stack else "global"

            if current_scope in self.scope_instructions:
                self.scope_instructions[current_scope].append(instr)

            if instr.opcode == IROpCode.DECLARE:
                var = instr.get_operands()[0]
                # var_scopes 也用带 scope 前缀的 key 存，保持一致
                self.var_scopes[self._key(current_scope, var.name)] = current_scope
                self._ref_init(current_scope, var.name)

            elif instr.opcode == IROpCode.FUNCTION:
                func = instr.get_operands()[0]
                for param in func.params:
                    self.root_vars.add(self._key(current_scope, param.get_name()))
                    self._ref_add(current_scope, param.get_name())

            elif instr.opcode == IROpCode.CALL_METHOD:
                if instr.opcode == IROpCode.CALL:
                    result_var, func, args = instr.get_operands()
                else:
                    result_var, _, func, args = instr.get_operands()

                if result_var:
                    self._ref_add(current_scope, result_var.name)

                for param_name, arg_ref in args.items():
                    if isinstance(arg_ref, Reference) and arg_ref.value_type == ValueType.VARIABLE:
                        self._ref_add(current_scope, arg_ref.get_name())

            elif instr.opcode == IROpCode.RETURN:
                value = instr.get_operands()[0]
                if isinstance(value, Reference) and value.value_type == ValueType.VARIABLE:
                    self._ref_add(current_scope, value.get_name())

            elif instr.opcode == IROpCode.COND_JUMP:
                cond_var = instr.get_operands()[0]
                self._ref_add(current_scope, cond_var.name)

            elif instr.opcode == IROpCode.ASSIGN:
                target, source = instr.get_operands()
                if source.value_type == ValueType.VARIABLE:
                    self._ref_add(current_scope, source.get_name())
                self._ref_init(current_scope, target.name)

            elif instr.opcode in (IROpCode.BINARY_OP, IROpCode.UNARY_OP, IROpCode.COMPARE):
                operands = instr.get_operands()
                result = operands[0]
                self._ref_init(current_scope, result.name)

                for op in operands[2:]:
                    if isinstance(op, Reference) and op.value_type == ValueType.VARIABLE:
                        self._ref_add(current_scope, op.get_name())

            elif instr.opcode == IROpCode.CAST:
                target, dtype, source = instr.get_operands()
                if isinstance(source, Reference) and source.value_type == ValueType.VARIABLE:
                    self._ref_add(current_scope, source.get_name())

    def _remove_dead_declarations(self) -> None:
        """删除无效的变量声明"""
        iterator = self.builder.__iter__()
        current_scope = "global"

        while True:
            try:
                instr = next(iterator)
            except StopIteration:
                break

            if instr.opcode == IROpCode.SCOPE_BEGIN:
                current_scope = instr.get_operands()[0]

            elif instr.opcode == IROpCode.DECLARE:
                var = instr.get_operands()[0]
                var_name = var.name
                scoped_key = self._key(current_scope, var_name)

                if (scoped_key in self.root_vars or
                        self._ref_get(current_scope, var_name) > 0 or
                        self._is_scope_root(var_name, current_scope) or
                        self._is_used_in_nested_scope(var_name, current_scope)):
                    continue

                iterator.remove_current()
                self._changed = True

    def _is_scope_root(self, var_name: str, scope: str) -> bool:
        """判断变量是否是作用域根变量"""
        parent = self.scope_tree.get(scope)
        if not parent:
            return False
        return self.var_scopes.get(self._key(scope, var_name)) == parent

    def _is_used_in_nested_scope(self, var_name: str, scope: str) -> bool:
        """判断变量是否在嵌套作用域中被使用"""
        for nested_scope, parent in self.scope_tree.items():
            if parent == scope:
                if self._is_var_used_in_scope(var_name, nested_scope):
                    return True
        return False

    def _is_var_used_in_scope(self, var_name: str, scope: str) -> bool:
        """判断变量是否在特定作用域中被使用"""
        if scope not in self.scope_instructions:
            return False

        for instr in self.scope_instructions[scope]:
            for operand in instr.get_operands():
                if isinstance(operand, Reference) and operand.get_name() == var_name:
                    return True
        return False
