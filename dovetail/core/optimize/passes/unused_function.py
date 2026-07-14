# coding=utf-8
"""
未使用函数消除 Pass

移除从未被 CALL 或 CALL_METHOD 指令引用的函数。

算法：
  1. _analyze_functions：
     一次遍历 IR，收集所有 FUNCTION 指令声明的函数名，
     以及所有 CALL / CALL_METHOD 指令调用的函数名。

  2. _remove_unused_functions：
     对每个声明但未被调用的函数，调用 _remove_function 删除。
     带有 no_dce 标志的函数跳过（用于 tick/load 等入口函数及被导出函数）。

  3. _remove_function：
     再次遍历 IR，找到目标函数的 FUNCTION 指令，
     随后进入"删除模式"：用 level 计数跟踪 SCOPE_BEGIN/END 配对，
     level 降回 0 时退出删除模式（即函数体的最外层 SCOPE_END 已删）。

level 计数细节：
  - 遇到 FUNCTION 指令时进入删除模式，level = 0
  - 遇到 SCOPE_BEGIN：先 remove，然后 level += 1
  - 遇到 SCOPE_END：先 level -= 1，若 level == 0 则 remove 后退出，
                    否则 remove 继续
  这样函数体的第一个 SCOPE_BEGIN 将 level 推至 1，
  最后一个 SCOPE_END 将 level 降回 0 触发退出。
"""
from __future__ import annotations

from dovetail.core.compile_config import CompileConfig
from dovetail.core.enums import OptimizationLevel
from dovetail.core.instructions import IROpCode
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
    phase=PassPhase.CLEANUP,
    provided_features=("removed_unused_functions",),
))
class UnusedFunctionEliminationPass(IROptimizationPass):
    """未使用函数消除优化 Pass"""

    def __init__(self, builder: IRBuilder, config: CompileConfig):
        super().__init__(builder, config)
        self.function_calls: dict[str, int] = {}
        self.function_declarations: dict[str, Function] = {}
        self.function_has_side_effect: dict[str, bool] = {}
        self._changed = False

    def execute(self) -> bool:
        self._changed = False
        self._analyze_functions()
        self._remove_unused_functions()
        return self._changed

    def _analyze_functions(self) -> None:
        """收集函数声明、调用信息和副作用信息"""
        current_function: str | None = None
        function_body_depth = 0

        for instr in self.builder.get_instructions():
            if instr.opcode == IROpCode.FUNCTION:
                func = instr.operands[0]
                self.function_declarations[func.name] = func
                self.function_has_side_effect[func.name] = False
                current_function = func.name
                function_body_depth = 0
                continue

            if current_function is not None:
                if instr.opcode == IROpCode.SCOPE_BEGIN:
                    function_body_depth += 1
                elif instr.opcode == IROpCode.SCOPE_END:
                    function_body_depth -= 1
                    if function_body_depth == 0:
                        current_function = None
                        continue

            if instr.opcode == IROpCode.CALL:
                func = instr.operands[1]
                self.function_calls[func.name] = self.function_calls.get(func.name, 0) + 1
                if current_function is not None:
                    self.function_has_side_effect[current_function] = True

            elif instr.opcode == IROpCode.CALL_METHOD:
                func = instr.operands[2]
                self.function_calls[func.name] = self.function_calls.get(func.name, 0) + 1
                if current_function is not None:
                    self.function_has_side_effect[current_function] = True

            elif current_function is not None and instr.opcode in (
                    IROpCode.NEW_OBJ,
                    IROpCode.GET_PROPERTY,
                    IROpCode.SET_PROPERTY,
            ):
                self.function_has_side_effect[current_function] = True

    def _remove_unused_functions(self) -> None:
        for func_name, func in self.function_declarations.items():
            if func_name not in self.function_calls:
                if self.function_has_side_effect.get(func_name, False):
                    continue
                if "no_dce" not in func.all_flags():
                    self._remove_function(func_name)

    def _remove_function(self, func_name: str) -> None:
        """
        删除指定函数的 FUNCTION 指令及其完整函数体。

        状态机：
          in_function=False → 扫描 FUNCTION 指令
          in_function=True  → 按 SCOPE_BEGIN/END 配对计数，全部删除
          level=0 + SCOPE_END → 函数体结束，退出删除模式
        """
        iterator = self.builder.__iter__()
        in_function = False
        level = 0

        while True:
            try:
                instr = next(iterator)
            except StopIteration:
                break

            if not in_function:
                if instr.opcode == IROpCode.FUNCTION:
                    func = instr.operands[0]
                    if func.name == func_name:
                        iterator.remove_current()
                        self._changed = True
                        in_function = True
                        level = 0
                continue

            # ── 删除模式 ────────────────────────────────────
            if instr.opcode == IROpCode.SCOPE_BEGIN:
                iterator.remove_current()
                self._changed = True
                level += 1

            elif instr.opcode == IROpCode.SCOPE_END:
                level -= 1
                iterator.remove_current()
                self._changed = True
                if level == 0:
                    in_function = False

            else:
                iterator.remove_current()
                self._changed = True