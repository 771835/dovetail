# coding=utf-8
from transpiler.plugins.plugin_api.v1.registry import registry_backend

from transpiler.plugins.plugin_api import Plugin
from .generator import CodeGenerator


class JE1204(Plugin):
    def __init__(self):
        super().__init__()

    def load(self):
        registry_backend(CodeGenerator)

    def unload(self):
        pass

    def validate(self):
        return True, None
