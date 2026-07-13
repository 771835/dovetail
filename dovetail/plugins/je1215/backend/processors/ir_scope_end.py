# coding=utf-8
"""
IRScopeEnd 指令处理器
"""
from dovetail.core.backend import ir_processor, IRProcessor, GenerationContext
from dovetail.core.instructions import IROpCode, IRScopeEnd
from ..backend import JE1215Backend


@ir_processor(JE1215Backend, IROpCode.SCOPE_END)
class IRScopeEndProcessor(IRProcessor):
    def process(self, instruction: IRScopeEnd, context: GenerationContext):
        context.pop_scope()
