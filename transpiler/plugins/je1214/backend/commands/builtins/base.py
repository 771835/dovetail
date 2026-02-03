# coding=utf-8
from abc import abstractmethod
from typing import Protocol

from transpiler.core.backend import GenerationContext
from transpiler.core.config import get_project_logger
from transpiler.core.symbols import Variable, Constant, Reference
from .template.parameter import ParameterBuilder
from .template.template import TemplateRegistry
from .template.template_engine import TemplateEngine


class CommandHandler(Protocol):
    """命令处理器协议"""

    @abstractmethod
    def handle(
            self,
            result: Variable | Constant | None,
            context: GenerationContext,
            args: dict[str, Reference]
    ) -> None:
        """
        处理命令执行

        Args:
            result: 返回值变量
            context: 代码生成上下文
            args: 参数字典
        """
        pass


class TemplateCommandHandler(CommandHandler):
    """
    基于模板的命令处理器基类

    子类只需指定模板名称即可自动处理
    """

    template_name: str = None  # 子类需覆盖

    def handle(
            self,
            result: Variable | Constant | None,
            context: GenerationContext,
            args: dict[str, Reference]
    ) -> None:
        # 执行预处理程序
        self._pre_process(result,context,args)

        # 获取模板
        template = TemplateRegistry.get(self.template_name)
        if not template:
            raise ValueError(f"Template not found: {self.template_name}")

        # 构建参数
        builder = ParameterBuilder(context.current_scope, context.objective)
        params = builder.build_all(args, template.param_names)

        # 渲染命令
        engine = TemplateEngine(context.namespace, context.objective)
        commands = engine.render_from_template(template, params)

        # 添加到作用域
        for cmd in commands:
            context.current_scope.add_command(cmd)

        # 执行清理程序
        self._post_process(result, context, args)

    def _pre_process(
            self,
            result: Variable | Constant | None,
            context: GenerationContext,
            args: dict[str, Reference]
    ) -> None:
        """处理模板前执行的处理程序"""
        pass

    def _post_process(
            self,
            result: Variable | Constant | None,
            context: GenerationContext,
            args: dict[str, Reference]
    ) -> None:
        """处理模板后执行的处理程序"""
        pass

class DefaultCommandHandler(CommandHandler):
    def __init__(self, name: str):
        self.name = name

    def handle(self, result, context, args):
        get_project_logger().error(f"Cannot find function '{self.name}'")
        context.current_scope.add_command(f"# Cannot find function '{self.name}'")


class CommandRegistry:
    """命令注册中心"""
    _handlers: dict[str, CommandHandler] = {}
    _lock = __import__('threading').Lock()

    @classmethod
    def register(cls, name: str, handler: CommandHandler = None):
        """
        注册命令处理器

        用法1：作为装饰器
            @CommandRegistry.register('exec')
            class ExecCommand: ...

        用法2：直接注册
            CommandRegistry.register('exec', ExecCommand())
        """

        def decorator(handler_class):
            with cls._lock:
                if isinstance(handler_class, type):
                    # 类对象，实例化
                    cls._handlers[name] = handler_class()
                else:
                    # 已实例化的对象
                    cls._handlers[name] = handler_class
            return handler_class

        if handler is not None:
            # 直接注册模式
            with cls._lock:
                cls._handlers[name] = handler
            return handler

        # 装饰器模式
        return decorator

    @classmethod
    def get(cls, name: str) -> CommandHandler:
        """根据名称获得对应命令处理器"""
        command_handler = cls._handlers.get(name)
        if command_handler is None:
            return DefaultCommandHandler(name)
        return command_handler

    @classmethod
    def all(cls) -> dict[str, CommandHandler]:
        """获取所有命令处理器"""
        return cls._handlers.copy()

    @classmethod
    def clear(cls):
        """清空注册表"""
        with cls._lock:
            cls._handlers.clear()
