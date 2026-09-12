# coding=utf-8
"""
IRStructSet 指令处理器
"""
from typing import cast

from dovetail.core.backend import ir_processor, IRProcessor, GenerationContext
from dovetail.core.instructions import IRInstruction, IROpCode
from dovetail.core.symbols import Reference
from ..backend import JE1215Backend
from ..commands import DataPath, Copy


@ir_processor(JE1215Backend, IROpCode.STRUCT_SET)
class IRStructSetProcessor(IRProcessor):
    def process(self, instruction: IRInstruction, context: GenerationContext):
        instance, field, value = cast(tuple[Reference, str, Reference], instruction.operands)

        data_path = DataPath.from_symbol(context, instance) / field

        context.add_command(
            Copy.copy_all(
                data_path,
                value.value.value if value.is_literal() else DataPath.from_symbol(context, value),
            )
        )

