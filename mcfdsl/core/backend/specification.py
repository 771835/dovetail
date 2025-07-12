# coding=utf-8
from __future__ import annotations

from abc import ABC, abstractmethod
from enum import IntEnum, auto
from pathlib import Path
from typing import NamedTuple

from mcfdsl.core.backend.ir_builder import IRBuilder
from mcfdsl.core.safe_enum import SafeEnum


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


class IROptimizerSpec(ABC):
    """IR优化器"""

    @abstractmethod
    def __init__(self, builder: IRBuilder,
                 level: OptimizationLevel = OptimizationLevel.O0, debug: bool = False):
        """初始化"""

    @abstractmethod
    def optimize(self) -> IRBuilder:
        """对原始IR优化"""

    @classmethod
    @abstractmethod
    def is_support(
            cls, version: MinecraftVersion) -> bool:
        """判断是否支持该版本"""


class IROptimizationPass(ABC):
    @abstractmethod
    def __init__(self, builder: IRBuilder, debug: bool = False):
        """初始化"""

    @abstractmethod
    def exec(self):
        """执行优化"""
        pass


class CodeGeneratorSpec(ABC):
    """代码生成部分接口"""

    @abstractmethod
    def __init__(self, builder: IRBuilder,
                 target: Path, debug: bool = False, namespace: str = 'example'):
        """初始化"""

    @abstractmethod
    def generate_commands(self):
        """将优化的IR编译为Minecraft命令"""

    @classmethod
    @abstractmethod
    def is_support(
            cls, version: MinecraftVersion) -> bool:
        """判断是否支持该版本"""
