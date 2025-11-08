# coding=utf-8
from __future__ import annotations

from typing import TYPE_CHECKING

from attrs import define, field, validators

from .base import Symbol
from ..enums.types import FunctionType, DataTypeBase, DataType

if TYPE_CHECKING:
    # 仅类型检查时导入
    from . import Parameter, Class


@define(slots=True)
class Function(Symbol):
    name: str = field(validator=validators.instance_of(str))
    params: list[Parameter] = field(validator=validators.instance_of(list))
    return_type: DataType | Class = field(validator=validators.instance_of(DataTypeBase))
    function_type: FunctionType = field(validator=validators.instance_of(FunctionType), default=FunctionType.FUNCTION)
    annotations: list[str] = field(validator=validators.instance_of(list), default=[])

    def get_name(self):
        """
        获得函数名称

        :return: 函数的名称
        """
        return self.name

    def __hash__(self):
        return hash((self.name, tuple(self.params), id(self.return_type)))
