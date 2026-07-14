# coding=utf-8
"""
优化器主模块

Optimizer 是优化阶段的对外入口，持有 IRBuilder 和 CompileConfig，
委托 OptimizationPipeline 完成实际的 Pass 调度与执行。

Pass 注册机制：
  所有内置 Pass 通过 ensure_passes_registered() 在 Optimizer.__init__
  中按需注册，与模块导入顺序无关，且多次调用幂等。
"""
from __future__ import annotations

from dovetail.core.compile_config import CompileConfig
from dovetail.core.ir_builder import IRBuilder
from dovetail.core.optimize.base import IROptimizer
from dovetail.core.optimize.pipeline import OptimizationPipeline

_passes_registered: bool = False


def ensure_passes_registered() -> None:
    """
    确保所有内置 Pass 已注册到全局注册表。

    每个 Pass 模块在被 import 时，其顶层的 @register_pass 装饰器
    会立即执行并将 Pass 类注册到全局注册表。
    """
    global _passes_registered
    if _passes_registered:
        return

    # 导入优化管道，触发各自的 @register_pass 装饰器
    import dovetail.core.optimize.passes # noqa: F401

    _passes_registered = True


class Optimizer(IROptimizer):
    """
    IR 优化器

    职责：
      1. 触发内置 Pass 注册
      2. 构建 OptimizationPipeline（含依赖排序）
      3. 调用 pipeline.run() 执行优化
    """

    def __init__(self, builder: IRBuilder, config: CompileConfig):
        """
        初始化优化器

        Args:
            builder: 待优化的 IR 构建器
            config:  编译配置（决定优化级别、调试模式等）
        """
        ensure_passes_registered()
        self.builder = builder
        self.config = config
        self.pipeline = OptimizationPipeline(config)

    def optimize(self) -> IRBuilder:
        """
        执行优化，返回优化后的 IRBuilder（原地修改，同一对象）。
        """
        # 使用管道执行优化
        return self.pipeline.run(self.builder)