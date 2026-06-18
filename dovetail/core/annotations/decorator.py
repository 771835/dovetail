# coding=utf-8

from dovetail.core.annotations.base import AnnotationProcessor
from dovetail.core.annotations.registry import get_registry


def annotation_processor(cls: type[AnnotationProcessor]):
    """
    装饰器：自动注册注解处理器到全局注册表

    用法：
        @annotation_processor
        class VersionProcessor(AnnotationProcessor):
            annotation_name = "version"
            ...
    """
    get_registry().register_class(cls)
    return cls
