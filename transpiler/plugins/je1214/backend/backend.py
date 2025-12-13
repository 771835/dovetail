# coding=utf-8
from transpiler.core.backend import Backend
from transpiler.core.compile_config import CompileConfig
from transpiler.core.enums import MinecraftVersion, MinecraftEdition


class JE1214Backend(Backend):
    @staticmethod
    def is_support(config: CompileConfig) -> bool:
        version = config.minecraft_version
        if version != MinecraftVersion(1, 20, 4, MinecraftEdition.JAVA_EDITION):
            return False
        if config.enable_recursion or config.enable_experimental:
            return False
        return True

    @staticmethod
    def get_name() -> str:
        return "je1214"

