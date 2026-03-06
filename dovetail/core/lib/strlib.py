import uuid
from typing import Callable

from dovetail.core.enums import DataType, BinaryOps, FunctionType
from dovetail.core.instructions import IRInstruction, IRDeclare, IRBinaryOp
from dovetail.core.ir_builder import IRBuilder
from dovetail.core.lib.library import Library
from dovetail.core.symbols import Reference, Function, Variable, Literal, Parameter


class Strlib(Library):
    def __init__(self, builder: IRBuilder):
        self.builder = builder

    def __str__(self) -> str:
        return "strlib"

    def load(self) -> list[IRInstruction]:
        return []

    def get_functions(self) -> dict[Function, Callable[..., Variable  | Literal]]:
        return {
            Function(
                "strcat",
                [
                    Parameter(Variable("dest", DataType.STRING)),
                    Parameter(Variable("src", DataType.STRING))
                ],
                DataType.STRING,
                FunctionType.LIBRARY
            ): self._strcat,
            Function(
                "strlen",
                [
                    Parameter(Variable("s", DataType.STRING))
                ],
                DataType.INT,
                FunctionType.BUILTIN
            ): None,
            Function(
                "substring",
                [
                    Parameter(Variable("s", DataType.STRING)),
                    Parameter(Variable("start", DataType.INT)),
                    Parameter(Variable("end", DataType.INT))
                ],
                DataType.STRING,
                FunctionType.BUILTIN
            ): None,
        }

    def _strcat(self, dest: Reference[Variable  | Literal],
                src: Reference[Variable  | Literal]) -> Variable:
        var = Variable(uuid.uuid4().hex, DataType.STRING)
        self.builder.insert(IRDeclare(var))
        self.builder.insert(IRBinaryOp(var, BinaryOps.ADD, dest, src))
        return var

    def get_variables(self) -> dict[Variable, Reference]:
        return {}
