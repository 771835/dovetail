# coding=utf-8
"""
死代码消除 Pass

基于作用域感知的活跃变量分析（Liveness Analysis），
移除永远不会被使用的变量赋值和计算结果。

算法概述：
  第一遍（_collect_defs_and_uses）：
    扫描所有指令，以 "scope::var_name" 为唯一键，
    建立 定义表（defs）、使用表（uses）和 根活跃集（roots）。

  第二遍（_propagate_liveness）：
    从 roots 出发，沿 use → def 方向反向传播，
    标记所有可达的活跃变量。

  第三遍（_remove_dead_code）：
    删除结果变量不在活跃集中的指令。
"""
from __future__ import annotations

from collections import deque

from dovetail.core.compile_config import CompileConfig
from dovetail.core.enums import OptimizationLevel
from dovetail.core.enums.types import ValueType, VariableType
from dovetail.core.instructions import (
    IROpCode
)
from dovetail.core.ir_builder import IRBuilder
from dovetail.core.optimize.base import IROptimizationPass
from dovetail.core.optimize.pass_metadata import PassMetadata, PassPhase
from dovetail.core.optimize.pass_registry import register_pass
from dovetail.core.symbols import Reference

# ---- 类型别名 ----
_VarKey = str  # "scope_name::var_name"
_DefMap = dict[_VarKey, _VarKey]  # result_key → 产生它的指令的唯一标识（此处复用 result_key）
_UseMap = dict[_VarKey, set[_VarKey]]  # operand_key → {依赖它的 result_key 集合}


def _make_key(scope: str, var_name: str) -> _VarKey:
    """构造作用域限定的变量唯一键。"""
    return f"{scope}::{var_name}"


@register_pass(PassMetadata(
    name="dead_code_elimination",
    display_name="死代码消除",
    description="移除永远不会使用的变量赋值和计算结果",
    level=OptimizationLevel.O1,
    phase=PassPhase.CLEANUP,
    provided_features=("cleaned_dead_code",)
))
class DeadCodeEliminationPass(IROptimizationPass):
    """
    死代码消除优化 Pass

    以 "scope::var_name" 作为变量唯一键，避免不同作用域的同名变量相互污染。
    不依赖 Variable 对象的 id() 或内存地址，依赖名字。
    """

    def __init__(self, builder: IRBuilder, config: CompileConfig):
        super().__init__(builder, config)

        # 定义图：result_key → set of operand_keys（该结果依赖哪些操作数）
        self._def_graph: dict[_VarKey, set[_VarKey]] = {}

        # 反向使用图：operand_key → set of result_keys（哪些结果依赖该操作数）
        self._use_graph: dict[_VarKey, set[_VarKey]] = {}

        # 活跃变量集（_VarKey）
        self._live: set[_VarKey] = set()

        # 已声明变量的键集合，用于过滤从未声明的幽灵变量
        self._declared: set[_VarKey] = set()

        self._changed = False

    # ------------------------------------------------------------------ #
    #  公开接口                                                            #
    # ------------------------------------------------------------------ #

    def execute(self) -> bool:
        self._changed = False
        self._prescan_declarations()  # 先收集所有声明
        roots = self._collect_defs_and_uses()
        self._propagate_liveness(roots)
        self._remove_dead_code()
        return self._changed

    # ------------------------------------------------------------------ #
    #  第一遍：收集定义、使用关系，确定活跃根                                  #
    # ------------------------------------------------------------------ #

    def _prescan_declarations(self) -> None:
        """预扫描，收集所有变量声明及其所在作用域，填充 _declared。"""
        scope_stack: list[str] = ["global"]
        for instr in self.builder.get_instructions():
            if instr.opcode == IROpCode.SCOPE_BEGIN:
                scope_stack.append(instr.get_operands()[0])
            elif instr.opcode == IROpCode.SCOPE_END:
                if len(scope_stack) > 1:
                    scope_stack.pop()
            elif instr.opcode == IROpCode.DECLARE:
                var = instr.get_operands()[0]
                self._declared.add(_make_key(scope_stack[-1], var.get_name()))

    def _collect_defs_and_uses(self) -> set[_VarKey]:
        """
        单遍扫描 IR，建立定义/使用图，同时收集活跃根。

        活跃根定义：
          - 函数参数（VariableType.PARAMETER）
          - 函数返回变量（VariableType.RETURN）
          - IRReturn 的返回值
          - IRCondJump 的条件变量
          - IRCall / IRCallMethod 的所有实参及 obj
          - 有外部可见副作用的指令（CALL、CALL_METHOD）的结果变量
            （即使结果没人用，调用本身也不能删）

        Returns:
            roots: 初始活跃变量键集合
        """
        roots: set[_VarKey] = set()
        scope_stack: list[str] = ["global"]

        for instr in self.builder.get_instructions():
            current_scope = scope_stack[-1]

            opcode = instr.opcode

            if opcode == IROpCode.SCOPE_BEGIN:
                scope_stack.append(instr.get_operands()[0])
                continue

            if opcode == IROpCode.SCOPE_END:
                if len(scope_stack) > 1:
                    scope_stack.pop()
                continue

            # ---------- DECLARE ----------
            if opcode == IROpCode.DECLARE:
                var = instr.get_operands()[0]
                key = _make_key(current_scope, var.get_name())
                self._declared.add(key)

                # 参数和返回槽天然活跃
                if var.var_type in (VariableType.PARAMETER, VariableType.RETURN):
                    roots.add(key)
                continue

            # ---------- ASSIGN ----------
            if opcode == IROpCode.ASSIGN:
                target, source = instr.get_operands()
                target_key = self._lookup_key(target.get_name(), current_scope, scope_stack)
                self._ensure_def(target_key)

                if isinstance(source, Reference) and source.value_type == ValueType.VARIABLE:
                    src_key = self._lookup_key(source.get_name(), current_scope, scope_stack)
                    self._add_edge(target_key, src_key)
                continue

            # ---------- BINARY_OP / COMPARE ----------
            if opcode in (IROpCode.BINARY_OP, IROpCode.COMPARE):
                operands = instr.get_operands()
                result, _op, left, right = operands[0], operands[1], operands[2], operands[3]
                result_key = _make_key(current_scope, result.get_name())
                self._ensure_def(result_key)

                for ref in (left, right):
                    if isinstance(ref, Reference) and ref.value_type == ValueType.VARIABLE:
                        op_key = self._lookup_key(ref.get_name(), current_scope, scope_stack)
                        self._add_edge(result_key, op_key)
                continue

            # ---------- UNARY_OP ----------
            if opcode == IROpCode.UNARY_OP:
                result, _op, operand = instr.get_operands()
                result_key = _make_key(current_scope, result.get_name())
                self._ensure_def(result_key)

                if isinstance(operand, Reference) and operand.value_type == ValueType.VARIABLE:
                    op_key = self._lookup_key(operand.get_name(), current_scope, scope_stack)
                    self._add_edge(result_key, op_key)
                continue

            # ---------- CAST ----------
            if opcode == IROpCode.CAST:
                result, _dtype, source = instr.get_operands()
                result_key = _make_key(current_scope, result.get_name())
                self._ensure_def(result_key)

                if isinstance(source, Reference) and source.value_type == ValueType.VARIABLE:
                    src_key = self._lookup_key(source.get_name(), current_scope, scope_stack)
                    self._add_edge(result_key, src_key)
                continue

            # ---------- CALL ----------
            if opcode == IROpCode.CALL:
                result, _func, args = instr.get_operands()

                # 调用本身有外部副作用，result 强制活跃（即使没人读返回值）
                if result is not None:
                    result_key = _make_key(current_scope, result.get_name())
                    self._ensure_def(result_key)
                    roots.add(result_key)

                # 所有实参活跃
                for arg_ref in args.values():
                    if isinstance(arg_ref, Reference) and arg_ref.value_type == ValueType.VARIABLE:
                        roots.add(self._lookup_key(arg_ref.get_name(), current_scope, scope_stack))
                continue

            # ---------- CALL_METHOD ----------
            if opcode == IROpCode.CALL_METHOD:
                result, obj_ref, _method, args = instr.get_operands()

                if result is not None:
                    result_key = _make_key(current_scope, result.get_name())
                    self._ensure_def(result_key)
                    roots.add(result_key)

                # obj 本身也是操作数，必须活跃
                if isinstance(obj_ref, Reference) and obj_ref.value_type == ValueType.VARIABLE:
                    roots.add(self._lookup_key(obj_ref.get_name(), current_scope, scope_stack))

                for arg_ref in args.values():
                    if isinstance(arg_ref, Reference) and arg_ref.value_type == ValueType.VARIABLE:
                        roots.add(self._lookup_key(arg_ref.get_name(), current_scope, scope_stack))
                continue

            # ---------- RETURN ----------
            if opcode == IROpCode.RETURN:
                operands = instr.get_operands()
                # IRReturn(value=None) 时 operands 可能是 (None,) 或空，防御一下
                value_ref = operands[0] if operands else None
                if isinstance(value_ref, Reference) and value_ref.value_type == ValueType.VARIABLE:
                    roots.add(self._lookup_key(value_ref.get_name(), current_scope, scope_stack))
                continue

            # ---------- COND_JUMP ----------
            if opcode == IROpCode.COND_JUMP:
                cond_ref, _true_scope, _false_scope = instr.get_operands()
                # 按最新约定，cond 是 Reference
                if isinstance(cond_ref, Reference) and cond_ref.value_type == ValueType.VARIABLE:
                    roots.add(self._lookup_key(cond_ref.get_name(), current_scope, scope_stack))
                continue

        return roots

    # ------------------------------------------------------------------ #
    #  第二遍：从根出发反向传播活跃性                                          #
    # ------------------------------------------------------------------ #

    def _propagate_liveness(self, roots: set[_VarKey]) -> None:
        """
        BFS 反向传播：一个变量活跃 → 产生它所依赖的操作数也活跃。

        方向：result_key --(_def_graph)--> operand_keys
        """
        queue: deque[_VarKey] = deque()

        for key in roots:
            if key not in self._live:
                self._live.add(key)
                queue.append(key)

        while queue:
            key = queue.popleft()

            # 该变量活跃 → 它的所有操作数也活跃
            for operand_key in self._def_graph.get(key, ()):
                if operand_key not in self._live:
                    self._live.add(operand_key)
                    queue.append(operand_key)

    # ------------------------------------------------------------------ #
    #  第三遍：删除死代码                                                    #
    # ------------------------------------------------------------------ #

    def _remove_dead_code(self) -> None:
        """
        删除结果变量不在活跃集中的指令。

        只删纯计算指令（ASSIGN、BINARY_OP、COMPARE、UNARY_OP、CAST）。
        有副作用的指令（CALL、CALL_METHOD、RETURN 等）绝不删除。
        """
        scope_stack: list[str] = ["global"]
        iterator = self.builder.__iter__()

        for instr in iterator:
            opcode = instr.opcode

            if opcode == IROpCode.SCOPE_BEGIN:
                scope_stack.append(instr.get_operands()[0])
                continue

            if opcode == IROpCode.SCOPE_END:
                if len(scope_stack) > 1:
                    scope_stack.pop()
                continue

            current_scope = scope_stack[-1]

            if opcode == IROpCode.ASSIGN:
                target, _source = instr.get_operands()
                key = self._lookup_key(target.get_name(), current_scope, scope_stack)
                if key not in self._live:
                    iterator.remove_current()
                    self._changed = True

            elif opcode in (IROpCode.BINARY_OP, IROpCode.COMPARE,
                            IROpCode.UNARY_OP, IROpCode.CAST):
                result = instr.get_operands()[0]
                key = self._lookup_key(result.get_name(),current_scope, scope_stack)
                if key not in self._live:

                    iterator.remove_current()
                    self._changed = True

    # ------------------------------------------------------------------ #
    #  图操作辅助                                                           #
    # ------------------------------------------------------------------ #

    def _ensure_def(self, result_key: _VarKey) -> None:
        """确保 result_key 在 _def_graph 中有条目（即使没有操作数依赖）。"""
        if result_key not in self._def_graph:
            self._def_graph[result_key] = set()

    def _add_edge(self, result_key: _VarKey, operand_key: _VarKey) -> None:
        """
        建立 result → operand 的依赖边，同时维护反向使用图。
        """
        self._def_graph.setdefault(result_key, set()).add(operand_key)
        self._use_graph.setdefault(operand_key, set()).add(result_key)

    # ------------------------------------------------------------------ #
    #  作用域查找辅助                                                        #
    # ------------------------------------------------------------------ #

    def _lookup_key(self, var_name: str, current_scope: str, scope_stack: list[str]) -> _VarKey:
        """
        沿作用域栈向上查找变量的声明作用域，返回声明作用域限定的键。
        找不到则 fallback 到当前作用域（理论上不应发生）。
        """
        # 从当前作用域开始向上找，直到找到声明了该变量的作用域
        for scope in reversed(scope_stack):
            if _make_key(scope, var_name) in self._declared:
                return _make_key(scope, var_name)

        # 【魔法兜底】：找不到声明，可能是跨 pass 产生的临时变量，
        # 降级到当前作用域，保守处理不删除。
        return _make_key(current_scope, var_name)