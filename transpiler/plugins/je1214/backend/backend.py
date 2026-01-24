# coding=utf-8
from pathlib import Path

from transpiler.core.backend import Backend, TagWriter, CommandWriter, MetadataWriter, FunctionWriter
from transpiler.core.compile_config import CompileConfig
from transpiler.core.ir_builder import IRBuilder
from .literal_pool_writer import LiteralPoolWriter


class JE1214Backend(Backend):
    def __init__(self, ir_builder: IRBuilder, target: Path, config: CompileConfig):
        super().__init__(ir_builder, target, config)
        self.output_manager.register_writer(TagWriter())
        self.output_manager.register_writer(CommandWriter())
        self.output_manager.register_writer(MetadataWriter())
        self.output_manager.register_writer(FunctionWriter())
        self.output_manager.register_writer(LiteralPoolWriter())

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
