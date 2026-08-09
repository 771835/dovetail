# coding=utf-8

from dovetail.core.enums import StructureType
from dovetail.core.errors import Errors
from dovetail.core.instructions import IRCall, IRCondJump
from dovetail.core.lib.lib_factory import LibraryBase, library_func
from dovetail.core.symbols import Function, Variable, Literal, Reference, Symbol


class Assertion(LibraryBase):
    def __init__(self, context):
        self.emitter = context.emitter
        self.error_reporter = context.error_reporter
        self.config = context.config
        self._init(context)

    @library_func(name="assert")
    def _assert(self, condition: bool, message: str | int | bool):
        condition: Reference[Variable | Literal]
        message: Reference[Variable | Literal]
        if not self.config.debug:
            return

        tellraw_text: Symbol | None = self._get_function("tellraw_text")
        _exec: Symbol | None = self._get_function("exec")
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
        self.emitter.emit(IRCondJump(condition, false_scope=scope_name))

    def __str__(self) -> str:
        return "Assertion"
