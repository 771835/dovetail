# coding=utf-8
from dovetail.core.enums import PrimitiveDataType, BinaryOps
from dovetail.core.lib.lib_factory import LibraryBase, library_func, builtin_func
from dovetail.core.symbols import Reference, Variable, Literal


class Strlib(LibraryBase):
    def __init__(self, context):
        self.error_reporter = context.error_reporter
        self.emitter = context.emitter
        self._init(context)

    def __str__(self) -> str:
        return "strlib"

    @library_func(returns=str, name="strcat")
    def _strcat(self, a: str, b: str):
        a: Reference[Variable | Literal]
        b: Reference[Variable | Literal]
        return self.emitter.emit_binary_calc(a, BinaryOps.ADD, b, "strcat")

    @builtin_func(name="strcat_fast")
    def _strcat_fast(self, a: str, b: str) -> str: ...

    @builtin_func(name="strlen")
    def _strlen(self, s: str) -> int: ...

    @builtin_func(name="substring")
    def _substring(self, s: str, start: int, end: int) -> str: ...
