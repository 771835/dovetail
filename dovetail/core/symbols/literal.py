# coding=utf-8
from __future__ import annotations

import weakref
from typing import ClassVar

from attrs import define

from .base import Symbol
from ..enums.datatypes import DataTypeBase

_Literal_Type = str | int | bool


@define(slots=True, frozen=True)
class Literal(Symbol):
    """一个编译期已知的字面量"""
    _cache: ClassVar[
        weakref.WeakValueDictionary[tuple[DataTypeBase, _Literal_Type], Literal]] = weakref.WeakValueDictionary()

    dtype: DataTypeBase
    value: _Literal_Type

    def __new__(cls, dtype: DataTypeBase, value: _Literal_Type):
        # 尝试从缓存获取
        if value in cls._cache:
            return cls._cache[(dtype, value)]

        # 如果没有，则创建新实例
        instance = super().__new__(cls)

        # 存入弱引用缓存
        cls._cache[(dtype, value)] = instance
        return instance

    def get_name(self):
        """
        根据存储的数据返回其对应的展示名

        Returns:
            str: 存储的数据对应的展示名
        """
        return repr(self.value)

    def get_dtype(self):
        return self.dtype
