# coding=utf-8

from typing import Any, Callable

from attrs import define, field, validators

from transpiler.core.enums import DataType, ValueType
from transpiler.core.symbols.literal import Literal
from transpiler.core.symbols.reference import Reference


@define(slots=True, frozen=True)
class Result:
    """表达式求值结果容器"""
    value: Reference | None = field(validator=validators.instance_of(Reference | None))
    error: bool = field(validator=validators.instance_of(bool), default=False)
    error_type: str | None = field(validator=validators.instance_of(str | None), default=None)
    error_message: str | None = field(validator=validators.instance_of(str | None), default=None)

    def OK(self, function: Callable):
        """成功时处理"""
        if not self.error:
            function(self)
        return self

    def ERR(self, function: Callable):
        """错误时处理"""
        if self.error:
            function(self)
        return self

    def __str__(self):
        return self.__repr__()

    @classmethod
    def from_literal(cls, value: Any, dtype: DataType):
        """创建字面量结果"""
        return cls(
            value=Reference(ValueType.LITERAL, Literal(dtype, value))
        )

    @classmethod
    def create_error(cls, error_type: str, message: str):
        """创建错误结果"""
        return cls(
            value=None,
            error_message=message,
            error=True,
            error_type=error_type
        )
