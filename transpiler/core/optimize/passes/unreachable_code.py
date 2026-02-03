# coding=utf-8
"""
不可达代码移除 Pass

移除 return/break/continue 之后的不可达代码。
"""
from __future__ import annotations

from transpiler.core.compile_config import CompileConfig
from transpiler.core.enums import OptimizationLevel
from transpiler.core.instructions import *
from transpiler.core.ir_builder import IRBuilder
from transpiler.core.optimize.base import IROptimizationPass
from transpiler.core.optimize.pass_metadata import PassMetadata, PassPhase
from transpiler.core.optimize.pass_registry import register_pass


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
                if isinstance(instr, IRScopeBegin):
                    level += 1
                elif isinstance(instr, IRScopeEnd):
                    if level == 0:
                        in_unreachable = False
                        continue
                    level -= 1

                iterator.remove_current()
                self._changed = True
                continue

            if isinstance(instr, (IRReturn, IRBreak, IRContinue)):
                in_unreachable = True

        return self._changed
