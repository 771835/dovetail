# coding=utf-8
from pathlib import Path
from typing import Optional

from lark.tree import Meta

from dovetail.core.errors import Errors
from dovetail.core.parser.components.error_reporter import ErrorReporter
from .event import Event
from dovetail.utils.mixin_manager import Mixin, Inject, At, CallbackInfoReturnable


class ErrorReportEvent(Event):
    def __init__(self, error_reporter: ErrorReporter, error: Errors, *args: str, filepath: Path | str,
                 meta: Optional[Meta],
                 suggestion: Optional[str]):
        super().__init__()
        self._error_reporter = error_reporter
        self._suggestion = suggestion
        self._meta = meta
        self._filepath = filepath
        self._args = args
        self._error = error
        self._cancelled = False

    @property
    def error_reporter(self) -> ErrorReporter:
        return self._error_reporter

    @property
    def suggestion(self) -> Optional[str]:
        return self._suggestion

    @suggestion.setter
    def suggestion(self, suggestion: Optional[str]):
        self._suggestion = suggestion

    @property
    def meta(self) -> Optional[Meta]:
        return self._meta

    @property
    def filepath(self) -> Path:
        return self._error_reporter.filepath

    @filepath.setter
    def filepath(self, filepath: Path):
        self._error_reporter.filepath = filepath

    @property
    def args(self) -> tuple[str, ...]:
        return self._args

    @property
    def error(self) -> Errors:
        return self._error

    def cancel(self):
        self._cancelled = True

    def is_cancelled(self):
        return self._cancelled


@Mixin(ErrorReporter)
class ErrorReporterMixin:
    @staticmethod
    @Inject("report", At(At.HEAD), True)
    def _report(ci: CallbackInfoReturnable, error_reporter: ErrorReporter, error: Errors, *args: str,
                filepath: Path | str = "<unknown>", meta: Optional[Meta] = None, suggestion: Optional[str] = None):
        event = ErrorReportEvent(error_reporter, error, *args, filepath=filepath, meta=meta, suggestion=suggestion)
        event.call_event()
        ci.set_args(error_reporter, event.error, *event.args, meta=event.meta, suggestion=event.suggestion)
        if event.is_cancelled():
            ci.cancel()
