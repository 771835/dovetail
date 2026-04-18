from dovetail.core.enums import PrimitiveDataType, BinaryOps, FunctionType
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
                    Parameter(Variable("dest", PrimitiveDataType.STRING)),
                    Parameter(Variable("src", PrimitiveDataType.STRING))
                ],
                PrimitiveDataType.STRING,
                FunctionType.LIBRARY
            ): self._strcat,
            Function(
                "strlen",
                [
                    Parameter(Variable("s", PrimitiveDataType.STRING))
                ],
                PrimitiveDataType.INT,
                FunctionType.BUILTIN
            ): None,
            Function(
                "substring",
                [
                    Parameter(Variable("s", PrimitiveDataType.STRING)),
                    Parameter(Variable("start", PrimitiveDataType.INT)),
                    Parameter(Variable("end", PrimitiveDataType.INT))
                ],
                PrimitiveDataType.STRING,
                FunctionType.BUILTIN
            ): None,
        }

    def _strcat(self, dest: Reference[Variable | Literal],
                src: Reference[Variable | Literal]) -> Variable:
        return self.emitter.emit_binary_calc(dest, BinaryOps.ADD, src, PrimitiveDataType.STRING, "strcat")
