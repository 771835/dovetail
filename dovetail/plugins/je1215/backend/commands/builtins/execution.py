# coding=utf-8
"""
执行指令模块

此模块提供了动态执行指令的支持，例如ExecCommand类

Classes:
    ExecCommand: exec函数的后端实现
"""
from .base import CommandRegistry, TemplateCommandHandler


@CommandRegistry.register('exec')
class ExecCommand(TemplateCommandHandler):
    """
    执行原始命令

    Attributes:
        template_name (str): 常量"exec"，不应被修改
    """
    template_name = "exec"
