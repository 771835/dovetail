# coding=utf-8
import os

from .generator import CodeGenerator
from transpiler.plugins.plugin_api_v1 import Plugin, registry_backend


class Decompiler(Plugin):
    def __init__(self):
        super().__init__()

    def load(self):
        registry_backend(CodeGenerator)

    def unload(self):
        pass

    def validate(self):
        return bool(os.environ.get("DECOMPILER", None))