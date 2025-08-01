# coding=utf-8
from __future__ import annotations

from enum import IntEnum, auto
from typing import NamedTuple

from attrs import define, field, validators

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


@define(slots=True, frozen=True)
class GeneratorConfig:
    namespace: str = field(validator=validators.instance_of(str))
    optimization_level: OptimizationLevel = field(validator=validators.instance_of(OptimizationLevel))
    minecraft_version: MinecraftVersion = field(validator=validators.instance_of(MinecraftVersion))
    debug: bool = field(validator=validators.instance_of(bool), default=False)
    no_generate_commands: bool = field(validator=validators.instance_of(bool), default=False)
    enable_recursion: bool = field(validator=validators.instance_of(bool), default=False)
    enable_same_name_function_nesting: bool = field(validator=validators.instance_of(bool), default=False)
    enable_experimental: bool = field(validator=validators.instance_of(bool), default=False)
