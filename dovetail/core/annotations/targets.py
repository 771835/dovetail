# coding=utf-8
from __future__ import annotations

from dovetail.utils.safe_enum import SafeEnum


class AnnotationTarget(SafeEnum):
    """注解可作用于的符号类型"""
    FUNCTION = "function"
    VARIABLE = "variable"
    CLASS = "class"
    STRUCT = "struct"
    ENUM = "enum"
    INCLUDE = "include"  # 很不合理，但是为了条件编译暂时忍忍？