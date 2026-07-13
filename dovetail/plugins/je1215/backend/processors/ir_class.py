# coding=utf-8
"""
IRClass 指令处理器
"""
from dovetail.core.backend import ir_processor, IRProcessor, GenerationContext
from dovetail.core.instructions import IRInstruction, IROpCode
from ..backend import JE1215Backend


@ir_processor(JE1215Backend, IROpCode.CLASS)
class IRClassProcessor(IRProcessor):
    def process(self, instruction: IRInstruction, context: GenerationContext):
        pass
