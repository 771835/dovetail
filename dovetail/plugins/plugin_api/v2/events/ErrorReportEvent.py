# coding=utf-8
from pathlib import Path
from typing import Optional

from dovetail.core.errors import Errors
from dovetail.core.parser.parser import ASTVisitor
from dovetail.plugins.plugin_api.v2.event import Event
from dovetail.utils.mixin_manager import Mixin, Inject, At, CallbackInfoReturnable


class ErrorReportEvent(Event):
    def __init__(self, error: Errors, *args: str, filepath: Path | str, line: int, column: int,
                 suggestion: Optional[str]):
        super().__init__()
        self.suggestion = suggestion
        self.column = column
        self.line = line
        self.filepath = filepath
        self.args = args
        self.error = error
        self._cancelled = False

    def cancel(self):
        self._cancelled = True

    def is_cancelled(self):
        return self._cancelled


@Mixin(ASTVisitor)
class ASTVisitorMixin:
    @staticmethod
    @Inject("_report", At(At.HEAD), True)
    def _report(ci: CallbackInfoReturnable, _: ASTVisitor, error: Errors, *args: str,
                filepath: Path | str = "<unknown>", line: int = -1, column: int = -1, suggestion: Optional[str] = None):
        event = ErrorReportEvent(error, *args, filepath=filepath, line=line, column=column, suggestion=suggestion)
        event.call_event()
        if event.is_cancelled():
            ci.cancel()
