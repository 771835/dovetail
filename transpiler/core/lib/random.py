# coding=utf-8
import uuid
from typing import Callable

from transpiler.core.backend.ir_builder import IRBuilder
from transpiler.core.instructions import IRInstruction, IRRawCmd
from transpiler.core.language_enums import DataType, ValueType
from transpiler.core.lib.library import Library
from transpiler.core.symbols import Constant, Reference, Function, Variable, Literal


class Random(Library):
    def __init__(self, builder: IRBuilder):
        self.builder = builder
        self._constant: dict[Constant, Reference] = {
        }
        self._functions: dict[Function, Callable[..., Variable | Constant | Literal]] = {
            Function(
                "randint",
                [
                    Variable("min", DataType.INT),
                    Variable("max", DataType.INT)
                ],
                DataType.INT
            ): self._randint
        }

    def _randint(self, minn: Reference[Variable | Constant | Literal], maxx: Reference[Variable | Constant | Literal]):
        result_var = Variable("randint_" + uuid.uuid4().hex, DataType.INT)
        if minn.value_type == ValueType.LITERAL and maxx.value_type == ValueType.LITERAL:
            self.builder.insert(IRRawCmd(Reference(ValueType.LITERAL, Literal(DataType.STRING,
                                                                              f"exectue random value {minn.value.value}..{maxx.value.value}"))))


        return Literal(DataType.INT, 114514)

    def __str__(self) -> str:
        pass

    def load(self) -> list[IRInstruction]:
        return []

    def get_functions(self) -> dict[Function, Callable[..., Variable | Constant | Literal]]:
        return self._functions

    def get_constants(self) -> dict[Constant, Reference]:
        return self._constant
