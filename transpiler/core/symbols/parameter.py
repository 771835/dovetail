# coding=utf-8
from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, NoReturn

from transpiler.core.enums import DataType
from transpiler.core.symbols.base import NewSymbol

if TYPE_CHECKING:
    from transpiler.core.symbols import Variable, Reference, Literal, Constant, Class


@dataclass
class Parameter(NewSymbol):
    var: Variable
    optional: bool = False
    default: Reference[Variable | Literal | Constant] = None

    def get_name(self) -> NoReturn:
        return self.var.get_name()

    def get_data_type(self) -> Class | DataType:
        return self.var.dtype

    def __hash__(self):
        return hash((self.var, self.optional))
