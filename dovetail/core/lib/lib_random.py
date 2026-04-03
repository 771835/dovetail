# coding=utf-8
from typing import Callable, Optional

from dovetail.core.enums.types import FunctionType, DataType
from dovetail.core.lib.library import Library
from dovetail.core.symbols import Function, Variable, Literal, Parameter


class Random(Library):
    def __init__(self, *_args, **_kwargs):
        self._functions: dict[Function, Optional[Callable[..., Variable | Literal | None]]] = {
            Function(
                "randint",
                [
                    Parameter(Variable("min", DataType.INT)),
                    Parameter(Variable("max", DataType.INT)),
                ],
                DataType.INT,
                FunctionType.BUILTIN
            ): None,
        }

    def __str__(self) -> str:
        return "random"

    def get_functions(self):
        return self._functions
