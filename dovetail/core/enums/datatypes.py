# coding=utf-8
from __future__ import annotations


from dovetail.utils.safe_enum import SafeEnum


class DataTypeBase:
    """
    类型基类

    See Also:
        此类不应该被实例化
    """


    def get_name(self) -> str:
        """
        获取类型名称

        Returns:
            str: 类型名称
        """

    def is_subclass_of(self, other: DataTypeBase) -> bool:
        """
        自身是否是other的子类

        Args:
            other: 其他类型

        Returns:
            是否是other的子类
        """
        return self is other

    def is_definable(self) -> bool:
        """
        自身是否可在变量定义时使用

        Returns:
            当自身可在变量定义使用时返回True

        """
        return True

    def __repr__(self):
        return self.get_name()


class PrimitiveDataType(DataTypeBase, SafeEnum):
    """
    表示变量存储类型的基础数据类型

    这些类型对应于可以存储在 Minecraft 命令系统和
    计分板操作中的基本数据表示。

    Type Hierarchy:
        - BOOLEAN 是 INT 的子类型（可以强制转换）
        - NULL_TYPE、UNDEFINED 是特殊类型，不能显式声明

    Attributes:
        INT: 整数类型
        STRING: 字符串类型
        BOOLEAN: 布尔类型
        NULL_TYPE: 句柄null的独有类型，不可作为其他值的类型
        VOID: 表示空
        UNDEFINED: 特殊类型，仅编译错误时使用
        FUNCTION: 函数句柄，表示一个函数
    """
    INT = 'int'
    STRING = 'string'
    BOOLEAN = 'boolean'
    NULL_TYPE = 'null'  # 特殊类型，不可作为变量的类型
    VOID = 'void'
    UNDEFINED = 'undefined'  # 特殊类型，仅编译期发生错误时使用，其他时候该类型不应被编译
    FUNCTION = 'function'

    # TYPE = 'type'  # 特殊类型，待使用

    def get_name(self) -> str:
        """获取类型的显示名称"""
        return str(self.value)

    def is_subclass_of(self, other):
        """检查当前类型是否为另一类型的子类型"""
        if self is other:
            return True
        if self == PrimitiveDataType.BOOLEAN and other == PrimitiveDataType.INT:
            return True
        return False

    def is_definable(self) -> bool:
        return self not in (PrimitiveDataType.UNDEFINED, PrimitiveDataType.NULL_TYPE, PrimitiveDataType.VOID)

    @staticmethod
    def from_literal(value: int | str | bool | float | None):
        if isinstance(value, bool):
            return PrimitiveDataType.BOOLEAN
        elif isinstance(value, int):
            return PrimitiveDataType.INT
        elif isinstance(value, str):
            return PrimitiveDataType.STRING
        elif value is None:
            return PrimitiveDataType.NULL_TYPE
        else:
            raise TypeError(f"Unsupported literal type: {type(value)}")

    def __repr__(self):
        return self.get_name()


class ListType(DataTypeBase):

    def __init__(self, dtype: DataTypeBase):
        """
        构造ListType

        Args:
            dtype(DataTypeBase): 存储数据的类型
        """
        self.dtype = dtype

    def get_name(self) -> str:
        return f"list<{self.dtype!r}>"


class ArrayType(DataTypeBase):

    def __init__(self, dtype: DataTypeBase):
        """
        构造ArrayType

        Args:
            dtype(DataTypeBase): 存储数据的类型
        """
        self.dtype = dtype

    def get_name(self) -> str:
        return f"array<{self.dtype!r}>"


class DictType(DataTypeBase):
    def __init__(self, key_dtype: DataTypeBase, value_dtype: DataTypeBase):
        """
        构造DictType

        Args:
            key_dtype: 键的类型
            value_dtype: 值的类型
        """
        self.key_dtype = key_dtype
        self.value_dtype = value_dtype

    def get_name(self) -> str:
        return f"dict<{self.key_dtype!r}, {self.value_dtype!r}>"


class UnionType(DataTypeBase):
    """
    一种特殊类型，仅用于前端使用

    可以同时包含多种类型和复合类型，不应该被声明或在最终代码中存在
    """

    def __init__(self, *types: DataTypeBase | type):
        self.types = types

    def is_definable(self) -> bool:
        return False

    def __repr__(self):
        return " | ".join(map(str, self.types))

BUILT_IN_COMPOSITE_TYPES = ArrayType | DictType | ListType
