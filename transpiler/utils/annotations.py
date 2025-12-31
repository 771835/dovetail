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

# 类型变量
T = TypeVar('T')
F = TypeVar('F', bound=Callable[..., Any])


def experimental(reason: str = ""):
    """标记实验性功能"""

    def decorator(obj: Any) -> Any:
        message = f"{obj.__name__} is experimental"
        if reason: message += f": {reason}"

        if inspect.isclass(obj):
            return _create_experimental_class(obj, message)
        else:
            return _create_experimental_function(obj, message)

    return decorator


def _create_experimental_class(cls: Type[T], message: str) -> Type[T]:
    class ExperimentalClass(cls):
        def __init__(self, *args, **kwargs):
            warnings.warn(message, UserWarning, stacklevel=2)
            super().__init__(*args, **kwargs)

    ExperimentalClass.__name__ = cls.__name__
    return ExperimentalClass


def _create_experimental_function(func: F, message: str) -> F:
    @wraps(func)
    def wrapper(*args, **kwargs):
        warnings.warn(message, UserWarning, stacklevel=2)
        return func(*args, **kwargs)

    return cast(F, wrapper)


# ==================== 性能相关注解 ====================

def timed(message: str = "用时{:.3f}s"):
    """
    测量函数执行时间

    Args:
        message: 时间输出格式，默认"用时{:.3f}s"

    Example:
        >>> @timed("执行耗时: {:.3f} 秒")
        >>> def slow_function():
        >>>     time.sleep(1)
    """

    def decorator(func: F) -> F:
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.perf_counter()
            result = func(*args, **kwargs)
            end_time = time.perf_counter()
            elapsed = end_time - start_time
            print(message.format(elapsed))
            return result

        return cast(F, wrapper)

    return decorator


# ==================== 验证相关注解 ====================

def validate_args(validate_return: bool = False):
    """参数验证装饰器"""

    def decorator(func: F) -> F:
        @wraps(func)
        def wrapper(*args, **kwargs):
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
    """检查类型匹配"""
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
    """确保返回值不为None"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        if result is None:
            raise ValueError(f"{func.__name__} returned None, which is not allowed")
        return result

    return cast(F, wrapper)


# ==================== 安全相关注解 ====================

def rate_limited(requests_per_minute: int = 60):
    """速率限制装饰器"""
    request_times: list[float] = []

    def decorator(func: F) -> F:
        @wraps(func)
        def wrapper(*args, **kwargs):
            current_time = time.time()

            # 清理过期的请求记录
            request_times[:] = [t for t in request_times if current_time - t < 60]

            if len(request_times) >= requests_per_minute:
                raise RuntimeError("Rate limit exceeded")

            request_times.append(current_time)
            return func(*args, **kwargs)

        return cast(F, wrapper)

    return decorator
