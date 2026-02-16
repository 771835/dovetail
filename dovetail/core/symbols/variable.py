# coding=utf-8
from __future__ import annotations

from attrs import define

from .base import Symbol
from ..enums.types import DataTypeBase, VariableType


@define(slots=True)
class Variable(Symbol):
    """
    变量符号
    """
    name: str
    dtype: DataTypeBase
    var_type: VariableType = VariableType.COMMON

    def get_name(self) -> str:
        """
        获取变量名

        :return: 变量的名称
        """
        return self.name

    def __hash__(self):
        return hash((self.name, id(self.dtype), self.var_type))
