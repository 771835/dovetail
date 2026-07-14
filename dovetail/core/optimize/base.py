# coding=utf-8
"""
优化 Pass 基类

IROptimizer      : 优化器门面接口，由 Optimizer 实现。
IROptimizationPass: 单个优化 Pass 的接口，所有内置/插件 Pass 继承此类。
"""
from __future__ import annotations

from abc import ABC, abstractmethod

from dovetail.core.compile_config import CompileConfig
from dovetail.core.enums.optimization import OptimizationLevel
from dovetail.core.ir_builder import IRBuilder
from dovetail.core.optimize.context import OptimizationContext
from dovetail.core.optimize.pass_metadata import PassMetadata


class IROptimizer(ABC):
    """IR 优化器门面接口"""

    @abstractmethod
    def __init__(self, builder: IRBuilder, config: CompileConfig):
        """初始化"""

    @abstractmethod
    def optimize(self) -> IRBuilder:
        """对原始 IR 执行优化，返回优化后的 IRBuilder"""


class IROptimizationPass(ABC):
    """
    优化 Pass 基类

    生命周期：
      1. __init__     由 pipeline 在每轮迭代中为每个 Pass 创建新实例
      2. should_run   pipeline 调用，决定本 Pass 本轮是否执行
      3. analyze      可选，收集分析信息写入 context，不修改 IR
      4. execute      核心逻辑，修改 IR，返回是否发生了变更
    """

    @abstractmethod
    def __init__(self, builder: IRBuilder, config: CompileConfig):
        """
        初始化 Pass

        Args:
            builder: 当前 IR 构建器，Pass 直接在此对象上操作
            config:  编译配置
        """
        self.builder = builder
        self.config = config

    @classmethod
    def get_metadata(cls) -> PassMetadata:
        """
        获取 Pass 元数据。

        优先返回 @register_pass 装饰器注入的 _pass_metadata。
        若子类未使用装饰器，则必须覆盖此方法。

        Returns:
            PassMetadata 对象

        Raises:
            NotImplementedError: 既未注入元数据也未覆盖此方法
        """
        if hasattr(cls, "_pass_metadata") and isinstance(cls._pass_metadata, PassMetadata):
            return cls._pass_metadata
        raise NotImplementedError(
            f"{cls.__name__} 必须使用 @register_pass 装饰器，或覆盖 get_metadata() 方法"
        )

    @abstractmethod
    def execute(self) -> bool:
        """
        执行优化。

        Returns:
            True 表示本次执行修改了 IR，False 表示无变化
        """

    def should_run(self, context: OptimizationContext) -> bool:
        """
        判断本 Pass 在当前上下文下是否应该运行。

        检查顺序（任一失败即返回 False）：
          1. 优化级别：config 的级别 value 必须 >= Pass 声明的级别 value
          2. 必需特性：IR 必须已具备所有 required_features
          3. 互斥 Pass：incompatible_with 中的 Pass 不能已执行过

        Args:
            context: 当前优化上下文

        Returns:
            是否应该运行
        """
        metadata = self.get_metadata()

        # 优化级别检查
        config_level = self.config.optimization_level
        pass_level = metadata.level
        # 统一取 .value 比较（OptimizationLevel 是 SafeEnum，value 为 tuple 首元素或整数）
        config_val = config_level.value if isinstance(config_level, OptimizationLevel) else int(config_level)
        pass_val = pass_level.value if isinstance(pass_level, OptimizationLevel) else int(pass_level)
        # SafeEnum 的 value 可能是 tuple（如 (1, "O1")），取第一个元素
        if isinstance(config_val, tuple):
            config_val = config_val[0]
        if isinstance(pass_val, tuple):
            pass_val = pass_val[0]
        if config_val < pass_val:
            return False

        # 必需特性检查
        for feature in metadata.required_features:
            if not context.has_feature(feature):
                return False

        # 互斥 Pass 检查
        for incompatible in metadata.incompatible_with:
            if context.was_executed(incompatible):
                return False

        return True

    def analyze(self) -> dict:
        """
        分析 IR（可选实现）。

        此方法不应修改 IR，只收集信息。
        返回值会被存入 context.analysis_results。

        Returns:
            分析结果字典，空字典表示无分析结果
        """
        return {}