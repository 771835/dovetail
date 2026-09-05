# coding=utf-8
from __future__ import annotations

import weakref
from typing import TypeVar, Generic, ClassVar

from attrs import define, field

from .class_ import Class
from .function import Function
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
    _cache: ClassVar[weakref.WeakValueDictionary[Symbol, Reference[Symbol]]] = weakref.WeakValueDictionary()

    value: T
    _value_type: ValueType = field(init=False, repr=False)

    def __new__(cls, value: T):
        # 尝试从缓存获取
        if value in cls._cache:
            return cls._cache[value]

        if isinstance(value, Function):
            v_type = ValueType.FUNCTION
        elif isinstance(value, Class):
            v_type = ValueType.CLASS
        elif isinstance(value, Literal):
            v_type = ValueType.LITERAL
        else:
            v_type = ValueType.VARIABLE

        # 如果没有，则创建新实例
        instance = super().__new__(cls)
        object.__setattr__(instance, '_value_type', v_type)

        if not FAST_MODE and isinstance(value, Reference):
            logger.error(f"多重引用: {value}")
        # 存入弱引用缓存
        cls._cache[value] = instance
        return instance

    def __deepcopy__(self, memo):
        # 直接返回 self，不进行任何深拷贝操作
        # 因为它是不可变的，且在内存中是唯一的
        return self

    @property
    def value_type(self) -> ValueType:
        return self._value_type

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
    def literal(cls: type[Reference], value: bool | int | str) -> Reference[Literal]:
        return cls(Literal(PrimitiveDataType.from_literal(value), value))  # noqa

    @classmethod
    def variable(cls: type[Reference], var_name: str, dtype: PrimitiveDataType,
                 var_type: VariableType = VariableType.COMMON,
                 mutable: bool = True) -> Reference[Variable]:
        return cls(Variable(var_name, dtype, var_type, mutable))  # noqa

    def is_literal(self) -> bool:
        return isinstance(self.value, Literal)

    def get_display_value(self) -> str:
        from . import Literal
        if self.is_literal():
            assert isinstance(self.value, Literal)
            return repr(self.value.value)
        else:
            return self.get_name()

    @classmethod
    def null(cls) -> Reference[Variable]:
        """
        返回一个类型为 PrimitiveDataType.NULLTYPE 的句柄

        通常用于逻辑不可达路径

        Returns:
            一个类型为 PrimitiveDataType.NULLTYPE 的句柄
        """
        return NULL

    @classmethod
    def void(cls) -> Reference[Variable]:
        """
        返回一个类型为 PrimitiveDataType.VOID 的不可声明变量

        通常用于逻辑不可达路径

        Returns:
            一个类型为 PrimitiveDataType.VOID 的不可声明变量
        """
        return VOID

    @classmethod
    def undefined(cls) -> Reference[Variable]:
        """
        返回一个类型为 PrimitiveDataType.UNDEFINED 的不可声明变量

        通常用于语义错误时填充的默认值

        Returns:
            一个类型为 PrimitiveDataType.UNDEFINED 的不可声明变量
        """
        return UNDEFINED

    @classmethod
    def default(cls, dtype: DataTypeBase) -> Reference[Literal | Variable] | None:
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
            return Reference.null()
        else:
            return None

    def __repr__(self):
        return self.get_display_value()


NULL = Reference.variable("null", PrimitiveDataType.NULL_TYPE, mutable=False)
VOID = Reference.variable("_", PrimitiveDataType.VOID, mutable=False)
UNDEFINED = Reference.variable("_", PrimitiveDataType.UNDEFINED, mutable=False)