# coding=utf-8
from __future__ import annotations

from typing import TypeVar, Generic

from attrs import define

from .base import Symbol

from ..enums.types import DataTypeBase, DataType, ValueType, VariableType

T = TypeVar('T', bound=Symbol)


@define(slots=True, hash=True, repr=False)
class Reference(Symbol, Generic[T]):
    value: T

    def __attrs_post_init__(self):
        if isinstance(self.value, Reference):
            # 对于多重引用的情况自动拆解
            self.value = self.value.value

    @property
    def value_type(self) -> ValueType:
        from . import Class, Function, Literal
        if isinstance(self.value, Function):
            return ValueType.FUNCTION
        elif isinstance(self.value, Class):
            return ValueType.CLASS
        elif isinstance(self.value, Literal):
            return ValueType.LITERAL
        else:
            return ValueType.VARIABLE

    def get_name(self) -> str | None:
        """
        返回所引用的符号的名称

        :return: 符号名称
        """
        return self.value.get_name()

    def get_dtype(self) -> DataTypeBase:
        return self.value.get_dtype()

    @classmethod
    def literal(cls, value):
        from .literal import Literal
        if isinstance(value, bool):
            return cls(Literal(DataType.BOOLEAN, value))
        elif isinstance(value, (int, float)):
            return cls(Literal(DataType.INT, int(value)))
        elif isinstance(value, str):
            return cls(Literal(DataType.STRING, str(value)))
        elif value is None:
            return cls(Literal(DataType.NULL_TYPE, None))
        else:
            raise TypeError(f"Unsupported literal type: {type(value)}")

    @classmethod
    def variable(cls, var_name, dtype: DataType, var_type: VariableType = VariableType.COMMON,
                 mutable: bool = True) -> Reference:
        from .variable import Variable
        return cls(Variable(var_name, dtype, var_type, mutable))

    def is_literal(self) -> bool:
        return self.value_type == ValueType.LITERAL

    def get_display_value(self) -> str | None:
        from . import Literal
        if self.is_literal():
            assert isinstance(self.value, Literal)
            return repr(self.value.value)
        else:
            return self.get_name()

    def __repr__(self):
        return self.get_display_value()
