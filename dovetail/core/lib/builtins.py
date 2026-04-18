# coding=utf-8
from typing import Callable, Optional

from dovetail.core.enums.types import FunctionType, PrimitiveDataType
from dovetail.core.errors import report, Errors
from dovetail.core.instructions import IRCast, IRCall, IRJump
from dovetail.core.lib.library import Library
from dovetail.core.parser.tools import SymbolResolver, IREmitter, ErrorReporter
from dovetail.core.symbols import Function, Reference, Variable, Literal, Parameter
from dovetail.utils.naming import NameNormalizer

_n = NameNormalizer.normalize


class Builtins(Library):

    def __init__(self, symbol_resolver: SymbolResolver, emitter: IREmitter,
                 error_reporter: ErrorReporter):

        self.error_reporter = error_reporter
        self.emitter = emitter
        self.symbol_resolver = symbol_resolver
        self._functions: dict[Function, Optional[Callable[..., Variable | Literal | None]]] = {
            Function(
                "int",
                [
                    Parameter(Variable("value", PrimitiveDataType.STRING))
                ],
                PrimitiveDataType.INT,
                FunctionType.LIBRARY
            ): self._int,
            Function(
                "str",
                [
                    Parameter(Variable("value", PrimitiveDataType.INT))
                ],
                PrimitiveDataType.STRING,
                FunctionType.LIBRARY
            ): self._str,
            Function(
                _n("str_i"),
                [
                    Parameter(Variable("value", PrimitiveDataType.INT))
                ],
                PrimitiveDataType.STRING,
                FunctionType.LIBRARY
            ): self._str,
            Function(
                _n("str_b"),
                [
                    Parameter(Variable("value", PrimitiveDataType.BOOLEAN))
                ],
                PrimitiveDataType.STRING,
                FunctionType.LIBRARY
            ): self._str,
            Function(
                "print",
                [
                    Parameter(Variable("msg", PrimitiveDataType.STRING))
                ],
                PrimitiveDataType.VOID,
                FunctionType.LIBRARY
            ): self._print,
            Function(
                _n("_call"),
                [
                    Parameter(Variable("scope", PrimitiveDataType.STRING)),
                ],
                PrimitiveDataType.VOID,
                FunctionType.LIBRARY
            ): self._call,
            Function(
                "exec",
                [
                    Parameter(Variable("command", PrimitiveDataType.STRING))
                ],
                PrimitiveDataType.VOID,
                FunctionType.BUILTIN
            ): None,
            Function(
                "tellraw_text",
                [
                    Parameter(Variable("target", PrimitiveDataType.STRING)),
                    Parameter(Variable("msg", PrimitiveDataType.STRING)),
                ],
                PrimitiveDataType.VOID,
                FunctionType.BUILTIN
            ): None,
            Function(
                "tellraw_json",
                [
                    Parameter(Variable("target", PrimitiveDataType.STRING)),
                    Parameter(Variable("json", PrimitiveDataType.STRING)),
                ],
                PrimitiveDataType.VOID,
                FunctionType.BUILTIN
            ): None,
        }

        """
        Function(
            "setblock",
            [
                Parameter(Variable("x", PrimitiveDataType.INT)),
                Parameter(Variable("y", PrimitiveDataType.INT)),
                Parameter(Variable("z", PrimitiveDataType.INT)),
                Parameter(Variable("block_id", PrimitiveDataType.STRING)),
                Parameter(Variable("mode", PrimitiveDataType.STRING), optional=True, default=Reference.literal("destroy")),
            ],
            PrimitiveDataType.INT,
            FunctionType.BUILTIN
        ): None,
        Function(
            "item_spawn",
            [
                Parameter(Variable("x", PrimitiveDataType.INT)),
                Parameter(Variable("y", PrimitiveDataType.INT)),
                Parameter(Variable("z", PrimitiveDataType.INT)),
                Parameter(Variable("item_id", PrimitiveDataType.STRING)),
                Parameter(Variable("count", PrimitiveDataType.INT), True)
            ],
            PrimitiveDataType.INT,
            FunctionType.BUILTIN
        ): None,
        Function(
            "tp",
            [
                Parameter(Variable("player", PrimitiveDataType.STRING)),
                Parameter(Variable("x", PrimitiveDataType.INT)),
                Parameter(Variable("y", PrimitiveDataType.INT)),
                Parameter(Variable("z", PrimitiveDataType.INT))
            ],
            PrimitiveDataType.INT,
            FunctionType.BUILTIN
        ): None,
        Function(
            "give",
            [
                Parameter(Variable("player", PrimitiveDataType.STRING)),
                Parameter(Variable("item_id", PrimitiveDataType.STRING)),
                Parameter(Variable("count", PrimitiveDataType.INT), True)
            ],
            PrimitiveDataType.INT,
            FunctionType.BUILTIN
        ): None,
        Function(
            "summon",
            [
                Parameter(Variable("entity_id", PrimitiveDataType.STRING)),
                Parameter(Variable("x", PrimitiveDataType.INT)),
                Parameter(Variable("y", PrimitiveDataType.INT)),
                Parameter(Variable("z", PrimitiveDataType.INT)),
                Parameter(Variable("nbt", PrimitiveDataType.STRING), True)
            ],
            PrimitiveDataType.INT,
            FunctionType.BUILTIN
        ): None,
        Function(
            "kill",
            [Parameter(Variable("target", PrimitiveDataType.STRING))],
            PrimitiveDataType.INT,
            FunctionType.BUILTIN
        ): None,
        Function(
            "time_set",
            [Parameter(Variable("value", PrimitiveDataType.INT))],
            PrimitiveDataType.INT,
            FunctionType.BUILTIN
        ): None,
        Function(
            "weather",
            [Parameter(Variable("type", PrimitiveDataType.STRING))],
            PrimitiveDataType.INT,
            FunctionType.BUILTIN
        ): None,
        Function(
            "difficulty",
            [Parameter(Variable("level", PrimitiveDataType.STRING))],
            PrimitiveDataType.INT,
            FunctionType.BUILTIN
        ): None,
        Function(
            "gamerule",
            [
                Parameter(Variable("rule", PrimitiveDataType.STRING)),
                Parameter(Variable("value", PrimitiveDataType.STRING))
            ],
            PrimitiveDataType.INT,
            FunctionType.BUILTIN
        ): None,
        Function(
            "fill",
            [
                Parameter(Variable("x1", PrimitiveDataType.INT)),
                Parameter(Variable("y1", PrimitiveDataType.INT)),
                Parameter(Variable("z1", PrimitiveDataType.INT)),
                Parameter(Variable("x2", PrimitiveDataType.INT)),
                Parameter(Variable("y2", PrimitiveDataType.INT)),
                Parameter(Variable("z2", PrimitiveDataType.INT)),
                Parameter(Variable("block", PrimitiveDataType.STRING))
            ],
            PrimitiveDataType.INT,
            FunctionType.BUILTIN
        ): None,
        Function(
            "effect",
            [
                Parameter(Variable("target", PrimitiveDataType.STRING)),
                Parameter(Variable("effect", PrimitiveDataType.STRING)),
                Parameter(Variable("duration", PrimitiveDataType.INT), True),
                Parameter(Variable("amplifier", PrimitiveDataType.INT), True)
            ],
            PrimitiveDataType.INT,
            FunctionType.BUILTIN
        ): None,
        Function(
            "attribute",
            [
                Parameter(Variable("target", PrimitiveDataType.STRING)),
                Parameter(Variable("attr", PrimitiveDataType.STRING)),
                Parameter(Variable("value", PrimitiveDataType.STRING), True)
            ],
            PrimitiveDataType.INT,
            FunctionType.BUILTIN
        ): None,
        Function(
            "tag",
            [
                Parameter(Variable("target", PrimitiveDataType.STRING)),
                Parameter(Variable("action", PrimitiveDataType.STRING)),
                Parameter(Variable("tag", PrimitiveDataType.STRING))
            ],
            PrimitiveDataType.INT,
            FunctionType.BUILTIN
        ): None,
        Function(
            "damage",
            [
                Parameter(Variable("target", PrimitiveDataType.STRING)),
                Parameter(Variable("amount", PrimitiveDataType.INT)),
                Parameter(Variable("source", PrimitiveDataType.STRING), True)
            ],
            PrimitiveDataType.INT,
            FunctionType.BUILTIN
        ): None,
        Function(
            "scoreboard",
            [
                Parameter(Variable("op", PrimitiveDataType.STRING)),
                Parameter(Variable("target", PrimitiveDataType.STRING)),
                Parameter(Variable("objective", PrimitiveDataType.STRING)),
                Parameter(Variable("value", PrimitiveDataType.STRING), True)
            ],
            PrimitiveDataType.INT,
            FunctionType.BUILTIN
        ): None,
        Function(
            "bossbar",
            [
                Parameter(Variable("op", PrimitiveDataType.STRING)),
                Parameter(Variable("id", PrimitiveDataType.STRING)),
                Parameter(Variable("value", PrimitiveDataType.STRING), True)
            ],
            PrimitiveDataType.INT,
            FunctionType.BUILTIN
        ): None,
        """

    def _int(self, value: Reference[Variable | Literal]) -> Variable:
        result: Variable = self.emitter.create_temp_var_declared(PrimitiveDataType.INT, "to_int")
        self.emitter.emit(IRCast(result, PrimitiveDataType.INT, value))
        return result

    def _str(self, value: Reference[Variable | Literal]) -> Variable:
        result: Variable = self.emitter.create_temp_var_declared(PrimitiveDataType.STRING, "to_str")
        self.emitter.emit(IRCast(result, PrimitiveDataType.STRING, value))
        return result

    def _print(self, msg: Reference[Variable | Literal]) -> None:
        tellraw_text = next((function for function in self._functions if function.name == "tellraw_text"), None)
        if tellraw_text is None:
            self.error_reporter.report(
                Errors.SymbolResolution,
                "函数",
                "tellraw_text"
            )
            return None

        self.emitter.emit(
            IRCall(
                None,
                tellraw_text,
                {
                    "target": Reference.literal("@a"),
                    "msg": msg
                }
            )
        )
        return None

    def _call(self, scope: Reference[Literal]):
        if not scope.is_literal() or scope.get_dtype() != PrimitiveDataType.STRING:
            report(
                Errors.InvalidSyntax,
                "跳转目标必须是字面量字符串"
            )
            return None

        scope_name = str(scope.value.value)

        current_scope = self.symbol_resolver.scope_stack[-1]

        if current_scope.resolve_scope(scope_name) is None:
            self.error_reporter.report(
                Errors.InvalidControlFlow,
                f"待跳转目标作用域 '{scope_name}' 不存在"
            )
            return None

        self.emitter.emit(IRJump(scope_name))

        return None

    def _type_of(self, value: Reference[Variable | Literal]):
        return Literal(PrimitiveDataType.STRING, str(value.get_dtype().get_name()))

    def _type_repr_of(self, value: Reference[Variable | Literal]):
        return Literal(PrimitiveDataType.STRING, repr(value.get_dtype()))

    def __str__(self) -> str:
        return "built-in"

    def get_functions(self):
        return self._functions
