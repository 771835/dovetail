# coding=utf-8
"""
注解声明规范（纯声明，不含逻辑）

_specs 字典不再手写，由 @annotation_processor 装饰器在注册处理器时自动填充。
仍保留 get_annotation_spec / inject_annotation_spec 供外部查询和插件注入。
"""
from typing import Optional, Any

from attrs import define

from dovetail.core.annotations.category import AnnotationCategory


@define(slots=True, hash=False, repr=False)
class Annotation:
    name: str
    params: Optional[dict[str, Any]]
    category: AnnotationCategory

    def __repr__(self):
        return f"@{self.name}({','.join(self.params.keys()) if self.params else ''})"

    def __hash__(self):
        if self.params is None:
            return hash((self.name, self.category))
        return hash((self.name, frozenset(self.params.items()), self.category))


# 由 @annotation_processor 装饰器自动填充，不再手写
_specs: dict[str, Annotation] = {}


def get_annotation_spec(name: str) -> Annotation | None:
    return _specs.get(name)


def inject_annotation_spec(annotation: Annotation):
    """插件注入自定义注解声明，或由 @annotation_processor 自动调用"""
    _specs[annotation.name] = annotation