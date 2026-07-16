# coding=utf-8
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, TYPE_CHECKING

from dovetail.core.enums.datatypes import DataTypeBase

if TYPE_CHECKING:
    from dovetail.core.symbols import Function
    from dovetail.core.annotations.base import AnnotationAttachment


class Symbol(ABC):
    @abstractmethod
    def get_name(self) -> str:
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
        from dovetail.core.enums import PrimitiveDataType
        return PrimitiveDataType.UNDEFINED


class Annotatable(ABC):
    @property
    @abstractmethod
    def annotations(self) -> dict[str, "AnnotationAttachment"]:
        """强制子类提供注解存储"""
        ...

    def has_annotation(self, name: str) -> bool:
        return name in self.annotations

    def get_flags(self, name: str) -> set[str]:
        a = self.annotations.get(name)
        return a.flags if a else set()

    def get_metadata(self, name: str) -> dict[str, Any]:
        a = self.annotations.get(name)
        return a.metadata if a else {}

    def all_flags(self) -> set[str]:
        """汇总所有注解的 flags，优化器和后端统一入口"""
        result: set[str] = set()
        for a in self.annotations.values():
            result |= a.flags
        return result

    def all_metadata(self) -> dict[str, Any]:
        """汇总所有注解的 metadata"""
        result: dict[str, Any] = {}
        for a in self.annotations.values():
            result |= a.metadata
        return result


class MethodHost(ABC):

    @property
    @abstractmethod
    def methods(self) -> dict[str, Function]:
        """强制子类提供方法存储"""
        ...

    def get_method(self, name: str) -> Function | None:
        return self.methods.get(name)

    def has_method(self, name: str) -> bool:
        return name in self.methods
