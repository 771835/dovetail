# coding=utf-8
"""
库函数声明工厂

提供装饰器驱动的库声明方式。

用法:
    class Math(LibraryBase):

        INT_MAX = lib_var(INT, 2147483647)

        def __init__(self, context):
            self._init(context)

        def __str__(self):
            return "math"

        @builtin_func(returns=INT)
        def abs(self, value: INT): ...

        @library_func(returns=INT)
        def my_func(self, x: INT) -> Variable:
            # 在编译期执行的 Python 逻辑
            return self.emitter.create_temp_var_declared(INT, "result")
"""
from __future__ import annotations

import inspect
import types as py_types
from abc import abstractmethod
from typing import Any, Callable, Optional, Union, cast, get_origin, get_args, get_type_hints

from dovetail.core.enums import PrimitiveDataType
from dovetail.core.enums.datatypes import DataTypeBase, UnionType
from dovetail.core.enums.types import FunctionType
from dovetail.core.lib.library import Library, LibraryContext
from dovetail.core.symbols import Function, Parameter, Variable, Reference
from dovetail.utils.naming import NameNormalizer

# ── 类型快捷别名 ──────────────────────────────────────────────────
INT = PrimitiveDataType.INT
STRING = PrimitiveDataType.STRING
BOOLEAN = PrimitiveDataType.BOOLEAN
VOID = PrimitiveDataType.VOID

_PYTHON_TYPE_MAP: dict[type | None, PrimitiveDataType] = {
    int: PrimitiveDataType.INT,
    str: PrimitiveDataType.STRING,
    bool: PrimitiveDataType.BOOLEAN,
    None: PrimitiveDataType.VOID
}

# 挂载在方法上的元数据 key
_META_KEY = "_lib_factory_meta"


# ── 装饰器 ────────────────────────────────────────────────────────────────────

def builtin_func(
        returns: DataTypeBase | type | None = VOID,
        *,
        name: Optional[str] = None,
        defaults: Optional[dict[str, Any]] = None,
) -> Callable:
    """
    声明一个 BUILTIN 类型的库函数。

    handler 固定为 None，函数体写 `...` 即可，逻辑由后端处理。

    Args:
        returns:  返回类型，默认 VOID
        name:     覆盖函数名（默认用方法名，传入原始函数名即可，无需归一化名称）
        defaults: 可选参数的默认字面量值 {param_name: value}
    """
    return _make_decorator(
        returns=_resolve_type(returns),
        is_builtin=True,
        name=name,
        defaults=defaults or {},
    )


def library_func(
        returns: DataTypeBase | type | None = VOID,
        *,
        name: Optional[str] = None,
        defaults: Optional[dict[str, Any]] = None,
) -> Callable:
    """
    声明一个 LIBRARY 类型的库函数。

    方法体就是编译期 handler，参数在运行时收到 Reference[Variable | Literal]。

    Args:
        returns:  返回类型，默认 VOID
        name:     覆盖函数名
        defaults: 可选参数的默认字面量值 {param_name: value}
    """
    return _make_decorator(
        returns=_resolve_type(returns),
        is_builtin=False,
        name=name,
        defaults=defaults or {},
    )


def _resolve_type(t: DataTypeBase | type | None) -> DataTypeBase:
    """将 Python 原生类型或 DataTypeBase 实例统一转换为 DataTypeBase。"""
    if isinstance(t, DataTypeBase):
        return t
    if get_origin(t) is py_types.UnionType:
        types: list[DataTypeBase] = []
        for arg in get_args(t):
            types.append(_resolve_type(arg))
        return UnionType(*types)

    mapped = _PYTHON_TYPE_MAP.get(t)
    if mapped is not None:
        return mapped
    raise TypeError(
        f"不支持的类型注解 '{t}'，请使用 int/str/bool/None 或 DataTypeBase 实例"
    )


def _make_decorator(
        returns: DataTypeBase,
        is_builtin: bool,
        name: Optional[str],
        defaults: dict[str, Any],
) -> Callable:
    def decorator(method: Callable) -> Callable:
        setattr(method, _META_KEY, {
            "returns": returns,
            "is_builtin": is_builtin,
            "name": name,  # None 表示用方法名
            "defaults": defaults,
        })
        return method

    return decorator


# ── lib_var ───────────────────────────────────────────────────────────────────

class _LibVarDescriptor:
    """lib_var() 的返回值，挂在类属性上供 LibraryBase 收集。"""
    __slots__ = ("override_name", "dtype", "value", "mutable")

    def __init__(
            self,
            dtype: DataTypeBase,
            value: Union[int, str, bool, None],
            name: Optional[str],
            mutable: bool,
    ):
        self.override_name = name
        self.dtype = dtype
        self.value = value
        self.mutable = mutable


def lib_var(
        dtype: DataTypeBase | type,
        value: Union[int, str, bool, None],
        *,
        name: Optional[str] = None,
        mutable: bool = False,
) -> _LibVarDescriptor:
    """
    声明一个库级常量/变量。

    用法:
        INT_MAX = lib_var(INT, 2147483647)
        MY_FLAG = lib_var(BOOLEAN, False, mutable=True)
    """
    return _LibVarDescriptor(dtype=_resolve_type(dtype), value=value, name=name, mutable=mutable)


# ── LibraryBase ───────────────────────────────────────────────────────────────

class LibraryBase(Library):
    """
    Library 的声明式子类。

    子类规则：
      1. 用 @builtin_func / @library_func 装饰方法声明函数
      2. 用 lib_var() 声明类级常量
      3. 在 __init__ 中调用 self._init(context)
      4. 实现 __str__ 返回库名

    _init() 会扫描所有装饰器标记，自动构建符号表。
    get_functions() / get_variables() 无需重写。
    """

    @abstractmethod
    def __init__(self, context: LibraryContext):
        pass

    @abstractmethod
    def __str__(self) -> str:
        """返回库的描述性字符串"""
        pass

    def _init(self, context: LibraryContext) -> None:
        """扫描装饰器标记，构建 _functions 和 _variables。必须在 __init__ 中调用。"""
        self.context = context
        self._functions: dict[Function, Optional[Callable]] = {}
        self._variables: dict[Variable, Reference] = {}

        self._collect_functions()
        self._collect_variables()

    def _collect_functions(self) -> None:
        for attr_name in dir(self):
            if attr_name.startswith("__"):
                continue
            method: Callable = cast(Callable, getattr(self, attr_name, None))
            meta = getattr(method, _META_KEY, None)
            if meta is None:
                continue

            func_name: str = NameNormalizer.normalize(meta["name"] or attr_name)
            returns: DataTypeBase = meta["returns"]

            if meta["returns"] == VOID:
                # 尝试解析返回类型
                hints = get_type_hints(method)
                try:
                    returns = _resolve_type(hints.get("return",None))
                except TypeError:
                    pass

            is_builtin: bool = meta["is_builtin"]
            defaults_map: dict[str, Any] = meta["defaults"]

            params = self._extract_params(method, func_name, defaults_map)

            func_type = FunctionType.BUILTIN if is_builtin else FunctionType.LIBRARY
            handler = None if is_builtin else method

            self._functions[Function(func_name, params, returns, func_type)] = handler

    def _extract_params(
            self,
            method: Callable,
            func_name: str,
            defaults_map: dict[str, Any],
    ) -> list[Parameter]:
        optional_set = set(defaults_map.keys())
        sig = inspect.signature(method)
        params: list[Parameter] = []

        for param_name, param in sig.parameters.items():
            if param_name == "self":
                continue

            annotation = param.annotation
            if annotation is inspect.Parameter.empty:
                raise TypeError(
                    f"库函数 '{func_name}' 的参数 '{param_name}' 缺少类型注解，"
                    f"请使用 int / str / bool 或 DataTypeBase 实例"
                )

            # 统一解析，Python 原生类型和 DataTypeBase 实例都接受
            dtype = _resolve_type(annotation)

            default_ref: Optional[Reference]
            if param_name in optional_set:
                default_ref = Reference.literal(defaults_map.get(param_name))
            else: # 检查是否存在默认值
                if param.default is not inspect.Parameter.empty:
                    default_ref = Reference.literal(param.default)
                else:
                    default_ref = None


            params.append(Parameter(Variable(param_name, dtype), default=default_ref))

        return params

    def _collect_variables(self) -> None:
        for attr_name in dir(type(self)):
            if attr_name.startswith("_"):
                continue
            descriptor = getattr(type(self), attr_name, None)
            if not isinstance(descriptor, _LibVarDescriptor):
                continue
            var_name = NameNormalizer.normalize(descriptor.override_name or attr_name)
            var = Variable(var_name, descriptor.dtype, mutable=descriptor.mutable)
            self._variables[var] = Reference.literal(descriptor.value)

    # Library 接口

    def get_functions(self) -> dict[Function, Optional[Callable]]:
        return self._functions

    def get_variables(self) -> dict[Variable, Reference]:
        return self._variables

    # 内部接口

    def _get_function(self, func_name: str) -> Function | None:
        """
        根据名字获得 Function 实例，优先搜索自身

        Args:
            func_name: 原始函数名(归一化前)

        Returns:
            Function or None
        """
        func_name_n = NameNormalizer.normalize(func_name)
        try:
            return next(func for func in self._functions.keys() if func.name == func_name_n)
        except StopIteration:
            return cast(Function | None,
                        self.context.symbol_resolver.resolve_symbol(func_name_n, expected_type=Function))
