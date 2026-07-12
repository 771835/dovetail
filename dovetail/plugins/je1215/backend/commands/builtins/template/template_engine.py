# coding=utf-8
"""
模板命令引擎
"""
import hashlib
import re
import uuid

from dovetail.utils.logger import get_logger
from .parameter import TemplateParameter
from .template import CommandTemplate, TemplateRegistry
from ... import LiteralPoolTools, DataPath, Copy, StorageLocation
from ....commands import FunctionBuilder

logger = get_logger(__name__)

class TemplateEngine:
    """
    模板命令引擎

    核心逻辑：渲染时自动内联所有字面量参数，仅变量参数走宏调用。
    handler 不再需要关心渲染模式选择和动态模板注册。
    """

    VAR_PATTERN = re.compile(r'\$\((\w+)\)')

    def __init__(self, namespace: str, objective: str):
        self.namespace = namespace
        self.objective = objective

    # ==================== 公开接口 ====================

    def render(self, template_str: str, function_path: str,
               params: dict[str, TemplateParameter]) -> list[str]:
        """
        核心渲染方法

        1. 把所有字面量参数内联进模板字符串
        2. 如果没有残留 $(var) → 返回一行纯命令
        3. 如果有残留 $(var) → 自动注册烘焙模板，走宏调用
        """
        # 第一步：内联所有字面量
        baked_str = template_str
        variable_params = {}

        for name, param in params.items():
            if param.is_literal():
                baked_str = baked_str.replace(f"$({name})", str(param.value))
            else:
                variable_params[name] = param

        # 第二步：检查残留的宏变量
        if not self.VAR_PATTERN.search(baked_str):
            return [baked_str]

        # 第三步：自动注册烘焙模板（供 .mcfunction 文件生成使用）
        baked_id = self._baked_id(function_path, baked_str)
        if not TemplateRegistry.has(baked_id):
            TemplateRegistry.register(CommandTemplate(
                name=baked_id,
                template=baked_str,
                function_path=baked_id,
                param_names=list(variable_params.keys()),
            ))
            TemplateRegistry.get.cache_clear()

        # 第四步：仅变量参数走宏调用
        return self._macro_call(baked_id, variable_params)

    def render_from_template(self, template: CommandTemplate,
                             params: dict[str, TemplateParameter]) -> list[str]:
        """使用 CommandTemplate 对象渲染"""
        param_values = {name: p.value for name, p in params.items()}
        all_params = template.get_all_params(param_values)
        valid, error = template.validate_params(all_params)
        if not valid:
            logger.error(
                f"Template '{template.name}' parameter validation failed: {error}")
            return []
        return self.render(template.template, template.function_path, params)

    def render_by_name(self, template_name: str,
                       params: dict[str, TemplateParameter]) -> list[str]:
        """通过模板名称渲染"""
        template = TemplateRegistry.get(template_name)
        if not template:
            raise ValueError(f"Template not found: {template_name}")
        return self.render_from_template(template, params)

    def render_by_path(self, function_path: str,
                       params: dict[str, TemplateParameter]) -> list[str]:
        """通过函数路径渲染（无模板时回退为原始宏调用）"""
        template = TemplateRegistry.get_by_path(function_path)
        if not template:
            return self._raw_macro_call(function_path, params)
        return self.render_from_template(template, params)

    # ==================== 私有方法 ====================

    @staticmethod
    def _baked_id(function_path: str, baked_str: str) -> str:
        """根据烘焙后的模板字符串计算唯一标识"""
        h = hashlib.sha256(baked_str.encode()).hexdigest()[:8]
        return f"{function_path}_{h}"

    def _macro_call(self, function_path: str,
                    variable_params: dict[str, TemplateParameter]) -> list[str]:
        """生成宏调用命令（仅传入变量参数）"""
        commands = []
        args_path = f"args.{uuid.uuid4().hex}"

        for name, param in variable_params.items():
            if param.is_literal():
                logger.error(f"模板 '{function_path}' 的参数 '{name}' 应该是一个变量")
                continue
            source = param.get_data_path()
            target = DataPath(
                f"{args_path}.{name}",
                self.objective,
                StorageLocation.STORAGE
            )
            commands.append(Copy.copy(target, source))

        commands.append(
            FunctionBuilder.run_with_source(
                f"{self.namespace}:{function_path.replace('.', '/')}",
                "storage",
                f"{self.objective} {args_path}"
            )
        )
        return commands

    def _raw_macro_call(self, function_path: str,
                        params: dict[str, TemplateParameter]) -> list[str]:
        """
        原始宏调用（无模板时的回退方案）
        字面量从 literal pool 拷贝，变量从存储路径拷贝
        """
        commands = []
        args_path = f"args.{uuid.uuid4().hex}"

        for name, param in params.items():
            if param.is_literal():
                source = LiteralPoolTools.get_literal_path(param.value, self.objective)
            else:
                source = param.get_data_path()
            target = DataPath(
                f"{args_path}.{name}",
                self.objective,
                StorageLocation.STORAGE
            )
            commands.append(Copy.copy(target, source))

        commands.append(
            FunctionBuilder.run_with_source(
                f"{self.namespace}:{function_path.replace('.', '/')}",
                "storage",
                f"{self.objective} {args_path}"
            )
        )
        return commands