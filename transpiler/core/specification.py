# coding=utf-8
from abc import ABC, abstractmethod
from pathlib import Path

from typing_extensions import deprecated

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
    """IR 优化管道"""

    @abstractmethod
    def __init__(self, builder: IRBuilder, config: CompileConfig):
        """初始化"""

    @abstractmethod
    def exec(self):
        """执行优化"""
        pass


@deprecated("请用 transpiler.core.backend.base.Backend 代替")
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
