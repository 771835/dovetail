# coding=utf-8
"""
IRStructGet 指令处理器
"""
from typing import cast

from dovetail.core.backend import ir_processor, IRProcessor, GenerationContext
from dovetail.core.instructions import IRInstruction, IROpCode
from dovetail.core.symbols import Variable, Reference
from ..backend import JE1215Backend
from ..commands import DataPath, Copy


@ir_processor(JE1215Backend, IROpCode.STRUCT_GET)
class IRStructGetProcessor(IRProcessor):
    def process(self, instruction: IRInstruction, context: GenerationContext):
        result, instance, field = cast(tuple[Variable, Reference, str], instruction.operands)

        data_path = DataPath.from_symbol(context, instance) / field

        context.add_command(Copy.copy(DataPath.from_symbol(context, result), data_path))
