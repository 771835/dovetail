# coding=utf-8
from __future__ import annotations

from ._data import DataBuilder
from ._execute import Execute
from ._scoreboard import ScoreboardBuilder
from .tools import DataPath, StorageLocation


class Copy:
    """
    复制模块，用于生成复制数据的指令
    """
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
                .store_result_storage(*reversed(target), 'int', 1.0) # noqa
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
    ) -> str:
        assert isinstance(source, int | str | bool | None), f"Invalid literal type: {type(source)}"
        if isinstance(source, int):
            return ScoreboardBuilder.set_score(*target, int(source)) # noqa
        elif isinstance(source, str):
            return DataBuilder.modify_storage_set_value(*reversed(target), f"\"{source}\"")
        elif source is None:
            return ScoreboardBuilder.set_score(*target, 0) # noqa
        raise

    @staticmethod
    def copy(target: DataPath, source: DataPath) -> str:
        """
        复制函数

        将 source 的数据复制到 target

        Args:
            target: 目标位置
            source: 被复制的位置

        Returns:
            生成的指令
        """
        if target.location == source.location:
            # 两数据位于同一位置
            if target.location == StorageLocation.SCORE:
                return Copy.copy_score_to_score(target, source)
            return Copy.copy_storage_to_storage(target, source)
        else:  # 两数据位于不同位置
            if target.location == StorageLocation.SCORE:
                return Copy.copy_storage_to_score(target, source)
            return Copy.copy_score_to_storage(target, source)

    @staticmethod
    def copy_all(target: DataPath, source: DataPath | int | str | bool | None) -> str:
        """
        通用复制函数

        当 source 为 DataPath 时，将 source 的数据复制到 target

        当 source 为字面量时，将字面量赋值给 target

        Args:
            target: 目标位置
            source: 被复制的位置或字面量数据

        Returns:
            生成的指令
        """
        if isinstance(source, DataPath):
            return Copy.copy(target, source)
        else:
            return Copy.copy_literals(target, source)
