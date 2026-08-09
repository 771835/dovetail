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

from dovetail.core.config import PLUGIN_METADATA_VALIDATOR
from dovetail.plugins.plugin_api.plugin import Plugin
from dovetail.utils.logger import get_logger

__all__ = [
    "plugin_loader",
]

logger = get_logger(__name__)

load_stack = []


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
        "dovetail/plugins",
        "plugins",
    ]

    def __init__(self):
        """初始化 PluginLoader 实例"""
        self.plugins_locals: dict[str, dict] = {}
        self.plugins_instance: dict[str, Plugin] = {}

    def load_plugin(self, plugin_input: str) -> None:
        """加载指定名称的插件

        Args:
            plugin_input (str): 需要被加载的插件名称或插件目录的绝对路径
        """

        # 判断输入的是否是绝对路径（或者包含路径的文件夹）
        input_path = Path(plugin_input)
        is_absolute_path = input_path.is_absolute() and input_path.exists() and input_path.is_dir()

        # 如果是绝对路径，直接使用路径作为 plugin_path，名字可以用文件夹名
        if is_absolute_path:
            plugin_path = input_path
            plugin_name = plugin_path.name
        else:
            plugin_name = plugin_input

        if plugin_name in self.plugins_instance:
            logger.warning(f"插件重复加载：插件 '{plugin_name}' 已经被加载了")
            return

        # 根据插件目录名获取插件入口代码
        metadata = None
        code = None

        # 如果是绝对路径，跳过搜索循环；否则执行原有的搜索逻辑
        if is_absolute_path:
            search_paths = [plugin_path]
        else:
            search_paths = [Path(p) / plugin_name for p in PluginLoader.plugins_paths]

        for p_path in search_paths:
            if p_path.exists() and p_path.is_dir():
                plugin_path = p_path
                metadata_path = plugin_path / "plugin.metadata"
                if metadata_path.exists() and metadata_path.is_file():
                    try:
                        with open(metadata_path, encoding="utf-8") as metadata_file:
                            metadata = json.load(metadata_file)
                    except json.decoder.JSONDecodeError as e:
                        logger.error(f"Failed to load plugin metadata file '{plugin_path}': {e}")
                        if os.environ.get("PLUGIN_DEBUG", None):
                            traceback.print_tb(e.__traceback__)
                        continue
                    try:
                        # 效验插件配置文件是否正确
                        PLUGIN_METADATA_VALIDATOR(metadata)
                    except Exception as e:
                        logger.error(f"Failed to load plugin metadata file '{plugin_path}': {e}")
                        if os.environ.get("PLUGIN_DEBUG", None):
                            traceback.print_tb(e.__traceback__)
                        continue

                    # 读取入口文件
                    plugin_main = plugin_path / metadata.get("plugin_main")
                    if plugin_main.exists() and plugin_main.is_file():
                        with open(plugin_main, encoding="utf-8") as plugin_main_file:
                            code = plugin_main_file.read()
                        break
                    else:
                        logger.error(f"Plugin '{plugin_path}' is invalid: main file not found")
                        continue
        else:
            logger.error(f"No valid plugin found for '{plugin_input}'")
            return

        if not metadata or not plugin_main or code is None:
            logger.error(f"Plugin '{plugin_path}' is invalid")
            return
        logger.debug(f"插件 '{plugin_name}' 被从 '{plugin_path}' 加载")

        load_stack.append(plugin_name)
        logger.debug(f"插件加载栈：{' -> '.join(load_stack)}， 长度为 {len(load_stack)}")

        # 获得插件的作用域
        plugin_locals = self.plugins_locals.get(plugin_name, {})
        try:
            global_env: dict = dict()

            # 处理相对路径计算，防止绝对路径加载时 relative_to 报错
            try:
                package_path = str(plugin_path.resolve().relative_to(Path.cwd())).replace(os.sep, ".")
            except ValueError:
                # 如果绝对路径不在当前工作目录下，则直接用插件名作为包名
                package_path = plugin_name

            global_env.update(
                {
                    "__path__": str(plugin_path.resolve()),
                    "__package__": package_path,
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
                    logger.warning(f"Plugin '{plugin_name}' is invalid, reason: {reason}")
                self.plugins_instance[plugin_name].initialize()
                self.plugins_instance[plugin_name].load()
            else:
                raise ModuleNotFoundError(f"Plugin '{plugin_name}' is invalid")
        except Exception as e:

            logger.error(f"加载插件{plugin_name}失败，原因：{e.__str__()}")
            if self.plugins_locals.get(plugin_name, None):
                del self.plugins_locals[plugin_name]
            if self.plugins_instance.get(plugin_name, None):
                del self.plugins_instance[plugin_name]
            if os.environ.get("PLUGIN_DEBUG", None):
                traceback.print_tb(e.__traceback__)

        load_stack.pop()


plugin_loader = PluginLoader()
