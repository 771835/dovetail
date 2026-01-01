# coding=utf-8
"""
优化上下文模块

定义优化过程中的上下文对象，用于在 Pass 之间
共享状态和信息。
"""
from __future__ import annotations

from typing import Any

from attr import evolve
from attrs import define, field


@define(slots=True, frozen=True)
class OptimizationContext:
    """
    优化上下文

    在优化管道执行过程中，Pass 可以通过上下文
    共享信息，如已执行的 Pass、当前 IR 特性等。

    Attributes:
        executed_passes: 已执行的 Pass 名称集合
        ir_features: 当前 IR 具备的特性集合
        analysis_results: Pass 分析结果字典
        iteration: 当前迭代次数
        max_iterations: 最大迭代次数
        debug: 是否启用调试模式
    """
    executed_passes: set[str] = field(factory=set)
    ir_features: set[str] = field(factory=set)
    analysis_results: dict[str, dict[str, Any]] = field(factory=dict)
    iteration: int = 0
    max_iterations: int = 1
    debug: bool = False

    def with_updates(
            self,
            **updates
    ) -> "OptimizationContext":
        """
        创建更新后的上下文副本

        Args:
            **updates: 要更新的字段

        Returns:
            新的上下文对象
        """
        valid_fields = {f.name for f in self.__attrs_attrs__}  # NOQA
        invalid_fields = set(updates.keys()) - valid_fields

        if invalid_fields:
            raise ValueError(f"Invalid fields: {invalid_fields}")

        # 预处理集合和字典类型的更新
        processed_updates = {}
        for key, value in updates.items():
            current_value = getattr(self, key)

            if isinstance(current_value, set):
                processed_updates[key] = current_value | set(value)
            elif isinstance(current_value, dict):
                processed_updates[key] = {**current_value, **value}
            else:
                processed_updates[key] = value

        return evolve(self, **processed_updates)

    def get_analysis(self, pass_name: str) -> dict[str, Any]:
        """
        获取指定 Pass 的分析结果

        Args:
            pass_name: Pass 名称

        Returns:
            分析结果字典
        """
        return self.analysis_results.get(pass_name, {})

    def has_feature(self, feature: str) -> bool:
        """
        检查 IR 是否具备指定特性

        Args:
            feature: 特性名称

        Returns:
            是否具备该特性
        """
        return feature in self.ir_features

    def was_executed(self, pass_name: str) -> bool:
        """
        检查指定 Pass 是否已执行

        Args:
            pass_name: Pass 名称

        Returns:
            是否已执行
        """
        return pass_name in self.executed_passes
