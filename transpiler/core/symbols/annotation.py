# coding=utf-8
from typing import Any

from attrs import define

from .base import Symbol
from ..enums.types import AnnotationCategory


@define(slots=True)
class Annotation(Symbol):
    name: str  # 注解名称
    params: dict[str, Any]  # 参数字典
    category: AnnotationCategory  # 分类枚举

    def get_name(self) -> str:
        return self.name
