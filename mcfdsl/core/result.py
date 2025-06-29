# coding=utf-8
from __future__ import annotations

import uuid
from dataclasses import dataclass
from typing import Any

from mcfdsl.core._interfaces import ISymbol, IScope
from mcfdsl.core.language_types import DataType, ValueType, SymbolType
from mcfdsl.core.symbol import Symbol


@dataclass
class Result:
    """表达式求值结果容器"""
    value_type: ValueType  # 值的类型（变量引用/字面量等）
    data_type: DataType  # 数据类型（int/string等）
    value: Any  # 实际值 例如Symbol
    error: bool = False  # 是否错误结果
    error_type: str | None = None  # 错误类型标识

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

    def to_symbol(self, scope: IScope = None, name: str = None, objective: str = None):
        if self.value_type == ValueType.VARIABLE:
            assert isinstance(self.value, ISymbol)
            return self.value
        if name is None:
            name = f"__{uuid.uuid4().hex}_result__"

        if self.value_type == ValueType.LITERAL:
            if objective is None:
                return None
            return Symbol(name, SymbolType.VARIABLE, scope, self.data_type,
                          objective, self.value, ValueType.LITERAL)
        else:
            return None

    @classmethod
    def from_literal(cls, value: Any, dtype: DataType):
        """创建字面量结果"""
        return cls(
            value_type=ValueType.LITERAL,
            data_type=dtype,
            value=value
        )

    @classmethod
    def from_variable(cls, symbol: ISymbol):
        """创建变量引用结果"""
        return cls(
            value_type=ValueType.VARIABLE,
            data_type=symbol.data_type,
            value=symbol
        )

    @classmethod
    def create_error(cls, error_type: str, message: str):
        """创建错误结果"""
        return cls(
            value_type=ValueType.ERROR,
            data_type=DataType.VOID,
            value=message,
            error=True,
            error_type=error_type
        )
