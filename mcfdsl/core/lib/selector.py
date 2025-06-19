from typing import Callable

from mcfdsl.core._interfaces import ISymbol
from mcfdsl.core.language_types import TargetSelectorVariables
from mcfdsl.core.lib.lib_base import Lib


class Selector(Lib):
    def const(self) -> list[ISymbol]:
        pass

    def load(self) -> None:
        pass

    def method(self) -> list[Callable[..., list[str]]]:
        pass

    var:TargetSelectorVariables
    arguments:dict

    def __str__(self):
        format_argument = lambda key: f"{key} = {self.arguments[key]}"
        arguments_str = ', '.join(map(format_argument, self.arguments))
        return f"{self.var.value}[{arguments_str}]"

