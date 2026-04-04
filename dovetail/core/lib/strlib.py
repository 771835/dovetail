from dovetail.core.enums import DataType, BinaryOps, FunctionType
from dovetail.core.lib.library import Library
from dovetail.core.parser.tools import SymbolResolver, ErrorReporter, IREmitter
from dovetail.core.symbols import Reference, Function, Variable, Literal, Parameter


class Strlib(Library):
    def __init__(self, symbol_resolver: SymbolResolver, emitter: IREmitter,
                 error_reporter: ErrorReporter):
        self.error_reporter = error_reporter
        self.emitter = emitter
        self.symbol_resolver = symbol_resolver

    def __str__(self) -> str:
        return "strlib"

    def get_functions(self):
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

    def _strcat(self, dest: Reference[Variable | Literal],
                src: Reference[Variable | Literal]) -> Variable:
        return self.emitter.emit_binary_calc(dest, BinaryOps.ADD, src, DataType.STRING, "strcat")
