# coding=utf-8
from transpiler.plugins.je1214.backend.core import JE1214Backend
from transpiler.plugins.plugin_api import Plugin
from transpiler.plugins.plugin_api.v2.registry import registry_backend


class PluginMain(Plugin):
    def load(self):
        print("je1214.PluginMain.load:run")
        registry_backend(JE1214Backend)

    def unload(self) -> bool:
        pass

    def validate(self) -> tuple[bool, str | None]:
        return True, None
