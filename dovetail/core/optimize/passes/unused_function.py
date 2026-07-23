# coding=utf-8
"""
未使用函数消除 Pass

移除从未被 CALL 或 CALL_METHOD 指令引用的函数。

算法：
  1. _analyze_functions：
     一次遍历 IR，收集所有 FUNCTION 指令声明的函数名，
     以及所有 CALL / CALL_METHOD 指令调用的函数名。

     对于同名函数（前向声明 + 实现），以"实现"为准覆盖存储，
     确保 function_declarations 里保留的是带函数体的那个 Function 对象。

  2. _remove_unused_functions：
     对每个声明但未被调用的函数，调用 _remove_function 删除。
     带有 no_dce 标志的函数跳过（用于 tick/load 等入口函数及被导出函数）。

  3. _remove_function：
     再次遍历 IR，找到所有 name == func_name 的 FUNCTION 指令，逐一删除。

     关键：前向声明（FUNCTION_UNIMPLEMENTED）没有函数体，
     不会跟随 SCOPE_BEGIN/END，因此命中后直接删除该指令，
     不进入删除模式，继续向后扫描。

     只有带函数体的 FUNCTION 指令才进入删除模式，
     用 level 计数跟踪 SCOPE_BEGIN/END 配对，level 降回 0 时退出。

level 计数细节：
  - 遇到带 body 的 FUNCTION 指令时进入删除模式，level = 0
  - 遇到 SCOPE_BEGIN：remove，然后 level += 1
  - 遇到 SCOPE_END：level -= 1，remove，若 level == 0 则退出删除模式
  - 遇到其他指令：直接 remove
  - 删除模式中途再次遇到 FUNCTION 指令（理论上不应发生）：
    强制退出删除模式，不删除该指令，防止误伤其他函数
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
        """删除未被调用的函数（含其前向声明）"""
        for func_name, func in self.function_declarations.items():
            if func_name not in self.function_calls:
                if "no_dce" not in func.all_flags():
                    self._remove_function(func_name)

    def _remove_function(self, func_name: str) -> None:
        """
        删除指定函数的所有 IR 指令，包括前向声明和实现。

        状态机：
          in_function=False → 扫描模式，寻找 name==func_name 的 FUNCTION 指令
          in_function=True  → 删除模式，按 SCOPE_BEGIN/END 配对计数删除函数体

        前向声明（FUNCTION_UNIMPLEMENTED）没有 SCOPE 体，
        命中后直接删除该指令，不进入删除模式，继续扫描后续指令，
        以便同时删除后面的实现。
        """
        iterator = self.builder.__iter__()
        in_function = False
        level = 0

        while True:
            try:
                instr = next(iterator)
            except StopIteration:
                break

            # ── 扫描模式 ────────────────────────────────────
            if not in_function:
                if instr.opcode == IROpCode.FUNCTION:
                    func: Function = instr.get_operands()[0]
                    if func.name == func_name:
                        iterator.remove_current()
                        self._changed = True
                        # 前向声明没有函数体，不进入删除模式，继续向后扫描
                        if func.function_type != FunctionType.FUNCTION_UNIMPLEMENTED:
                            in_function = True
                            level = 0
                continue

            # ── 删除模式 ────────────────────────────────────

            # 删除模式中途遇到新的 FUNCTION 指令，
            # 说明上一个函数体已意外结束（正常情况不应发生），
            # 强制退出，绝不误删其他函数。
            if instr.opcode == IROpCode.FUNCTION:
                in_function = False
                continue

            if instr.opcode == IROpCode.SCOPE_BEGIN:
                iterator.remove_current()
                self._changed = True
                level += 1

            elif instr.opcode == IROpCode.SCOPE_END:
                level -= 1
                iterator.remove_current()
                self._changed = True
                if level == 0:
                    in_function = False  # 函数体删完，回到扫描模式

            else:
                iterator.remove_current()
                self._changed = True
