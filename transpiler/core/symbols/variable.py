# coding=utf-8
from __future__ import annotations

from typing import TYPE_CHECKING

from attrs import define, field, validators

from transpiler.core.enums import DataType, VariableType, DataTypeBase
from .base import NewSymbol

if TYPE_CHECKING:
    from .class_ import Class


@define(slots=True)
class Variable(NewSymbol):
    name: str = field(validator=validators.instance_of(str))
    dtype: DataType | Class = field(validator=validators.instance_of(DataTypeBase))
    var_type: VariableType = field(validator=validators.instance_of(VariableType), default=VariableType.COMMON)

    def get_name(self) -> str:
        return self.name

    def __hash__(self):
        return hash((self.name, id(self.dtype), self.var_type))
