# coding=utf-8
"""
优化 Pass 元数据模块

定义优化 Pass 的元数据结构，用于声明 Pass 的
基本信息、依赖关系、特性要求等。
"""
from __future__ import annotations

from attrs import define, field

from dovetail.core.enums.optimization import OptimizationLevel
from dovetail.utils.safe_enum import SafeEnum


class PassPhase(SafeEnum):
    """优化 Pass 执行阶段"""

    PRUNE = "prune"
    """裁剪阶段：优先裁剪无用 IR，减小代码体积，提高后续处理效率"""

    ANALYZE = "analyze"
    """分析阶段：收集 IR 信息，不修改 IR"""

    TRANSFORM = "transform"
    """转换阶段：修改 IR 结构"""

    CLEANUP = "cleanup"
    """清理阶段：清理冗余代码"""

    @classmethod
    def get_phase_order(cls) -> tuple[PassPhase, ...]:
        """获取阶段执行顺序"""
        return cls.PRUNE, cls.ANALYZE, cls.TRANSFORM, cls.CLEANUP


@define(frozen=True, slots=True)
class PassMetadata:
    """
    优化 Pass 的元数据描述符

    Attributes:
        name:               Pass 的全局唯一标识符（用于依赖声明）
        display_name:       人类可读的显示名称
        description:        Pass 功能描述
        level:              启用此 Pass 所需的最低优化级别
        phase:              所属执行阶段（影响调度顺序）
        depends_on:         依赖的其他 Pass 名称（保证在其之后执行）
        incompatible_with:  不兼容的 Pass 名称（不能与其共同执行）
        repeatable:         是否可在多轮迭代中重复执行（保留字段）
        required_features:  运行前 IR 必须具备的特性集合
        provided_features:  执行后向 IR 提供的特性集合
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
