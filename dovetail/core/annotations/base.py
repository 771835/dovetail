# dovetail/core/annotations/base.py
# coding=utf-8
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, TYPE_CHECKING

from attrs import define, field

from dovetail.core.annotations.category import AnnotationCategory, AnnotationTiming
from dovetail.core.annotations.targets import AnnotationTarget
from dovetail.core.symbols.class_ import Class
from dovetail.core.symbols.enumeration import Enumeration
from dovetail.core.symbols.function import Function
from dovetail.core.symbols.structure import Structure

if TYPE_CHECKING:
    from lark.tree import Meta
    from dovetail.core.enums import FunctionType
    from dovetail.core.compile_config import CompileConfig
    from dovetail.core.parser.components import ErrorReporter, SymbolResolver

CAN_ANNOTATION_SYMBOLS = Class | Structure | Enumeration | Function


@define(slots=True)
class AnnotationResult:
    """
    注解处理的结构化结果。

    三个消费方各取所需：
      visitor   → skip, type_override
      optimizer → flags
      backend   → flags, metadata

    See Also:
        skip 字段需要在 AnnotationTiming.PRE_SYMBOL 时机执行，因此 AnnotationTiming.POST_SYMBOL 跳过无效
    """
    # visitor 消费
    skip: bool = False
    type_override: FunctionType | None = None

    # optimizer 消费
    flags: set[str] = field(factory=set)

    # backend / 工具链消费
    metadata: dict[str, Any] = field(factory=dict)

    def merge(self, other: AnnotationResult) -> AnnotationResult:
        """合并同一符号上多个注解的结果"""
        return AnnotationResult(
            skip=self.skip or other.skip,
            type_override=(
                    other.type_override or self.type_override
            ),
            flags=self.flags | other.flags,
            metadata={**self.metadata, **other.metadata},
        )


@define(slots=True, repr=False)
class AnnotationAttachment:
    """附着在符号上的单个注解实例（处理后的完整信息）"""
    name: str
    args: dict[str, Any]
    result: AnnotationResult

    @property
    def flags(self) -> set[str]:
        return self.result.flags

    @property
    def metadata(self) -> dict[str, Any]:
        return self.result.metadata

    def __repr__(self):
        return f"({self.name!r}, {self.args!r})"


@define(slots=True)
class AnnotationContext:
    """
    注解处理上下文。
    处理器只依赖此对象，不依赖 visitor 本身。
    """
    config: CompileConfig
    error_reporter: ErrorReporter
    meta: Meta
    symbol_name: str = ""
    symbol: CAN_ANNOTATION_SYMBOLS | None = None
    symbol_target: AnnotationTarget | None = None
    symbol_resolver: SymbolResolver | None = None


class AnnotationProcessor(ABC):
    """注解处理器基类"""

    annotation_name: str
    applicable_targets: list[AnnotationTarget] | None = None  # None = 不限
    repeatable: bool = False
    experimental: bool = False
    timing: AnnotationTiming | None = None  # None = 由 category 推导
    category: AnnotationCategory = AnnotationCategory.METADATA  # 默认类别

    @property
    def effective_timing(self) -> AnnotationTiming:
        """实际执行时机：显式指定优先，否则从 category 推导"""
        if self.timing is not None:
            return self.timing
        return self.category.default_timing

    def validate(self, args: dict[str, Any], context: AnnotationContext) -> bool:
        """
        参数校验。校验失败时自行调用 context.error_reporter.report()，返回 False。
        默认实现：直接通过。
        """
        return True

    @abstractmethod
    def process(
            self,
            args: dict[str, Any],
            context: AnnotationContext,
    ) -> AnnotationResult:
        """执行注解语义，返回结构化结果。"""
        raise NotImplementedError