# coding=utf-8
"""
优化上下文模块

状态生命周期说明：
  - executed_passes  : 跨迭代持久。记录历史上曾成功执行的 Pass 名称，
                       供 incompatible_with 做全局互斥判断。
  - ir_features      : 单轮状态。每轮迭代开始时清空，由本轮执行的
                       Pass 的 provided_features 重新填充，反映当前
                       IR 的真实特性集合。
  - analysis_results : 单轮状态。每轮迭代开始时清空，由本轮各 Pass
                       的 analyze() 结果填充。
"""
from __future__ import annotations

from typing import Any

from attr import evolve
from attrs import define, field


@define(slots=True, frozen=True)
class OptimizationContext:
    """
    优化上下文（不可变值对象）

    所有"修改"操作均返回新对象，原对象不变。
    这确保了管道在迭代过程中的状态可追溯。

    Attributes:
        executed_passes:  历史已执行 Pass 的名称集合（跨迭代持久）
        ir_features:      当前轮次 IR 具备的特性集合（单轮状态）
        analysis_results: 当前轮次各 Pass 的分析结果（单轮状态）
        iteration:        当前迭代轮次（从 0 开始）
        max_iterations:   最大允许迭代次数
        debug:            是否启用调试模式
    """
    executed_passes: frozenset[str] = field(factory=frozenset)
    ir_features: frozenset[str] = field(factory=frozenset)
    analysis_results: dict[str, dict[str, Any]] = field(factory=dict)
    iteration: int = 0
    max_iterations: int = 1
    debug: bool = False

    def next_iteration(self) -> OptimizationContext:
        """
        推进到下一轮迭代，返回新上下文。

        持久状态（executed_passes）原样保留。
        单轮状态（ir_features、analysis_results）清空，
        由新一轮的 Pass 执行结果重新填充。

        Returns:
            下一轮迭代的上下文对象
        """
        return evolve(
            self,
            iteration=self.iteration + 1,
            ir_features=frozenset(),
            analysis_results={},
        )

    def with_updates(self, **updates) -> OptimizationContext:
        """
        创建合并了指定字段的新上下文副本。

        合并规则：
          - frozenset 字段：取并集
          - set 字段：取并集（兼容旧代码）
          - dict 字段：浅合并（新值覆盖同名旧值）
          - 其他字段：直接替换

        Args:
            **updates: 要更新的字段名及新值

        Returns:
            新的上下文对象

        Raises:
            ValueError: 字段名不存在于 OptimizationContext 时
        """
        valid_fields = {f.name for f in self.__attrs_attrs__}
        invalid = set(updates) - valid_fields
        if invalid:
            raise ValueError(f"Invalid context fields: {invalid}")

        processed: dict[str, Any] = {}
        for key, value in updates.items():
            current = getattr(self, key)
            if isinstance(current, frozenset):
                processed[key] = current | frozenset(value)
            elif isinstance(current, set):
                processed[key] = current | set(value)
            elif isinstance(current, dict):
                processed[key] = {**current, **value}
            else:
                processed[key] = value

        return evolve(self, **processed)

    def has_feature(self, feature: str) -> bool:
        """检查当前轮次 IR 是否具备指定特性"""
        return feature in self.ir_features

    def was_executed(self, pass_name: str) -> bool:
        """检查指定 Pass 历史上是否曾成功执行过（跨迭代）"""
        return pass_name in self.executed_passes

    def get_analysis(self, pass_name: str) -> dict[str, Any]:
        """获取指定 Pass 在当前轮次的分析结果，不存在则返回空字典"""
        return self.analysis_results.get(pass_name, {})