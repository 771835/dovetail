from __future__ import annotations

from typing import Any

from mcfdsl.core._interfaces import ISymbol, IScope
from mcfdsl.core.language_types import SymbolType, DataType, ValueType


class Symbol(ISymbol):
    def __init__(self, name: str, symbol_type: SymbolType, scope: IScope | None, data_type: DataType | None = None,
                 objective: str | None = None, value: Any = None, value_type: ValueType | None = None):
        self.name = name
        self.symbol_type = symbol_type
        self.data_type = data_type
        self.value_type = value_type
        self.scope = scope
        self.objective = objective
        self.value = value  # 用于存储初始值或记录代码中指定的值

    def get_unique_name(self):
        if self.scope:
            return self.scope.get_name() + "_" + self.name
        else:
            return self.name
