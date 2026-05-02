# coding=utf-8
from typing import Callable

from dovetail.core.instructions import IRInstruction
from dovetail.core.ir_builder import IRBuilder
from dovetail.core.lib.library import Library
from dovetail.core.symbols import Reference, Function, Variable, Literal


class Experimental(Library):
    def __init__(self, context):
        pass

    def __str__(self) -> str:
        return "experimental"
