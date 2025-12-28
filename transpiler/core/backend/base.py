# coding=utf-8
"""
后端基类
"""
from abc import ABC, abstractmethod
from pathlib import Path

from transpiler.core.backend.context import GenerationContext
from transpiler.core.backend.output import OutputManager
from transpiler.core.backend.processor import ProcessorRegistry
from transpiler.core.compile_config import CompileConfig
from transpiler.core.ir_builder import IRBuilder


class Backend(ABC):
    """后端基类"""

    # 核心组件
    processor_registry = ProcessorRegistry()
    output_manager = OutputManager()

    def __init__(self, ir_builder: IRBuilder, target: Path, config: CompileConfig):
        self.ir_builder = ir_builder
        self.target = target
        self.config = config

    @staticmethod
    @abstractmethod
    def is_support(config: CompileConfig) -> bool:
        """判断是否支持该配置"""
        raise NotImplementedError()

    @staticmethod
    @abstractmethod
    def get_name() -> str:
        """获取后端名称"""
        raise NotImplementedError()

    def generate(self):
        """生成代码（主流程）"""
        # 创建生成上下文
        context = GenerationContext(config=self.config, target=self.target)

        # 处理IR指令
        self._process_instructions(context)

        # 写入输出
        self._write_outputs(context)

    def _process_instructions(self, context: GenerationContext):
        """处理所有IR指令"""
        for instruction in self.ir_builder:
            processor = self.processor_registry.get_processor(instruction.opcode)

            try:
                processor.process(instruction, context)
            except Exception as e:
                print(f"[ERROR] Failed to process {instruction.opcode.name}: {e}")
                if self.config.debug:
                    raise

    def _write_outputs(self, context: GenerationContext):
        """写入所有输出"""
        self.output_manager.write_all(context)
