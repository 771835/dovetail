# coding=utf-8
"""
内置注解

本文件根据DFP-6内置注解规范定义了全部内置注解及获取函数

Examples:
    >>> get_annotation("init") # 获取init注解的注解对象

"""
from typing import Final
from dovetail.core.enums.types import AnnotationCategory
from dovetail.core.symbols.annotation import Annotation

_annotations: Final[dict[str, Annotation]] = {
    # 生命周期
    "init": Annotation("init", None, AnnotationCategory.LIFECYCLE),
    "tick": Annotation("tick", {"interval": 1}, AnnotationCategory.LIFECYCLE),

    # 可见性
    "internal": Annotation("internal", None, AnnotationCategory.VISIBILITY),
    "noinline": Annotation("noinline", None, AnnotationCategory.VISIBILITY),

    # 链接
    "export": Annotation("export", {"path": "", "abi": "dovetail"}, AnnotationCategory.LINKAGE),
    "extern": Annotation("extern", {"path": "", "abi": "dovetail"}, AnnotationCategory.LINKAGE),

    # 条件编译
    "target": Annotation("target", {"edition": "java"}, AnnotationCategory.CONDITION),
    "version": Annotation("version", {"min": "1.20.4", "max": "1.21.4"}, AnnotationCategory.CONDITION),
    "if_not_exists": Annotation("if_not_exists", None, AnnotationCategory.CONDITION),
    "if_symbol": Annotation("if_symbol", {"name": "", "type": "any"}, AnnotationCategory.CONDITION),
    "if_feature": Annotation("if_feature", {"feature": ""}, AnnotationCategory.CONDITION),

    # 后端提示
    "recursive": Annotation("recursive", None, AnnotationCategory.BACKEND_HINT),

    # 元数据
    "deprecated": Annotation("deprecated", {"msg": ""}, AnnotationCategory.METADATA),
    "doc": Annotation("doc", {"text": ""}, AnnotationCategory.METADATA),
    "author": Annotation("author", {"name": ""}, AnnotationCategory.METADATA),
    "since": Annotation("since", {"version": ""}, AnnotationCategory.METADATA),
}

def get_annotation(name: str) -> Annotation | None:
    """
    获取内建注解的注解对象

    若插件要增加注解应当注入这个函数，而非直接修改_annotations

    Args:
        name (str): 内建函数的函数名

    Returns:
        注解对象，当不存在时返回None
    """
    return _annotations.get(name)
