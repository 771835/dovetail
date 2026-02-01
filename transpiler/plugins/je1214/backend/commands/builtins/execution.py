# coding=utf-8
from .base import CommandRegistry, TemplateCommandHandler


@CommandRegistry.register('exec')
class ExecCommand(TemplateCommandHandler):
    """执行原始命令"""
    template_name = "exec"