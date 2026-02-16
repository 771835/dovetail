# coding=utf-8
from __future__ import annotations

from attrs import define

from .base import Symbol
from .constant import Constant
from .literal import Literal
from .reference import Reference
from .variable import Variable
from ..enums.types import DataTypeBase


@define(slots=True,repr=False)
class Parameter(Symbol):
    var: Variable
    optional: bool = False
    default: Reference[Variable | Literal | Constant] = None

    def get_name(self) -> str:
        return self.var.get_name()

    def get_data_type(self) -> DataTypeBase:
        return self.var.dtype

    def __repr__(self):
        return f"{self.var.name}: {self.var.dtype.get_name()}"

    def __hash__(self):
        return hash((self.var, self.optional))
