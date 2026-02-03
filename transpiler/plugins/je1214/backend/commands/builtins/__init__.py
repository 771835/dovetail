# coding=utf-8
from .base import CommandRegistry
from .template import TemplateRegistry
from .template.builtin_templates import register_builtin_templates


def initialize_command_system():
    """初始化命令系统"""

    # 注册内置模板
    register_builtin_templates()

    # 导入所有命令处理器
    from .execution import ExecCommand
    from .ui import TellrawJsonCommand, TellrawTextCommand
    from .math import AbsCommand, RandintCommand


# 在插件加载时调用
initialize_command_system()
