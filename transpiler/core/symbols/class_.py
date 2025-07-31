# coding=utf-8
from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional

from transpiler.core.enums import ClassType
from transpiler.core.symbols.base import NewSymbol
from transpiler.core.symbols.reference import Reference

if TYPE_CHECKING:
    from transpiler.core.symbols.constant import Constant
    from transpiler.core.symbols.function import Function
    from transpiler.core.symbols.variable import Variable


@dataclass
class Class(NewSymbol):
    name: str
    methods: list[Function]  # 方法列表
    interface: Optional[Class]
    parent: Optional[Class]
    constants: set[Reference[Constant]]
    variables: list[Reference[Variable]]
    type: ClassType = ClassType.CLASS

    def get_name(self) -> str:
        return self.name

    def __hash__(self):
        return hash((self.name, tuple(self.methods), id(self.interface), id(self.parent), tuple(self.constants),
                     tuple(self.variables), self.type))
