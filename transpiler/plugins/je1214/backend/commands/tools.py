# coding=utf-8
from enum import auto

from attrs import define

from transpiler.core.enums import DataType
from transpiler.core.enums.types import DataTypeBase
from transpiler.utils.safe_enum import SafeEnum


class StorageLocation(SafeEnum):
    STORAGE = auto()
    SCORE = auto()

    @staticmethod
    def get_storage(dtype: DataTypeBase) -> 'StorageLocation':
        if dtype in (DataType.BOOLEAN, DataType.INT):
            return StorageLocation.SCORE
        else:
            return StorageLocation.STORAGE


@define(slots=True,frozen=True)
class DataPath:
    """
    数据路径

    表示一个存储地址或一个积分项
    """

    path: str
    target: str
    location: StorageLocation = StorageLocation.SCORE

    def __iter__(self):
        yield self.path
        yield self.target

    def __reversed__(self):
        yield self.target
        yield self.path


class LiteralPoolTools:
    @staticmethod
    def get_literal_path_str(literal):
        if isinstance(literal, str):
            return f"literal_pool.str.{hash(literal)}"
        elif isinstance(literal, int):
            return f"literal_pool.int.{'n' if literal < 0 else ''}{abs(literal)}"
        else:
            raise TypeError(f"literal type {type(literal)} is not supported")

    @staticmethod
    def get_literal_path(literal: int | bool | str, target: str) -> DataPath:
        assert isinstance(literal, (int, bool, str)), f"literal type {type(literal)} is not supported"
        if isinstance(literal, str):
            return DataPath(f"literal_pool.str.{hash(literal)}", target, StorageLocation.STORAGE)
        elif isinstance(literal, int):
            return DataPath(f"literal_pool.int.{'n' if literal < 0 else ''}{abs(literal)}", target)
