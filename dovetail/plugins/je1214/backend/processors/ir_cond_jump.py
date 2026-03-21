# coding=utf-8
"""
IRCondJump 指令处理器
"""
from dovetail.core.backend import ir_processor, GenerationContext
from dovetail.core.instructions import IRInstruction, IROpCode
from dovetail.core.symbols import Variable, Literal
from .ir_jump import IRJumpProcessor
from ..backend import JE1214Backend
from ..commands import FunctionBuilder, Execute


@ir_processor(JE1214Backend, IROpCode.COND_JUMP)
class IRCondJumpProcessor(IRJumpProcessor):
    def process(self, instruction: IRInstruction, context: GenerationContext):
        cond_var: Variable | Literal = instruction.get_operands()[0]
        true_scope_name: str | None = instruction.get_operands()[1]
        false_scope_name: str | None = instruction.get_operands()[2]

        if isinstance(cond_var, Literal):
            scope_name = true_scope_name if cond_var.value else false_scope_name
            if scope_name:
                scope = context.current_scope.resolve_scope(scope_name)
                context.current_scope.add_command(
                    FunctionBuilder.run(
                        f"{context.namespace}:{scope.get_absolute_path('/')}"
                    )
                )
        else:
            if true_scope_name:  # 生成条件满足时的作用域
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
            if false_scope_name:  # 生成条件不满足时的作用域
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
