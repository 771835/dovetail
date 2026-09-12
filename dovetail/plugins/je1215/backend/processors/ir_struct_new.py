# coding=utf-8
"""
IRStructNew 指令处理器
"""
from typing import cast

from dovetail.core.backend import ir_processor, IRProcessor, GenerationContext
from dovetail.core.instructions import IRInstruction, IROpCode
from dovetail.core.symbols import Variable, Reference
from dovetail.core.symbols.structure import Structure
from ..backend import JE1215Backend
from ..commands import Copy, DataPath


@ir_processor(JE1215Backend, IROpCode.STRUCT_NEW)
class IRStructNewProcessor(IRProcessor):
    def process(self, instruction: IRInstruction, context: GenerationContext):
        result, structure, field_values = cast(tuple[Variable, Structure, dict[str, Reference]], instruction.operands)

        data_path = DataPath.from_symbol(context, result)

        for fname, value in field_values.items():
            context.current_scope.add_command(
                Copy.copy_all(
                    data_path / fname,
                    value.value.value if value.is_literal() else DataPath.from_symbol(context, value)
                )
            )