# coding=utf-8
"""
优化 Pass 基类
"""
from abc import ABC, abstractmethod

from transpiler.core.compile_config import CompileConfig
from transpiler.core.ir_builder import IRBuilder
from transpiler.core.optimize.context import OptimizationContext
from transpiler.core.optimize.pass_metadata import PassMetadata


class IROptimizer(ABC):
    """IR优化器接口"""

    @abstractmethod
    def __init__(self, builder: IRBuilder,
                 config: CompileConfig):
        """初始化"""

    @abstractmethod
    def optimize(self) -> IRBuilder:
        """对原始IR优化"""


class IROptimizationPass(ABC):
    """
    优化 Pass 接口

    提供元数据支持、条件执行和分析能力。
    """

    @abstractmethod
    def __init__(self, builder: IRBuilder, config: CompileConfig):
        """初始化"""
        self.builder = builder
        self.config = config

    @classmethod
    def get_metadata(cls) -> PassMetadata:
        """
        获取 Pass 元数据

        Returns:
            PassMetadata 对象
        """
        if hasattr(cls, "_pass_metadata") and isinstance(cls._pass_metadata, PassMetadata):
            return cls._pass_metadata
        raise NotImplementedError

    @abstractmethod
    def execute(self) -> bool:
        """
        执行优化

        Returns:
            是否产生了 IR 变更
        """
        pass

    def should_run(self, context: OptimizationContext) -> bool:
        """
        判断是否应该运行此 Pass

        Args:
            context: 优化上下文

        Returns:
            是否应该运行
        """
        metadata = self.get_metadata()

        # 检查必需特性
        for feature in metadata.required_features:
            if not context.has_feature(feature):
                return False

        # 检查不兼容的 Pass
        for incompatible in metadata.incompatible_with:
            if context.was_executed(incompatible):
                return False

        return True

    def analyze(self) -> dict:
        """
        分析 IR（可选实现）

        Returns:
            分析结果字典
        """
        return {}
