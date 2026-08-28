# coding=utf-8
"""
未使用函数消除 Pass

基于调用图从根节点出发做 BFS，标记所有可达函数，
未被标记的函数（含前向声明）一律删除。

"""
from __future__ import annotations

from collections import defaultdict, deque

from dovetail.core.compile_config import CompileConfig
from dovetail.core.enums import OptimizationLevel, FunctionType
from dovetail.core.instructions import *
from dovetail.core.ir_builder import IRBuilder
from dovetail.core.optimize.base import IROptimizationPass
from dovetail.core.optimize.pass_metadata import PassMetadata, PassPhase
from dovetail.core.optimize.pass_registry import register_pass
from dovetail.core.symbols import Function
from dovetail.utils.logger import get_logger

logger = get_logger(__name__)


@register_pass(PassMetadata(
    name="unused_function_elimination",
    display_name="未使用函数消除",
    description="基于调用图可达性分析，移除所有不可达函数",
    level=OptimizationLevel.O1,
    phase=PassPhase.PRUNE,
    provided_features=("removed_unused_functions",)
))
class UnusedFunctionEliminationPass(IROptimizationPass):
    """基于调用图可达性分析的死函数消除 Pass"""

    def __init__(self, builder: IRBuilder, config: CompileConfig):
        super().__init__(builder, config)
        # func_name -> Function 对象（以实现为准）
        self.function_declarations: dict[str, Function] = {}
        # 调用图：caller -> set of callees
        self.call_graph: dict[str, set[str]] = defaultdict(set)
        # 函数体内的指令属于哪个函数（构建调用图时用）
        self._changed = False

    def execute(self, context) -> bool:
        self._changed = False
        self._build_call_graph()
        reachable = self._compute_reachable()
        self._prune(reachable)
        return self._changed

    # ──────────────────────────────────────────────────────────
    # Phase 1：构建调用图
    # ──────────────────────────────────────────────────────────

    def _build_call_graph(self) -> None:
        """
        单次扫描 IR，同时完成两件事：
        1. 收集所有函数声明（以实现覆盖前向声明）
        2. 建立 caller -> {callee, ...} 的调用图

        顶层调用（不在任何函数体内）归入虚拟根节点 "__root__"。
        """
        current_func: str = "__root__"
        scope_depth: int = 0

        for instr in self.builder.get_instructions():
            opcode = instr.opcode

            if opcode == IROpCode.FUNCTION:
                func: Function = instr.get_operands()[0]
                existing = self.function_declarations.get(func.name)
                if existing is None or func.func_type != FunctionType.FUNCTION_UNIMPLEMENTED:
                    self.function_declarations[func.name] = func

                if func.func_type != FunctionType.FUNCTION_UNIMPLEMENTED:
                    # 进入函数体
                    current_func = func.name
                    scope_depth = 0
                # 前向声明不改变 current_func

            elif opcode == IROpCode.SCOPE_BEGIN:
                scope_depth += 1

            elif opcode == IROpCode.SCOPE_END:
                scope_depth -= 1
                if scope_depth < 0:
                    # 函数体结束，回到根上下文
                    current_func = "__root__"
                    scope_depth = 0

            elif opcode.is_call:
                callee: Function
                for operand in instr.operands:
                    if isinstance(operand, Function):
                        callee = operand
                        self.call_graph[current_func].add(callee.name)
                        break
                else:
                    logger.debug("在调用指令的参数中找不到被调用的函数")

    # ──────────────────────────────────────────────────────────
    # Phase 2：BFS 计算可达集合
    # ──────────────────────────────────────────────────────────

    def _compute_reachable(self) -> set[str]:
        """
        从 __root__ 出发 BFS，返回所有可达函数名。
        同时尊重 no_dce 标志——打了该标志的函数视为根节点。
        """
        roots: set[str] = {"__root__"}
        for func_name, func in self.function_declarations.items():
            if func.has_flag("no_dce"):
                roots.add(func_name)

        visited: set[str] = set()
        queue: deque[str] = deque(roots)

        while queue:
            node = queue.popleft()
            if node in visited:
                continue
            visited.add(node)
            for callee in self.call_graph.get(node, ()):
                if callee not in visited:
                    queue.append(callee)

        return visited  # 包含 __root__ 本身，不影响后续判断

    # ──────────────────────────────────────────────────────────
    # Phase 3：删除不可达函数
    # ──────────────────────────────────────────────────────────

    def _prune(self, reachable: set[str]) -> None:
        """
        单次遍历 IR，删除所有不可达函数（含前向声明和函数体）。
        复杂度 O(N)，N 为 IR 指令总数。

        Notes: 删除建立在函数仅为单层，不删除类方法的前提下
        """

        instructions = self.builder.get_instructions()

        remove_mode = False
        level: int = 0
        keep_flags = [True] * len(instructions)

        for i, instr in enumerate(instructions):
            if instr.opcode == IROpCode.FUNCTION:
                func: Function = instr.operands[0]
                if func.name not in reachable:
                    keep_flags[i] = False
                    self._changed = True
                    if func.func_type != FunctionType.FUNCTION_UNIMPLEMENTED:
                        remove_mode = True
                continue

            if instr.opcode == IROpCode.SCOPE_BEGIN:
                level += 1

            elif instr.opcode == IROpCode.SCOPE_END:
                level -= 1
                name, scope_type = instr.operands
                if name not in reachable and scope_type == StructureType.FUNCTION and level == 0:
                    keep_flags[i] = False
                    remove_mode = False
                    continue

            if remove_mode:
                keep_flags[i] = False

        if self._changed:
            # 一次重建，单次 memmove
            instructions[:] = [instr for instr, keep in zip(instructions, keep_flags) if keep]
