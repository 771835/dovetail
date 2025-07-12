# coding=utf-8
from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from mcfdsl.core.language_enums import DataType, VariableType
from mcfdsl.core.symbols.base import NewSymbol

if TYPE_CHECKING:
    from mcfdsl.core.symbols import Class


@dataclass
class Constant(NewSymbol):
    name: str
    dtype: DataType | Class
    var_type: VariableType = VariableType.GENERAL

    def get_name(self) -> str:
        return self.name

    def __hash__(self):
        return hash((self.name, self.dtype, self.var_type))
