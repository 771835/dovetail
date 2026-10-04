# coding=utf-8
"""
插件加载器模块

提供插件的自动发现、加载和管理功能，支持从指定目录加载插件并执行其生命周期方法。
"""

from dovetail.plugins.plugin_api.plugin import Plugin
from dovetail.plugins.plugin_api.v2 import plugin_manager


class PluginMain(Plugin):
    """插件加载器插件

    负责自动发现和加载其他插件的核心插件。
    """

    def __init__(self):
        """初始化实例"""
        super().__init__()

    def load(self):
        """加载所有可用的插件"""
        loader_instance = plugin_manager.get_loader_instance()
        loader_instance.load_all()

    def unload(self):
        """卸载插件

        清理插件资源，当前实现为空。
        """
        pass

    def validate(self) -> tuple[bool, str | None]:
        """验证插件有效性

        Returns:
            tuple[bool, str | None]: 验证结果和错误信息，始终返回(True, None)
        """
        return True, None
