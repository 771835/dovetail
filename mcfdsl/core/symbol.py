# coding=utf-8
from __future__ import annotations

from typing import Any

from mcfdsl.core._interfaces import ISymbol, IScope
from mcfdsl.core.command_builder import Composite, Scoreboard
from mcfdsl.core.command_builder._data import Data
from mcfdsl.core.language_class import Class
from mcfdsl.core.language_types import SymbolType, DataType, ValueType


class Symbol(ISymbol):
    def __init__(self, name: str, symbol_type: SymbolType, scope: IScope | None, data_type: DataType| Class | None = None,
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
            return self.scope.get_name() + "." + self.name
        else:
            return self.name

    def init_commands(self, value = None) -> str|None:
        if self.symbol_type != SymbolType.VARIABLE:
            return None

        if self.data_type in (DataType.INT, DataType.BOOLEAN, DataType.STRING):
            self.value = value
            return Composite.var_init(self, value)
        else:
            if isinstance(self.data_type, Class):
                # TODO: 处理class支持
                return None
            else:
                return None

    def del_commands(self) -> str|None:
        if self.symbol_type != SymbolType.VARIABLE:
            return None

        if self.data_type in (DataType.INT, DataType.BOOLEAN):
            return Scoreboard.reset_score(self.get_unique_name(), self.objective)
        elif self.data_type == DataType.STRING:
            return Data.remove_storage(self.get_unique_name(), self.get_storage_path())
        return None

    def get_storage_path(self) -> str:
        return f"{self.scope.namespace}:{self.objective}"