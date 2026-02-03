# coding=utf-8
"""
IRClass 指令处理器
"""
from transpiler.core.backend import ir_processor, IRProcessor, GenerationContext
from transpiler.core.instructions import IRInstruction, IROpCode
from ..backend import JE1214Backend


@ir_processor(JE1214Backend, IROpCode.CLASS)
class IRClassProcessor(IRProcessor):
    def process(self, instruction: IRInstruction, context: GenerationContext):
        pass
