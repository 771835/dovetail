# coding=utf-8
from dovetail.core.annotations.base import AnnotationProcessor, AnnotationContext
from dovetail.core.annotations.decorator import annotation_processor
from dovetail.core.annotations.registry import get_registry, AnnotationRegistry


def __auto_register__():
    # 触发所有处理器的自动注册
    import dovetail.core.annotations.handlers.condition  # noqa
    import dovetail.core.annotations.handlers.lifecycle  # noqa
    import dovetail.core.annotations.handlers.linkage  # noqa
    import dovetail.core.annotations.handlers.metadata  # noqa
    import dovetail.core.annotations.handlers.visibility  # noqa


__auto_register__()
