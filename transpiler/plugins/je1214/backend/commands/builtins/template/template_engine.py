# coding=utf-8
import re
import uuid

from transpiler.core.config import get_project_logger
from .parameter import TemplateParameter, ParamBindingType
from .template import CommandTemplate, TemplateRegistry
from ... import LiteralPoolTools, DataPath, Copy, StorageLocation
from ....commands import FunctionBuilder


class TemplateEngine:
    """模板命令引擎 - 统一处理模板渲染和宏调用"""

    VAR_PATTERN = re.compile(r'\$\((\w+)\)')

    def __init__(self, namespace: str, objective: str):
        self.namespace = namespace
        self.objective = objective

    def render_inline(self, template: str, params: dict[str, TemplateParameter]) -> str:
        """
        内联渲染 - 所有参数都是字面量时使用

        Args:
            template: 模板字符串，如 "$setblock $(x) $(y) $(z) $(block)"
            params: 参数字典

        Returns:
            渲染后的命令字符串
        """

        def replacer(match):
            param_name = match.group(1)
            if param_name not in params:
                raise ValueError(f"Missing parameter: {param_name}")

            param = params[param_name]
            if param.binding_type != ParamBindingType.LITERAL:
                raise ValueError(f"Cannot inline non-literal parameter: {param_name}")

            return str(param.value)

        return self.VAR_PATTERN.sub(replacer, template)

    def render_macro(self, template_path: str, params: dict[str, TemplateParameter]) -> list[str]:
        """
        宏渲染 - 有引用参数时使用，生成 data modify + function 调用

        Args:
            template_path: 模板函数路径，如 "builtins/tellraw/tellraw_text"
            params: 参数字典

        Returns:
            命令列表
        """
        commands = []
        args_path = f"args.{uuid.uuid4().hex}"

        for name, param in params.items():
            if param.binding_type == ParamBindingType.LITERAL:
                source_path = LiteralPoolTools.get_literal_path(param.value, self.objective)
            else:
                source_path = DataPath(
                    param.storage_path,
                    param.objective,
                    StorageLocation.get_storage(param.dtype)
                )
            commands.append(
                Copy.copy(
                    DataPath(
                        f"{args_path}.{name}",
                        self.objective,
                        StorageLocation.STORAGE
                    ),
                    source_path
                )
            )

        # 调用宏函数
        commands.append(
            FunctionBuilder.run_with_source(
                f"{self.namespace}:{template_path}",
                "storage",
                f"{self.objective} {args_path}"
            )
        )

        return commands

    def render(
            self,
            template_str: str,
            function_path: str,
            params: dict[str, TemplateParameter]
    ) -> list[str]:
        """
        智能渲染 - 自动选择内联或宏模式

        Args:
            template_str: 模板字符串
            function_path: 函数路径
            params: 参数字典

        Returns:
            命令列表
        """
        # 检查是否所有参数都是字面量
        all_literal = all(p.is_literal() for p in params.values())

        if all_literal:
            return [self.render_inline(template_str, params)]
        else:
            return self.render_macro(function_path, params)

    def render_from_template(
            self,
            template: CommandTemplate,
            params: dict[str, TemplateParameter]
    ) -> list[str]:
        """
        使用 CommandTemplate 对象渲染

        Args:
            template: 命令模板对象
            params: 参数字典

        Returns:
            命令列表
        """
        # 合并默认参数
        param_values = {name: p.value for name, p in params.items()}
        all_params = template.get_all_params(param_values)

        # 验证参数
        valid, error = template.validate_params(all_params)
        if not valid:
            get_project_logger().error(f"Template '{template.name}' parameter validation failed: {error}")
            return []

        # 智能选择渲染模式
        return self.render(template.template, template.function_path, params)

    def render_by_name(
            self,
            template_name: str,
            params: dict[str, TemplateParameter]
    ) -> list[str]:
        """
        通过模板名称渲染（自动从注册表获取）

        Args:
            template_name: 模板名称
            params: 参数字典

        Returns:
            命令列表
        """
        template = TemplateRegistry.get(template_name)
        if not template:
            raise ValueError(f"Template not found: {template_name}")

        return self.render_from_template(template, params)

    def render_by_path(
            self,
            function_path: str,
            params: dict[str, TemplateParameter]
    ) -> list[str]:
        """
        通过函数路径渲染（自动从注册表获取）

        Args:
            function_path: 函数路径
            params: 参数字典

        Returns:
            命令列表
        """
        template = TemplateRegistry.get_by_path(function_path)
        if not template:
            # 回退到直接宏调用
            return self.render_macro(function_path, params)

        return self.render_from_template(template, params)
