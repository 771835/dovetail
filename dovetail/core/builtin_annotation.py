# coding=utf-8
from dovetail.core.enums.types import AnnotationCategory
from dovetail.core.symbols.annotation import Annotation

builtin_annotations: dict[str, Annotation] = {
    "init": Annotation("init", None, AnnotationCategory.LIFECYCLE),
    "tick": Annotation("tick", {"interval": 1}, AnnotationCategory.LIFECYCLE),
    "export": Annotation("export", None, AnnotationCategory.VISIBILITY),
    "extern": Annotation("extern", {"path": "", "abi": "dovetail"}, AnnotationCategory.VISIBILITY),
    "internal": Annotation("internal", None, AnnotationCategory.VISIBILITY),
    "noinline": Annotation("noinline", None, AnnotationCategory.OPTIMIZATION),
    "target": Annotation("target", {"edition": "java"}, AnnotationCategory.CONDITIONAL),
    "version": Annotation("version", {"min": "1.20.4", "max": "1.21.4"}, AnnotationCategory.METADATA),
    "deprecated": Annotation("deprecated", {"msg": "Please use newFunction instead"}, AnnotationCategory.METADATA),
    "doc": Annotation("doc", {"doce": "why use @doc?"}, AnnotationCategory.METADATA),
    "author": Annotation("author", {"author": ""}, AnnotationCategory.CONDITIONAL),
    "since": Annotation("author", {"version": ""}, AnnotationCategory.CONDITIONAL)
}


def get_annotation(name: str) -> Annotation | None:
    """
    获取内建注解的注解对象

    如果插件要增加自己设置的注解可以注入这个函数，不推荐直接修改builtin_annotations

    Args:
        name: 内建函数的函数名

    Returns:
        注解对象
    """
    return builtin_annotations.get(name)
