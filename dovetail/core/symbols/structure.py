# coding=utf-8
from __future__ import annotations

from typing import TYPE_CHECKING

from attrs import define, field

from .base import Symbol, AnnotationMixin
from ..enums.datatypes import DataTypeBase

if TYPE_CHECKING:
    from ..annotations.base import AnnotationAttachment


@define(slots=True, frozen=True)
class Structure(Symbol, DataTypeBase, AnnotationMixin):
    name: str
    fields: dict[str, DataTypeBase]
    annotations: dict[str, AnnotationAttachment] = field(factory=dict)

    def get_name(self) -> str:
        return self.name

    def get_dtype(self) -> DataTypeBase:
        return self
