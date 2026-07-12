# coding=utf-8
from typing import cast

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

        val: Variable | Literal = args["value"].value
        result_path = DataPath.from_symbol(context, result)
        if isinstance(val, Literal):
            context.current_scope.add_command(
                Copy.copy_literals(
                    result_path,
                    abs(int(cast(int | bool | str, val.value)))
                )
            )

        else:
            if result.name != val.name:
                context.current_scope.add_command(
                    Copy.copy(
                        result_path,
                        DataPath.from_symbol(context, val)
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


class BinaryOpCommand(CommandHandler):
    """
    通用二元运算命令基类。
    子类只需声明 op，无需重写 handle。
    """
    no_size_effects = True
    op: BinaryOps = None  # 子类声明

    def handle(self, result, context, args):
        assert result is not None
        a = args["a"].value
        b = args["b"].value
        result_path = DataPath(
            context.current_scope.get_symbol_path(result),
            context.objective
        )
        a_path = a.value if isinstance(a, Literal) else DataPath(
            context.current_scope.get_symbol_path(a), context.objective
        )
        b_path = b.value if isinstance(b, Literal) else DataPath(
            context.current_scope.get_symbol_path(b), context.objective
        )
        context.add_commands(BinaryOp.op_all(result_path, self.op, a_path, b_path))  # noqa


@CommandRegistry.register('min')
class MinCommand(BinaryOpCommand):
    op = BinaryOps.MIN


@CommandRegistry.register('max')
class MaxCommand(BinaryOpCommand):
    op = BinaryOps.MAX
