# coding=utf-8
from typing import Any, Optional

from attrs import define

from .base import Symbol
from ..enums import PrimitiveDataType
from ..enums.types import AnnotationCategory, DataTypeBase


@define(slots=True, hash=False, frozen=True, repr=False)
class Annotation(Symbol):
    name: str  # 注解名称
    params: Optional[dict[str, Any]]  # 参数字典
    category: AnnotationCategory  # 分类枚举

    def get_name(self) -> str:
        return self.name

    def get_dtype(self) -> DataTypeBase:
        """
        类型注解不作为数据存储，因此不返回类型

        Returns:
            PrimitiveDataType.UNDEFINED
        """

        return PrimitiveDataType.UNDEFINED

    def __repr__(self):
        return f"@{self.name}({','.join(self.params.keys())})"

    def __hash__(self):
        """
        哈希注解对象

        Returns:
            int: 哈希值
        """
        if self.params is None:
            return hash((self.name, self.category))
        return hash((self.name, frozenset(self.params.items()), self.category))
