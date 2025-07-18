# coding=utf-8
from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path

from transpiler.core.backend.ir_builder import IRBuilder
from transpiler.core.generator_config import MinecraftVersion, GeneratorConfig


class IROptimizerSpec(ABC):
    """IR优化器"""

    @abstractmethod
    def __init__(self, builder: IRBuilder,
                 config: GeneratorConfig):
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
    def __init__(self, builder: IRBuilder, config: GeneratorConfig):
        """初始化"""

    @abstractmethod
    def exec(self):
        """执行优化"""
        pass


class CodeGeneratorSpec(ABC):
    """代码生成部分接口"""

    @abstractmethod
    def __init__(self, builder: IRBuilder,
                 target: Path, config: GeneratorConfig):
        """初始化"""

    @abstractmethod
    def generate_commands(self):
        """将优化的IR编译为Minecraft命令"""

    @staticmethod
    @abstractmethod
    def is_support(config: GeneratorConfig) -> bool:
        """判断是否支持该配置"""
