# coding=utf-8
import itertools
from abc import abstractmethod
from typing import Protocol, Optional

from dovetail.core.backend import GenerationContext
from dovetail.core.symbols import Variable, Reference
from dovetail.utils.logger import get_logger
from .template.parameter import ParameterBuilder, TemplateParameter
from .template.template import CommandTemplate, TemplateRegistry
from .template.template_engine import TemplateEngine

logger = get_logger(__name__)


class CommandHandler(Protocol):
    """
    命令处理器协议

    Attributes:
        no_size_effects(bool): 是否有副作用
    """

    no_size_effects: bool

    def call(
            self,
            result: Variable | None,
            context: GenerationContext,
            args: dict[str, Reference]
    ) -> None:
        """
        调用函数，当函数为无副作用函数且无返回变量时跳过调用

        Args:
            result: 返回值变量
            context: 代码生成上下文
            args: 参数字典

        Notes:
            通常该方法不应被覆盖
        """
        if hasattr(self, "no_size_effects") and self.no_size_effects and not result:
            return
        self.handle(result, context, args)

    @abstractmethod
    def handle(
            self,
            result: Variable | None,
            context: GenerationContext,
            args: dict[str, Reference]
    ) -> None:
        """
        处理命令执行/调用

        Args:
            result: 返回值变量
            context: 代码生成上下文
            args: 参数字典

        Notes:
            通常子处理器应覆写该方法而非call方法
        """
        pass


class TemplateCommandHandler(CommandHandler):
    """
    基于模板的命令处理器基类

    子类只需：
      1. 指定 template_name
      2. （可选）覆写 build_params 自定义参数映射
      3. （可选）覆写 _post_process 做渲染后处理

    引擎自动内联字面量，自动注册烘焙模板，子类不用管。
    """

    template_name: str = None

    def handle(
            self,
            result: Variable | None,
            context: GenerationContext,
            args: dict[str, Reference]
    ) -> None:
        template = TemplateRegistry.get(self.template_name)
        if not template:
            raise ValueError(f"找不到宏命令模板: {self.template_name}")

        params = self.build_params(result, context, args, template)
        engine = TemplateEngine(context.namespace, context.objective)
        commands = engine.render_from_template(template, params)

        for cmd in commands:
            context.current_scope.add_command(cmd)

        self._post_process(result, context, args)

    def build_params(
            self,
            result: Variable | None,
            context: GenerationContext,
            args: dict[str, Reference],
            template: CommandTemplate
    ) -> dict[str, TemplateParameter]:
        """
        构建模板参数。子类可覆写以自定义参数映射。

        默认实现：按模板定义的参数名从 args 中构建，
        缺失的可选参数用默认值填充为字面量。
        """
        builder = ParameterBuilder(context.current_scope, context.objective)
        all_param_names = list(itertools.chain(
            template.param_names, template.optional_params.keys()
        ))
        params = builder.build_all(args, all_param_names)

        for name, default_value in template.optional_params.items():
            if name not in params and default_value is not None:
                params[name] = TemplateParameter.literal(name, default_value)

        return params

    def _post_process(
            self,
            result: Variable | None,
            context: GenerationContext,
            args: dict[str, Reference]
    ) -> None:
        """模板渲染后的钩子，子类可覆写"""
        pass


class DefaultCommandHandler(CommandHandler):
    def __init__(self, name: str):
        self.name = name

    def handle(self, result, context, args):
        logger.error(f"Cannot find function '{self.name}'")
        context.current_scope.add_command(f"# Cannot find function '{self.name}'")


class CommandRegistry:
    """命令注册中心"""
    _handlers: dict[str, CommandHandler] = {}
    _lock = __import__('threading').Lock()

    @classmethod
    def register(cls, name: str, handler: Optional[CommandHandler] = None):
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
