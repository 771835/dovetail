# coding=utf-8
from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, TypeVar, Generic

from mcfdsl.core.symbols.base import NewSymbol

if TYPE_CHECKING:
    from mcfdsl.core.language_types import ValueType, DataType
    from mcfdsl.core.symbols import Class, Constant, Literal, Variable, Function
T = TypeVar(
    'T',
    'Variable', 'Constant', 'Literal', 'Function', 'Class'  # 使用字符串前向引用
)


@dataclass
class Reference(NewSymbol, Generic[T]):
    value_type: ValueType
    value: T

    def get_name(self) -> str:
        return self.value.get_name()

    def get_data_type(self) -> DataType | Class:
        from mcfdsl.core.symbols.function import Function
        from mcfdsl.core.symbols.class_ import Class

        if isinstance(self.value, Function):
            return self.value.return_type
        elif isinstance(self.value, Class):
            return self.value
        else:
            from mcfdsl.core.symbols.variable import Variable
            from mcfdsl.core.symbols.constant import Constant
            from mcfdsl.core.symbols.literal import Literal

            # 确保类型安全（避免mypy错误）
            if isinstance(self.value, (Variable, Constant, Literal)):
                return self.value.dtype
            else:
                raise TypeError("Unsupported value type")
