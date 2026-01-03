# coding=utf-8
"""
IRScopeEnd 指令处理器
"""
from transpiler.core.backend import ir_processor, IRProcessor, GenerationContext
from transpiler.core.instructions import IROpCode, IRScopeEnd
from ..backend import JE1214Backend


@ir_processor(JE1214Backend, IROpCode.SCOPE_END)
class IRScopeEndProcessor(IRProcessor):
    def process(self, instruction: IRScopeEnd, context: GenerationContext):
        context.pop_scope()
