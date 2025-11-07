# coding=utf-8
from functools import lru_cache

from .plugin import Plugin


@lru_cache(maxsize=None)
def get_loader_instance():
    """
    返回加载器实例
    """
    from ..plugin_loader.loader import plugin_loader
    return plugin_loader


def get_loaded_plugins() -> dict[str, Plugin]:
    """获取已加载的插件列表"""
    return get_loader_instance().plugins_main_class


def get_plugin(plugin_name: str) -> Plugin | None:
    """根据插件名称获得插件实例"""
    return get_loaded_plugins().get(plugin_name, None)


def load_plugin(plugin_name: str) -> bool:
    """
    加载插件

    :param plugin_name:被加载的插件的目录名
    :return:
    """
    try:
        get_loader_instance().load_plugin(plugin_name)
        return True
    except Exception as e:
        return False


def get_plugin_config(plugin_name: str) -> dict:
    """获取插件配置"""
    pass


def get_api_version() -> tuple[int, int, int]:
    """
    获取api版本号
    """
    return 1, 0, 0
