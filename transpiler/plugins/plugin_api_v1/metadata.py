# coding=utf-8

from transpiler.plugins.plugin_api_v1 import Plugin


def get_loaded_plugins() -> dict[str, Plugin]:
    """获取已加载的插件列表"""
    from ..load_plugin.plugin_loader import plugin_loader
    return plugin_loader.plugins_main_class

def get_plugin(plugin_name: str) -> Plugin:
    from ..load_plugin.plugin_loader import plugin_loader
    return plugin_loader.plugins[plugin_name]




def get_plugin_config(plugin_name: str) -> dict:
    """获取插件配置"""
    pass


def set_plugin_config(plugin_name: str, config: dict) -> bool:
    """设置插件配置"""
    pass


def get_compiler_version() -> str:
    """获取编译器版本"""
    pass


