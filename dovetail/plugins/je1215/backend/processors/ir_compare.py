# coding=utf-8
"""
IRCompare 指令处理器
"""
from dovetail.core.backend import ir_processor, IRProcessor, GenerationContext
from dovetail.core.enums import ValueType
from dovetail.core.instructions import IRInstruction, IROpCode
from ..backend import JE1215Backend
from ..commands.compare import Compare
from ..commands.tools import DataPath


@ir_processor(JE1215Backend, IROpCode.COMPARE)
class IRCompareProcessor(IRProcessor):
    def process(self, instr: IRInstruction, context: GenerationContext):
        result, op, a, b = instr.operands
        result_path = DataPath.from_symbol(context, result)
        if a.value_type == ValueType.LITERAL:
            a_path = a.value.value
        else:
            a_path = DataPath.from_symbol(context, a)
        if b.value_type == ValueType.LITERAL:
            b_path = b.value.value
        else:
            b_path = DataPath.from_symbol(context, b)
        context.add_commands(
            Compare.compare(
                result_path,
                op,
                a_path,
                b_path
            )
        )
