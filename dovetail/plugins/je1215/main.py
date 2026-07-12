# coding=utf-8
from dovetail.utils.logger import get_logger
from .backend.backend import JE1214Backend
from .backend.processors import *  # NOQA
from ..plugin_api import Plugin
from ..plugin_api.v2.registry import registry_backend


class PluginMain(Plugin):
    logger = None

    def load(self):
        self.logger = get_logger("Backend-1.21.5-JE")
        self.logger.info("插件加载中")
        registry_backend(JE1214Backend)

    def unload(self) -> bool:
        self.logger.info("插件卸载中")
        return True

    def validate(self) -> tuple[bool, str | None]:
        return True, None
