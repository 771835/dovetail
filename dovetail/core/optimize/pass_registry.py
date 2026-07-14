# coding=utf-8
"""
优化 Pass 注册表模块

全局注册表是单例，通过 get_registry() 获取。
Pass 通过 @register_pass 装饰器在模块导入时自动注册。
"""
from __future__ import annotations

from dovetail.core.optimize.base import IROptimizationPass
from dovetail.core.optimize.pass_metadata import PassMetadata


class PassRegistry:
    """
    优化 Pass 注册表

    职责：存储和检索 Pass 类，不参与调度逻辑。
    调度（依赖排序、级别过滤）由 OptimizationPipeline 负责。
    """

    def __init__(self):
        self._passes: dict[str, type[IROptimizationPass]] = {}

    def register(self, pass_class: type[IROptimizationPass]) -> None:
        """
        注册一个 Pass 类。

        Args:
            pass_class: 要注册的 Pass 类

        Raises:
            ValueError: Pass 名称已存在时（防止重复注册）
        """
        metadata = pass_class.get_metadata()
        if metadata.name in self._passes:
            raise ValueError(
                f"Pass '{metadata.name}' 已注册，不允许重复注册。"
                f"已注册的类：{self._passes[metadata.name].__name__}，"
                f"新类：{pass_class.__name__}"
            )
        self._passes[metadata.name] = pass_class

    def get(self, name: str) -> type[IROptimizationPass] | None:
        """按名称获取 Pass 类，不存在返回 None"""
        return self._passes.get(name)

    def get_all(self) -> dict[str, type[IROptimizationPass]]:
        """获取所有已注册 Pass 的名称→类映射（返回副本）"""
        return self._passes.copy()

    def get_by_level(self, level: int) -> list[type[IROptimizationPass]]:
        """获取优化级别不超过 level 的所有 Pass"""
        return [
            p for p in self._passes.values()
            if p.get_metadata().level <= level
        ]

    def get_by_phase(self, phase: str) -> list[type[IROptimizationPass]]:
        """获取指定阶段的所有 Pass"""
        return [
            p for p in self._passes.values()
            if p.get_metadata().phase == phase
        ]

    def clear(self) -> None:
        """清空注册表（主要用于测试）"""
        self._passes.clear()


# ── 全局单例 ──────────────────────────────────────────────────

_registry = PassRegistry()


def get_registry() -> PassRegistry:
    """获取全局注册表单例"""
    return _registry


def register_pass(pass_metadata: PassMetadata | None = None):
    """
    装饰器：将 Pass 类注册到全局注册表。

    支持两种调用方式：

    方式一（带 PassMetadata）：
        @register_pass(PassMetadata(name="my_pass", ...))
        class MyPass(IROptimizationPass):
            ...

    方式二（不带括号，Pass 自行实现 get_metadata()）：
        @register_pass
        class MyPass(IROptimizationPass):
            @classmethod
            def get_metadata(cls):
                return PassMetadata(name="my_pass", ...)

    Args:
        pass_metadata: PassMetadata 实例，或 None（不带括号时）

    Returns:
        装饰器函数（或直接返回类，若不带括号调用）
    """
    # 不带括号调用时，pass_metadata 实际上是类本身
    if pass_metadata is not None and not isinstance(pass_metadata, PassMetadata):
        cls = pass_metadata
        get_registry().register(cls)
        return cls

    # 带括号调用时，返回真正的装饰器
    def decorator(pass_class: type[IROptimizationPass]) -> type[IROptimizationPass]:
        if pass_metadata is not None:
            pass_class._pass_metadata = pass_metadata
        get_registry().register(pass_class)
        return pass_class

    return decorator