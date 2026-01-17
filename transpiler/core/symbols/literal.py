# coding=utf-8

from attrs import define

from .base import Symbol
from ..enums.types import DataTypeBase


@define(slots=True, frozen=True)
class Literal(Symbol):
    dtype: DataTypeBase
    value: str | int | bool | None

    def get_name(self) -> None:
        """
        返回空值
        """
        return
