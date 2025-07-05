# coding=utf-8
from __future__ import annotations

from mcfdsl.core.safe_enum import SafeEnum


class TargetSelectorVariables(SafeEnum):
    NEAREST_PLAYER = "@p"
    RANDOM_PLAYER = "@r"
    ALL_PLAYER = "@a"
    ALL_ENTITIES = "@e"
    ENTITY_EXECUTING_COMMAND = "@s"
    NEAREST_ENTITY = "@n"


class FunctionType(SafeEnum):
    NORMAL = "function"
    METHOD = "method"
    CONSTRUCTOR = "constructor"


class SymbolType(SafeEnum):
    """符号类型：标识符号的类别"""
    VARIABLE = "variable"
    CONSTANT = 'constant'
    FUNCTION = "function"
    CLASS = "class"
    INTERFACE = 'interface'
    NAMESPACE = 'namespace'


class DataType(SafeEnum):
    """基础数据类型：表示变量的存储类型"""
    INT = 'int'
    STRING = 'string'
    FSTRING = 'fstring'  # 特殊类型，将在编译时改为STRING # TODO:改为运行时拼接
    BOOLEAN = 'boolean'
    VOID = 'void'
    NULL = 'null'  # 特殊类型，不可为声明变量时的类型
    ANY = 'any'  # 特殊类型，用于类型推断


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
    VARIABLE = "variable"  # 变量
    # COMPOSITE = "composite"  # 复合表达式结果
    FUNCTION = "function"  # 函数
    CLASS = "class"
    ERROR = "error"  # 错误
    OTHER = 'other'
