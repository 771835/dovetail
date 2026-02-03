# coding=utf-8
"""
IRCondJump 指令处理器
"""
from transpiler.core.backend import ir_processor, GenerationContext
from transpiler.core.instructions import IRInstruction, IROpCode
from transpiler.core.symbols import Variable
from .ir_jump import IRJumpProcessor
from ..backend import JE1214Backend
from ..commands import FunctionBuilder, Execute


@ir_processor(JE1214Backend, IROpCode.COND_JUMP)
class IRCondJumpProcessor(IRJumpProcessor):
    def process(self, instruction: IRInstruction, context: GenerationContext):
        cond_var: Variable = instruction.get_operands()[0]
        true_scope_name: str | None = instruction.get_operands()[1]
        false_scope_name: str | None = instruction.get_operands()[2]
        if true_scope_name:
            true_scope = context.current_scope.resolve_scope(true_scope_name)
            context.current_scope.add_command(
                Execute.execute()
                .if_score_matches(
                    context.current_scope.get_symbol_path(cond_var),
                    context.objective,
                    "1"
                )
                .run(
                    FunctionBuilder.run(
                        f"{context.namespace}:{true_scope.get_absolute_path('/')}"
                    )
                )
            )
            self._handle_flags(true_scope, context)
        if false_scope_name:
            false_scope = context.current_scope.resolve_scope(false_scope_name)
            context.current_scope.add_command(
                Execute.execute()
                .unless_score_matches(
                    context.current_scope.get_symbol_path(cond_var),
                    context.objective,
                    "1"
                )
                .run(
                    FunctionBuilder.run(
                        f"{context.namespace}:{false_scope.get_absolute_path('/')}"
                    )
                )
            )
            self._handle_flags(false_scope, context)
