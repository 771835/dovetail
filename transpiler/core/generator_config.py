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
    """Minecraft游戏版本类型枚举

    Attributes:
        JAVA_EDITION: Java版 (JE)
        BEDROCK_EDITION: 基岩版 (BE)
    """
    JAVA_EDITION = "java_edition"
    BEDROCK_EDITION = "bedrock_edition"


@define(frozen=True, slots=True, eq=True, repr=False)
class MinecraftVersion:
    """Minecraft版本信息"""
    major: int = field(converter=int)
    minor: int = field(converter=int)
    patch: int = field(converter=int)
    edition: MinecraftEdition = field(validator=validators.instance_of(MinecraftEdition))

    @classmethod
    def from_str(cls, version: str, edition: str = "java_edition") -> MinecraftVersion:
        """从字符串创建Minecraft版本对象

        Args:
            version: 版本字符串，格式如 "1.20.4"
            edition: 版本类型，默认为java_edition

        Returns:
            MinecraftVersion: Minecraft版本对象

        Raises:
            ValueError: 当版本字符串格式不正确时
        """
        minecraft_edition = MinecraftEdition.JAVA_EDITION
        if 'be' in edition.lower() or 'bedrock' in edition.lower():
            minecraft_edition = MinecraftEdition.BEDROCK_EDITION

        try:
            version_parts = list(map(int, version.split(".")))
            if len(version_parts) < 2:
                raise ValueError(f"Invalid version format: {version}")

            major = version_parts[0]
            minor = version_parts[1]
            patch = version_parts[2] if len(version_parts) > 2 else 0

            return cls(major=major, minor=minor, patch=patch, edition=minecraft_edition)
        except ValueError as e:
            raise ValueError(f"Invalid version string: {version}") from e

    def __repr__(self):
        return f"{self.edition.value}-{self.major}.{self.minor}.{self.patch}"


@define(slots=True, frozen=True)
class CompileConfig:
    """
    编译配置

    Attributes:
        source_path: 源文件路径
        target_path: 目标输出路径
        namespace: 命名空间
        optimization_level: 优化等级
        minecraft_version: Minecraft版本信息
        backend_name: 后端名称
        debug: 调试模式开关
        no_generate_commands: 不生成指令开关
        output_temp_file: 输出临时文件开关
        enable_recursion: 启用递归开关
        enable_same_name_function_nesting: 启用同名函数嵌套开关
        enable_first_class_functions: 启用函数一等公民开关
        enable_experimental: 启用实验性功能开关
        lib_path: 库文件路径
    """
    source_path: Path = field(validator=validators.instance_of(Path))
    target_path: Path = field(validator=validators.instance_of(Path))
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
