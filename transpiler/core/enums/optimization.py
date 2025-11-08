# coding=utf-8
"""
MCDL 转译器优化相关枚举模块

此模块包含编译器优化级别的定义，用于控制
转译过程中的优化策略和程度。
"""
from __future__ import annotations

from enum import IntEnum


class OptimizationLevel(IntEnum):
    """
    编译器优化级别枚举

    定义不同程度的优化策略，影响生成代码的
    性能和可读性权衡。

    Attributes:
        O0: 无优化，保持代码结构清晰，便于调试
        O1: 基本优化，去除明显的冗余操作
        O2: 标准优化，平衡性能和编译时间
        O3: 激进优化，最大化运行时性能
    """
    O0 = 0
    O1 = 1
    O2 = 2
    O3 = 3
