# coding=utf-8
from __future__ import annotations

from enum import IntEnum
from pathlib import Path

from attrs import define, field, validators

from transpiler.core.safe_enum import SafeEnum


class OptimizationLevel(IntEnum):
    """
    优化等级

    - O0 不优化
    - O1 少量优化
    - O2 正常优化
    - O3 激进优化
    """
    O0 = 0
    O1 = 1
    O2 = 2
    O3 = 3


class MinecraftEdition(SafeEnum):
    """Minecraft游戏版本类型枚举"""
    JAVA_EDITION = "java_edition"  # Java版 (JE)
    BEDROCK_EDITION = "bedrock_edition"  # 基岩版 (BE)


@define(frozen=True, slots=True, eq=True, repr=False)
class MinecraftVersion:
    major: int = field(converter=int)
    minor: int = field(converter=int)
    patch: int = field(converter=int)
    edition: MinecraftEdition = field(validator=validators.instance_of(MinecraftEdition))

    @classmethod
    def from_str(cls, version: str, edition: str = "java_edition") -> MinecraftVersion:
        minecraft_edition: MinecraftEdition = MinecraftEdition.JAVA_EDITION
        # 如果edition字段中存在be等字段即视为基岩版
        if 'be' in edition.lower() or 'bedrock' in edition.lower():
            minecraft_edition = MinecraftEdition.BEDROCK_EDITION

        version_ = list(map(int, version.split(".")))
        return cls(
            major=version_[0],
            minor=version_[1],
            patch=version_[2] if len(version_) > 2 else 0,
            edition=minecraft_edition
        )

    def __repr__(self):
        return f"{self.edition.value}-{self.major}.{self.minor}.{self.patch}"


@define(slots=True, frozen=True)
class GeneratorConfig:
    """
    编译配置
    """
    namespace: str = field(validator=validators.instance_of(str))
    optimization_level: OptimizationLevel = field(validator=validators.instance_of(OptimizationLevel))
    minecraft_version: MinecraftVersion = field(validator=validators.instance_of(MinecraftVersion))
    backend_name: str = field(validator=validators.instance_of(str), default="")
    debug: bool = field(validator=validators.instance_of(bool), default=False)
    no_generate_commands: bool = field(validator=validators.instance_of(bool), default=False)
    output_temp_file: bool = field(validator=validators.instance_of(bool), default=False)
    enable_recursion: bool = field(validator=validators.instance_of(bool), default=False)
    enable_same_name_function_nesting: bool = field(validator=validators.instance_of(bool), default=False)
    enable_first_class_functions: bool = field(validator=validators.instance_of(bool), default=False)
    enable_experimental: bool = field(validator=validators.instance_of(bool), default=False)
    lib_path: Path = field(validator=validators.instance_of(Path), default=Path("lib").resolve())
