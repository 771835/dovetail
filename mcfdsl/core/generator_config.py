# coding=utf-8
from dataclasses import dataclass

from mcfdsl.core.backend.specification import OptimizationLevel, MinecraftVersion


@dataclass
class GeneratorConfig:
    namespace: str
    optimization_level: OptimizationLevel
    minecraft_version: MinecraftVersion
    debug: bool = False
    no_generator_commands: bool = False
    enable_recursion: bool = False
    enable_experimental: bool = False

    def __post_init__(self):
        if not isinstance(self.optimization_level, OptimizationLevel) or not isinstance(self.minecraft_version,
                                                                                        MinecraftVersion):
            raise ValueError("Invalid optimization level")
