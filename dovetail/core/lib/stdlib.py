# coding=utf-8
from typing import Optional, Callable

from dovetail.core.enums import PrimitiveDataType, FunctionType
from dovetail.core.enums.datatypes import UnionType, ArrayType, DictType, ListType
from dovetail.core.lib.library import Library
from dovetail.core.symbols import Function, Variable, Literal, Parameter


class Stdlib(Library):
    def __init__(self, context):
        self.context = context

    def get_functions(self) -> dict[Function, Optional[Callable[..., Variable | Literal | None]]]:
        return {
            Function(
                "malloc",
                [
                    Parameter(
                        Variable(
                            "array",
                            UnionType(ArrayType, DictType, ListType)
                        )
                    ),
                    Parameter(
                        Variable(
                            "size",
                            PrimitiveDataType.INT
                        )
                    ),
                ],
                PrimitiveDataType.VOID,
                FunctionType.BUILTIN,
                {}
            ): None
        }

    def __str__(self) -> str:
        return "stdlib"
