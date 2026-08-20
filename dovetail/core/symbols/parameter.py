# coding=utf-8
from __future__ import annotations

from typing import Optional

from attrs import define

from .base import Symbol
from .literal import Literal
from .reference import Reference
from .variable import Variable
from ..enums import VariableType
from ..enums.datatypes import DataTypeBase


@define(slots=True, repr=False, frozen=True)
class Parameter(Symbol):
    var: Variable
    default: Optional[Reference[Variable | Literal]] = None

    @property
    def dtype(self) -> DataTypeBase:
        return self.var.dtype

    @classmethod
    def new(cls, name: str, dtype: DataTypeBase, default: Optional[Reference] = None) -> Parameter:
        """
        快速构建参数

        Args:
            name: 参数名
            dtype: 参数类型
            default: 参数默认值

        Returns:
            参数实例
        """
        return Parameter(Variable(name, dtype, VariableType.PARAMETER), default)

    def is_optional(self) -> bool:
        """
        参数是否选填

        Returns:
            bool: 代表参数是否选填

        """
        return True if self.default is not None else False

    def get_name(self) -> str:
        return self.var.get_name()

    def get_dtype(self) -> DataTypeBase:
        return self.var.dtype

    def __repr__(self):
        if self.default is not None:
            return f"{self.var.name}: {self.var.dtype.get_name()} = {self.default}"
        return f"{self.var.name}: {self.var.dtype.get_name()}"
