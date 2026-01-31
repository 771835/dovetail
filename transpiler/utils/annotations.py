# coding=utf-8
"""
Annotations - Python 注解工具库
提供类似 Java 注解的功能，用于代码标记、验证和元数据处理
"""

import inspect
import time
import warnings
from functools import wraps
from typing import (
    Any, Callable, TypeVar, Union, Type, cast,
    get_type_hints, get_origin, get_args
)

from transpiler.core.config import get_project_logger
from transpiler.utils.logging_plus import get_logger

# 类型变量
T = TypeVar('T')
F = TypeVar('F', bound=Callable[..., Any])


def experimental(reason: str = "") -> Callable[[Any], Any]:
    """标记实验性功能

    Args:
        reason (str): 标记为实验性功能的原因说明

    Returns:
        Callable[[Any], Any]: 装饰器函数
    """

    def decorator(obj: Any) -> Any:
        """实验性功能装饰器

        Args:
            obj (Any): 被装饰的类或函数

        Returns:
            Any: 装饰后的类或函数
        """
        message = f"{obj.__name__} is experimental"
        if reason: message += f": {reason}"

        if inspect.isclass(obj):
            return _create_experimental_class(obj, message)
        else:
            return _create_experimental_function(obj, message)

    return decorator


def _create_experimental_class(cls: Type[T], message: str) -> Type[T]:
    """创建实验性类

    Args:
        cls (Type[T]): 原始类
        message (str): 警告消息

    Returns:
        Type[T]: 带有警告功能的实验性类
    """

    class ExperimentalClass(cls):
        """实验性类包装器"""

        def __init__(self, *args, **kwargs):
            """初始化实验性类实例

            Args:
                *args: 位置参数
                **kwargs: 关键字参数
            """
            warnings.warn(message, UserWarning, stacklevel=2)
            super().__init__(*args, **kwargs)

    ExperimentalClass.__name__ = cls.__name__
    return ExperimentalClass


def _create_experimental_function(func: F, message: str) -> F:
    """创建实验性函数

    Args:
        func (F): 原始函数
        message (str): 警告消息

    Returns:
        F: 带有警告功能的实验性函数
    """

    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        """实验性函数包装器

        Args:
            *args: 位置参数
            **kwargs: 关键字参数

        Returns:
            Any: 函数执行结果
        """
        warnings.warn(message, UserWarning, stacklevel=2)
        return func(*args, **kwargs)

    return cast(F, wrapper)


# ==================== 性能相关注解 ====================

def timed(message: str = "用时{:.3f}s") -> Callable[[F], F]:
    """测量函数执行时间

    Args:
        message (str): 时间输出格式，默认"用时{:.3f}s"

    Returns:
        Callable[[F], F]: 装饰器函数

    Example:
        >>> @timed("执行耗时: {:.3f} 秒")
        >>> def slow_function():
        >>>     time.sleep(1)
    """

    def decorator(func: F) -> F:
        """计时装饰器

        Args:
            func (F): 被装饰的函数

        Returns:
            F: 装饰后的函数
        """

        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            """计时包装器

            Args:
                *args: 位置参数
                **kwargs: 关键字参数

            Returns:
                Any: 函数执行结果
            """
            start_time = time.perf_counter()
            result = func(*args, **kwargs)
            end_time = time.perf_counter()
            elapsed = end_time - start_time
            if logger := get_project_logger():
                logger.info(message.format(elapsed))
            else:
                get_logger("time").info(message.format(elapsed))
            return result

        return cast(F, wrapper)

    return decorator


# ==================== 验证相关注解 ====================

def validate_args(validate_return: bool = False) -> Callable[[F], F]:
    """参数验证装饰器

    Args:
        validate_return (bool): 是否验证返回值类型，默认False

    Returns:
        Callable[[F], F]: 装饰器函数
    """

    def decorator(func: F) -> F:
        """参数验证装饰器

        Args:
            func (F): 被装饰的函数

        Returns:
            F: 装饰后的函数
        """

        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            """参数验证包装器

            Args:
                *args: 位置参数
                **kwargs: 关键字参数

            Returns:
                Any: 函数执行结果

            Raises:
                TypeError: 当参数类型不匹配时抛出异常
            """
            # 获取类型提示
            type_hints = get_type_hints(func)
            sig = inspect.signature(func)

            # 验证参数
            bound_args = sig.bind(*args, **kwargs)
            bound_args.apply_defaults()

            for param_name, param_value in bound_args.arguments.items():
                if param_name in type_hints:
                    expected_type = type_hints[param_name]
                    if not _check_type(param_value, expected_type):
                        raise TypeError(f"Parameter {param_name} should be {expected_type}, got {type(param_value)}")

            result = func(*args, **kwargs)

            # 验证返回值
            if validate_return and 'return' in type_hints:
                return_type = type_hints['return']
                if not _check_type(result, return_type):
                    raise TypeError(f"Return value should be {return_type}, got {type(result)}")

            return result

        return cast(F, wrapper)

    return decorator


def _check_type(value: Any, expected_type: Any) -> bool:
    """检查类型匹配

    Args:
        value (Any): 待检查的值
        expected_type (Any): 期望的类型

    Returns:
        bool: 类型是否匹配
    """
    origin = get_origin(expected_type)
    args = get_args(expected_type)

    if origin is Union:
        return any(_check_type(value, arg) for arg in args)
    elif origin is list and args:
        return isinstance(value, list) and all(_check_type(item, args[0]) for item in value)
    elif origin is dict and len(args) == 2:
        return (isinstance(value, dict) and
                all(_check_type(k, args[0]) and _check_type(v, args[1])
                    for k, v in value.items()))
    else:
        return isinstance(value, expected_type)


def not_null(func: F) -> F:
    """确保返回值不为None

    Args:
        func (F): 被装饰的函数

    Returns:
        F: 装饰后的函数

    Raises:
        ValueError: 当函数返回None时抛出异常
    """

    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        """非空检查包装器

        Args:
            *args: 位置参数
            **kwargs: 关键字参数

        Returns:
            Any: 函数执行结果

        Raises:
            ValueError: 当函数返回None时抛出异常
        """
        result = func(*args, **kwargs)
        if result is None:
            raise ValueError(f"{func.__name__} returned None, which is not allowed")
        return result

    return cast(F, wrapper)


# ==================== 安全相关注解 ====================

def rate_limited(requests_per_minute: int = 60) -> Callable[[F], F]:
    """速率限制装饰器

    Args:
        requests_per_minute (int): 每分钟允许的请求数，默认60

    Returns:
        Callable[[F], F]: 装饰器函数
    """
    request_times: list[float] = []

    def decorator(func: F) -> F:
        """速率限制装饰器

        Args:
            func (F): 被装饰的函数

        Returns:
            F: 装饰后的函数

        Raises:
            RuntimeError: 当超过速率限制时抛出异常
        """

        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            """速率限制包装器

            Args:
                *args: 位置参数
                **kwargs: 关键字参数

            Returns:
                Any: 函数执行结果

            Raises:
                RuntimeError: 当超过速率限制时抛出异常
            """
            current_time = time.time()

            # 清理过期的请求记录
            request_times[:] = [t for t in request_times if current_time - t < 60]

            if len(request_times) >= requests_per_minute:
                raise RuntimeError("Rate limit exceeded")

            request_times.append(current_time)
            return func(*args, **kwargs)

        return cast(F, wrapper)

    return decorator
