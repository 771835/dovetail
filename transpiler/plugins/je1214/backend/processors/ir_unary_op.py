# coding=utf-8
# coding=utf-8
"""
IRUnaryOp 指令处理器
"""
from transpiler.core.backend import ir_processor, IRProcessor, GenerationContext
from transpiler.core.config import get_project_logger
from transpiler.core.enums import UnaryOps
from transpiler.core.instructions import IRInstruction, IROpCode
from ..backend import JE1214Backend
from ..commands import UnaryOp, DataPath


@ir_processor(JE1214Backend, IROpCode.UNARY_OP)
class IRUnaryOpProcessor(IRProcessor):
    def process(self, instruction: IRInstruction, context: GenerationContext):
        result = instruction.operands[0]
        op = instruction.operands[1]
        operand = instruction.operands[2].value
        result_path = DataPath(context.current_scope.get_symbol_path(result),context.objective)
        operand_path = DataPath(context.current_scope.get_symbol_path(operand), context.objective)
        if op == UnaryOps.NOT:
            context.add_commands(UnaryOp.not_(result_path,operand_path))
        else:
            get_project_logger().error(f"The unary operation {op} is not implemented.")

