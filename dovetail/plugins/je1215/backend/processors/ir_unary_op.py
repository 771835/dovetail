# coding=utf-8
# coding=utf-8
"""
IRUnaryOp 指令处理器
"""
from dovetail.core.backend import ir_processor, IRProcessor, GenerationContext
from dovetail.core.enums import UnaryOps
from dovetail.core.instructions import IRInstruction, IROpCode
from dovetail.utils.logger import get_logger
from ..backend import JE1215Backend
from ..commands import UnaryOp, DataPath

logger = get_logger(__name__)


@ir_processor(JE1215Backend, IROpCode.UNARY_OP)
class IRUnaryOpProcessor(IRProcessor):
    def process(self, instruction: IRInstruction, context: GenerationContext):
        result = instruction.operands[0]
        op = instruction.operands[1]
        operand = instruction.operands[2].value
        result_path = DataPath.from_symbol(context, result)
        operand_path = DataPath.from_symbol(context, operand)
        if op == UnaryOps.NOT:
            context.add_commands(UnaryOp.not_(result_path, operand_path))
        else:
            logger.error(f"The unary operation {op} is not implemented.")
