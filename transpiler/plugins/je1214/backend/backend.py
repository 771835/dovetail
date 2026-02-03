# coding=utf-8
import functools
from pathlib import Path

from transpiler.core.backend import Backend, TagWriter, CommandWriter, MetadataWriter, FunctionWriter
from transpiler.core.backend.context import DependencyFile
from transpiler.core.backend.output import DependentDatapackWriter
from transpiler.core.compile_config import CompileConfig
from transpiler.core.ir_builder import IRBuilder
from .commands.builtins import TemplateRegistry
from .initializer_function_writer import InitializerFunctionWriter
from .literal_pool_writer import LiteralPoolWriter

PACK_FORMAT_1214 = 61


class JE1214Backend(Backend):
    def __init__(self, ir_builder: IRBuilder, target: Path, config: CompileConfig):
        super().__init__(ir_builder, target, config)
        self.output_manager.register_writer(TagWriter())
        self.output_manager.register_writer(CommandWriter())
        self.output_manager.register_writer(MetadataWriter("A datapack of Minecraft 1.21.4"))
        self.output_manager.register_writer(FunctionWriter(callback=self._get_builtin_functions))
        self.output_manager.register_writer(LiteralPoolWriter())
        self.output_manager.register_writer(DependentDatapackWriter(self.get_dependency_files()))
        self.output_manager.register_writer(InitializerFunctionWriter())

    @staticmethod
    def is_support(config: CompileConfig) -> bool:
        version = config.version
        if version.display_version != "1.21.4" or version.is_bedrock_edition():
            return False
        if config.recursion or config.experimental:
            return False
        return True

    @staticmethod
    def get_name() -> str:
        return "je1214"

    @functools.lru_cache(maxsize=None)
    def get_dependency_files(self) -> list[DependencyFile]:
        return [
            # # dnt 很好，但是不支持1.21.4
            # DependencyFile(
            #     "https://codeload.github.com/Dahesor/DNT-Dahesor-NBT-Transformer/zip/refs/heads/main",
            #     "6872f86b49fd28dfdbb231b8108b2eca2620c6dfb418f1142557e25de2fabb67",
            #     get_datapack_format('1.21.4'),
            #     get_datapack_format('1.21.11')
            # ),
            DependencyFile(
                "https://cdn.modrinth.com/data/h94rwz9p/versions/vb7U4ITG/StringLib%20v0.1.0%20%281.21%29.zip",
                "9604b264fda4de2107fea5b02cdc52de88527ee9ba65717a674506894ba5933b",
                61,
                94.1,
            ),

        ]

    def _get_builtin_functions(self) -> dict[str, str]:
        templates: dict[str, str] = {}
        for template in TemplateRegistry.all().values():
            templates[template.function_path] = '\n'.join(
                f"${line}" if '$' in line else line for line in template.template.split('\n'))
        return templates
