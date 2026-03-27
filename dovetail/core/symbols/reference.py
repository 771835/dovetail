# coding=utf-8
from __future__ import annotations

from typing import Optional, TypeVar, Generic

from attrs import define

from .base import Symbol
from .literal import Literal
from .variable import Variable
from ..config import FAST_MODE
from ..enums.types import DataTypeBase, DataType, ValueType, VariableType

T = TypeVar('T', bound=Symbol)


@define(slots=True, hash=True, repr=False)
class Reference(Symbol, Generic[T]):
    value: T

    if not FAST_MODE:
        def __attrs_post_init__(self):
            if isinstance(self.value, Reference):
                # 对于多重引用的情况自动拆解
                self.value = self.value.value  # type: ignore
                from warnings import warn
                warn("不应该存在的多重引用")

    @property
    def value_type(self) -> ValueType:
        from . import Class, Function
        if isinstance(self.value, Function):
            return ValueType.FUNCTION
        elif isinstance(self.value, Class):
            return ValueType.CLASS
        elif isinstance(self.value, Literal):
            return ValueType.LITERAL
        else:
            return ValueType.VARIABLE

    def get_name(self) -> Optional[str]:
        """
        返回所引用的符号的名称

        Returns:
            Optional[str]: 所引用符号的名称，当为字面量时返回None
        """
        if self.is_literal():
            assert isinstance(self.value, Literal)
            return str(self.value.value)
        return self.value.get_name()

    def get_dtype(self) -> DataTypeBase:
        return self.value.get_dtype()

    @classmethod
    def literal(cls: type[Reference[Literal]], value: bool | int | float | str | None) -> Reference[Literal]:
        return cls(Literal(DataType.from_literal(value), value))

    @classmethod
    def variable(cls: type[Reference[Variable]], var_name: str, dtype: DataType,
                 var_type: VariableType = VariableType.COMMON,
                 mutable: bool = True) -> Reference[Variable]:
        return cls(Variable(var_name, dtype, var_type, mutable))

    def is_literal(self) -> bool:
        return self.value_type == ValueType.LITERAL

    def get_display_value(self) -> str:
        from . import Literal
        if self.is_literal():
            assert isinstance(self.value, Literal)
            return repr(self.value.value)
        else:
            return self.get_name()

    def __repr__(self):
        return self.get_display_value()
