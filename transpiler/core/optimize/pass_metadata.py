# coding=utf-8
"""
优化 Pass 元数据模块

定义优化 Pass 的元数据结构，用于声明 Pass 的
基本信息、依赖关系、特性要求等。
"""
from __future__ import annotations

from attrs import define, field

from transpiler.core.enums.optimization import OptimizationLevel
from transpiler.utils.safe_enum import SafeEnum


class PassPhase(SafeEnum):
    """优化 Pass 执行阶段常量"""

    ANALYZE = "analyze"
    """分析阶段：收集 IR 信息，不修改 IR"""

    TRANSFORM = "transform"
    """转换阶段：修改 IR 结构"""

    CLEANUP = "cleanup"
    """清理阶段：清理冗余代码"""

    @classmethod
    def get_phase_order(cls) -> tuple[PassPhase, ...]:
        """获取阶段执行顺序"""
        return cls.ANALYZE, cls.TRANSFORM, cls.CLEANUP


@define(frozen=True, slots=True)
class PassMetadata:
    """
    优化 Pass 的元数据

    Attributes:
        name: Pass 的唯一标识符
        display_name: 显示名称
        description: Pass 功能描述
        level: 默认优化级别
        phase: 所属阶段
        depends_on: 依赖的其他 Pass 名称
        incompatible_with: 不兼容的 Pass 名称
        repeatable: 是否可重复执行
        required_features: 运行所需的 IR 特性
        provided_features: 执行后提供的 IR 特性
    """
    name: str
    display_name: str
    description: str = ""
    level: OptimizationLevel = OptimizationLevel.O0
    phase: PassPhase = PassPhase.TRANSFORM
    depends_on: tuple[str, ...] = field(factory=tuple)
    incompatible_with: tuple[str, ...] = field(factory=tuple)
    repeatable: bool = False
    required_features: tuple[str, ...] = field(factory=tuple)
    provided_features: tuple[str, ...] = field(factory=tuple)
