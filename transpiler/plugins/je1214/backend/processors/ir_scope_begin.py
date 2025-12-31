# coding=utf-8
"""
IR指令ScopeBegin处理器
"""
from transpiler.core.backend import ir_processor, IRProcessor, GenerationContext
from transpiler.core.instructions import IROpCode, IRScopeBegin
from ..backend import JE1214Backend


@ir_processor(JE1214Backend, IROpCode.SCOPE_BEGIN)
class IRScopeBeginProcessor(IRProcessor):
    def process(self, instruction: IRScopeBegin, context: GenerationContext):
        sub_scope = context.create_scope(instruction.operands[0], instruction.operands[1])
        context.push_scope(sub_scope)
