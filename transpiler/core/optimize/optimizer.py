# coding=utf-8
"""
优化器主模块

实现基于使用优化管道管理 Pass 的执行。
"""
from __future__ import annotations

import copy

from transpiler.core.compile_config import CompileConfig
from transpiler.core.ir_builder import IRBuilder
from transpiler.core.optimize.base import IROptimizer
from transpiler.core.optimize.passes import *  # NOQA
from transpiler.core.optimize.pipeline import OptimizationPipeline


class Optimizer(IROptimizer):
    """
    IR 优化器

    使用优化管道管理 Pass 的执行，提供灵活的
    优化策略配置。
    """

    def __init__(self, builder: IRBuilder, config: CompileConfig):
        """
        初始化优化器

        Args:
            builder: IR 构建器
            config: 编译配置
        """
        self.config = config
        self.initial_builder = builder
        self.builder = copy.deepcopy(builder)
        self.pipeline = OptimizationPipeline(config)

    def optimize(self) -> IRBuilder:
        """
        执行优化

        Returns:
            优化后的 IR 构建器
        """
        # 使用管道执行优化
        return self.pipeline.run(self.builder)
