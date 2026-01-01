# coding=utf-8
"""
优化 Pass 注册表模块

管理所有注册的优化 Pass，提供查询和验证功能。
"""
from __future__ import annotations

from transpiler.core.optimize.base import IROptimizationPass
from transpiler.core.optimize.pass_metadata import PassMetadata


class PassRegistry:
    """优化 Pass 注册表"""

    def __init__(self):
        self._passes: dict[str, type[IROptimizationPass]] = {}

    def register(self, pass_class: type[IROptimizationPass]) -> None:
        """
        注册优化 Pass

        Args:
            pass_class: Pass 类对象

        Raises:
            ValueError: 当 Pass 名称已存在时
        """
        metadata = pass_class.get_metadata()

        if metadata.name in self._passes:
            raise ValueError(f"Pass with name '{metadata.name}' already registered")

        self._passes[metadata.name] = pass_class

    def get(self, name: str) -> type[IROptimizationPass] | None:
        """
        获取指定名称的 Pass 类

        Args:
            name: Pass 名称

        Returns:
            Pass 类，不存在则返回 None
        """
        return self._passes.get(name)

    def get_all(self) -> dict[str, type[IROptimizationPass]]:
        """
        获取所有注册的 Pass

        Returns:
            Pass 名称到类对象的映射
        """
        return self._passes.copy()

    def get_by_level(
            self,
            level: int
    ) -> list[type["IROptimizationPass"]]:
        """
        获取指定优化级别及以下的所有 Pass

        Args:
            level: 优化级别

        Returns:
            Pass 类列表
        """
        return [
            pass_class for pass_class in self._passes.values()
            if pass_class.get_metadata().level <= level
        ]

    def get_by_phase(
            self,
            phase: str
    ) -> list[type["IROptimizationPass"]]:
        """
        获取指定阶段的所有 Pass

        Args:
            phase: 阶段名称

        Returns:
            Pass 类列表
        """
        return [
            pass_class for pass_class in self._passes.values()
            if pass_class.get_metadata().phase == phase
        ]

    def clear(self) -> None:
        """清空注册表"""
        self._passes.clear()


# 全局注册表实例
_registry = PassRegistry()


def get_registry() -> PassRegistry:
    """获取全局注册表实例"""
    return _registry


def register_pass(pass_metadata: PassMetadata | None = None):
    """
    装饰器：注册优化 Pass

    Example:
        支持两种使用方式：

        1. 不带参数：Pass 类自己实现 get_metadata() 方法
           @register_pass
           class MyPass(IROptimizationPassV2):
               @classmethod
               def get_metadata(cls):
                   return PassMetadata(...)

        2. 带参数：直接传入 PassMetadata
           @register_pass(PassMetadata(...))
           class MyPass(IROptimizationPassV2):
               pass
    """

    def decorator(pass_class: type[IROptimizationPass]):
        """内部装饰器"""
        pass_class._pass_metadata = pass_metadata
        get_registry().register(pass_class)
        return pass_class

    return decorator
