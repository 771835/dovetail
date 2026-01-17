# coding=utf-8
from __future__ import annotations

from attrs import define

from .base import Symbol
from .parameter import Parameter
from ..enums.types import FunctionType, DataTypeBase


@define(slots=True)
class Function(Symbol):
    name: str
    params: list[Parameter]
    return_type: DataTypeBase
    function_type: FunctionType = FunctionType.FUNCTION
    annotations: list[str] = None

    def __attrs_post_init__(self):
        if self.annotations is None:
            self.annotations = []

    def get_name(self) -> str:
        """
        获得函数名称

        :return: 函数的名称
        """
        return self.name

    def __hash__(self):
        return hash((self.name, tuple(self.params), id(self.return_type)))
