# coding=utf-8
from __future__ import annotations

import warnings
from dataclasses import dataclass
from typing import TYPE_CHECKING, TypeVar, Generic

from transpiler.core.symbols.base import NewSymbol

if TYPE_CHECKING:
    from transpiler.core.language_enums import ValueType, DataType
    from transpiler.core.symbols import Class, Constant, Literal, Variable, Function
T = TypeVar(
    'T',
    'Variable', 'Constant', 'Literal', 'Function', 'Class'  # 使用字符串前向引用
)


@dataclass(unsafe_hash=True)
class Reference(NewSymbol, Generic[T]):
    value_type: ValueType
    value: T

    def __post_init__(self):
        if isinstance(self.value, Reference):
            warnings.warn("多重引用")
            self.value_type = self.value.value_type
            self.value = self.value.value

    def get_name(self) -> str:
        return self.value.get_name()

    def get_data_type(self) -> DataType | Class:
        from transpiler.core.symbols.function import Function
        from transpiler.core.symbols.class_ import Class

        if isinstance(self.value, Function):
            return self.value.return_type
        elif isinstance(self.value, Class):
            return self.value
        else:
            from transpiler.core.symbols.variable import Variable
            from transpiler.core.symbols.constant import Constant
            from transpiler.core.symbols.literal import Literal

            # 确保类型安全（避免mypy错误）
            if isinstance(self.value, (Variable, Constant, Literal)):
                return self.value.dtype
            else:
                raise TypeError("Unsupported value type")
