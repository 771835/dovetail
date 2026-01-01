# coding=utf-8
"""
插件加载器模块

提供插件的自动发现、加载和管理功能，支持从指定目录加载插件并执行其生命周期方法。
"""

from pathlib import Path

from transpiler.plugins.plugin_api.plugin import Plugin
from transpiler.plugins.plugin_api.v1 import plugin_manager


class LoaderPlugin(Plugin):
    """插件加载器插件

    负责自动发现和加载其他插件的核心插件。
    """

    def __init__(self):
        """初始化 LoaderPlugin 实例"""
        super().__init__()

    def load(self):
        """加载所有可用的插件

        遍历插件目录，自动发现并加载所有符合条件的插件。
        """
        loader_instance = plugin_manager.get_loader_instance()
        # 首先尝试加载 plugin_api
        plugin_manager.load_plugin("plugin_api")
        for plugins_dir in loader_instance.plugins_paths:
            plugins_path = Path(plugins_dir)
            if plugins_path.exists() and plugins_path.is_dir():
                for plugin_dir in plugins_path.iterdir():
                    plugin_name = plugin_dir.name
                    # 对于已加载或名称前缀为特殊符号的跳过加载
                    if plugin_manager.get_plugin(plugin_name) is not None or plugin_name[0] in ("_", ".", "!"):
                        continue
                    if plugin_dir.is_dir():
                        plugin_manager.load_plugin(plugin_name)

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
