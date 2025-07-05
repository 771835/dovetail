# coding=utf-8
from __future__ import annotations

from dataclasses import dataclass

from mcfdsl.core.language_types import DataType
from mcfdsl.core.symbols.base import NewSymbol
from mcfdsl.core.symbols.class_ import Class
from mcfdsl.core.symbols.reference import Reference


@dataclass
class Variable(NewSymbol):
    name: str
    dtype: DataType | 'Class'
    value: Reference = None

    def get_name(self) -> str:
        return self.name
