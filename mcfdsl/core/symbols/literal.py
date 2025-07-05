# coding=utf-8
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from mcfdsl.core.language_types import DataType
from mcfdsl.core.symbols.base import NewSymbol


@dataclass
class Literal(NewSymbol):
    dtype: DataType
    value: Any

    def get_name(self) -> str:
        ...
