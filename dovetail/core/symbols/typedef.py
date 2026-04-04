# coding=utf-8
from __future__ import annotations

import attrs

from .base import Symbol
from ..enums.types import DataTypeBase


@attrs.define(slots=True, frozen=True)
class Typedef(Symbol):
    name: str
    dtype: DataTypeBase

    def get_name(self) -> str:
        return self.name

    def get_dtype(self) -> DataTypeBase:
        return self.dtype
