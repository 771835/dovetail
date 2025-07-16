# coding=utf-8
from typing import Callable

from transpiler.core.lib.lib_base import Lib
from transpiler.core.safe_enum import SafeEnum
from transpiler.core.symbols import Constant


class TargetSelectorVariables(SafeEnum):
    NEAREST_PLAYER = "@p"
    RANDOM_PLAYER = "@r"
    ALL_PLAYER = "@a"
    ALL_ENTITIES = "@e"
    ENTITY_EXECUTING_COMMAND = "@s"
    NEAREST_ENTITY = "@n"


class Selector(Lib):
    def const(self) -> list[Constant]:
        pass

    def load(self) -> None:
        pass

    def method(self) -> list[Callable[..., list[str]]]:
        pass

    var: TargetSelectorVariables
    arguments: dict

    def __str__(self):
        def format_argument(key): return f"{key} = {self.arguments[key]}"

        arguments_str = ', '.join(map(format_argument, self.arguments))
        return f"{self.var.value}[{arguments_str}]"
