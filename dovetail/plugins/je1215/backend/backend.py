# coding=utf-8
import functools
import os
from pathlib import Path

from dovetail.core.backend import Backend, TagWriter, CommandWriter, MetadataWriter, FunctionWriter
from dovetail.core.backend.context import DependencyFile, GenerationContext
from dovetail.core.backend.output import DependentDatapackWriter
from dovetail.core.compile_config import CompileConfig
from dovetail.core.ir_builder import IRBuilder
from .commands.builtins import TemplateRegistry
from .initializer_function_writer import InitializerFunctionWriter
from .literal_pool_writer import LiteralPoolWriter


class JE1214Backend(Backend):
    def __init__(self, ir_builder: IRBuilder, target: Path, config: CompileConfig):
        super().__init__(ir_builder, target, config)
        self.output_manager.register_writer(TagWriter(["initializer"], []))
        self.output_manager.register_writer(CommandWriter())
        self.output_manager.register_writer(MetadataWriter())
        self.output_manager.register_writer(FunctionWriter(callback=self._get_builtin_functions))
        self.output_manager.register_writer(LiteralPoolWriter())
        self.output_manager.register_writer(DependentDatapackWriter(self.get_dependency_files()))
        self.output_manager.register_writer(InitializerFunctionWriter())

    def generate(self):
        """生成代码（主流程）"""
        # 创建生成上下文
        context = GenerationContext(self.config, self.target, self.ir_builder)

        # 处理IR指令
        self._process_instructions(context)

        # 优化生成指令末尾的return
        for scope in context.get_all_scopes():
            if len(scope.commands) > 0 and scope.commands[-1].startswith("return "):
                scope.commands.pop()

        # 写入输出
        self._write_outputs(context)

    @staticmethod
    def is_support(config: CompileConfig) -> bool:
        version = config.version
        if version.display_version != "1.21.5" or version.is_bedrock_edition():
            return False
        if config.recursion or config.experimental:
            return False
        return True

    @staticmethod
    def get_name() -> str:
        return "java1.21.5"

    @functools.lru_cache(maxsize=None)
    def get_dependency_files(self) -> list[DependencyFile]:
        dnt_url = "https://github.com/Dahesor/DNT-Dahesor-NBT-Transformer/archive/refs/heads/pre-1.21.11.zip"
        if os.environ.get("USED_MIRROR_GITHUB_CN"):
            dnt_url = "https://gh-proxy.org/" +  dnt_url
        return [
            DependencyFile(
                dnt_url,
                "c764372d2a244832ede13d7d8f09dfeae14c1aae021f8cc2681303fb84acb189",
                71,  # 1.21.5
                94.1  # 1.21.11
            ),
        ]

    def _get_builtin_functions(self) -> dict[str, str]:
        templates: dict[str, str] = {}
        for template_ in TemplateRegistry.all().values():
            if self.config.debug:
                templates[template_.function_path] = \
                    f'''# {template_.function_path}
# {template_.name}({", ".join(template_.param_names)}, {", ".join(f"{name}={repr(value)}" for name, value in template_.optional_params.items())})
# {template_.description}
'''
            else:
                templates[template_.function_path] = ''
            templates[template_.function_path] += '\n'.join(
                f"${line}" if '$' in line else line for line in template_.template.split('\n'))
        return templates
