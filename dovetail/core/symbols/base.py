# coding=utf-8
from abc import ABC, abstractmethod
from typing import Optional

from dovetail.core.enums.types import DataTypeBase


class Symbol(ABC):
    @abstractmethod
    def get_name(self) -> Optional[str]:
        """
        返回符号名称
        """
        return "undefined"

    @abstractmethod
    def get_dtype(self) -> DataTypeBase:
        """
        返回数据类型

        Returns:
            本符号的数据类型，如果符号不存在或不支持数据类型则返回DataType.UNDEFINED
        """
        from dovetail.core.enums import DataType
        return DataType.UNDEFINED
