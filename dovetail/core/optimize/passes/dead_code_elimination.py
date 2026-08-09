# coding=utf-8
"""
死代码消除 Pass

基于作用域感知的活跃变量分析（Liveness Analysis），
移除永远不会被使用的变量赋值、计算结果和变量声明。

算法概述：
  第一遍（_collect_defs_and_uses）：
    扫描所有指令，以 "scope::var_name" 为唯一键，
    建立 定义图（_def_graph）和 根活跃集（roots）。
    同时收集所有 DECLARE，填充 _declared 供作用域查找使用。

  第二遍（_propagate_liveness）：
    从 roots 出发，沿 _def_graph 反向传播，
    标记所有可达的活跃变量。

  第三遍（_remove_dead_code）：
    删除结果变量不在活跃集中的纯计算指令。
    删除变量不在活跃集中的 DECLARE 指令（PARAMETER/RETURN 除外）。

Key 一致性原则：
  所有变量的 key 统一通过 _lookup_key 构造，
  沿作用域栈向上寻找实际声明作用域。
  构建图和删除判断使用完全相同的 key，保证活跃集查找可靠。
"""
from __future__ import annotations

from collections import deque

from dovetail.core.compile_config import CompileConfig
from dovetail.core.enums import OptimizationLevel
from dovetail.core.enums.types import ValueType, VariableType
from dovetail.core.instructions import IROpCode
from dovetail.core.ir_builder import IRBuilder
from dovetail.core.optimize.base import IROptimizationPass
from dovetail.core.optimize.pass_metadata import PassMetadata, PassPhase
from dovetail.core.optimize.pass_registry import register_pass
from dovetail.core.symbols import Reference
from dovetail.utils.logger import get_logger

_VarKey = str  # "scope_name::var_name"

logger = get_logger(__name__)


def _make_key(scope: str, var_name: str) -> _VarKey:
    """构造作用域限定的变量唯一键。"""
    return f"{scope}::{var_name}"


@register_pass(PassMetadata(
    name="dead_code_elimination",
    display_name="死代码消除",
    description=(
            "移除永远不会使用的变量赋值、计算结果和声明。"
            "基于活跃变量图传播分析，覆盖引用计数的全部能力，"
            "并额外处理传递性死代码。"
    ),
    level=OptimizationLevel.O1,
    phase=PassPhase.CLEANUP,
    provided_features=("cleaned_dead_code", "cleaned_declarations"),
))
class DeadCodeEliminationPass(IROptimizationPass):
    """
    死代码消除优化 Pass（含声明清理）

    以 "scope::var_name" 作为变量唯一键，
    所有 key 均通过 _lookup_key 统一构造，
    保证构建图和活跃集查找时同一变量对应同一 key。
    """

    def __init__(self, builder: IRBuilder, config: CompileConfig):
        super().__init__(builder, config)

        # 定义图：result_key → set of operand_keys（该结果依赖哪些操作数）
        self._def_graph: dict[_VarKey, set[_VarKey]] = {}

        # 活跃变量集
        self._live: set[_VarKey] = set()

        # 已声明变量的键集合，供 _lookup_key 作用域查找使用
        self._declared: set[_VarKey] = set()

        self._changed: bool = False

    # ------------------------------------------------------------------ #
    #  公开接口                                                            #
    # ------------------------------------------------------------------ #

    def execute(self) -> bool:
        self._changed = False
        self._def_graph.clear()
        self._live.clear()
        self._declared.clear()

        roots = self._collect_defs_and_uses()
        self._propagate_liveness(roots)
        self._remove_dead_code()
        return self._changed

    # ------------------------------------------------------------------ #
    #  第一遍：收集声明、定义图、活跃根                                       #
    # ------------------------------------------------------------------ #

    def _collect_defs_and_uses(self) -> set[_VarKey]:
        """
        单遍扫描 IR，收集变量声明，建立定义图，确定活跃根。

        活跃根：
          - PARAMETER / RETURN 类型的变量声明
          - RETURN 指令的返回值
          - COND_JUMP 的条件变量
          - CALL / CALL_METHOD 的所有实参、obj 以及结果变量
            （有副作用，调用不能删，结果强制活跃）
        """
        roots: set[_VarKey] = set()
        scope_stack: list[str] = ["global"]

        for instr in self.builder:
            opcode = instr.opcode
            current_scope = scope_stack[-1]

            # ------ 作用域边界 ------
            if opcode == IROpCode.SCOPE_BEGIN:
                scope_stack.append(instr.get_operands()[0])
                continue

            if opcode == IROpCode.SCOPE_END:
                if len(scope_stack) > 1:
                    scope_stack.pop()
                continue

            # ------ DECLARE ------
            if opcode == IROpCode.DECLARE:
                var = instr.get_operands()[0]
                key = _make_key(current_scope, var.get_name())
                self._declared.add(key)
                if var.var_type == VariableType.PARAMETER:
                    roots.add(key)
                continue

            # ------ ASSIGN ------
            if opcode == IROpCode.ASSIGN:
                target, source = instr.get_operands()
                target_key = self._lookup_key(target.get_name(), current_scope, scope_stack)
                self._ensure_def(target_key)
                if isinstance(source, Reference) and source.value_type == ValueType.VARIABLE:
                    src_key = self._lookup_key(source.get_name(), current_scope, scope_stack)
                    self._add_edge(target_key, src_key)
                continue

            # ------ BINARY_OP / COMPARE ------
            if opcode in (IROpCode.BINARY_OP, IROpCode.COMPARE):
                operands = instr.get_operands()
                result, _op, left, right = operands[0], operands[1], operands[2], operands[3]
                result_key = self._lookup_key(result.get_name(), current_scope, scope_stack)
                self._ensure_def(result_key)
                for ref in (left, right):
                    if isinstance(ref, Reference) and ref.value_type == ValueType.VARIABLE:
                        op_key = self._lookup_key(ref.get_name(), current_scope, scope_stack)
                        self._add_edge(result_key, op_key)
                continue

            # ------ UNARY_OP ------
            if opcode == IROpCode.UNARY_OP:
                result, _op, operand = instr.get_operands()
                result_key = self._lookup_key(result.get_name(), current_scope, scope_stack)
                self._ensure_def(result_key)
                if isinstance(operand, Reference) and operand.value_type == ValueType.VARIABLE:
                    op_key = self._lookup_key(operand.get_name(), current_scope, scope_stack)
                    self._add_edge(result_key, op_key)
                continue

            # ------ CAST ------
            if opcode == IROpCode.CAST:
                result, _dtype, source = instr.get_operands()
                result_key = self._lookup_key(result.get_name(), current_scope, scope_stack)
                self._ensure_def(result_key)
                if isinstance(source, Reference) and source.value_type == ValueType.VARIABLE:
                    src_key = self._lookup_key(source.get_name(), current_scope, scope_stack)
                    self._add_edge(result_key, src_key)
                continue

            # ------ CALL ------
            if opcode == IROpCode.CALL:
                result, _func, args = instr.get_operands()
                if result is not None:
                    result_key = self._lookup_key(result.get_name(), current_scope, scope_stack)
                    self._ensure_def(result_key)
                    roots.add(result_key)
                for arg_ref in args.values():
                    if isinstance(arg_ref, Reference) and arg_ref.value_type == ValueType.VARIABLE:
                        roots.add(self._lookup_key(arg_ref.get_name(), current_scope, scope_stack))
                continue

            # ------ CALL_METHOD ------
            if opcode == IROpCode.CALL_METHOD:
                result, obj_ref, _method, args = instr.get_operands()
                if result is not None:
                    result_key = self._lookup_key(result.get_name(), current_scope, scope_stack)
                    self._ensure_def(result_key)
                    roots.add(result_key)
                if isinstance(obj_ref, Reference) and obj_ref.value_type == ValueType.VARIABLE:
                    roots.add(self._lookup_key(obj_ref.get_name(), current_scope, scope_stack))
                for arg_ref in args.values():
                    if isinstance(arg_ref, Reference) and arg_ref.value_type == ValueType.VARIABLE:
                        roots.add(self._lookup_key(arg_ref.get_name(), current_scope, scope_stack))
                continue

            # ------ RETURN ------
            if opcode == IROpCode.RETURN:
                operands = instr.get_operands()
                value_ref = operands[0] if operands else None
                if isinstance(value_ref, Reference) and value_ref.value_type == ValueType.VARIABLE:
                    roots.add(self._lookup_key(value_ref.get_name(), current_scope, scope_stack))
                continue

            # ------ COND_JUMP ------
            if opcode == IROpCode.COND_JUMP:
                cond_ref, _true_scope, _false_scope = instr.get_operands()
                if isinstance(cond_ref, Reference) and cond_ref.value_type == ValueType.VARIABLE:
                    roots.add(self._lookup_key(cond_ref.get_name(), current_scope, scope_stack))
                continue

        return roots

    # ------------------------------------------------------------------ #
    #  第二遍：BFS 反向传播活跃性                                            #
    # ------------------------------------------------------------------ #

    def _propagate_liveness(self, roots: set[_VarKey]) -> None:
        """从根出发，沿 _def_graph 传播：result 活跃 → 其依赖的 operands 也活跃。"""
        queue: deque[_VarKey] = deque()
        for key in roots:
            if key not in self._live:
                self._live.add(key)
                queue.append(key)

        while queue:
            key = queue.popleft()
            for operand_key in self._def_graph.get(key, ()):
                if operand_key not in self._live:
                    self._live.add(operand_key)
                    queue.append(operand_key)

    # ------------------------------------------------------------------ #
    #  第三遍：删除死计算指令和死声明                                         #
    # ------------------------------------------------------------------ #

    def _remove_dead_code(self) -> None:
        """
        删除死计算指令和死声明。

        删除条件：
          - DECLARE：变量不在活跃集，且不是 PARAMETER/RETURN
          - ASSIGN：target 不在活跃集
          - BINARY_OP/COMPARE/UNARY_OP/CAST：result 不在活跃集

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

            if opcode == IROpCode.DECLARE:
                var = instr.get_operands()[0]
                if var.var_type == VariableType.PARAMETER:
                    continue
                key = self._lookup_key(var.get_name(), current_scope, scope_stack)
                if key not in self._live:
                    iterator.remove_current()
                    self._changed = True
                continue

            if opcode == IROpCode.ASSIGN:
                target, _source = instr.get_operands()
                key = self._lookup_key(target.get_name(), current_scope, scope_stack)
                if key not in self._live:
                    iterator.remove_current()
                    self._changed = True
                continue

            if opcode in (IROpCode.BINARY_OP, IROpCode.COMPARE,
                          IROpCode.UNARY_OP, IROpCode.CAST):
                result = instr.get_operands()[0]
                key = self._lookup_key(result.get_name(), current_scope, scope_stack)
                if key not in self._live:
                    iterator.remove_current()
                    self._changed = True
                continue

    # ------------------------------------------------------------------ #
    #  辅助方法                                                            #
    # ------------------------------------------------------------------ #

    def _ensure_def(self, result_key: _VarKey) -> None:
        if result_key not in self._def_graph:
            self._def_graph[result_key] = set()

    def _add_edge(self, result_key: _VarKey, operand_key: _VarKey) -> None:
        self._def_graph.setdefault(result_key, set()).add(operand_key)

    def _lookup_key(self, var_name: str, current_scope: str, scope_stack: list[str]) -> _VarKey:
        """
        沿作用域栈向上查找变量的实际声明作用域，返回声明作用域限定的 key。
        找不到时降级到 current_scope 并发出警告——这不应发生在正常 IR 中。
        """
        for scope in reversed(scope_stack):
            candidate = _make_key(scope, var_name)
            if candidate in self._declared:
                return candidate

        logger.warning(
            f"变量 '{var_name}' 在作用域链 {scope_stack} 中未找到声明，"
            f"降级到当前作用域 '{current_scope}'。",
            stacklevel=2,
        )
        return _make_key(current_scope, var_name)
