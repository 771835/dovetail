# coding=utf-8

from attrs import define, field, validators

from .base import Symbol
from ..enums.types import DataType


@define(slots=True, frozen=True)
class Literal(Symbol):
    dtype: DataType = field(validator=validators.instance_of(DataType))
    value: str | int | bool | None = field(validator=validators.instance_of(str | int | bool | None))

    def get_name(self) -> None:
        """
        返回空值
        """
        return
