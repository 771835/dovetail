from __future__ import annotations

from transpiler.core.symbols import Variable
from transpiler.utils.escape_processor import auto_escape
from ._data import DataBuilder
from ._scoreboard import ScoreboardBuilder


class MCCopy:
    @staticmethod
    def copy_variable_base_type(
            target: Variable,
            target_scope: CodeGeneratorScope,
            target_objective: str,
            source: Variable | Constant,
            source_scope: CodeGeneratorScope,
            source_objective: str
    ):
        if source.dtype == DataType.STRING:
            return DataBuilder.modify_storage_set_from_storage(
                f"{target_objective}",
                target_scope.get_symbol_path(target.get_name()),
                f"{source_objective}",
                source_scope.get_symbol_path(source.get_name()))
        elif source.dtype in (DataType.INT, DataType.BOOLEAN):
            return ScoreboardBuilder.set_op(
                target_scope.get_symbol_path(target.get_name()),
                target_objective,
                source_scope.get_symbol_path(source.get_name()),
                source_objective)
        return None

    @staticmethod
    def copy_literal_base_type(
            target_path: str,
            target_objective: str,
            source: int | str | bool | None
    ):
        if isinstance(source, int):
            return ScoreboardBuilder.set_score(target_path, target_objective, int(source))
        elif isinstance(source, str):
            return DataBuilder.modify_storage_set_value(target_objective, target_path, auto_escape(source))
        return None

    @staticmethod
    def copy_score_to_storage(
            target: Variable | Constant,
            target_scope: CodeGeneratorScope,
            target_objective: str
    ):
        return (
            Execute.execute()
            .store_result_storage(
                target_objective,
                BasicCommands.get_symbol_path(target_scope, target),
                'int',
                1.0
            )
            .run(
                ScoreboardBuilder.get_score(
                    BasicCommands.get_symbol_path(target_scope, target),
                    target_objective
                )
            )
        )

    @staticmethod
    def copy_base_type(
            target: Variable | Constant,
            target_scope: CodeGeneratorScope,
            target_objective: str,
            source: Variable | Constant | Literal,
            source_scope: CodeGeneratorScope,
            source_objective: str
    ) -> str | None:
        if target.get_name() == source.get_name() and target_scope == source_scope:
            return ""
        if isinstance(source, Literal):
            return BasicCommands.Copy.copy_literal_base_type(
                target,
                target_scope,
                target_objective,
                source
            )
        else:
            return BasicCommands.Copy.copy_variable_base_type(
                target,
                target_scope,
                target_objective,
                source,
                source_scope,
                source_objective
            )

    @staticmethod
    def copy(
            target: Variable | Constant,
            target_scope: CodeGeneratorScope,
            target_objective: str,
            source: Variable | Constant | Literal,
            source_scope: CodeGeneratorScope,
            source_objective: str
    ):
        if isinstance(target.dtype, DataType):
            return BasicCommands.Copy.copy_base_type(
                target,
                target_scope,
                target_objective,
                source,
                source_scope,
                source_objective
            )
        else:
            assert isinstance(target.dtype, Class)
            # 类仅存储引用
            return ScoreboardBuilder.set_op(
                BasicCommands.get_symbol_path(target_scope, target),
                target_objective,
                BasicCommands.get_symbol_path(source_scope, source),
                source_objective
            )


@staticmethod
def get_symbol_path(scope: CodeGeneratorScope, symbol: Symbol | str):
    return scope.get_symbol_path(symbol.get_name() if isinstance(symbol, Symbol) else symbol)
