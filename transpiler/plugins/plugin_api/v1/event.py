# coding=utf-8
"""
事件系统基类
"""
from __future__ import annotations

from abc import ABC
from typing import Callable, TypeVar

T = TypeVar('T', bound='Event')


class Event(ABC):
    @classmethod
    def register_handler(cls, handler: Callable[[T], None]):
        if hasattr(cls, "__HANDLERS__"):
            cls.__HANDLERS__.append(handler)
        else:
            cls.__HANDLERS__ = []

    @classmethod
    def unregister_handler(cls, handler: Callable[[T], None]):
        """注销事件处理器"""
        if hasattr(cls, "__HANDLERS__") and handler in cls.__HANDLERS__:
            cls.__HANDLERS__.remove(handler)

    @classmethod
    def clear_handlers(cls):
        """清除所有处理器"""
        if hasattr(cls, "__HANDLERS__"):
            cls.__HANDLERS__.clear()

    def call_event(self):
        if hasattr(self.__class__, "__HANDLERS__"):
            for handler in self.__HANDLERS__:
                handler(self)
