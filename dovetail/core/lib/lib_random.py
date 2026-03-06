# coding=utf-8
from typing import Callable

from dovetail.core.enums.types import FunctionType, DataType
from dovetail.core.instructions import IRInstruction
from dovetail.core.ir_builder import IRBuilder
from dovetail.core.lib.library import Library
from dovetail.core.symbols import Reference, Function, Variable, Literal, Parameter


class Random(Library):
    def __init__(self, builder: IRBuilder):
        self.builder = builder
        self._functions: dict[Function, Callable[..., Variable | Literal] | None] = {
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

    def load(self) -> list[IRInstruction]:
        return []

    def get_functions(self) -> dict[Function, Callable[..., Variable | Literal]]:
        return self._functions

    def get_variables(self) -> dict[Variable, Reference]:
        return {}
