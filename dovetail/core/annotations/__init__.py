# coding=utf-8
from dovetail.core.annotations.base import AnnotationProcessor, AnnotationContext
from dovetail.core.annotations.decorator import annotation_processor
from dovetail.core.annotations.registry import get_registry, AnnotationRegistry


def __auto_register__():
    # 从合一定义模块触发所有处理器的自动注册
    import dovetail.core.annotations.defs  # noqa


__auto_register__()