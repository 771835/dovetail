# coding=utf-8
from dovetail.plugins.plugin_api import Plugin, registry_backend
from dovetail.utils.logger import get_logger
from .backend.backend import JE1215Backend
from .backend.processors import *  # NOQA
from .optimize import *  # NOQA: 加载优化管道


class PluginMain(Plugin):
    logger = None

    def load(self):
        super().__init__()
        self.logger = get_logger("Backend-1.21.5-JE")
        registry_backend(JE1215Backend)

    def unload(self) -> bool:
        return True

    def validate(self) -> tuple[bool, str | None]:
        return True, None
