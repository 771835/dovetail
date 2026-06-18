# coding=utf-8
from __future__ import annotations
from abc import ABC, abstractmethod
from enum import auto
from typing import Any, TYPE_CHECKING

from attrs import define, field

from dovetail.core.symbols.class_ import Class
from dovetail.core.symbols.function import Function
from dovetail.core.symbols.enumeration import Enumeration
from dovetail.core.symbols.structure import Structure
from dovetail.utils.safe_enum import SafeEnum

if TYPE_CHECKING:
    from lark.tree import Meta

    from dovetail.core.enums import FunctionType
    from dovetail.core.compile_config import CompileConfig
    from dovetail.core.parser.components import ErrorReporter, SymbolResolver

CAN_ANNOTATION_SYMBOLS = Class | Structure | Enumeration | Function


class AnnotationTarget(SafeEnum):
    """注解可作用于的符号类型"""
    FUNCTION = "function"
    VARIABLE = "variable"
    CLASS = "class"
    STRUCT = "struct"
    ENUM = "enum"


class AnnotationTiming(SafeEnum):
    """
    注解语义的执行时机。

    PRE_SYMBOL:  符号对象创建之前执行（条件编译类）
    POST_SYMBOL: 符号对象创建之后执行（标记类、校验类）
    """
    PRE_SYMBOL = auto()
    POST_SYMBOL = auto()


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
    skip: bool = False  # 需要在 AnnotationTiming.PRE_SYMBOL 时机执行
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


@define(slots=True)
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
    symbol_resolver: SymbolResolver = None


class AnnotationProcessor(ABC):
    """注解处理器基类"""

    annotation_name: str = None
    applicable_targets: list[AnnotationTarget] | None = None  # None = 不限
    repeatable: bool = False
    experimental: bool = False
    timing: AnnotationTiming = AnnotationTiming.PRE_SYMBOL

    def validate(self, args: dict[str, Any], ctx: AnnotationContext) -> bool:
        """
        参数校验。校验失败时自行调用 ctx.error_reporter.report()，返回 False。
        默认实现：直接通过。
        """
        return True

    @abstractmethod
    def process(
            self,
            args: dict[str, Any],
            ctx: AnnotationContext,
    ) -> AnnotationResult:
        """执行注解语义，返回结构化结果。"""
        raise NotImplementedError


class AnnotationCategory(SafeEnum):
    """
    注解系统声明类型

    用于区分注解类型并根据注解类型在不同时机处理

    Attributes:
        LIFECYCLE: 控制函数执行时机
        VISIBILITY: 控制可见性和优化
        LINKAGE: 控制后端链接接口指令的生成
        CONDITION: 条件编译
        METADATA: 元数据注解，不影响编译逻辑
    """
    # 核心语义注解 - 影响代码生成和执行
    LIFECYCLE = "lifecycle"  # 控制函数执行时机
    VISIBILITY = "visibility"  # 控制可见性和优化
    LINKAGE = "linkage"  # 控制后端链接接口指令的生成
    BACKEND_HINT = "backend_hint"  # 控制后端代码生成

    # 条件编译注解 - 在AST遍历阶段处理
    CONDITION = "condition"  # 控制代码编译生成

    # 元数据注解 - 不影响编译逻辑
    METADATA = "metadata"  # 元数据注解
