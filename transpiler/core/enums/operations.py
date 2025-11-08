# coding=utf-8
"""
MCDL 转译器操作符枚举模块

此模块包含 MCDL 语言中所有运算操作符的枚举定义，
用于语法解析、表达式求值和代码生成。
"""
from transpiler.utils.safe_enum import SafeEnum


class UnaryOps(SafeEnum):
    """
    一元运算操作符枚举

    定义可以作用于单个操作数的运算符，主要用于
    表达式解析器和 IR 指令生成。

    Attributes:
        NEG: 数值取负运算 (-a)
        NOT: 逻辑非运算 (!bool)
        BIT_NOT: 按位取反运算 (~int)

    Note:
        由于正常情况 BIT_NOT 不会被使用，因此部分后端不会实现该运算符
    """
    NEG = '-'  # 数值取负: -a
    NOT = '!'  # 逻辑非: !bool
    BIT_NOT = '~'  # 按位取反: ~int


class BinaryOps(SafeEnum):
    """
    二元运算操作符枚举

    定义可以作用于两个操作数的运算符，按功能分为
    算术运算、位运算和特殊功能三类。

    Operator Categories:
        算术运算: ADD, SUB, MUL, DIV, MOD

        位运算: BIT_AND, BIT_OR, BIT_XOR, SHL, SHR

        特殊功能: MIN, MAX

    Attributes:
        ADD: 加法运算 (a + b)
        SUB: 减法运算 (a - b)
        MUL: 乘法运算 (a * b)
        DIV: 除法运算 (a / b)
        MOD: 取模运算 (a % b)
        BIT_AND: 按位与运算 (a & b)
        BIT_OR: 按位或运算 (a | b)
        BIT_XOR: 按位异或运算 (a ^ b)
        SHL: 左移位运算 (a << b)
        SHR: 右移位运算 (a >> b)
        MIN: 最小值函数 min(a, b)
        MAX: 最大值函数 max(a, b)

    Note:
        由于正常情况 BIT_AND BIT_OR BIT_XOR SHL SHR 不会被使用，因此部分后端不会实现该运算符
    """
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
    """
    比较运算操作符枚举

    定义用于比较两个值关系的运算符，结果为布尔类型。

    Attributes:
        EQ: 等于比较 (a == b)
        NE: 不等于比较 (a != b)
        LT: 小于比较 (a < b)
        LE: 小于等于比较 (a <= b)
        GT: 大于比较 (a > b)
        GE: 大于等于比较 (a >= b)
    """
    EQ = '=='  # 等于: a == b
    NE = '!='  # 不等于: a != b
    LT = '<'  # 小于: a < b
    LE = '<='  # 小于等于: a <= b
    GT = '>'  # 大于: a > b
    GE = '>='  # 大于等于: a >= b
