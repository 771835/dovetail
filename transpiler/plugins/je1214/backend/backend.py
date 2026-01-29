# coding=utf-8
import functools
from pathlib import Path

from transpiler.core.backend import Backend, TagWriter, CommandWriter, MetadataWriter, FunctionWriter
from transpiler.core.backend.output import DependentDatapackWriter
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
        self.output_manager.register_writer(DependentDatapackWriter(self.get_dependencies()))

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

    @staticmethod
    @functools.lru_cache(maxsize=None)
    def get_dependencies() -> dict[str, tuple[str | None, int]]:
        return {
            "https://codeload.github.com/Dahesor/DNT-Dahesor-NBT-Transformer/zip/refs/heads/main":
                (
                    "6872f86b49fd28dfdbb231b8108b2eca2620c6dfb418f1142557e25de2fabb67",
                    61
                ),
            "https://cdn.modrinth.com/data/h94rwz9p/versions/vb7U4ITG/StringLib%20v0.1.0%20%281.21%29.zip":
                (
                    "9604b264fda4de2107fea5b02cdc52de88527ee9ba65717a674506894ba5933b",
                    61
                ),
        }
