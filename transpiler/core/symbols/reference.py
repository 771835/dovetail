# coding=utf-8
from __future__ import annotations

import warnings
from typing import TYPE_CHECKING, TypeVar, Generic

from attrs import define, field, validators

from .base import Symbol
from .literal import Literal
from .variable import Variable
from ..enums.types import DataTypeBase, DataType, ValueType, VariableType

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
            # 对于多重引用的情况自动拆解
            warnings.warn("多重引用")
            self.value_type = self.value.value_type
            self.value = self.value.value

    def get_name(self) -> str | None:
        """
        返回所引用的符号的名称

        :return: 符号名称
        """
        return self.value.get_name()

    def get_data_type(self) -> DataTypeBase:
        """
        返回所引用的符号的数据类型

        :return: 符号数据类型
        """
        from . import Class, Function, Parameter
        if isinstance(self.value, Class):
            return self.value
        elif isinstance(self.value, Function):
            return DataType.Function
        elif isinstance(self.value, Parameter):
            return self.value.get_data_type()
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
            raise TypeError(f"Unsupported literal type: {type(value)}")

    @classmethod
    def variable(cls, var_name, dtype: DataType, var_type: VariableType = VariableType.COMMON) -> Reference:
        return cls(ValueType.VARIABLE, Variable(var_name, dtype, var_type))

    def is_literal(self) -> bool:
        return self.value_type == ValueType.LITERAL