# coding=utf-8
"""
后端框架核心模块
"""

from .base import Backend
from .context import GenerationContext, Scope
from .processor import IRProcessor, ProcessorRegistry, ir_processor
from .output import (
    OutputWriter, OutputManager,
    CommandWriter, FunctionWriter, MetadataWriter, TagWriter
)
from .factory import BackendFactory, BackendNotFoundError

__all__ = [
    # 基类
    'Backend',

    # 上下文
    'GenerationContext',
    'Scope',

    # 处理器
    'IRProcessor',
    'ProcessorRegistry',
    'ir_processor',

    # 输出
    'OutputWriter',
    'OutputManager',
    'CommandWriter',
    'FunctionWriter',
    'MetadataWriter',
    'TagWriter',

    # 工厂
    'BackendFactory',
    'BackendNotFoundError',
]