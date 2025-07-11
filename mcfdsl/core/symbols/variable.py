# coding=utf-8
from __future__ import annotations

from dataclasses import dataclass

from mcfdsl.core.language_enums import DataType
from mcfdsl.core.symbols.base import NewSymbol
from mcfdsl.core.symbols.class_ import Class


@dataclass
class Variable(NewSymbol):
    name: str
    dtype: DataType | 'Class'

    def get_name(self) -> str:
        return self.name

    def __hash__(self):
        return hash((self.name, self.dtype))
