# coding=utf-8
from __future__ import annotations

import warnings
from dataclasses import dataclass
from typing import Any

from mcfdsl.core.language_enums import DataType, ValueType
from mcfdsl.core.symbols.literal import Literal
from mcfdsl.core.symbols.reference import Reference


@dataclass
class Result:
    """表达式求值结果容器"""
    value: Reference | None  # 实际值
    error: bool = False  # 是否错误结果
    error_type: str | None = None  # 错误类型标识
    error_message: str = None

    def OK(self, function: callable):
        """成功时处理"""
        if not self.error:
            function(self)
        return self

    def ERR(self, function: callable):
        """错误时处理"""
        if self.error:
            function(self)
        return self

    def __str__(self):
        return self.__repr__()

    def to_symbol(self, scope: 'Scope' = None, name: str = None,
                  objective: str = None):
        warnings.warn("方法已弃用", DeprecationWarning)

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
