# coding=utf-8
"""
未使用函数消除 Pass

移除从未被 CALL 或 CALL_METHOD 指令引用的函数。

"""
from __future__ import annotations

from dovetail.core.compile_config import CompileConfig
from dovetail.core.enums import OptimizationLevel, FunctionType
from dovetail.core.instructions import *
from dovetail.core.ir_builder import IRBuilder
from dovetail.core.optimize.base import IROptimizationPass
from dovetail.core.optimize.pass_metadata import PassMetadata, PassPhase
from dovetail.core.optimize.pass_registry import register_pass
from dovetail.core.symbols import Function


@register_pass(PassMetadata(
    name="unused_function_elimination",
    display_name="未使用函数消除",
    description="移除从未被调用的函数",
    level=OptimizationLevel.O1,
    phase=PassPhase.PRUNE,
    provided_features=("removed_unused_functions",)
))
class UnusedFunctionEliminationPass(IROptimizationPass):
    """未使用函数消除优化 Pass"""

    def __init__(self, builder: IRBuilder, config: CompileConfig):
        super().__init__(builder, config)
        self.function_calls: dict[str, int] = {}
        self.function_declarations: dict[str, Function] = {}
        self._changed = False

    def execute(self) -> bool:
        """执行未使用函数消除优化"""
        self._changed = False
        self._analyze_functions()
        self._remove_unused_functions()
        return self._changed

    def _analyze_functions(self) -> None:
        """
        收集函数声明与调用信息。

        同名函数可能同时存在前向声明（FUNCTION_UNIMPLEMENTED）和实现（FUNCTION），
        以实现为准写入 function_declarations，确保后续 no_dce 等标志判断正确。
        """
        for instr in self.builder.get_instructions():
            if instr.opcode == IROpCode.FUNCTION:
                func: Function = instr.get_operands()[0]
                existing = self.function_declarations.get(func.name)
                # 尚未记录，或当前是实现（非前向声明）→ 覆盖
                if existing is None or func.function_type != FunctionType.FUNCTION_UNIMPLEMENTED:
                    self.function_declarations[func.name] = func

            elif instr.opcode == IROpCode.CALL:
                func = instr.get_operands()[1]
                self.function_calls[func.name] = self.function_calls.get(func.name, 0) + 1

            elif instr.opcode == IROpCode.CALL_METHOD:
                func = instr.get_operands()[2]
                self.function_calls[func.name] = self.function_calls.get(func.name, 0) + 1

    def _remove_unused_functions(self) -> None:
        """
        高效删除所有未被调用的函数（含其前向声明）。
        复杂度：O(M)，只对 IR 完整扫描一次。
        """
        # 1. 收集所有需要被删除的函数名
        unused_func_names: set[str] = set()
        for func_name, func in self.function_declarations.items():
            if func_name not in self.function_calls:
                if "no_dce" not in func.all_flags():
                    unused_func_names.add(func_name)

        if not unused_func_names:
            return  # 没有要删的，直接退出

        # 2. 单次遍历 IR，精准干掉所有无用函数
        iterator = self.builder.__iter__()
        current_deleting_func: str | None = None
        level = 0

        while True:
            try:
                instr = next(iterator)
            except StopIteration:
                break

            # ── 如果当前正在删除某个函数的函数体 ──────────────────
            if current_deleting_func is not None:
                # 安全防范：中途遇到新的 FUNCTION 指令
                if instr.opcode == IROpCode.FUNCTION:
                    current_deleting_func = None
                    # 不要跳过当前 instr，让它进入下面的扫描逻辑

                elif instr.opcode == IROpCode.SCOPE_BEGIN:
                    iterator.remove_current()
                    self._changed = True
                    level += 1
                    continue

                elif instr.opcode == IROpCode.SCOPE_END:
                    level -= 1
                    iterator.remove_current()
                    self._changed = True
                    if level == 0:
                        current_deleting_func = model = None  # 删完了
                    continue

                else:
                    iterator.remove_current()
                    self._changed = True
                    continue

            # ── 扫描模式：寻找未使用的函数 ────────────────────────
            if instr.opcode == IROpCode.FUNCTION:
                func: Function = instr.get_operands()[0]
                if func.name in unused_func_names:
                    iterator.remove_current()
                    self._changed = True

                    # 如果是带函数体的实现，进入删除模式
                    if func.function_type != FunctionType.FUNCTION_UNIMPLEMENTED:
                        current_deleting_func = func.name
                        level = 0
