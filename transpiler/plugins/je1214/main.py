# coding=utf-8
from transpiler.plugins.plugin_api import Plugin
from transpiler.plugins.plugin_api.v2.registry import registry_backend
from .backend.backend import JE1214Backend
from .backend.processors import * # NOQA


class PluginMain(Plugin):
    def load(self):
        print("je1214.PluginMain.load:run")
        registry_backend(JE1214Backend)

    def unload(self) -> bool:
        pass

    def validate(self) -> tuple[bool, str | None]:
        return True, None

