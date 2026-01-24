# coding=utf-8
"""
插件加载器核心实现

负责插件的实际加载、执行环境构建和生命周期管理。
"""

import json
import os
import traceback
from pathlib import Path
from typing import Dict

from transpiler.core.config import PLUGIN_METADATA_VALIDATOR, get_project_logger
from transpiler.plugins.plugin_api.plugin import Plugin

__all__ = [
    "plugin_loader",
]


class PluginLoader:
    """
    插件加载器

    Attributes:
        plugins_paths (List[str]): 插件搜索路径列表
        plugins_locals (Dict[str, Dict]): 插件的本地变量作用域映射
        plugins_instance (Dict[str, Plugin]): 已加载插件实例映射
    """

    # 插件搜索路径
    plugins_paths = [
        "transpiler/plugins",
        "plugins",
    ]

    def __init__(self):
        """初始化 PluginLoader 实例"""
        self.plugins_locals: dict[str, dict] = {}
        self.plugins_instance: dict[str, Plugin] = {}

    def load_plugin(self, plugin_name: str) -> None:
        """加载指定名称的插件

        Args:
            plugin_name (str): 要加载的插件名称

        该方法会搜索插件路径，读取插件元数据和主文件，创建执行环境并实例化插件。
        """
        # 根据插件目录名获取插件入口代码
        metadata = None
        code = None

        for plugins_path in PluginLoader.plugins_paths:
            plugin_path = Path(plugins_path) / plugin_name
            if plugin_path.exists() and plugin_path.is_dir():
                metadata_path = plugin_path / "plugin.metadata"
                if metadata_path.exists() and metadata_path.is_file():
                    try:
                        with open(metadata_path) as metadata_file:
                            metadata = json.load(metadata_file)
                    except json.decoder.JSONDecodeError as e:
                        get_project_logger().error(f"Failed to load plugin metadata file '{plugin_path}': {e}")
                        if os.environ.get("PLUGIN_DEBUG", None):
                            traceback.print_tb(e.__traceback__)
                        continue
                    try:
                        # 效验插件配置文件是否正确
                        PLUGIN_METADATA_VALIDATOR(metadata)
                    except Exception as e:
                        get_project_logger().error(f"Failed to load plugin metadata file '{plugin_path}': {e}")
                        if os.environ.get("PLUGIN_DEBUG", None):
                            traceback.print_tb(e.__traceback__)
                        continue
                    # 读取入口文件
                    plugin_main = Path(plugin_path) / metadata.get("plugin_main")
                    if plugin_main.exists() and plugin_main.is_file():
                        with open(plugin_main, encoding="utf-8") as plugin_main_file:
                            code = plugin_main_file.read()
                        break
                    else:
                        get_project_logger().error(f"Plugin '{plugin_path}' is invalid")
                        continue
                else:
                    continue
        else:
            get_project_logger().error(f"No plugin '{plugin_name}' found")
            return

        if not plugin_path or not metadata or not plugin_main or code is None:
            get_project_logger().error(f"Plugin '{plugin_path}' is invalid")
            return
        get_project_logger().info(f"Loading plugin '{plugin_name}' from '{plugin_path}'")

        # 获得插件的作用域
        plugin_locals = self.plugins_locals.get(plugin_name, {})
        try:
            global_env: dict = dict(globals())
            global_env.update(
                {
                    "__path__": str(plugin_path.resolve()),
                    "__package__": str(plugin_path.resolve().relative_to(Path.cwd())).replace("\\", "."),
                    "__name__": plugin_name,
                    "__file__": str(plugin_main.resolve()),
                    "__plugin_name__": metadata.get("display_name")
                }
            )
            # 执行代码
            exec(code, global_env, plugin_locals)
            global_env.update(plugin_locals)
            self.plugins_locals[plugin_name] = plugin_locals
            # 搜索入口类
            if plugin_main_class := plugin_locals.get(metadata["main_class"], None):
                self.plugins_instance[plugin_name] = plugin_main_class()
                is_validate, reason = self.plugins_instance[plugin_name].validate()
                if not is_validate:
                    raise Warning(reason)
                self.plugins_instance[plugin_name].initialize()
                self.plugins_instance[plugin_name].load()
            else:
                raise ModuleNotFoundError(f"Plugin '{plugin_name}' is invalid")
        except Exception as e:
            get_project_logger().error(f"加载插件{plugin_name}失败，原因：{e.__str__()}")
            if self.plugins_locals.get(plugin_name, None):
                del self.plugins_locals[plugin_name]
            if self.plugins_instance.get(plugin_name, None):
                del self.plugins_instance[plugin_name]
            if os.environ.get("PLUGIN_DEBUG", None):
                traceback.print_tb(e.__traceback__)


plugin_loader = PluginLoader()
