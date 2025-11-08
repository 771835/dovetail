# coding=utf-8
from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path

from transpiler.core.compile_config import CompileConfig
from transpiler.core.ir_builder import IRBuilder

__all__ = [
    'IROptimizerSpec',
    'IROptimizationPass',
    'CodeGeneratorSpec'
]


class IROptimizerSpec(ABC):
    """IR优化器"""

    @abstractmethod
    def __init__(self, builder: IRBuilder,
                 config: CompileConfig):
        """初始化"""

    @abstractmethod
    def optimize(self) -> IRBuilder:
        """对原始IR优化"""


class IROptimizationPass(ABC):
    @abstractmethod
    def __init__(self, builder: IRBuilder, config: CompileConfig):
        """初始化"""

    @abstractmethod
    def exec(self):
        pass


class CodeGeneratorSpec(ABC):
    """代码生成部分接口"""

    @abstractmethod
    def __init__(self, builder: IRBuilder,
                 target: Path, config: CompileConfig):
        """初始化"""

    @abstractmethod
    def generate(self):
        """将优化的IR编译为目标语言"""

    @staticmethod
    @abstractmethod
    def is_support(config: CompileConfig) -> bool:
        """判断是否支持该配置"""

    @staticmethod
    @abstractmethod
    def get_name() -> str:
        """获得后端名称"""
