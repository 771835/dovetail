# coding=utf-8
"""
IRAssign 指令处理器
"""
from dovetail.core.backend import ir_processor, IRProcessor, GenerationContext
from dovetail.core.instructions import IRInstruction, IROpCode
from ..backend import JE1215Backend
from ..commands.copy import Copy
from ..commands.tools import DataPath


@ir_processor(JE1215Backend, IROpCode.ASSIGN)
class IRAssignProcessor(IRProcessor):
    def process(self, instruction: IRInstruction, context: GenerationContext):
        target, source = instruction.operands
        if source.is_literal():
            context.add_command(
                Copy.copy_literals(
                    DataPath.from_symbol(context, target),
                    source.value.value
                )
            )
        else:
            context.add_command(
                Copy.copy(
                    DataPath.from_symbol(context, target),
                    DataPath.from_symbol(context, source)
                )
            )
