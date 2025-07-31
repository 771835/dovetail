# coding=utf-8
from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, NoReturn

from transpiler.core.enums import FunctionType
from transpiler.core.symbols.parameter import Parameter
from transpiler.core.symbols.base import NewSymbol

if TYPE_CHECKING:
    from transpiler.core.enums import DataType
    from transpiler.core.symbols.class_ import Class


@dataclass
class Function(NewSymbol):
    name: str
    params: list[Parameter]
    return_type: DataType | 'Class'
    function_type: FunctionType = FunctionType.FUNCTION

    def get_name(self) -> NoReturn:
        return self.name

    def __hash__(self):
        return hash((self.name, tuple(self.params), id(self.return_type)))
