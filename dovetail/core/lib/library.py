# coding=utf-8
from abc import ABCMeta, abstractmethod
from typing import Callable

from dovetail.core.instructions import IRInstruction
from dovetail.core.ir_builder import IRBuilder
from dovetail.core.symbols import Class, Function, Reference, Variable, Literal


class Library(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, builder: IRBuilder):
        pass

    @abstractmethod
    def __str__(self) -> str:
        """返回库的描述性字符串"""
        pass

    @abstractmethod
    def load(self) -> list[IRInstruction]:
        """加载库资源（如初始化状态、加载依赖等）"""
        pass

    @abstractmethod
    def get_functions(self) -> dict[Function, Callable[..., Variable | Literal]]:
        """获取函数及其处理函数的映射"""
        pass

    @abstractmethod
    def get_variables(self) -> dict[Variable, Reference]:
        """获取库中定义的所有量"""
        pass

    def get_classes(self) -> dict[Class, dict[str, Callable[..., Variable | Literal]]]:
        """获取库中定义的所有类"""
        return {}

    def get_name(self) -> str:
        """获取库的名字"""
        return self.__class__.__name__
