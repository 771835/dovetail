# coding=utf-8
"""
Decorators - Python 运行时装饰器工具库
提供实验性标记、计时、参数验证等功能。

注意：本模块与编译期注解系统（dovetail.core.annotations）无关。
"""

import inspect
import time
from functools import wraps
from typing import (
    Any, Callable, TypeVar, Union, cast,
    get_type_hints, get_origin, get_args
)

from dovetail.utils.logger import get_logger

logger = get_logger(__name__)

# 类型变量
T = TypeVar('T')
F = TypeVar('F', bound=Callable[..., Any])

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

            logger.info(message.format(elapsed))
            return result

        return wrapper

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
