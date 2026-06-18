# coding=utf-8
from __future__ import annotations

from typing import Optional
from typing import TYPE_CHECKING

from attrs import define, field

from .base import Symbol, AnnotationMixin
from ..enums.types import ClassType
from ..enums.datatypes import DataTypeBase

if TYPE_CHECKING:
    from . import Function, Variable
    from dovetail.core.annotations.base import AnnotationAttachment


@define(slots=True)
class Class(Symbol, DataTypeBase, AnnotationMixin):
    name: str
    methods: set[Function]
    interface: Optional[Class]
    parent: Optional[Class]
    properties: set[Variable]
    type: ClassType = ClassType.CLASS
    annotations: dict[str, "AnnotationAttachment"] = field(factory=dict)

    def get_name(self) -> str:
        return self.name

    def get_dtype(self) -> DataTypeBase:
        return self

    def is_subclass_of(self, other: DataTypeBase) -> bool:
        if self is other:
            return True
        current_class = self.parent
        while current_class:
            if current_class.parent is other:
                return True
            current_class = current_class.parent
        return False

    def __hash__(self):
        return hash(
            (
                self.name,
                tuple(self.methods),
                id(self.interface),
                id(self.parent),
                tuple(self.properties),
                self.type
            )
        )
