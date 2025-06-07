from __future__ import annotations

from enum import Enum


class ScopeType(Enum):
    GLOBAL = "global"
    FUNCTION = "function"
    CLASS = "class"
    LOOP = "loop"
    #CONDITIONAL_BLOCK = "conditional_block"
    INTERFACE = 'interface'


class FunctionType(Enum):
    NORMAL = "function"
    METHOD = "method"
    CONSTRUCTOR = "constructor"


class SymbolType(Enum):
    VARIABLE = "variable"
    CONST = 'const'
    FUNCTION = "function"
    CLASS = "class"
    INTERFACE = 'interface'


class BaseType(Enum):
    TYPE_INT = 'int'
    TYPE_STRING = 'string'
    TYPE_FSTRING = 'fstring'
    TYPE_BOOLEAN = 'boolean'
    TYPE_VOID = 'void'
    TYPE_ANY = 'any'
    TYPE_SELECTOR = 'Selector'


class Type(Enum):
    TYPE = 'type'
    TYPE_ANY = 'any'

    # 仅字面量或常量为以下几个参数，其他均为TYPE_VARIABLE，boolean拟成0/1，string/fstring仅限编译期使用，void仅编译器模拟
    TYPE_INT = 'int'  # 存储具体数值
    TYPE_STRING = 'string'  # 存储字符串
    TYPE_FSTRING = 'fstring'  # 该类型将会在解析后转为string
    TYPE_BOOLEAN = 'boolean'  # 存储bool
    TYPE_VOID = 'void'  # 存储None

    TYPE_SELECTOR = 'Selector'  # 特殊常量，存储选择器

    TYPE_VARIABLE = "variable"  # 变量，存储变量的unique_name
    TYPE_INTERFACE = 'interface'
    TYPE_FUNCTION = 'function'
    TYPE_CLASS = 'class'
    TYPE_BLOCK = 'block'
    TYPE_IMPORT = 'import'
    TYPE_ERROR = 'error'
