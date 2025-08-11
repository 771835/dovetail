# coding=utf-8
from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar, Generic

from attrs import define, field, validators

from transpiler.core.enums import ValueType, DataType
from .base import Symbol
from .literal import Literal

if TYPE_CHECKING:
    from . import Class, Function
T = TypeVar(
    'T',
    'Variable', 'Constant', 'Literal', 'Function', 'Class'  # 使用字符串前向引用
)


@define(slots=True, hash=True)
class Reference(Symbol, Generic[T]):
    value_type: ValueType = field(validator=validators.instance_of(ValueType))
    value: T = field(validator=validators.instance_of(Symbol))

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
            self.value: Function
            return self.value.return_type
        elif self.value_type == ValueType.CLASS:
            return self.value
        else:
            return self.value.dtype

    @classmethod
    def literal(cls, value):
        if isinstance(value, bool):
            return cls(ValueType.LITERAL, Literal(DataType.BOOLEAN, value))
        elif isinstance(value, (int, float)):
            return cls(ValueType.LITERAL, Literal(DataType.INT, int(value)))
        elif isinstance(value, str):
            return cls(ValueType.LITERAL, Literal(DataType.STRING, str(value)))
        else:
            raise  # TODO:补上抱错
