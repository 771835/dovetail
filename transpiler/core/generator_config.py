# coding=utf-8
from __future__ import annotations
from dataclasses import dataclass
from enum import IntEnum, auto
from typing import NamedTuple

from transpiler.core.safe_enum import SafeEnum


class OptimizationLevel(IntEnum):
    O0 = 0
    O1 = 1
    O2 = 2
    O3 = 3


class MinecraftEdition(SafeEnum):
    """Minecraft游戏版本类型枚举"""
    JAVA_EDITION = auto()  # Java版 (JE)
    BEDROCK_EDITION = auto()  # 基岩版 (BE)


class MinecraftVersion(NamedTuple):
    major: int
    minor: int
    patch: int
    edition: MinecraftEdition

    @classmethod
    def from_str(cls, version: str, edition: str = "java_edition") -> MinecraftVersion:
        minecraft_edition: MinecraftEdition = MinecraftEdition.JAVA_EDITION
        if 'be' in edition.lower() or 'bedrock' in edition.lower():
            minecraft_edition = MinecraftEdition.BEDROCK_EDITION

        version_ = list(map(int, version.split(".")))
        return cls(version_[0], version_[1], version_[2] if len(version_) > 2 else 0, minecraft_edition)


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
