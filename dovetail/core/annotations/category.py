# coding=utf-8
from __future__ import annotations

from enum import auto

from dovetail.utils.safe_enum import SafeEnum


class AnnotationTiming(SafeEnum):
    """
    注解语义的执行时机。

    PRE_SYMBOL:  符号对象创建之前执行（条件编译类）
    POST_SYMBOL: 符号对象创建之后执行（标记类、校验类）
    """
    PRE_SYMBOL = auto()
    POST_SYMBOL = auto()


class AnnotationCategory(SafeEnum):
    """
    注解系统声明类型

    用于区分注解类型并根据注解类型在不同时机处理

    Attributes:
        LIFECYCLE: 控制函数执行时机
        VISIBILITY: 控制可见性和优化
        LINKAGE: 控制后端链接接口指令的生成
        BACKEND_HINT: 控制后端代码生成
        CONDITION: 条件编译
        METADATA: 元数据注解，不影响编译逻辑
    """
    # 核心语义注解 - 影响代码生成和执行
    LIFECYCLE = "lifecycle"
    VISIBILITY = "visibility"
    LINKAGE = "linkage"
    BACKEND_HINT = "backend_hint"

    # 条件编译注解 - 在AST遍历阶段处理
    CONDITION = "condition"

    # 元数据注解 - 不影响编译逻辑
    METADATA = "metadata"

    @property
    def default_timing(self) -> AnnotationTiming:
        """根据类别推导默认执行时机，个别注解可显式覆盖"""
        if self == AnnotationCategory.CONDITION:
            return AnnotationTiming.PRE_SYMBOL
        return AnnotationTiming.POST_SYMBOL