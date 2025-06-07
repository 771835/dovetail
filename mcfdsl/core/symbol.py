from __future__ import annotations

from mcfdsl.core._interfaces import ISymbol, IScope
from mcfdsl.core.types import SymbolType, Type


class Symbol(ISymbol):
    def __init__(self, name: str, symbol_type: SymbolType, data_type: Type = None):
        self.name = name
        self.type = symbol_type
        self.data_type = data_type
        self.value = None  # 用于存储初始值或记录代码中指定的值

    def get_unique_name(self, scope: IScope):
        return scope.get_name() + "_" + self.name
