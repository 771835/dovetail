# coding=utf-8
from __future__ import annotations

from transpiler.utils.escape_processor import auto_escape
from ._data import DataBuilder
from ._execute import Execute
from ._scoreboard import ScoreboardBuilder
from .tools import DataPath, StorageLocation


class Copy:
    @staticmethod
    def copy_score_to_score(
            target: DataPath,
            source: DataPath,
    ):
        return ScoreboardBuilder.set_op(*target, *source)

    @staticmethod
    def copy_storage_to_storage(
            target: DataPath,
            source: DataPath,
    ):
        return DataBuilder.modify_storage_set_from_storage(*reversed(target), *reversed(source))

    @staticmethod
    def copy_storage_to_score(
            target: DataPath,
            source: DataPath,
    ):
        return Execute.execute().store_result_score(*target).run(DataBuilder.get_storage(*source))

    @staticmethod
    def copy_score_to_storage(
            target: DataPath,
            source: DataPath,
    ):
        return (Execute.execute()
                .store_result_storage(*reversed(target), 'int', 1.0)
                .run(ScoreboardBuilder.get_score(*source)))

    @staticmethod
    def copy_variables(
            target: DataPath,
            source: DataPath,
    ):
        if target.location == source.location:
            if target.location == StorageLocation.SCORE:
                return Copy.copy_score_to_score(target, source)
            elif target.location == StorageLocation.STORAGE:
                return Copy.copy_storage_to_storage(target, source)

        return None

    @staticmethod
    def copy_literals(
            target: DataPath,
            source: int | str | bool | None
    ):
        assert isinstance(source, int | str | bool | None), f"Invalid literal type: {type(source)}"
        if isinstance(source, int):
            return ScoreboardBuilder.set_score(*target, int(source))
        elif isinstance(source, str):
            return DataBuilder.modify_storage_set_value(*reversed(target), f"\"{auto_escape(source)}\"")
        elif source is None:
            return ScoreboardBuilder.set_score(*target, 0)

    @staticmethod
    def copy(
            target: DataPath,
            source: DataPath
    ):
        if target.location == source.location:
            if target.location == StorageLocation.SCORE:
                return Copy.copy_score_to_score(target, source)
            return Copy.copy_storage_to_storage(target, source)
        else:
            if target.location == StorageLocation.SCORE:
                return Copy.copy_score_to_storage(target, source)
            return Copy.copy_storage_to_score(target, source)

    @staticmethod
    def copy_all(
            target: DataPath,
            source: DataPath | int | str | bool | None
    ):
        if isinstance(source, DataPath):
            return Copy.copy(target, source)
        else:
            return Copy.copy_literals(target, source)
