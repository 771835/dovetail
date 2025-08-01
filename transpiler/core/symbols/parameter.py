# coding=utf-8
from __future__ import annotations

from typing import TYPE_CHECKING, NoReturn

from attrs import define, field, validators

from transpiler.core.enums import DataType
from .base import NewSymbol
from .reference import Reference
from .variable import Variable

if TYPE_CHECKING:
    from . import Literal, Constant, Class


@define(slots=True)
class Parameter(NewSymbol):
    var: Variable = field(validator=validators.instance_of(Variable))
    optional: bool = field(validator=validators.instance_of(bool), default=False)
    default: Reference[Variable | Literal | Constant] = field(
        validator=validators.instance_of(None | Reference), default=None)

    def get_name(self) -> NoReturn:
        return self.var.get_name()

    def get_data_type(self) -> 'Class' | DataType:
        return self.var.dtype

    def __hash__(self):
        return hash((self.var, self.optional))
