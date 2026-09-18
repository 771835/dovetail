# coding=utf-8
from __future__ import annotations

from typing import TYPE_CHECKING

from attrs import define, field

from .base import Symbol, Annotatable
from ..enums.datatypes import DataTypeBase

if TYPE_CHECKING:
    from dovetail.core.annotations.base import AnnotationAttachment


@define(slots=True, frozen=True, hash=False)
class Structure(Symbol, DataTypeBase, Annotatable):
    name: str
    fields: dict[str, DataTypeBase]
    annotations: dict[str, AnnotationAttachment] = field(factory=dict)

    def get_name(self) -> str:
        return self.name

    def get_dtype(self) -> DataTypeBase:
        return self

    def is_subclass_of(self, other: DataTypeBase) -> bool:
        if isinstance(other, Structure):
            return self.fields == other.fields # TODO:验证这行代码是否能正确的处理问题
        return super().is_subclass_of(other)

    def __hash__(self):
        return hash((self.name, id(self.fields), id(self.annotations)))

