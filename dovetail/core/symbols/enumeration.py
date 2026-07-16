# coding=utf-8
from __future__ import annotations

from typing import TYPE_CHECKING

from attrs import define, field

from .base import Symbol, Annotatable, MethodHost
from dovetail.core.enums.datatypes import DataTypeBase

if TYPE_CHECKING:
    from dovetail.core.symbols import Literal, Function
    from dovetail.core.annotations.base import AnnotationAttachment


@define(slots=True, frozen=True)
class Enumeration(Symbol, DataTypeBase, Annotatable, MethodHost):
    name: str
    member: dict[str, Literal]
    methods: dict[str, Function]
    annotations: dict[str, "AnnotationAttachment"] = field(factory=dict)

    def get_name(self) -> str:
        return self.name

    def get_dtype(self) -> DataTypeBase:
        return self
