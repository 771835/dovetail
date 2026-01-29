# coding=utf-8
"""
后端基类
"""
from abc import ABC, abstractmethod, ABCMeta
from pathlib import Path

from transpiler.core.backend.context import GenerationContext
from transpiler.core.backend.output import OutputManager
from transpiler.core.backend.processor import ProcessorRegistry
from transpiler.core.compile_config import CompileConfig
from transpiler.core.config import get_project_logger
from transpiler.core.ir_builder import IRBuilder


class BackendMeta(ABCMeta):
    """元类，确保每个子类有独立的类属性"""

    def __new__(cls, name, bases, attrs):
        # 创建新类
        new_class = super().__new__(cls, name, bases, attrs)

        # 为每个子类创建独立的实例
        if name != 'Backend':  # 避免为基类创建
            new_class.processor_registry = ProcessorRegistry()
            new_class.output_manager = OutputManager()

        return new_class


class Backend(ABC, metaclass=BackendMeta):
    """后端基类"""

    # 核心组件
    processor_registry: ProcessorRegistry = None
    output_manager: OutputManager = None

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
        context = GenerationContext(self.config, self.target, self.ir_builder)

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
                get_project_logger().error(f"Failed to process {instruction.opcode.name}: {e.__repr__()}")
                if self.config.debug:
                    raise

    def _write_outputs(self, context: GenerationContext):
        """写入所有输出"""
        self.output_manager.write_all(context)
