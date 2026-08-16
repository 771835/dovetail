# coding=utf-8
import hashlib
from enum import auto

from attrs import define

from dovetail.core.backend import GenerationContext
from dovetail.core.enums import PrimitiveDataType
from dovetail.core.enums.datatypes import DataTypeBase
from dovetail.core.symbols import Symbol
from dovetail.utils.safe_enum import SafeEnum


class StorageLocation(SafeEnum):
    STORAGE = auto()
    SCORE = auto()

    @staticmethod
    def get_storage(dtype: DataTypeBase) -> 'StorageLocation':
        if dtype in (PrimitiveDataType.BOOLEAN, PrimitiveDataType.INT):
            return StorageLocation.SCORE
        else:
            return StorageLocation.STORAGE


@define(slots=True, frozen=True)
class DataPath:
    """
    数据路径

    表示一个存储地址或一个积分项
    """

    path: str
    target: str
    location: StorageLocation = StorageLocation.SCORE

    @classmethod
    def from_symbol(cls, context: GenerationContext, symbol: Symbol) -> 'DataPath':
        return cls(
            context.current_scope.get_symbol_path(symbol.get_name()),
            context.objective,
            StorageLocation.get_storage(symbol.get_dtype())
        )

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
            return f"literal_pool.str.{hashlib.md5(literal.encode()).hexdigest()}"
        elif isinstance(literal, bool):
            return f"literal_pool.bool.{str(literal).lower()}"
        elif isinstance(literal, int):
            return f"literal_pool.int.{'n' if literal < 0 else ''}{abs(literal)}"
        elif literal is None:
            return f"null"
        else:
            raise TypeError(f"literal type {type(literal)} is not supported")

    @staticmethod
    def get_literal_path(literal: int | bool | str | None, target: str) -> DataPath:
        path_str = LiteralPoolTools.get_literal_path_str(literal)
        return DataPath(path_str, target, StorageLocation.STORAGE if isinstance(literal, str) else StorageLocation.SCORE)
