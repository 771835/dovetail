# coding=utf-8
from __future__ import annotations

from attrs import define, field, validators

from .base import Symbol
from ..enums.types import DataTypeBase, VariableType


@define(slots=True)
class Constant(Symbol):
    name: str = field(validator=validators.instance_of(str))
    dtype: DataTypeBase = field(validator=validators.instance_of(DataTypeBase))
    var_type: VariableType = field(validator=validators.instance_of(VariableType), default=VariableType.COMMON)

    def get_name(self) -> str:
        """
        获取常量名

        :return: 常量的名称
        """
        return self.name

    def __hash__(self):
        return hash((self.name, id(self.dtype), self.var_type))
