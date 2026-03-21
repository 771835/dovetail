# coding=utf-8
"""
不可达代码移除 Pass

移除 return/break/continue 之后的不可达代码。
"""
from __future__ import annotations

from dovetail.core.compile_config import CompileConfig
from dovetail.core.enums import OptimizationLevel
from dovetail.core.instructions import *
from dovetail.core.ir_builder import IRBuilder
from dovetail.core.optimize.base import IROptimizationPass
from dovetail.core.optimize.pass_metadata import PassMetadata, PassPhase
from dovetail.core.optimize.pass_registry import register_pass


@register_pass(PassMetadata(
    name="unreachable_code_removal",
    display_name="不可达代码移除",
    description="移除 return/break/continue 之后的不可达代码",
    level=OptimizationLevel.O1,
    phase=PassPhase.CLEANUP,
    provided_features=("removed_unreachable",)
))
class UnreachableCodeRemovalPass(IROptimizationPass):
    """不可达代码移除优化 Pass"""

    def __init__(self, builder: IRBuilder, config: CompileConfig):
        super().__init__(builder, config)
        self._changed = False

    def execute(self) -> bool:
        """执行不可达代码移除优化"""
        self._changed = False
        iterator = self.builder.__iter__()
        in_unreachable = False
        level = 0

        while True:
            try:
                instr = next(iterator)
            except StopIteration:
                break

            if in_unreachable:
                if instr.opcode == IROpCode.SCOPE_BEGIN:
                    level += 1
                elif instr.opcode == IROpCode.SCOPE_END:
                    if level == 0:
                        in_unreachable = False
                        continue
                    level -= 1

                iterator.remove_current()
                self._changed = True
                continue

            if instr.opcode in (IROpCode.RETURN, IROpCode.BREAK, IROpCode.CONTINUE):
                in_unreachable = True

        return self._changed
