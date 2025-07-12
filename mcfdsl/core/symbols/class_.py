# coding=utf-8
from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional

from mcfdsl.core.symbols.base import NewSymbol
from mcfdsl.core.symbols.reference import Reference

if TYPE_CHECKING:
    from mcfdsl.core.symbols.constant import Constant
    from mcfdsl.core.symbols.function import Function
    from mcfdsl.core.symbols.variable import Variable


@dataclass
class Class(NewSymbol):
    name: str
    methods: list[Function]  # 方法列表（保持有序）
    interfaces: Optional[Class]
    parent: Optional[Class]
    constants: set[Reference[Constant]]
    variables: list[Reference[Variable]]

    def get_name(self) -> str:
        return self.name

    def __hash__(self):
        return hash((self.name, tuple(self.methods), self.interfaces, self.parent, tuple(self.constants),
                     tuple(self.variables)))
