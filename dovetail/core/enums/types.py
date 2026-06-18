# coding=utf-8
"""
转译器类型系统枚举模块

此模块包含构成类型系统骨干的所有类型相关枚举，
包括数据类型、结构类型、值类别和类相关类型等。
"""
from __future__ import annotations

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
        EXTERN: 从外部导入方法
    """
    FUNCTION = "function"
    FUNCTION_UNIMPLEMENTED = "function-unimplemented"
    LIBRARY = "library"
    BUILTIN = "built-in"
    METHOD = "method"
    EXTERN = "extern"


class StructureType(SafeEnum):
    """
    表示不同作用域上下文的结构类型

    由作用域管理器使用，用于在不同代码结构中维护
    正确的变量可见性。

    Scope Nesting Rules:
        - GLOBAL: 顶级作用域，全局可见，通常唯一
        - FUNCTION: 函数局部作用域
        - CLASS: 类成员作用域
        - LOOP/CONDITION: 块级作用域

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
        RETURN: 函数返回值变量(不被优化删除)
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
