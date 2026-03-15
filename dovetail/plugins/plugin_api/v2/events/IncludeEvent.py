# coding=utf-8
from pathlib import Path

from dovetail.core.lib.library import Library
from dovetail.core.parser.parser import ASTVisitor
from dovetail.plugins.plugin_api.v2.event import Event
from dovetail.utils.mixin_manager import Mixin, Inject, At, CallbackInfoReturnable


class IncludeEvent(Event):
    def __init__(self, original_path: str, return_path: Path | None | Library, line=-1, column=-1):
        super().__init__()
        self._original_path = original_path
        self._return_path = return_path
        self.line = line
        self.column = column
        self._cancelled = False

    @property
    def original_path(self) -> str:
        return self._original_path

    @property
    def return_path(self):
        return self._return_path

    @return_path.setter
    def return_path(self, path: Path | None | Library):
        assert isinstance(path, (Path | None | Library))
        self._return_path = path

    def cancel(self):
        self._cancelled = True

    def is_cancelled(self):
        return self._cancelled


@Mixin(ASTVisitor)
class ASTVisitorMixin:
    @staticmethod
    @Inject("_search_include_path", At(At.TAIL), True)
    def _search_include_path(ci: CallbackInfoReturnable, _: ASTVisitor, path: str, line=-1,
                             column=-1) -> Path | None | Library:
        event = IncludeEvent(path, ci.return_value, line, column)
        event.call_event()
        if event.is_cancelled():
            ci.set_return_value(None)
            return
        ci.set_return_value(event.return_path)
