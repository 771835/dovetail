# coding=utf-8

from attrs import define, field

from .annotation import Annotation
from .base import Symbol
from .parameter import Parameter
from ..enums.types import FunctionType, DataTypeBase


@define(slots=True, repr=False)
class Function(Symbol):
    name: str
    params: list[Parameter]
    return_type: DataTypeBase
    function_type: FunctionType = FunctionType.FUNCTION
    annotations: list[Annotation] = field(factory=list)

    def get_name(self) -> str:
        """
        获得函数名称

        Returns:
            (str): 函数的名称
        """
        return self.name

    def __repr__(self):
        return f"{self.name}({', '.join(map(repr, self.params))}): {self.return_type.get_name()}"

    def __hash__(self):
        return hash((self.name, tuple(self.params), id(self.return_type)))
