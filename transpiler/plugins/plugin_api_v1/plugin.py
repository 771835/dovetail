# coding=utf-8
from __future__ import annotations
from abc import abstractmethod, ABC
from typing import Any


class Plugin(ABC):
    """
        插件基类
    """

    def __init__(self):
        pass

    @abstractmethod
    def load(self):
        """插件被加载时调用"""
        pass

    @abstractmethod
    def unload(self) -> bool:
        """插件被正常加载时调用(仅其他插件卸载时)"""
        pass

    @abstractmethod
    def validate(self) -> bool:
        """插件加载前的验证，检查依赖和兼容性"""
        pass

    def initialize(self) -> None:
        """插件初始化，在validate之后，load之前调用"""
        pass


    def get_dependencies(self) -> list[str]:
        """获取插件依赖列表"""
        return []

    def get_conflicts(self) -> list[str]:
        """获取与此插件冲突的插件列表"""
        return []

    def get_default_config(self) -> dict:
        """获取默认配置"""
        return {}

    def get_memory_usage(self) -> int:
        """获取插件内存占用（字节）"""
        return -1

    def handle_message(self, sender: Plugin, message: Any) -> Any:
        """处理来自其他插件的消息"""
        pass
