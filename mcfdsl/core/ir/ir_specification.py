# coding=utf-8
from abc import ABC, abstractmethod
from enum import IntEnum, auto
from pathlib import Path

from mcfdsl.core.ir.ir_builder import IRBuilder
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


class IROptimizerSpec(ABC):
    """IR优化器"""

    @abstractmethod
    def optimize(self, builder: IRBuilder, level: OptimizationLevel = OptimizationLevel.O0) -> IRBuilder:
        """对原始IR优化"""

    @classmethod
    @abstractmethod
    def is_support(cls, version: tuple[int, int, int, MinecraftEdition]) -> bool:
        """判断是否支持该版本"""


class IRCompilerSpec(ABC):
    """IR编译器"""

    @abstractmethod
    def compile(self, builder: IRBuilder, target: Path) -> list[str]:
        """将优化的IR编译为Minecraft命令"""

    @classmethod
    @abstractmethod
    def is_support(cls, version: tuple[int, int, int, MinecraftEdition]) -> bool:
        """判断是否支持该版本"""
