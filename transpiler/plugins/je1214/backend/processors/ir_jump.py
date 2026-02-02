# coding=utf-8
"""
IRJump 指令处理器
"""
from transpiler.core.backend import ir_processor, IRProcessor, GenerationContext, Scope
from transpiler.core.instructions import IRInstruction, IROpCode
from ..backend import JE1214Backend
from ..commands import FunctionBuilder, Execute


@ir_processor(JE1214Backend, IROpCode.JUMP)
class IRJumpProcessor(IRProcessor):
    def process(self, instruction: IRInstruction, context: GenerationContext):
        scope_name: str = instruction.get_operands()[0]
        jump_scope = context.current_scope.resolve_scope(scope_name)
        context.add_command(FunctionBuilder.run(f"{context.namespace}:{jump_scope.get_absolute_path('/')}"))

    def _handle_flags(self, scope: Scope, context: GenerationContext):
        for flag in scope.flags:
            if scope.flags[flag] > 1:
                context.current_scope.flags[flag] = scope.flags[flag] - 1
            context.current_scope.add_command(
                Execute.execute()
                .if_score_matches(
                    f"#{flag.split(':')[0]}_{flag.split(':')[1]}",
                    context.objective,
                    '1'
                )
                .run(
                    "return 0"
                )
            )
