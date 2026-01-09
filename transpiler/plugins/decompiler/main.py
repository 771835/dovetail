# coding=utf-8
import os

from transpiler.plugins.plugin_api.v1.registry import registry_backend

from transpiler.plugins.plugin_api import Plugin


class Decompiler(Plugin):
    def __init__(self):
        super().__init__()

    def load(self):
        from .generator import CodeGenerator
        registry_backend(CodeGenerator)

    def unload(self):
        pass

    def validate(self):
        return bool(os.environ.get("DECOMPILER", None)), "未启用DECOMPILER环境变量"

    def handle_message(self, sender: Plugin, message):
        print(f"从 {sender} 收到消息: {message}")
