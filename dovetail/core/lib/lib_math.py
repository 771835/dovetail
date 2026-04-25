# coding=utf-8
from typing import Callable

from dovetail.core.enums.types import FunctionType, PrimitiveDataType
from dovetail.core.lib.library import Library
from dovetail.core.parser.components import SymbolResolver, IREmitter, ErrorReporter
from dovetail.core.symbols import Reference, Function, Variable, Parameter, Literal


class Math(Library):
    def __init__(self, symbol_resolver: SymbolResolver, emitter: IREmitter,
                 error_reporter: ErrorReporter):
        self._variable: dict[Variable, Reference] = {
            Variable("INT_MAX", PrimitiveDataType.INT, mutable=False): Reference.literal(2147483647),
            Variable("INT_MIN", PrimitiveDataType.INT, mutable=False): Reference.literal(-2147483648),
        }
        self._functions: dict[Function, Callable[..., Variable | Literal] | None] = {
            Function(
                "abs",
                [
                    Parameter(Variable("value", PrimitiveDataType.INT)),
                ],
                PrimitiveDataType.INT,
                FunctionType.BUILTIN
            ): None,
            Function(
                "min",
                [
                    Parameter(Variable("a", PrimitiveDataType.INT)),
                    Parameter(Variable("b", PrimitiveDataType.INT))
                ],
                PrimitiveDataType.INT,
                FunctionType.BUILTIN
            ): None,
            Function(
                "max",
                [
                    Parameter(Variable("a", PrimitiveDataType.INT)),
                    Parameter(Variable("b", PrimitiveDataType.INT))
                ],
                PrimitiveDataType.INT,
                FunctionType.BUILTIN
            ): None,
        }

    def __str__(self) -> str:
        return "math"

    def get_functions(self):
        return self._functions

    def get_variables(self) -> dict[Variable, Reference]:
        return self._variable
