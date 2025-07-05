# coding=utf-8
from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, NoReturn

from mcfdsl.core.symbols.base import NewSymbol

if TYPE_CHECKING:
    from mcfdsl.core.language_types import DataType
    from mcfdsl.core.symbols.variable import Variable
    from mcfdsl.core.symbols.class_ import Class


@dataclass
class Function(NewSymbol):
    name: str
    params: list[Variable]
    return_type: DataType | 'Class'

    def get_name(self) -> NoReturn:
        return self.name
