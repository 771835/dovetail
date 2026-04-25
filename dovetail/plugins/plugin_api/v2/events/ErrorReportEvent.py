# coding=utf-8
from pathlib import Path
from typing import Optional

from lark.tree import Meta

from dovetail.core.errors import Errors
from dovetail.core.parser.components.error_reporter import ErrorReporter
from dovetail.plugins.plugin_api.v2.event import Event
from dovetail.utils.mixin_manager import Mixin, Inject, At, CallbackInfoReturnable


class ErrorReportEvent(Event):
    def __init__(self, error: Errors, *args: str, filepath: Path | str, meta: Meta,
                 suggestion: Optional[str]):
        super().__init__()
        self.suggestion = suggestion
        self.meta = meta
        self.filepath = filepath
        self.args = args
        self.error = error
        self._cancelled = False

    def cancel(self):
        self._cancelled = True

    def is_cancelled(self):
        return self._cancelled


@Mixin(ErrorReporter)
class ErrorReporterMixin:
    @staticmethod
    @Inject("report", At(At.HEAD), True)
    def _report(ci: CallbackInfoReturnable, _: ErrorReporter, error: Errors, *args: str,
                filepath: Path | str = "<unknown>", meta: Meta = None, suggestion: Optional[str] = None):
        event = ErrorReportEvent(error, *args, filepath=filepath, meta=meta, suggestion=suggestion)
        event.call_event()
        if event.is_cancelled():
            ci.cancel()
