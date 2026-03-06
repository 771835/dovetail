# coding=utf-8
from __future__ import annotations

import attrs

from .annotation import Annotation
from .base import Symbol
from ..enums.types import DataTypeBase


@attrs.define(slots=True, frozen=True)
class Structure(Symbol, DataTypeBase):
    name: str
    field: dict[str, DataTypeBase]
    annotations: list[Annotation] = attrs.field(factory=list)

    def get_name(self) -> str:
        return self.name

    def get_dtype(self) -> DataTypeBase:
        return self
