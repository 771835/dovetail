# coding=utf-8
"""
IRScopeBegin 指令处理器
"""
from transpiler.core.backend import ir_processor, IRProcessor, GenerationContext
from transpiler.core.enums import StructureType
from transpiler.core.instructions import IROpCode, IRScopeBegin
from ..backend import JE1214Backend
from ..commands import ScoreboardBuilder


@ir_processor(JE1214Backend, IROpCode.SCOPE_BEGIN)
class IRScopeBeginProcessor(IRProcessor):
    def process(self, instruction: IRScopeBegin, context: GenerationContext):
        name: str = instruction.get_operands()[0]
        stype: StructureType = instruction.get_operands()[1]
        sub_scope = context.create_scope(name, stype)

        context.push_scope(sub_scope)
        if stype == StructureType.LOOP_CHECK:
            context.current_scope.parent.add_command(
                ScoreboardBuilder.set_score(
                    f"#break_{context.current_scope.get_absolute_path()}",
                    context.objective,
                    0
                )
            )
            context.current_scope.add_command(
                ScoreboardBuilder.set_score(
                    f"#continue_{context.current_scope.get_absolute_path()}",
                    context.objective,
                    0
                )
            )
        elif stype == StructureType.FUNCTION:
            context.current_scope.add_command(
                ScoreboardBuilder.set_score(
                    f"#return_{context.current_scope.get_absolute_path()}",
                    context.objective,
                    0
                )
            )
