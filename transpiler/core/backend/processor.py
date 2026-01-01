# coding=utf-8
"""
指令处理器基类和注册系统
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Dict, Type, TYPE_CHECKING

if TYPE_CHECKING:
    from transpiler.core.backend import Backend
from transpiler.core.instructions import IROpCode, IRInstructionType
from transpiler.core.backend.context import GenerationContext


class IRProcessor(ABC):
    """IR指令处理器基类"""

    opcode: IROpCode = None  # 子类必须指定

    @abstractmethod
    def process(self, instruction: IRInstructionType, context: GenerationContext):
        """
        处理单个IR指令

        Args:
            instruction: IR指令对象
            context: 生成上下文
        """
        raise NotImplementedError(f"{self.__class__.__name__} must implement process()")

    def can_handle(self, instruction: IRInstructionType) -> bool:
        """判断是否能处理该指令"""
        return instruction.opcode == self.opcode


class DefaultProcessor(IRProcessor):
    """默认处理器，用于未实现的指令"""

    opcode = None

    def process(self, instruction: IRInstructionType, context: GenerationContext):
        opcode_name = instruction.opcode.name
        context.add_command(f"# WARNING: No processor for {opcode_name}")
        print(f"[WARNING] No processor registered for opcode: {opcode_name}")


class ProcessorRegistry:
    """处理器注册表"""

    def __init__(self):
        self._processors: Dict[IROpCode, IRProcessor] = {}
        self._default_processor = DefaultProcessor()

    def register(self, processor: IRProcessor):
        """
        注册处理器

        Args:
            processor: 处理器实例
        """
        if processor.opcode is None:
            raise ValueError(f"Processor {processor.__class__.__name__} must specify opcode")

        if processor.opcode in self._processors:
            print(f"[WARNING] Overwriting processor for {processor.opcode.name}")

        self._processors[processor.opcode] = processor

    def register_class(self, processor_class: Type[IRProcessor]):
        """
        注册处理器类（会自动实例化）

        Args:
            processor_class: 处理器类
        """
        processor = processor_class()
        self.register(processor)

    def register_batch(self, processors: list[IRProcessor]):
        """批量注册处理器"""
        for processor in processors:
            self.register(processor)

    def get_processor(self, opcode: IROpCode) -> IRProcessor:
        """
        获取指令对应的处理器

        Args:
            opcode: 指令操作码

        Returns:
            处理器实例，如果未找到则返回默认处理器
        """
        return self._processors.get(opcode, self._default_processor)

    def has_processor(self, opcode: IROpCode) -> bool:
        """检查是否注册了指定指令的处理器"""
        return opcode in self._processors

    def get_all_opcodes(self) -> list[IROpCode]:
        """获取所有已注册的操作码"""
        return list(self._processors.keys())

    def clear(self):
        """清空注册表"""
        self._processors.clear()


def ir_processor(target: type[Backend] | ProcessorRegistry, opcode: IROpCode):
    """
    装饰器：自动注册处理器到指定后端

    Examples:
        @ir_processor(Backend,IROpCode.ASSIGN)
        class AssignProcessor(IRProcessor):
            def process(self, instruction, context):
                passes
    """

    def decorator(cls: type[IRProcessor]):
        cls.opcode = opcode
        if isinstance(target, ProcessorRegistry):
            target.register_class(cls)
        else:
            target.processor_registry.register_class(cls)
        return cls

    return decorator
