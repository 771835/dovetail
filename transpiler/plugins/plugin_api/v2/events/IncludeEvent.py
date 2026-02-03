# coding=utf-8
from pathlib import Path

from transpiler.core.ir_generator import IRGenerator
from transpiler.core.lib.library import Library
from transpiler.plugins.plugin_api.v2.event import Event
from transpiler.utils.mixin_manager import Mixin, Inject, At, CallbackInfoReturnable


class IncludeEvent(Event):
    def __init__(self, original_path: str, return_path: Path | None | Library):
        super().__init__()
        self._original_path = original_path
        self._return_path = return_path
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


@Mixin(IRGenerator)
class IRGeneratorMixin:
    @staticmethod
    @Inject("_get_include_path", At(At.TAIL), True)
    def _get_include_path(ci: CallbackInfoReturnable, _: IRGenerator, path: str) -> Path | None | Library:
        event = IncludeEvent(path, ci.return_value)
        event.call_event()
        if event.is_cancelled():
            ci.set_return_value(None)
            return
        ci.set_return_value(event.return_path)
