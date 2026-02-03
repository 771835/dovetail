# coding=utf-8

from typing import Any

from attrs import define, field, validators

from transpiler.core.enums.types import DataType, ValueType
from transpiler.core.symbols.literal import Literal
from transpiler.core.symbols.reference import Reference


@define(slots=True, frozen=True)
class Result:
    """表达式求值结果容器"""
    value: Reference | None = field(validator=validators.instance_of(Reference | None))

    def __str__(self):
        return self.__repr__()

    @classmethod
    def from_literal(cls, value: Any, dtype: DataType):
        """创建字面量结果"""
        return cls(Reference(ValueType.LITERAL, Literal(dtype, value)))
