# coding=utf-8
from typing import Callable

from dovetail.core.enums import PrimitiveDataType
from dovetail.core.enums.types import FunctionType
from dovetail.core.lib.library import Library
from dovetail.core.symbols import Reference, Function, Variable, Parameter, Literal
from dovetail.utils.naming import NameNormalizer


class Math(Library):
    def __init__(self, _):
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

    def get_variables(self):
        return {
            Variable(NameNormalizer.normalize("INT_MAX"), PrimitiveDataType.INT, mutable=False):
                Reference.literal(2147483647),
            Variable(NameNormalizer.normalize("INT_MIN"), PrimitiveDataType.INT, mutable=False):
                Reference.literal(-2147483648)
        }
