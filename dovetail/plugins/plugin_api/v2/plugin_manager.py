# coding=utf-8
from functools import lru_cache
from pathlib import Path

import sys

from dovetail.plugins.plugin_api.plugin import Plugin


@lru_cache(maxsize=None)
def get_loader_instance():
    """
    返回加载器实例
    """
    # 延迟导入防止循环依赖
    from dovetail.plugins.plugin_loader.loader import plugin_loader
    return plugin_loader


def get_loaded_plugins() -> dict[str, Plugin]:
    """获取已加载的插件列表"""
    return get_loader_instance().plugins_instance


def get_plugin(plugin_name: str) -> Plugin | None:
    """根据插件名称获得插件实例"""
    return get_loaded_plugins().get(plugin_name, None)


def load_plugin(plugin_name: str | Path) -> bool:
    """
    加载插件
    """
    try:
        get_loader_instance().load_plugin(plugin_name)
        return True
    except Exception as e:
        return False


def get_plugin_config(plugin_name: str) -> dict:
    """获取插件配置"""
    try:
        return get_loader_instance().plugin_metadata[plugin_name].get("config", {})
    except Exception as e:
        return {}


def find_build_plugin(tool_name: str = "") -> Plugin | None:
    """查找构建插件

    优先级：
    1. tool_name 显式指定
    2. dovetail.toml 中 [build].tool 字段
    3. 已加载插件中标记了 build_tool 的（默认 dovetail_build）
    """

    # 显式指定
    if tool_name:
        return get_plugin(tool_name)

    # 从 dovetail.toml 读取 [build].tool
    try:
        # 兼容 Python 3.10 及更低版本与 Python 3.11+
        if sys.version_info >= (3, 11):
            import tomllib
        else:
            try:
                import tomli as tomllib
            except ImportError:
                raise ImportError("请在 Python < 3.11 环境下安装 tomli 库: pip install tomli")

        toml_path = Path.cwd() / "dovetail.toml"
        if toml_path.exists():
            with open(toml_path, "rb") as f:
                data = tomllib.load(f)
            configured_tool = data.get("build", {}).get("tool", "")
            if configured_tool and configured_tool != "default":
                plugin = get_plugin(configured_tool)
                if plugin:
                    return plugin
    except Exception:
        pass

    # 默认：查找 dovetail_build 或任意标记为 build_tool 的插件
    for name, plugin in get_loaded_plugins().items():
        if getattr(plugin, "_is_build_tool", False):
            return plugin

    # 最终 fallback
    return get_plugin("dovetail_build")
