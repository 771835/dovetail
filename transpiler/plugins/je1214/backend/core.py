# coding=utf-8
from transpiler.core.backend import Backend
from transpiler.core.compile_config import CompileConfig


class JE1214Backend(Backend):
    @staticmethod
    def is_support(config: CompileConfig) -> bool:
        version = config.minecraft_version
        if version.display_version != "1.21.4" or version.is_bedrock_edition():
            return False
        if config.enable_recursion or config.enable_experimental:
            return False
        return True

    @staticmethod
    def get_name() -> str:
        return "je1214"
