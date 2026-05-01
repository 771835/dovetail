# coding=utf-8
from functools import lru_cache

from dovetail.core.backend import GenerationContext
from dovetail.core.symbols import Reference, Variable
from .. import TemplateRegistry, CommandRegistry
from ..base import TemplateCommandHandler
from ..template import CommandTemplate


@CommandRegistry.register("to_integer")
class ToIntegerCommand(TemplateCommandHandler):
    no_size_effects = True

    def _pre_process(
            self,
            result: Variable | None,
            context: GenerationContext,
            args: dict[str, Reference]
    ) -> None:
        """处理模板前执行的处理程序"""
        assert result is not None

        result_path = context.current_scope.get_symbol_path(result)

        self.register_template_auto(context.objective, result_path)
        self.template_name = self._get_template_name(context.objective, result_path)

    @classmethod
    def register_template_auto(cls, objective: str, path: str) -> str:
        """
        自动注册模板

        Args:
            objective: 记分板名
            path: 积分版路径

        Returns:
            (str): 被注册的路径
        """
        template_name = cls._get_template_name(objective, path)
        if not TemplateRegistry.has(template_name):
            TemplateRegistry.register(
                CommandTemplate(
                    name=template_name,
                    template=f"scoreboard players set {path} {objective} $(value)",
                    function_path=f"builtins/int/{template_name}",
                    param_names=["value"],
                    description="转换字符串为数字(自动生成模板)",
                    tags=["int", "data", "shortcut"]
                )
            )
        return template_name

    @staticmethod
    @lru_cache(maxsize=20)
    def _get_template_name(objective: str, path: str) -> str:
        prefix = f"{objective}_{path}"
        return f"to_integer_{prefix}_{hash(prefix)}"
