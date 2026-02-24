# coding=utf-8
from typing import Any, Optional

from attrs import define

from .base import Symbol
from ..enums import DataType
from ..enums.types import AnnotationCategory, DataTypeBase


@define(slots=True,frozen=True)
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
            DataType.UNDEFINED
        """

        return DataType.UNDEFINED