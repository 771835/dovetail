# coding=utf-8
from transpiler.core.safe_enum import SafeEnum

__all__ = [
    "ValueType",
    "VariableType",
    "FunctionType",
    "ClassType",
    "StructureType",
    "BinaryOps",
    "CompareOps",
    "UnaryOps",
    "DataType"
]


class FunctionType(SafeEnum):
    FUNCTION = "function"
    LIBRARY = "library"
    BUILTIN = "built-in"
    METHOD = "method"


class UnaryOps(SafeEnum):
    """一元运算操作符枚举"""
    NEG = '-'  # 数值取负: -a
    NOT = '!'  # 逻辑非: !bool
    BIT_NOT = '~'  # 按位取反: ~int


class BinaryOps(SafeEnum):
    """二元运算操作符枚举"""
    # 算术运算
    ADD = '+'  # 加: a+b
    SUB = '-'  # 减: a-b
    MUL = '*'  # 乘: a*b
    DIV = '/'  # 除: a/b
    MOD = '%'  # 取模: a%b

    # 位运算
    BIT_AND = '&'  # 按位与: a&b
    BIT_OR = '|'  # 按位或: a|b
    BIT_XOR = '^'  # 按位异或: a^b
    SHL = '<<'  # 左移: a<<b
    SHR = '>>'  # 右移 (逻辑): a>>b

    # 特殊功能
    MIN = 'min'  # 最小值: min(a,b)
    MAX = 'max'  # 最大值: max(a,b)


class CompareOps(SafeEnum):
    """比较运算操作符枚举"""
    EQ = '=='  # 等于: a == b
    NE = '!='  # 不等于: a != b
    LT = '<'  # 小于: a < b
    LE = '<='  # 小于等于: a <= b
    GT = '>'  # 大于: a > b
    GE = '>='  # 大于等于: a >= b


class DataTypeBase:
    def get_name(self) -> str:
        ...


class DataType(DataTypeBase, SafeEnum):
    """基础数据类型：表示变量的存储类型"""
    INT = 'int'
    STRING = 'string'
    BOOLEAN = 'boolean'
    NULL = 'null'  # 特殊类型，不可为声明变量时的类型
    Function = 'function'

    def get_name(self) -> str:
        return self.name


class StructureType(SafeEnum):
    """结构类型：表示作用域类型"""
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
    """值类型：表示值的类别"""
    LITERAL = "literal"  # 字面量
    CONSTANT = "constant"
    VARIABLE = "variable"  # 变量
    FUNCTION = "function"  # 函数
    CLASS = "class"


class VariableType(SafeEnum):
    """变量类型"""
    PARAMETER = "parameter"
    COMMON = "common"
    RETURN = "return"


class ClassType(SafeEnum):
    """类类型"""
    CLASS = "class"
    INTERFACE = "interface"
