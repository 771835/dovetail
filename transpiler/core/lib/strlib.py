import uuid
from typing import Callable

from transpiler.core.enums import DataType, BinaryOps, FunctionType
from transpiler.core.instructions import IRInstruction, IRDeclare, IRBinaryOp
from transpiler.core.ir_builder import IRBuilder
from transpiler.core.lib.library import Library
from transpiler.core.symbols import Constant, Reference, Function, Variable, Literal, Parameter


class Strlib(Library):
    def __init__(self, builder: IRBuilder):
        self.builder = builder

    def __str__(self) -> str:
        return "strlib"

    def load(self) -> list[IRInstruction]:
        return []

    def get_functions(self) -> dict[Function, Callable[..., Variable | Constant | Literal]]:
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

    def _strcat(self, dest: Reference[Variable | Constant | Literal],
                src: Reference[Variable | Constant | Literal]) -> Variable:
        var = Variable(uuid.uuid4().hex, DataType.STRING)
        self.builder.insert(IRDeclare(var))
        self.builder.insert(IRBinaryOp(var, BinaryOps.ADD, dest, src))
        return var

    def get_constants(self) -> dict[Constant, Reference]:
        return {}
