# coding=utf-8
from __future__ import annotations
from typing import TYPE_CHECKING

from attrs import define, field

from .base import Symbol, AnnotationMixin
from ..enums import PrimitiveDataType
from ..enums.types import FunctionType

if TYPE_CHECKING:
    from .parameter import Parameter
    from ..annotations.base import AnnotationAttachment
    from ..enums.datatypes import DataTypeBase


@define(slots=True, repr=False)
class Function(Symbol, AnnotationMixin):
    name: str
    params: list[Parameter]
    return_type: DataTypeBase
    function_type: FunctionType = FunctionType.FUNCTION
    annotations: dict[str, AnnotationAttachment] = field(factory=dict)

    def get_name(self) -> str:
        return self.name

    def get_dtype(self) -> DataTypeBase:
        return PrimitiveDataType.FUNCTION

    def __repr__(self):
        return f"{self.name}({', '.join(map(repr, self.params))}): {self.return_type.get_name()}"

    def __hash__(self):
        return hash((self.name, tuple(self.params), id(self.return_type)))
