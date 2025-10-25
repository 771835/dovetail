# coding=utf-8
"""插件间通信"""
from typing import Any

from .plugin import Plugin
from .plugin_manager import get_plugin


def send_message(sender: str | Plugin, target: str | Plugin, message: Any) -> bool:
    """发送消息给指定插件"""
    if plugin := get_plugin(target):
        plugin.handle_message(sender, message)
        return True
    return False
