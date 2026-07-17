# coding=utf-8
from __future__ import annotations

import functools
from typing import TypeVar, Generic

from attrs import define

from . import Class
from .base import Symbol
from .literal import Literal
from .variable import Variable
from ..config import FAST_MODE
from ..enums import PrimitiveDataType
from ..enums.datatypes import DataTypeBase
from ..enums.types import ValueType, VariableType
from ...utils.logger import get_logger

T = TypeVar('T', bound=Symbol)
logger = get_logger(__name__)


@define(slots=True, hash=True, repr=False, frozen=True)
class Reference(Symbol, Generic[T]):
    """
    引用容器

    引用其他符号对象并提供统一的使用接口

    Attributes:
        value (T): 被引用的对象
    """
    value: T

    if not FAST_MODE:
        def __attrs_post_init__(self):
            if isinstance(self.value, Reference):
                logger.error(f"多重引用: {self.value}")

    @property
    def value_type(self) -> ValueType:
        from . import Class, Function
        if isinstance(self.value, Function):
            return ValueType.FUNCTION
        elif isinstance(self.value, Class):
            return ValueType.CLASS
        elif isinstance(self.value, Literal):
            return ValueType.LITERAL
        else:
            return ValueType.VARIABLE

    @property
    def dtype(self) -> DataTypeBase:
        return self.get_dtype()

    def get_name(self) -> str:
        """
        返回所引用的符号的名称

        Returns:
            str: 所引用符号的名称，当为字面量时返回其所存储的数据的展示名形式
        """
        return self.value.get_name()

    def get_dtype(self) -> DataTypeBase:
        return self.value.get_dtype()

    @classmethod
    def literal(cls: type[Reference[Literal]], value: bool | int | str | None) -> Reference[Literal]:
        return cls(Literal(PrimitiveDataType.from_literal(value), value))

    @classmethod
    def variable(cls: type[Reference[Variable]], var_name: str, dtype: PrimitiveDataType,
                 var_type: VariableType = VariableType.COMMON,
                 mutable: bool = True) -> Reference[Variable]:
        return cls(Variable(var_name, dtype, var_type, mutable))

    def is_literal(self) -> bool:
        return self.value_type == ValueType.LITERAL

    def get_display_value(self) -> str:
        from . import Literal
        if self.is_literal():
            assert isinstance(self.value, Literal)
            return repr(self.value.value)
        else:
            return self.get_name()

    @classmethod
    @functools.lru_cache(maxsize=1)
    def void(cls) -> Reference[Variable]:
        """
        返回一个类型为 PrimitiveDataType.VOID 的不可声明变量

        通常用于逻辑不可达路径

        Returns:
            一个类型为 PrimitiveDataType.VOID 的不可声明变量
        """
        return cls.variable("_", PrimitiveDataType.VOID, mutable=False)

    @classmethod
    @functools.lru_cache(maxsize=1)
    def undefined(cls) -> Reference[Variable]:
        """
        返回一个类型为 PrimitiveDataType.UNDEFINED 的不可声明变量

        通常用于语义错误时填充的默认值

        Returns:
            一个类型为 PrimitiveDataType.UNDEFINED 的不可声明变量
        """
        return cls.variable("_", PrimitiveDataType.UNDEFINED, mutable=False)

    @classmethod
    @functools.lru_cache(maxsize=None)
    def default(cls, dtype: DataTypeBase) -> Reference[Literal] | None:
        """
        根据传入参数的默认值返回一个其类型的默认值

        Returns:
            当传入 int, bool, str 时返回 0, False, "" 的引用
            当传入类时返回 null 的引用
            当传入不可定义的基本类型或其他类型时返回 None
        """
        if dtype == PrimitiveDataType.INT:
            return Reference.literal(0)
        elif dtype == PrimitiveDataType.BOOLEAN:
            return Reference.literal(False)
        elif dtype == PrimitiveDataType.STRING:
            return Reference.literal("")
        elif isinstance(dtype, Class):
            return Reference.literal(None)
        else:
            return None

    def __repr__(self):
        return self.get_display_value()
