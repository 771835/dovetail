# coding=utf-8
from typing import Callable, Optional

from dovetail.core.enums import PrimitiveDataType, FunctionType, StructureType
from dovetail.core.errors import Errors
from dovetail.core.instructions import IRCall, IRCondJump
from dovetail.core.lib.library import Library
from dovetail.core.symbols import Function, Variable, Literal, Parameter, Reference, Symbol


class Assertion(Library):
    def __init__(self, context):
        self.symbol_resolver = context.symbol_resolver
        self.emitter = context.emitter
        self.error_reporter = context.error_reporter
        self.config = context.config

    def get_functions(self) -> dict[Function, Optional[Callable[..., Variable | Literal | None]]]:
        return {
            Function(
                "assert",
                [
                    Parameter(Variable("condition", PrimitiveDataType.BOOLEAN)),
                    Parameter(Variable("message", PrimitiveDataType.STRING)),
                ],
                PrimitiveDataType.VOID,
                FunctionType.LIBRARY
            ): self._assert
        }

    def _assert(self, condition: Reference[Variable | Literal], message: Reference[Variable | Literal]):
        if not self.config.debug:
            return

        tellraw_text: Symbol | None = self.symbol_resolver.resolve_symbol("tellraw_text", expected_type=Function)
        _exec: Symbol | None = self.symbol_resolver.resolve_symbol("exec", expected_type=Function)
        if not isinstance(tellraw_text, Function):
            self.error_reporter.report(
                Errors.SymbolResolution,
                "函数",
                "tellraw_text"
            )
            return
        if not isinstance(_exec, Function):
            self.error_reporter.report(
                Errors.SymbolResolution,
                "函数",
                "exec"
            )
            return

        with self.emitter.scope("assert", StructureType.CONDITIONAL) as scope_name:
            self.emitter.emit(
                IRCall(
                    None,
                    tellraw_text,
                    {
                        "target": Reference.literal("@a"),
                        "msg": message
                    }
                ),
                IRCall(
                    None,
                    _exec,
                    {
                        "command": Reference.literal("gamerule maxCommandChainLength 0"),
                    }
                )
            )
        self.emitter.emit(IRCondJump(condition.value, None, scope_name))

    def __str__(self) -> str:
        return "Assertion"
