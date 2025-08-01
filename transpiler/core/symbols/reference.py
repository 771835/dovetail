# coding=utf-8
from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar, Generic

from attrs import define, field, validators

from transpiler.core.enums import ValueType, DataType
from .base import NewSymbol

if TYPE_CHECKING:
    from . import Class
T = TypeVar(
    'T',
    'Variable', 'Constant', 'Literal', 'Function', 'Class'  # 使用字符串前向引用
)


@define(slots=True, hash=True)
class Reference(NewSymbol, Generic[T]):
    value_type: ValueType = field(validator=validators.instance_of(ValueType))
    value: T = field(validator=validators.instance_of(NewSymbol))

    def __attrs_post_init__(self):
        if isinstance(self.value, Reference):
            import warnings
            warnings.warn("多重引用")
            self.value_type = self.value.value_type
            self.value = self.value.value

    def get_name(self) -> str:
        return self.value.get_name()

    def get_data_type(self) -> DataType | Class:
        if self.value_type == ValueType.FUNCTION:
            return self.value.return_type
        elif self.value_type == ValueType.CLASS:
            return self.value
        else:
            return self.value.dtype
