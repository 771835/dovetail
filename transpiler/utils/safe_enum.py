# coding=utf-8
"""
增强型安全枚举实现 (Enhanced Safe Enum Implementation)
- 比较不相同的类型枚举时发出警告
- 提供值验证工具方法
"""

from __future__ import annotations

import warnings
from enum import Enum
from typing import Any, Callable


class SafeEnum(Enum):
    """
    类型安全的枚举基类，提供以下增强功能：

    主要特性：
    1. 类型检查：比较不相同的枚举类型时自动警告
    2. 值验证：检查值是否存在于枚举中

    使用示例：
    class Color(SafeEnum):
        RED = "red"
        GREEN = "green"
    """

    def __eq__(self, other: Any) -> bool:
        """
        重载等于运算符，添加类型安全检查

        Args:
            other (Any): 要比较的对象

        Returns:
            bool: 比较结果
        """
        return self._type_checked_compare(other, super().__eq__)

    def __ne__(self, other: Any) -> bool:
        """
        重载不等于运算符，添加类型安全检查

        Args:
            other (Any): 要比较的对象

        Returns:
            bool: 比较结果
        """
        return self._type_checked_compare(other, super().__ne__)

    def _type_checked_compare(self, other: Any,
                              compare_func: Callable) -> bool:
        """
        执行类型检查并调用比较函数

        Args:
            other (Any): 比较对象
            compare_func (Callable): 原始比较函数

        Returns:
            bool: 比较结果布尔值
        """
        if isinstance(other, Enum) and not self._is_same_enum_type(other):
            self._handle_type_mismatch(other)
        return compare_func(other)

    def _is_same_enum_type(self, other: Enum) -> bool:
        """
        检查是否为相同枚举类型或继承的类型

        Args:
            other (Enum): 要比较的枚举对象

        Returns:
            bool: 如果是相同类型返回True，否则返回False
        """
        return (
            isinstance(other, self.__class__)
        )

    def _handle_type_mismatch(self, other: Enum) -> None:
        """
        处理类型不匹配情况

        Args:
            other (Enum): 类型不匹配的枚举对象

        Returns:
            None: 无返回值
        """
        err_msg = (
            f"Enum type mismatch: Comparing {self.__class__.__name__} "
            f"with {other.__class__.__name__}"
        )
        warnings.warn(err_msg, UserWarning, stacklevel=3)

    @classmethod
    def is_valid_value(cls, value: Any) -> bool:
        """
        检查值是否存在于当前枚举中

        Args:
            value (Any): 要检查的值

        Returns:
            bool: 值是否有效
        """
        if isinstance(value, str):
            return any(value.casefold() == v.casefold() for v in cls.values())
        return value in cls.values()

    @classmethod
    def values(cls) -> tuple:
        """
        获取枚举所有值的元组

        Returns:
            tuple: 包含所有枚举值的元组
        """
        return tuple(member.value for member in cls)

    @classmethod
    def get_by_value(cls, value: Any) -> SafeEnum:
        """
        通过值获取枚举成员

        Args:
            value (Any): 枚举值

        Returns:
            SafeEnum: 对应的枚举成员

        Raises:
            ValueError: 值不存在时抛出
        """
        if isinstance(value, str):
            for member in cls:
                if member.value.casefold() == value.casefold():
                    return member
        return cls(value)  # 自动触发标准枚举的ValueError

    @classmethod
    def names(cls) -> tuple:
        """
        获取枚举所有名称的元组

        Returns:
            tuple: 包含所有枚举名称的元组
        """
        return tuple(member.name for member in cls)

    def __hash__(self) -> int:
        """
        返回枚举成员的哈希值

        Returns:
            int: 基于枚举值的哈希值
        """
        return hash(self.value)
