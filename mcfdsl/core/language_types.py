from __future__ import annotations

import warnings
from enum import Enum


class CheckedEnum(Enum):  # 基类名称建议
    def __eq__(self, other):
        if isinstance(other, Enum) and self.__class__ is not other.__class__:
            warnings.warn(
                f"Comparing different enum types: {self.__class__.__name__} vs {other.__class__.__name__}",
                UserWarning,
                stacklevel=2
            )
        return super().__eq__(other)

class TargetSelectorVariables(CheckedEnum):
    NEAREST_PLAYER = "@p"
    RANDOM_PLAYER = "@r"
    ALL_PLAYER = "@a"
    ALL_ENTITIES = "@e"
    ENTITY_EXECUTING_COMMAND = "@s"
    NEAREST_ENTITY = "@n"


class FunctionType(CheckedEnum):
    NORMAL = "function"
    METHOD = "method"
    CONSTRUCTOR = "constructor"


class SymbolType(CheckedEnum):
    """符号类型：标识符号的类别"""
    VARIABLE = "variable"
    CONSTANT = 'constant'
    FUNCTION = "function"
    CLASS = "class"
    INTERFACE = 'interface'
    NAMESPACE = 'namespace'

class DataType(CheckedEnum):
    """基础数据类型：表示变量的存储类型"""
    INT = 'int'
    STRING = 'string'
    FSTRING = 'fstring' # 特殊类型，将在编译时改为STRING
    BOOLEAN = 'boolean'
    VOID = 'void'
    SELECTOR = 'selector'
    ANY = 'any'  # 特殊类型，用于类型推断


class StructureType(CheckedEnum):
    """结构类型：表示作用域类型"""
    GLOBAL = "global"
    FUNCTION = "function"
    CLASS = "class"
    LOOP = "loop"
    INTERFACE = 'interface'
    BLOCK = 'block'



class ValueType(CheckedEnum):
    """值类型：表示值的类别"""
    LITERAL = "literal"  # 字面量
    VARIABLE = "variable"  # 变量引用
    # COMPOSITE = "composite"  # 复合表达式结果
    # FUNCTION = "function"  # 函数返回值
    ERROR = "error"  #  错误
    OTHER = 'other'