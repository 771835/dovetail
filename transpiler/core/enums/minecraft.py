# coding=utf-8
"""
MCDL 转译器 Minecraft 兼容性枚举模块

此模块包含与 Minecraft 游戏版本和平台相关的
枚举定义，用于确保生成的命令与目标环境兼容。
"""
from __future__ import annotations

from attrs import define, field, validators

from transpiler.utils.safe_enum import SafeEnum


class MinecraftEdition(SafeEnum):
    """
    Minecraft 游戏版本类型枚举

    用于区分不同的 Minecraft 平台，因为不同版本
    支持的命令语法和功能存在差异。
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
