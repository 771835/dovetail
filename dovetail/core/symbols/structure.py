# coding=utf-8
from __future__ import annotations

from typing import TYPE_CHECKING

from attrs import define, field

from .base import Symbol, Annotatable, MethodHost
from ..enums.datatypes import DataTypeBase

if TYPE_CHECKING:
    from dovetail.core.annotations.base import AnnotationAttachment
    from .function import Function


@define(slots=True, frozen=True, hash=False)
class Structure(Symbol, DataTypeBase, Annotatable, MethodHost):
    name: str
    fields: dict[str, DataTypeBase]
    methods: dict[str, Function]
    annotations: dict[str, AnnotationAttachment] = field(factory=dict)

    def get_name(self) -> str:
        return self.name

    def get_dtype(self) -> DataTypeBase:
        return self

    def __hash__(self):
        return hash((self.name, id(self.fields), id(self.methods), id(self.annotations)))
