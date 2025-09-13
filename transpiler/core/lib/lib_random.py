# coding=utf-8
from typing import Callable

from transpiler.core.ir_builder import IRBuilder
from transpiler.core.enums import DataType, FunctionType
from transpiler.core.instructions import IRInstruction
from transpiler.core.lib.library import Library
from transpiler.core.symbols import Constant, Reference, Function, Variable, Literal, Parameter


class Random(Library):
    def __init__(self, builder: IRBuilder):
        self.builder = builder
        self._constant: dict[Constant, Reference] = {
        }
        self._functions: dict[Function, Callable[..., Variable | Constant | Literal] | None] = {
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

    def get_functions(self) -> dict[Function, Callable[..., Variable | Constant | Literal]]:
        return self._functions

    def get_constants(self) -> dict[Constant, Reference]:
        return self._constant
