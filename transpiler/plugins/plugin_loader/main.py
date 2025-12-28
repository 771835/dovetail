# coding=utf-8
from pathlib import Path

from transpiler.plugins.plugin_api.v1 import plugin_manager
from transpiler.plugins.plugin_api.plugin import Plugin


class LoaderPlugin(Plugin):
    def __init__(self):
        super().__init__()

    def load(self):
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
        pass

    def validate(self):
        return True, None
