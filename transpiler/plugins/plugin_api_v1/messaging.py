# coding=utf-8
"""插件间通信"""
from typing import Any

from transpiler.plugins.plugin_api_v1 import Plugin


def send_message(target_plugin: str | Plugin, message: Any) -> bool:
    """发送消息给指定插件"""
    pass


def broadcast_message(message: Any, exclude: list[str] = None) -> int:
    """广播消息给所有插件，返回接收者数量"""
    pass

