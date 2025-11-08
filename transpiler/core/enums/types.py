# coding=utf-8
"""
MCDL 转译器类型系统枚举模块

此模块包含构成 MCDL 类型系统骨干的所有类型相关枚举，
包括数据类型、结构类型、值类别和类相关类型等。
"""
from transpiler.utils.safe_enum import SafeEnum


class FunctionType(SafeEnum):
    """
    MCDL 中不同类别可调用函数的枚举

    使用场景：
    - 符号解析器：用于函数分类
    - 插件加载器：用于库函数识别
    - 调用栈管理器：用于分发逻辑

    Attributes:
        FUNCTION: 用户定义的 MCDL 函数
        LIBRARY: 从 MCDL 库加载的函数
        BUILTIN: 转译器内置函数
        METHOD: 类方法函数
    """
    FUNCTION = "function"  # 用户定义的 MCDL 函数
    LIBRARY = "library"  # 从 MCDL 库加载的函数
    BUILTIN = "built-in"  # 后端内建函数
    METHOD = "method"  # 类方法函数


class DataTypeBase:
    """
    类型基类
    """

    def get_name(self) -> str:
        """
        获取类型名称
        """

    def is_subclass_of(self, other) -> bool:
        """
        自身是否是other的子类
        """
        return self is other


class DataType(DataTypeBase, SafeEnum):
    """
    MCDL 中表示变量存储类型的基础数据类型

    这些类型对应于可以存储在 Minecraft 命令系统和
    计分板操作中的基本数据表示。

    Type Hierarchy:
        - BOOLEAN 是 INT 的子类型（可以强制转换）
        - NULL 是特殊类型，不能显式声明

    Attributes:
        INT: 整数类型，对应 Minecraft 计分板分数
        STRING: 字符串类型，用于命名和文本处理
        BOOLEAN: 布尔类型，内部表示为 0/1 整数
        NULL: 空值类型，表示未初始化或无效值
    """
    INT = 'int'
    STRING = 'string'
    BOOLEAN = 'boolean'
    NULL = 'null'  # 特殊类型，不可为声明变量时的类型

    # Function = 'function'  # 特殊类型，待使用
    # Type = 'type'  # 特殊类型，待使用

    def get_name(self) -> str:
        """获取类型的显示名称"""
        return self.name

    def is_subclass_of(self, other):
        """检查当前类型是否为另一类型的子类型"""
        if self is other:
            return True
        if self == DataType.BOOLEAN and other == DataType.INT:
            return True
        return False

    def __repr__(self):
        return self.name


class StructureType(SafeEnum):
    """
    MCDL 中表示不同作用域上下文的结构类型

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
        LOOP: 循环体作用域
        LOOP_CHECK: 循环条件检查作用域
        LOOP_BODY: 循环体执行作用域
        INTERFACE: 接口定义作用域
        BLOCK: 代码块作用域
        CONDITIONAL: 条件语句作用域
    """
    GLOBAL = "global"
    FUNCTION = "function"
    CLASS = "class"
    LOOP = "loop"
    LOOP_CHECK = "loop_check"
    LOOP_BODY = "loop_body"
    INTERFACE = 'interface'
    BLOCK = 'block'
    CONDITIONAL = "conditional"


class ValueType(SafeEnum):
    """
    表示表达式语义性质的值类别

    由 IR 构建器使用，用于确定在代码生成和
    优化遍历过程中应如何处理值。

    Attributes:
        LITERAL: 字面量值，编译时已知
        CONSTANT: 常量值，不可修改
        VARIABLE: 变量值，运行时确定
        FUNCTION: 函数值，可调用对象
        CLASS: 类值，类型对象
    """
    LITERAL = "literal"  # 字面量
    CONSTANT = "constant"
    VARIABLE = "variable"  # 变量
    FUNCTION = "function"  # 函数
    CLASS = "class"


class VariableType(SafeEnum):
    """
    不同变量声明上下文的变量类别

    影响生成的 Minecraft 命令中的存储分配和生命周期管理。

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
    MCDL 面向对象系统中的类声明类型

    用于在继承检查和方法解析过程中区分
    具体类和接口契约。

    Attributes:
        CLASS: 具体类，可实例化
        INTERFACE: 接口类，定义契约
    """
    CLASS = "class"
    INTERFACE = "interface"
