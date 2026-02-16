# coding=utf-8
"""
MCDL 转译器枚举模块统一入口

此模块重新导出所有枚举类型，保持向后兼容性，
并提供统一的导入接口。
"""

# Minecraft 兼容性枚举
from .minecraft import MinecraftEdition, MinecraftVersion
# 操作符枚举
from .operations import (
    UnaryOps,
    BinaryOps,
    CompareOps
)
# 优化相关枚举
from .optimization import OptimizationLevel
# 类型系统枚举
from .types import (
    DataType,
    StructureType,
    ValueType,
    VariableType,
    ClassType, FunctionType
)

# 导出所有枚举
__all__ = [
    # 函数类型
    'FunctionType',

    # 类型系统
    'DataType',
    'StructureType',
    'ValueType',
    'VariableType',
    'ClassType',

    # 操作符
    'UnaryOps',
    'BinaryOps',
    'CompareOps',

    # 优化
    'OptimizationLevel',

    # Minecraft
    'MinecraftEdition',
    'MinecraftVersion'
]
