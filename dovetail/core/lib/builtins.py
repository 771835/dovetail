# coding=utf-8
from typing import Callable, Optional

from dovetail.core.enums.types import FunctionType, DataType
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
                    Parameter(Variable("value", DataType.STRING))
                ],
                DataType.INT,
                FunctionType.LIBRARY
            ): self._int,
            Function(
                "str",
                [
                    Parameter(Variable("value", DataType.INT))
                ],
                DataType.STRING,
                FunctionType.LIBRARY
            ): self._str,
            Function(
                _n("str_i"),
                [
                    Parameter(Variable("value", DataType.INT))
                ],
                DataType.STRING,
                FunctionType.LIBRARY
            ): self._str,
            Function(
                _n("str_b"),
                [
                    Parameter(Variable("value", DataType.BOOLEAN))
                ],
                DataType.STRING,
                FunctionType.LIBRARY
            ): self._str,
            Function(
                "print",
                [
                    Parameter(Variable("msg", DataType.STRING))
                ],
                DataType.VOID,
                FunctionType.LIBRARY
            ): self._print,
            Function(
                _n("_call"),
                [
                    Parameter(Variable("scope", DataType.STRING)),
                ],
                DataType.VOID,
                FunctionType.LIBRARY
            ): self._call,
            Function(
                "exec",
                [
                    Parameter(Variable("command", DataType.STRING))
                ],
                DataType.VOID,
                FunctionType.BUILTIN
            ): None,
            Function(
                "tellraw_text",
                [
                    Parameter(Variable("target", DataType.STRING)),
                    Parameter(Variable("msg", DataType.STRING)),
                ],
                DataType.VOID,
                FunctionType.BUILTIN
            ): None,
            Function(
                "tellraw_json",
                [
                    Parameter(Variable("target", DataType.STRING)),
                    Parameter(Variable("json", DataType.STRING)),
                ],
                DataType.VOID,
                FunctionType.BUILTIN
            ): None,
        }

        """
        Function(
            "setblock",
            [
                Parameter(Variable("x", DataType.INT)),
                Parameter(Variable("y", DataType.INT)),
                Parameter(Variable("z", DataType.INT)),
                Parameter(Variable("block_id", DataType.STRING)),
                Parameter(Variable("mode", DataType.STRING), optional=True, default=Reference.literal("destroy")),
            ],
            DataType.INT,
            FunctionType.BUILTIN
        ): None,
        Function(
            "item_spawn",
            [
                Parameter(Variable("x", DataType.INT)),
                Parameter(Variable("y", DataType.INT)),
                Parameter(Variable("z", DataType.INT)),
                Parameter(Variable("item_id", DataType.STRING)),
                Parameter(Variable("count", DataType.INT), True)
            ],
            DataType.INT,
            FunctionType.BUILTIN
        ): None,
        Function(
            "tp",
            [
                Parameter(Variable("player", DataType.STRING)),
                Parameter(Variable("x", DataType.INT)),
                Parameter(Variable("y", DataType.INT)),
                Parameter(Variable("z", DataType.INT))
            ],
            DataType.INT,
            FunctionType.BUILTIN
        ): None,
        Function(
            "give",
            [
                Parameter(Variable("player", DataType.STRING)),
                Parameter(Variable("item_id", DataType.STRING)),
                Parameter(Variable("count", DataType.INT), True)
            ],
            DataType.INT,
            FunctionType.BUILTIN
        ): None,
        Function(
            "summon",
            [
                Parameter(Variable("entity_id", DataType.STRING)),
                Parameter(Variable("x", DataType.INT)),
                Parameter(Variable("y", DataType.INT)),
                Parameter(Variable("z", DataType.INT)),
                Parameter(Variable("nbt", DataType.STRING), True)
            ],
            DataType.INT,
            FunctionType.BUILTIN
        ): None,
        Function(
            "kill",
            [Parameter(Variable("target", DataType.STRING))],
            DataType.INT,
            FunctionType.BUILTIN
        ): None,
        Function(
            "time_set",
            [Parameter(Variable("value", DataType.INT))],
            DataType.INT,
            FunctionType.BUILTIN
        ): None,
        Function(
            "weather",
            [Parameter(Variable("type", DataType.STRING))],
            DataType.INT,
            FunctionType.BUILTIN
        ): None,
        Function(
            "difficulty",
            [Parameter(Variable("level", DataType.STRING))],
            DataType.INT,
            FunctionType.BUILTIN
        ): None,
        Function(
            "gamerule",
            [
                Parameter(Variable("rule", DataType.STRING)),
                Parameter(Variable("value", DataType.STRING))
            ],
            DataType.INT,
            FunctionType.BUILTIN
        ): None,
        Function(
            "fill",
            [
                Parameter(Variable("x1", DataType.INT)),
                Parameter(Variable("y1", DataType.INT)),
                Parameter(Variable("z1", DataType.INT)),
                Parameter(Variable("x2", DataType.INT)),
                Parameter(Variable("y2", DataType.INT)),
                Parameter(Variable("z2", DataType.INT)),
                Parameter(Variable("block", DataType.STRING))
            ],
            DataType.INT,
            FunctionType.BUILTIN
        ): None,
        Function(
            "effect",
            [
                Parameter(Variable("target", DataType.STRING)),
                Parameter(Variable("effect", DataType.STRING)),
                Parameter(Variable("duration", DataType.INT), True),
                Parameter(Variable("amplifier", DataType.INT), True)
            ],
            DataType.INT,
            FunctionType.BUILTIN
        ): None,
        Function(
            "attribute",
            [
                Parameter(Variable("target", DataType.STRING)),
                Parameter(Variable("attr", DataType.STRING)),
                Parameter(Variable("value", DataType.STRING), True)
            ],
            DataType.INT,
            FunctionType.BUILTIN
        ): None,
        Function(
            "tag",
            [
                Parameter(Variable("target", DataType.STRING)),
                Parameter(Variable("action", DataType.STRING)),
                Parameter(Variable("tag", DataType.STRING))
            ],
            DataType.INT,
            FunctionType.BUILTIN
        ): None,
        Function(
            "damage",
            [
                Parameter(Variable("target", DataType.STRING)),
                Parameter(Variable("amount", DataType.INT)),
                Parameter(Variable("source", DataType.STRING), True)
            ],
            DataType.INT,
            FunctionType.BUILTIN
        ): None,
        Function(
            "scoreboard",
            [
                Parameter(Variable("op", DataType.STRING)),
                Parameter(Variable("target", DataType.STRING)),
                Parameter(Variable("objective", DataType.STRING)),
                Parameter(Variable("value", DataType.STRING), True)
            ],
            DataType.INT,
            FunctionType.BUILTIN
        ): None,
        Function(
            "bossbar",
            [
                Parameter(Variable("op", DataType.STRING)),
                Parameter(Variable("id", DataType.STRING)),
                Parameter(Variable("value", DataType.STRING), True)
            ],
            DataType.INT,
            FunctionType.BUILTIN
        ): None,
        """

    def _int(self, value: Reference[Variable | Literal]) -> Variable:
        result: Variable = self.emitter.create_temp_var_declared(DataType.INT, "to_int")
        self.emitter.emit(IRCast(result, DataType.INT, value))
        return result

    def _str(self, value: Reference[Variable | Literal]) -> Variable:
        result: Variable = self.emitter.create_temp_var_declared(DataType.STRING, "to_str")
        self.emitter.emit(IRCast(result, DataType.STRING, value))
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
        if not scope.is_literal() or scope.get_dtype() != DataType.STRING:
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
        return Literal(DataType.STRING, str(value.get_dtype().get_name()))

    def _type_repr_of(self, value: Reference[Variable | Literal]):
        return Literal(DataType.STRING, repr(value.get_dtype()))

    def __str__(self) -> str:
        return "built-in"

    def get_functions(self):
        return self._functions
