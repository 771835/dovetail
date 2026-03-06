# coding=utf-8
from __future__ import annotations

from typing import TYPE_CHECKING

from attrs import define, field

from .annotation import Annotation
from .base import Symbol
from ..enums.types import DataTypeBase

if TYPE_CHECKING:
    from . import Literal


@define(slots=True, frozen=True)
class Enumeration(Symbol, DataTypeBase):
    name: str
    member: dict[str, Literal]
    annotations: list[Annotation] = field(factory=list)

    def get_name(self) -> str:
        return self.name

    def get_dtype(self) -> DataTypeBase:
        return self
