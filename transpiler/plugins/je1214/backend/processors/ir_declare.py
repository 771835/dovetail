# coding=utf-8
"""
IRDeclare 指令处理器
"""
from transpiler.core.backend import ir_processor, IRProcessor, GenerationContext
from transpiler.core.instructions import IRInstruction, IROpCode
from ..backend import JE1214Backend


@ir_processor(JE1214Backend, IROpCode.DECLARE)
class IRDeclareProcessor(IRProcessor):
    def process(self, instruction: IRInstruction, context: GenerationContext):
        context.current_scope.add_symbol(instruction.operands[0])
