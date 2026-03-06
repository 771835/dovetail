# coding=utf-8
from typing import Callable

from dovetail.core.instructions import IRInstruction
from dovetail.core.ir_builder import IRBuilder
from dovetail.core.lib.library import Library
from dovetail.core.symbols import Reference, Function, Variable, Literal


class Experimental(Library):
    def __init__(self, builder: IRBuilder):
        self.builder = builder
        self._variable = {
        }
        self._functions: dict[Function, Callable[..., Variable | Literal]] = {
        }

    def __str__(self) -> str:
        return "experimental"

    def load(self) -> list[IRInstruction]:
        return []

    def get_functions(self) -> dict[Function, Callable[..., Variable | Literal]]:
        return self._functions

    def get_variables(self) -> dict[Variable, Reference]:
        return self._variable
