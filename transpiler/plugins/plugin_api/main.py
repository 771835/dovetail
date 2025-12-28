# coding=utf-8
from transpiler.plugins.plugin_api.plugin import Plugin


class PluginApi(Plugin):
    def __init__(self):
        super().__init__()

    def load(self):
        pass

    def unload(self):
        pass

    def validate(self):
        return True, None
