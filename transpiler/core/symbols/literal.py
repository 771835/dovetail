# coding=utf-8
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from transpiler.core.language_enums import DataType
from transpiler.core.symbols.base import NewSymbol


@dataclass
class Literal(NewSymbol):
    dtype: DataType
    value: Any

    def get_name(self) -> str:
        ...

    def __hash__(self):
        return hash((self.dtype, self.value))
