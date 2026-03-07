# coding=utf-8
from __future__ import annotations

from typing import Optional

from attrs import define

from .base import Symbol
from .literal import Literal
from .reference import Reference
from .variable import Variable
from ..enums.types import DataTypeBase


@define(slots=True, repr=False, frozen=True)
class Parameter(Symbol):
    var: Variable
    mutable: bool = False
    default: Optional[Reference[Variable | Literal]] = None

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
