# coding=utf-8
from __future__ import annotations

from typing import Any, Optional

from dovetail.core.annotations.base import AnnotationProcessor
from dovetail.core.annotations.category import AnnotationCategory
from dovetail.core.annotations.registry import get_registry
from dovetail.core.annotations.spec import Annotation, inject_annotation_spec


def annotation_processor(
        cls: type[AnnotationProcessor] = None,
        *,
        name: str | None = None,
        category: AnnotationCategory = AnnotationCategory.METADATA,
        params: Optional[dict[str, Any]] = None,
):
    """
    装饰器：自动注册注解处理器到全局注册表，同时注册 spec 声明。

    支持两种用法：

    1. 无参数（向后兼容）：
        @annotation_processor
        class MyProcessor(AnnotationProcessor):
            annotation_name = "foo"
            ...

    2. 带参数（合一模式）：
        @annotation_processor(name="foo", category=AnnotationCategory.LIFECYCLE, params={"x": 1})
        class MyProcessor(AnnotationProcessor):
            ...
    """

    def wrap(cls: type[AnnotationProcessor]) -> type[AnnotationProcessor]:
        # 如果装饰器参数提供了 name/category/params，写入类属性
        if name is not None:
            cls.annotation_name = name
        if category is not None:
            cls.category = category
        if params is not None:
            cls._spec_params = params  # 存到类上供 spec 注册使用

        # 注册处理器
        instance = cls()
        get_registry().register(instance)

        # 自动注册 spec 声明
        ann = Annotation(
            name=instance.annotation_name,
            params=getattr(cls, '_spec_params', None),
            category=instance.category,
        )
        inject_annotation_spec(ann)

        return cls

    # 无参数调用：@annotation_processor
    if cls is not None:
        return wrap(cls)

    # 带参数调用：@annotation_processor(name="foo", ...)
    return wrap