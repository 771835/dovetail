# coding=utf-8
"""
MCDL 转译器 Minecraft 兼容性枚举模块

此模块包含与 Minecraft 游戏版本和平台相关的
枚举定义，用于确保生成的命令与目标环境兼容。
"""
from __future__ import annotations

from abc import abstractmethod, ABC
from functools import total_ordering
from typing import TypeVar

from attrs import define, field, validators

from transpiler.utils.safe_enum import SafeEnum

MinecraftVersionType = TypeVar('MinecraftVersionType', bound='MinecraftVersion')


class UnknownMinecraftVersionError(Exception):
    """未知的 Minecraft 版本错误"""
    pass


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

    @property
    def display_name(self) -> str:
        """返回可读的版本名称"""
        names = {
            self.JAVA_EDITION: "Java Edition",
            self.BEDROCK_EDITION: "Bedrock Edition"
        }
        return names.get(self, self.value)


@total_ordering
class MinecraftVersion(ABC):
    """
    Minecraft版本信息基类
    """

    def __init__(self):
        self._edition: MinecraftEdition | None = None

    @staticmethod
    def instance(version: str, edition: str = "java_edition") -> MinecraftVersionType:
        """
        自动根据字符串创建Minecraft版本对象
        """
        try:
            # 验证版本字符串格式
            if not version or not isinstance(version, str):
                raise ValueError(f"Invalid version string: {version}")

            # 清理版本字符串
            version = version.strip()

            # 处理带前缀的版本号（如"1.20.4"）
            if version.startswith('1.'):
                return OldMinecraftVersion.from_str(version, edition)
            else:
                # 假设为新格式（年份格式）
                return NewMinecraftVersion.from_str(version, edition)

        except Exception as e:
            raise UnknownMinecraftVersionError(f"Cannot parse version '{version}': {str(e)}") from e

    @classmethod
    @abstractmethod
    def from_str(cls, version: str, edition: str = "java_edition") -> MinecraftVersionType:
        """从字符串创建版本对象"""
        raise NotImplementedError()

    @property
    @abstractmethod
    def edition(self) -> MinecraftEdition:
        """获取版本类型"""
        pass

    @property
    @abstractmethod
    def display_version(self) -> str:
        """获取可读的版本字符串"""
        pass

    @abstractmethod
    def __lt__(self, other: object) -> bool:
        """版本比较"""
        pass

    def __eq__(self, other: object) -> bool:
        """相等比较"""
        if not isinstance(other, MinecraftVersion):
            return NotImplemented
        return (self.edition == other.edition and
                self.display_version == other.display_version)

    def __str__(self) -> str:
        return f"{self.edition.display_name} {self.display_version}"

    def is_java_edition(self) -> bool:
        """是否为Java版"""
        return self.edition == MinecraftEdition.JAVA_EDITION

    def is_bedrock_edition(self) -> bool:
        """是否为基岩版"""
        return self.edition == MinecraftEdition.BEDROCK_EDITION


@define(frozen=True, slots=True, eq=False, repr=False)
@total_ordering
class OldMinecraftVersion(MinecraftVersion):
    """
    Minecraft版本信息(1.21.11及以前)
    """
    major: int = field(converter=int, validator=validators.instance_of(int))
    minor: int = field(converter=int, validator=validators.instance_of(int))
    patch: int = field(converter=int, validator=validators.instance_of(int))
    edition: MinecraftEdition = field(validator=validators.instance_of(MinecraftEdition))

    def __attrs_post_init__(self):
        # 验证版本号的合理性
        if self.major < 0 or self.minor < 0 or self.patch < 0:
            raise ValueError("Version numbers must be non-negative")

    @classmethod
    def from_str(cls, version: str, edition: str = "java_edition") -> OldMinecraftVersion:
        """从字符串创建旧版Minecraft版本对象"""
        # 标准化版本字符串
        clean_version = version.replace('v', '').strip()

        minecraft_edition = MinecraftEdition.JAVA_EDITION
        if any(keyword in edition.lower() for keyword in ['be', 'bedrock', 'pe']):
            minecraft_edition = MinecraftEdition.BEDROCK_EDITION

        try:
            # 处理版本号
            parts = clean_version.split('.')
            if not (2 <= len(parts) <= 3):
                raise ValueError(f"Old version format should be 'major.minor' or 'major.minor.patch'")

            version_parts = list(map(int, parts))

            major = version_parts[0]
            minor = version_parts[1]
            patch = version_parts[2] if len(version_parts) > 2 else 0

            return cls(major=major, minor=minor, patch=patch, edition=minecraft_edition)
        except (ValueError, IndexError) as e:
            raise ValueError(f"Invalid old version string: {version}") from e

    @property
    def display_version(self) -> str:
        """返回可读的版本号"""
        if self.patch == 0:
            return f"{self.major}.{self.minor}"
        return f"{self.major}.{self.minor}.{self.patch}"

    def __repr__(self) -> str:
        return f"OldMinecraftVersion({self.edition.value}-{self.display_version})"

    def __str__(self) -> str:
        return f"{self.edition.display_name} {self.display_version}"

    def __lt__(self, other: object) -> bool:
        """版本比较逻辑"""
        if not isinstance(other, MinecraftVersion):
            return NotImplemented

        if isinstance(other, NewMinecraftVersion):
            # 假设新版本总是比旧版本新（可根据实际需求调整）
            return True

        if not isinstance(other, OldMinecraftVersion):
            return NotImplemented

        # 同类型比较
        if self.major != other.major:
            return self.major < other.major
        if self.minor != other.minor:
            return self.minor < other.minor
        return self.patch < other.patch

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, OldMinecraftVersion):
            return False
        return (self.major == other.major and
                self.minor == other.minor and
                self.patch == other.patch and
                self.edition == other.edition)


@define(frozen=True, slots=True, eq=False, repr=False)
@total_ordering
class NewMinecraftVersion(MinecraftVersion):
    """
    Minecraft版本信息(1.21.11后的新格式：年份.补丁)
    """
    year: int = field(converter=int, validator=validators.instance_of(int))
    release: int = field(converter=int, validator=validators.instance_of(int))
    edition: MinecraftEdition = field(validator=validators.instance_of(MinecraftEdition))

    def __attrs_post_init__(self):
        # 验证年份和发布号的合理性
        if self.year > 2000:  # 若输入2024自动修复为24
            self.year -= 2000
        if self.year < 9:  # Minecraft发布年份
            raise ValueError("Year must be >= 09")
        if self.release < 0:
            raise ValueError("Release number must be non-negative")

    @classmethod
    def from_str(cls, version: str, edition: str = "java_edition") -> NewMinecraftVersion:
        """从字符串创建新版Minecraft版本对象"""
        minecraft_edition = MinecraftEdition.JAVA_EDITION
        if any(keyword in edition.lower() for keyword in ['be', 'bedrock', 'pe']):
            minecraft_edition = MinecraftEdition.BEDROCK_EDITION

        try:
            version_parts = list(map(int, version.split(".")))
            if len(version_parts) != 2:
                raise ValueError("New version format should be 'year.release'")

            year, release = version_parts
            return cls(year=year, release=release, edition=minecraft_edition)
        except (ValueError, IndexError) as e:
            raise ValueError(f"Invalid new version string: {version}") from e

    @property
    def display_version(self) -> str:
        """返回可读的版本号"""
        return f"{self.year}.{self.release}"

    def __repr__(self) -> str:
        return f"NewMinecraftVersion({self.edition.value}-{self.display_version})"

    def __str__(self) -> str:
        return f"{self.edition.display_name} {self.display_version}"

    def __lt__(self, other: object) -> bool:
        """版本比较逻辑"""
        if not isinstance(other, MinecraftVersion):
            return NotImplemented

        if isinstance(other, OldMinecraftVersion):
            # 假设新版本总是比旧版本新
            return False

        if not isinstance(other, NewMinecraftVersion):
            return NotImplemented

        # 同类型比较
        if self.year != other.year:
            return self.year < other.year
        return self.release < other.release

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, NewMinecraftVersion):
            return False
        return (self.year == other.year and
                self.release == other.release and
                self.edition == other.edition)
