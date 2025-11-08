# coding=utf-8
from typing import Callable

from transpiler.core.enums.types import FunctionType, DataType
from transpiler.core.instructions import IRInstruction
from transpiler.core.ir_builder import IRBuilder
from transpiler.core.lib.library import Library
from transpiler.core.symbols import Constant, Reference, Function, Variable, Parameter, Literal


class Math(Library):
    def __init__(self, builder: IRBuilder):
        self.builder = builder
        self._constant: dict[Constant, Reference] = {
            Constant("INT_MAX", DataType.INT): Reference.literal(2147483647),
            Constant("INT_MIN", DataType.INT): Reference.literal(-2147483648),
        }
        self._functions: dict[Function, Callable[..., Variable | Constant | Literal] | None] = {
            Function(
                "abs",
                [
                    Parameter(Variable("value", DataType.INT)),
                ],
                DataType.INT,
                FunctionType.BUILTIN
            ): None,
            Function(
                "min",
                [
                    Parameter(Variable("a", DataType.INT)),
                    Parameter(Variable("b", DataType.INT))
                ],
                DataType.INT,
                FunctionType.BUILTIN
            ): None,
            Function(
                "max",
                [
                    Parameter(Variable("a", DataType.INT)),
                    Parameter(Variable("b", DataType.INT))
                ],
                DataType.INT,
                FunctionType.BUILTIN
            ): None,
        }

    def __str__(self) -> str:
        return "math"

    def load(self) -> list[IRInstruction]:
        return []

    def get_functions(self) -> dict[Function, Callable[..., Variable | Constant | Literal]]:
        return self._functions

    def get_constants(self) -> dict[Constant, Reference]:
        return self._constant
