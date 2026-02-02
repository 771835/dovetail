# coding=utf-8
from ..plugin_api import Plugin
from ..plugin_api.v2.registry import registry_backend
from .backend.backend import JE1214Backend
from .backend.processors import *  # NOQA
from transpiler.utils.logger import get_logger


class PluginMain(Plugin):
    logger = None

    def load(self):
        self.logger = get_logger("Backend1.21.4JE")
        self.logger.info("Loading plugin...")
        registry_backend(JE1214Backend)

    def unload(self) -> bool:
        self.logger.info("Unloading plugin...")
        return True

    def validate(self) -> tuple[bool, str | None]:
        return True, None
