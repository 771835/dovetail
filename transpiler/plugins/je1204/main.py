# coding=utf-8
from .generator import CodeGenerator
from ..plugin_api_v1 import Plugin
from ..plugin_api_v1.registry import registry_backend


class JE1204(Plugin):
    def __init__(self):
        super().__init__()

    def load(self):
        registry_backend(CodeGenerator)

    def unload(self):
        pass

    def validate(self):
        return True, None
