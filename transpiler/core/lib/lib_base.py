# coding=utf-8
from abc import ABCMeta, abstractmethod
from typing import Callable

from transpiler.core.instructions import IRInstruction
from transpiler.core.symbols import Constant, Class, Function, Reference


class Library(metaclass=ABCMeta):
    @abstractmethod
    def __str__(self) -> str:
        """返回库的描述性字符串"""
        pass

    @staticmethod
    @abstractmethod
    def load() -> list[IRInstruction]:
        """加载库资源（如初始化状态、加载依赖等）"""
        pass

    @staticmethod
    @abstractmethod
    def get_functions() -> dict[Function, Callable[..., list[IRInstruction]]]:
        """获取函数及其处理函数的映射"""
        pass

    @staticmethod
    @abstractmethod
    def get_constants() -> dict[Constant, Reference]:
        """获取库中定义的所有常量"""
        pass

    @staticmethod
    def get_events() -> dict[str, Callable[..., list[IRInstruction]]]:
        """获取事件及其处理函数的映射"""
        return {}

    @staticmethod
    def get_annotations() -> dict[str, Callable[..., list[IRInstruction]]]:
        """获取注解及其处理函数的映射"""
        return {}

    @staticmethod
    def get_classes() -> list[Class]:
        """获取库中定义的所有类"""
        return []
