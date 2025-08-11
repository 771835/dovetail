# coding=utf-8
from typing import Callable

from transpiler.core.backend.ir_builder import IRBuilder
from transpiler.core.instructions import IRInstruction
from transpiler.core.lib.library import Library
from transpiler.core.symbols import Constant, Reference, Function, Variable, Literal


class Experimental(Library):
    def __init__(self, builder: IRBuilder):
        self.builder = builder
        self._constants = {
        }
        self._functions: dict[Function, Callable[..., Variable | Constant | Literal]] = {
        }

    def __str__(self) -> str:
        return "experimental"

    def load(self) -> list[IRInstruction]:
        return []

    def get_functions(self) -> dict[Function, Callable[..., Variable | Constant | Literal]]:
        return self._functions

    def get_constants(self) -> dict[Constant, Reference]:
        return self._constants
