# coding=utf-8

from attrs import define

from .base import Symbol
from ..enums.types import DataTypeBase


@define(slots=True, frozen=True)
class Literal(Symbol):
    dtype: DataTypeBase
    value: str | int | bool | None

    def get_name(self):
        """
        根据存储的数据返回其对应的展示名

        Returns:
            str: 存储的数据对应的展示名
        """
        return repr(self.value)

    def get_dtype(self):
        return self.dtype
