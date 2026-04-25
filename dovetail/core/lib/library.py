# coding=utf-8
from abc import ABCMeta, abstractmethod
from typing import Callable

from dovetail.core.parser.components import SymbolResolver, IREmitter, ErrorReporter
from dovetail.core.symbols import Class, Function, Reference, Variable, Literal


class Library(metaclass=ABCMeta):
    """
    内置库基类
    """

    @abstractmethod
    def __init__(self, symbol_resolver: SymbolResolver, emitter: IREmitter,
                 error_reporter: ErrorReporter):
        pass

    @abstractmethod
    def __str__(self) -> str:
        """返回库的描述性字符串"""
        pass

    def load(self):
        """加载库资源（如初始化状态、加载依赖等）"""
        pass

    def get_functions(self) -> dict[Function, Callable[..., Variable | Literal | None]]:
        """获取函数及其处理函数的映射"""
        return {}

    def get_variables(self) -> dict[Variable, Reference[Variable]]:
        """获取库中定义的所有量"""
        return {}

    def get_classes(self) -> dict[Class, dict[str, Callable[..., Variable | Literal | None]]]:
        """获取库中定义的所有类"""
        return {}

    def get_name(self) -> str:
        """获取库的名字"""
        return self.__class__.__name__
