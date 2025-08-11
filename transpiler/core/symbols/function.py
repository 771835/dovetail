# coding=utf-8
from __future__ import annotations

from typing import TYPE_CHECKING, NoReturn

from attrs import define, field, validators

from transpiler.core.enums import FunctionType, DataTypeBase, DataType
from .base import Symbol

if TYPE_CHECKING:
    from . import Parameter, Class


@define(slots=True)
class Function(Symbol):
    name: str = field(validator=validators.instance_of(str))
    params: list[Parameter] = field(validator=validators.instance_of(list))
    return_type: DataType | Class = field(validator=validators.instance_of(DataTypeBase))
    function_type: FunctionType = field(validator=validators.instance_of(FunctionType), default=FunctionType.FUNCTION)

    def get_name(self):
        return self.name

    def __hash__(self):
        return hash((self.name, tuple(self.params), id(self.return_type)))
