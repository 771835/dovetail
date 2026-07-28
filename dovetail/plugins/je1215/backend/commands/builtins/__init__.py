# coding=utf-8
from .base import CommandRegistry
from .template import TemplateRegistry


def initialize_command_system():
    """初始化命令系统"""
    from .template.builtin_templates import register_builtin_templates

    # 注册内置模板
    register_builtin_templates()

    # 导入所有命令处理器
    from . import data, math, ui, execution, world, player


# 在插件加载时调用
initialize_command_system()

__all__ = ["CommandRegistry", "TemplateRegistry"]
