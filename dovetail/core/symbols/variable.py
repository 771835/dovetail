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
    mutable: bool = True

    def is_mutable(self):
        """
        符号是否可变

        Returns:
            一个bool类型的数值，表示符号是否可变
        """
        return self.mutable

    def get_name(self) -> str:
        """
        获取变量名

        Returns:
            变量的名称
        """
        return self.name

    def get_dtype(self) -> DataTypeBase:
        return self.dtype

    def __hash__(self):
        return hash((self.name, id(self.dtype), self.var_type))
