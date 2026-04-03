# coding=utf-8
"""
转译器类型系统枚举模块

此模块包含构成类型系统骨干的所有类型相关枚举，
包括数据类型、结构类型、值类别和类相关类型等。
"""
from __future__ import annotations

from functools import reduce

from dovetail.utils.safe_enum import SafeEnum


class FunctionType(SafeEnum):
    """
    不同类别可调用函数的枚举

    使用场景：
    - 符号解析器：用于函数分类
    - 插件加载器：用于库函数识别
    - 调用栈管理器：用于分发逻辑

    Attributes:
        FUNCTION: 用户定义的函数
        FUNCTION_UNIMPLEMENTED: 声明但未实现的函数
        LIBRARY: 从库加载的函数
        BUILTIN: 转译器内置函数
        METHOD: 类方法函数
    """
    FUNCTION = "function"  # 用户定义的函数
    FUNCTION_UNIMPLEMENTED = "function-unimplemented"  # 声明但未实现的函数
    LIBRARY = "library"  # 从库加载的函数
    BUILTIN = "built-in"  # 后端内建函数
    METHOD = "method"  # 类方法函数


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


class DataType(DataTypeBase, SafeEnum):
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
    NULL_TYPE = 'null'  # 特殊类型，不可为变量的类型
    VOID = 'void'
    UNDEFINED = 'undefined'  # 特殊类型，仅编译期发生错误时使用，其他时候该类型不应被编译
    FUNCTION = 'function'

    # Type = 'type'  # 特殊类型，待使用

    def get_name(self) -> str:
        """获取类型的显示名称"""
        return self.value

    def is_subclass_of(self, other):
        """检查当前类型是否为另一类型的子类型"""
        if self is other:
            return True
        if self == DataType.BOOLEAN and other == DataType.INT:
            return True
        return False

    def is_definable(self) -> bool:
        return self not in (DataType.UNDEFINED, DataType.NULL_TYPE)

    @staticmethod
    def from_literal(value: int | str | bool | float | None):
        if isinstance(value, bool):
            return DataType.BOOLEAN
        elif isinstance(value, int):
            return DataType.INT
        elif isinstance(value, str):
            return DataType.STRING
        elif value is None:
            return DataType.NULL_TYPE
        else:
            raise TypeError(f"Unsupported literal type: {type(value)}")


class Array(DataTypeBase):
    """
    表示数组存储类型的特殊数据类型

    Attributes:
        dtype: 所存储的数据的类型
        size: 数组大小，当为-1时代表无限大
    """

    def __init__(self, dtype: DataType | DataTypeBase, size: list[int]):
        self.dtype = dtype
        self.size = size

    def get_name(self) -> str:
        return f"{repr(self.dtype)}{''.join(f'[{size}]' for size in self.size)}"

    def get_all_of_size(self) -> int:
        """
        获取数组总大小

        Returns:
            int: 该数组所有维度的大小的总乘积
        """
        return reduce(lambda x, y: x * y, self.size)

    def get_size(self) -> list[int]:
        """
        获得数组大小列表

        Returns:
            list[int]: 数组大小列表
        """
        return self.size

    def is_subclass_of(self, other):
        if self is other:
            return True
        return False


class StructureType(SafeEnum):
    """
    表示不同作用域上下文的结构类型

    由作用域管理器使用，用于在不同代码结构中维护
    正确的变量可见性。

    Scope Nesting Rules:
        - GLOBAL: 顶级作用域，全局可见，通常唯一
        - FUNCTION: 函数局部作用域
        - CLASS: 类成员作用域
        - LOOP/CONDITIONAL: 块级作用域

    Attributes:
        GLOBAL: 全局作用域
        FUNCTION: 函数作用域
        CLASS: 类定义作用域
        LOOP_CHECK: 循环条件检查作用域
        LOOP_BODY: 循环体执行作用域
        INTERFACE: 接口定义作用域
        CONDITIONAL: 条件语句作用域
    """
    GLOBAL = "global"
    FUNCTION = "function"
    CLASS = "class"
    LOOP_CHECK = "loop_check"
    LOOP_BODY = "loop_body"
    INTERFACE = "interface"
    CONDITIONAL = "conditional"


class ValueType(SafeEnum):
    """
    表示表达式语义性质的值类别

    由 IR 构建器使用，用于确定在代码生成和
    优化遍历过程中应如何处理值。

    Attributes:
        LITERAL: 字面量值，编译时已知
        VARIABLE: 变量
        FUNCTION: 函数值，可调用对象
        CLASS: 类值，类型对象
    """
    LITERAL = "literal"  # 字面量
    VARIABLE = "variable"  # 变量
    FUNCTION = "function"  # 函数
    CLASS = "class"


class VariableType(SafeEnum):
    """
    不同变量声明上下文的变量类别

    影响生成的 Minecraft 命令中的生命周期管理。

    Attributes:
        PARAMETER: 函数参数变量
        COMMON: 普通局部变量
        RETURN: 函数返回值变量(不被优化)
    """
    PARAMETER = "parameter"
    COMMON = "common"
    RETURN = "return"


class ClassType(SafeEnum):
    """
    面向对象系统中的类声明类型

    用于在继承检查和方法解析过程中区分
    具体类和接口契约。

    Attributes:
        CLASS: 具体类，可实例化
        ENUM: 枚举类，编译器时将被内联
    """
    CLASS = "class"
    ENUM = "enum"


class AnnotationCategory(SafeEnum):
    """
    注解系统声明类型

    用于区分注解类型并根据注解类型在不同时机处理

    Attributes:
        LIFECYCLE: 控制函数执行时机
        VISIBILITY: 控制可见性和优化
        OPTIMIZATION: 控制优化行为
        LINKAGE: 控制后端链接接口指令的生成
        CONDITIONAL: 条件编译
        METADATA: 元数据注解，不影响编译逻辑
    """
    # 核心语义注解 - 影响代码生成和执行
    LIFECYCLE = "lifecycle"  # @init, @tick - 控制函数执行时机
    VISIBILITY = "visibility"  # @internal - 控制可见性和优化
    OPTIMIZATION = "optimization"  # @noinline - 控制优化行为
    LINKAGE = "linkage"  # @export, @extern - 控制后端链接接口指令的生成

    # 条件编译注解 - 在AST阶段处理
    CONDITIONAL = "conditional"  # @target, @version - 条件编译

    # 元数据注解 - 不影响编译逻辑
    METADATA = "metadata"  # @doc, @author, @since, @deprecated
