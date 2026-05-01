# coding=utf-8
from dovetail.core.backend import GenerationContext
from dovetail.core.enums import BinaryOps
from dovetail.core.symbols import Variable, Reference, Literal
from ..base import CommandRegistry, CommandHandler
from ... import Copy, DataPath, Execute, ScoreboardBuilder, LiteralPoolTools, BinaryOp


@CommandRegistry.register('abs')
class AbsCommand(CommandHandler):
    no_size_effects = True

    def handle(self, result: Variable | None, context: GenerationContext, args: dict[str, Reference]):
        assert result is not None

        value: Variable | Literal = args["value"].value
        result_path = DataPath(context.current_scope.get_symbol_path(result), context.objective)
        if isinstance(value, Literal):
            context.current_scope.add_command(
                Copy.copy_literals(
                    result_path,
                    abs(value.value)
                )
            )

        else:
            if result.name != value.name:
                context.current_scope.add_command(
                    Copy.copy(
                        result_path,
                        DataPath(context.current_scope.get_symbol_path(value), context.objective)
                    )
                )
            context.current_scope.add_command(
                Execute.execute()
                .if_score_matches(
                    *result_path,
                    "..0"
                )
                .run(
                    ScoreboardBuilder.mul_op(
                        *result_path,
                        *LiteralPoolTools.get_literal_path(-1, context.objective)
                    )
                )
            )


@CommandRegistry.register('min')
class MinCommand(CommandHandler):
    no_size_effects = True

    def handle(self, result: Variable | None, context: GenerationContext, args: dict[str, Reference]):
        assert result is not None
        a = args["a"].value
        b = args["b"].value
        result_path = DataPath(context.current_scope.get_symbol_path(result), context.objective)
        a_path = a.value if isinstance(a, Literal) else DataPath(context.current_scope.get_symbol_path(a),
                                                                 context.objective)
        b_path = b.value if isinstance(b, Literal) else DataPath(context.current_scope.get_symbol_path(b),
                                                                 context.objective)

        context.add_commands(BinaryOp.op_all(result_path, BinaryOps.MIN, a_path, b_path))


@CommandRegistry.register('max')
class MaxCommand(CommandHandler):
    no_size_effects = True

    def handle(self, result: Variable | None, context: GenerationContext, args: dict[str, Reference]):
        assert result is not None
        a = args["a"].value
        b = args["b"].value
        result_path = DataPath(context.current_scope.get_symbol_path(result), context.objective)
        a_path = a.value if isinstance(a, Literal) else DataPath(context.current_scope.get_symbol_path(a),
                                                                 context.objective)
        b_path = b.value if isinstance(b, Literal) else DataPath(context.current_scope.get_symbol_path(b),
                                                                 context.objective)

        context.add_commands(BinaryOp.op_all(result_path, BinaryOps.MAX, a_path, b_path))
