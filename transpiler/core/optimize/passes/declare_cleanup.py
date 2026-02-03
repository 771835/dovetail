# coding=utf-8
"""
声明清理 Pass

移除未使用的变量声明。
"""
from __future__ import annotations

from typing import Dict, Set, Optional

from transpiler.core.compile_config import CompileConfig
from transpiler.core.enums import OptimizationLevel
from transpiler.core.enums.types import ValueType
from transpiler.core.instructions import *
from transpiler.core.ir_builder import IRBuilder
from transpiler.core.optimize.base import IROptimizationPass
from transpiler.core.optimize.pass_metadata import PassMetadata, PassPhase
from transpiler.core.optimize.pass_registry import register_pass
from transpiler.core.symbols import Reference


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
        var_scopes (Dict[str, str]): 变量到其声明作用域的映射
        var_references (Dict[str, int]): 变量引用计数映射
        root_vars (Set[str]): 根变量集合
        scope_instructions (Dict[str, list]): 每个作用域中的指令列表
        _changed (bool): 标记优化过程中是否发生了变化
    """

    def __init__(self, builder: IRBuilder, config: CompileConfig):
        """初始化 DeclareCleanupPass 实例

        Args:
            builder (IRBuilder): IR构建器实例
            config (CompileConfig): 编译配置
        """
        super().__init__(builder, config)
        self.scope_tree: Dict[str, Optional[str]] = {}
        self.var_scopes: Dict[str, str] = {}
        self.var_references: Dict[str, int] = {}
        self.root_vars: Set[str] = set()
        self.scope_instructions: Dict[str, list] = {}
        self._changed: bool = False

    def execute(self) -> bool:
        """执行声明清理优化

        Returns:
            bool: 如果优化过程中发生了变化则返回True，否则返回False
        """
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

            if isinstance(instr, IRScopeBegin):
                scope_name = instr.get_operands()[0]
                parent = scope_stack[-1] if scope_stack else None
                self.scope_tree[scope_name] = parent
                scope_stack.append(scope_name)

            elif isinstance(instr, IRScopeEnd):
                if scope_stack:
                    scope_stack.pop()

    def _analyze_variable_usage(self) -> None:
        """分析变量使用

        该方法通过遍历所有指令来统计变量的使用情况，包括：
        - 变量声明位置
        - 变量引用次数
        - 作用域信息
        - 根变量识别
        """
        iterator = self.builder.__iter__()
        scope_stack = []
        current_scope = "global"

        while True:
            try:
                instr = next(iterator)
            except StopIteration:
                break

            # 处理作用域开始和结束
            if isinstance(instr, IRScopeBegin):
                scope_name = instr.get_operands()[0]
                scope_stack.append(scope_name)
                current_scope = scope_name
                self.scope_instructions[scope_name] = []
            elif isinstance(instr, IRScopeEnd):
                if scope_stack:
                    scope_stack.pop()
                    current_scope = scope_stack[-1] if scope_stack else "global"

            # 记录作用域中的指令
            if current_scope in self.scope_instructions:
                self.scope_instructions[current_scope].append(instr)

            # 分析不同类型的指令
            if isinstance(instr, IRDeclare):
                var = instr.get_operands()[0]
                self.var_scopes[var.name] = current_scope

            elif isinstance(instr, IRFunction):
                func = instr.get_operands()[0]
                for param in func.params:
                    self.root_vars.add(param.get_name())
                    self.var_references[param.get_name()] = self.var_references.get(param.get_name(), 0) + 1

            elif isinstance(instr, (IRCall, IRCallMethod)):
                if isinstance(instr, IRCall):
                    result_var, func, args = instr.get_operands()
                else:
                    result_var, _, func, args = instr.get_operands()

                if result_var:
                    self.var_references[result_var.name] = self.var_references.get(result_var.name, 0) + 1

                for param_name, arg_ref in args.items():
                    if isinstance(arg_ref, Reference) and arg_ref.value_type == ValueType.VARIABLE:
                        self.var_references[arg_ref.get_name()] = self.var_references.get(arg_ref.get_name(), 0) + 1

            elif isinstance(instr, IRReturn):
                value = instr.get_operands()[0]
                if isinstance(value, Reference) and value.value_type == ValueType.VARIABLE:
                    self.var_references[value.get_name()] = self.var_references.get(value.get_name(), 0) + 1

            elif isinstance(instr, IRCondJump):
                cond_var = instr.get_operands()[0]
                self.var_references[cond_var.name] = self.var_references.get(cond_var.name, 0) + 1

            elif isinstance(instr, IRAssign):
                target, source = instr.get_operands()
                if source.value_type == ValueType.VARIABLE:
                    self.var_references[source.get_name()] = self.var_references.get(source.get_name(), 0) + 1
                self.var_references[target.name] = self.var_references.get(target.name, 0)

            elif isinstance(instr, (IRBinaryOp, IRCompare, IRUnaryOp)):
                operands = instr.get_operands()
                result = operands[0]
                self.var_references[result.name] = self.var_references.get(result.name, 0)

                for op in operands[2:]:
                    if isinstance(op, Reference) and op.value_type == ValueType.VARIABLE:
                        self.var_references[op.get_name()] = self.var_references.get(op.get_name(), 0) + 1

            elif isinstance(instr, IRCast):
                target, dtype, source = instr.get_operands()
                if isinstance(source, Reference) and source.value_type == ValueType.VARIABLE:
                    self.var_references[source.get_name()] = self.var_references.get(source.get_name(), 0) + 1

    def _remove_dead_declarations(self) -> None:
        """删除无效的变量声明"""
        iterator = self.builder.__iter__()
        current_scope = "global"

        while True:
            try:
                instr = next(iterator)
            except StopIteration:
                break

            if isinstance(instr, IRScopeBegin):
                current_scope = instr.get_operands()[0]

            elif isinstance(instr, IRDeclare):
                var = instr.get_operands()[0]
                var_name = var.name

                if (var_name in self.root_vars or
                        self.var_references.get(var_name, 0) > 0 or
                        self._is_scope_root(var_name, current_scope) or
                        self._is_used_in_nested_scope(var_name, current_scope)):
                    continue

                iterator.remove_current()
                self._changed = True

    def _is_scope_root(self, var_name: str, scope: str) -> bool:
        """判断变量是否是作用域根变量

        Args:
            var_name (str): 变量名称
            scope (str): 当前作用域名称

        Returns:
            bool: 如果变量是作用域根变量则返回True，否则返回False
        """
        parent = self.scope_tree.get(scope)
        if not parent:
            return False
        return self.var_scopes.get(var_name) == parent

    def _is_used_in_nested_scope(self, var_name: str, scope: str) -> bool:
        """判断变量是否在嵌套作用域中被使用

        Args:
            var_name (str): 变量名称
            scope (str): 当前作用域名称

        Returns:
            bool: 如果变量在嵌套作用域中被使用则返回True，否则返回False
        """
        for nested_scope, parent in self.scope_tree.items():
            if parent == scope:
                if self._is_var_used_in_scope(var_name, nested_scope):
                    return True
        return False

    def _is_var_used_in_scope(self, var_name: str, scope: str) -> bool:
        """判断变量是否在特定作用域中被使用

        Args:
            var_name (str): 变量名称
            scope (str): 要检查的作用域名称

        Returns:
            bool: 如果变量在指定作用域中被使用则返回True，否则返回False
        """
        if scope not in self.scope_instructions:
            return False

        for instr in self.scope_instructions[scope]:
            for operand in instr.get_operands():
                if isinstance(operand, Reference) and operand.get_name() == var_name:
                    return True
        return False
