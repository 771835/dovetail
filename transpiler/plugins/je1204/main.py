# coding=utf-8
from transpiler.plugins.plugin_api_v1 import registry_backend, Plugin
from .generator import CodeGenerator


class JE1204(Plugin):
    def __init__(self):
        super().__init__()

    def load(self):
        registry_backend(CodeGenerator)

    def unload(self):
        pass

    def validate(self):
        return True