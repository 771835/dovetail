# coding=utf-8
"""
注解处理器模块

负责注解提取、上下文构建、参数校验和两阶段处理流程。
"""
from typing import Any
from lark.tree import Meta

from dovetail.core.annotations import get_registry, AnnotationContext
from dovetail.core.annotations.base import AnnotationTarget, AnnotationCategory
from dovetail.core.annotations.spec import get_annotation_spec, Annotation
from dovetail.core.compile_config import CompileConfig
from dovetail.core.errors import Errors
from dovetail.core.parser.components.error_reporter import ErrorReporter
from dovetail.core.parser.components.symbol_resolver import SymbolResolver
from dovetail.core.symbols import Symbol, Function
from dovetail.core.symbols.base import Annotatable


class AnnotationProcessor:
    """注解处理器 - 管理注解的提取、校验和两阶段处理"""

    def __init__(
            self,
            config: CompileConfig,
            error_reporter: ErrorReporter,
            symbol_resolver: SymbolResolver
    ):
        self.config = config
        self.error_reporter = error_reporter
        self.symbol_resolver = symbol_resolver

    # ==================== 上下文构建 ====================

    def make_context(
            self,
            name: str,
            symbol: Symbol | None,
            target: AnnotationTarget,
            meta: Meta
    ) -> AnnotationContext:
        """
        构建注解处理上下文

        Args:
            name: 符号名
            symbol: 符号对象（PRE_SYMBOL 阶段可能为 None）
            target: 注解目标（FUNCTION / CLASS 等）
            meta: AST 元数据

        Returns:
            AnnotationContext 实例
        """
        return AnnotationContext(
            config=self.config,
            error_reporter=self.error_reporter,
            meta=meta,
            symbol_name=name,
            symbol=symbol, # noqa
            symbol_target=target,
            symbol_resolver=self.symbol_resolver,
        )

    # ==================== 校验 ====================

    def validate_and_resolve(
            self,
            name: str,
            children: list,
            meta: Meta
    ) -> tuple[Annotation | None, dict[str, Any] | None, bool]:
        """
        校验注解名和参数，返回处理结果。

        三段返回值的含义：
          - (annotation, param_dict, True)  → 校验通过，参数已就绪
          - (annotation, None, True)        → 校验通过，参数待 visit 填充
          - (None, {}, False)              → 校验失败

        Args:
            name: 注解名（如 "inline"、"export"）
            children: 参数子节点列表
            meta: 元数据

        Returns:
            (注解对象, 参数字典或None, 是否成功)
        """
        annotation = get_annotation_spec(name)

        # 注解不存在
        if annotation is None:
            self.error_reporter.report(Errors.InvalidAnnotation, name, meta=meta)
            return None, {}, False

        # 无参数注解
        if annotation.params is None:
            if children:
                self.error_reporter.report(
                    Errors.ArgumentNumberMismatch,
                    name, "0", str(len(children)), meta=meta
                )
            return annotation, {}, True

        # 参数数量不匹配
        if len(children) != len(annotation.params):
            self.error_reporter.report(
                Errors.ArgumentNumberMismatch,
                name, str(len(annotation.params)), str(len(children)), meta=meta
            )
            return None, {}, False

        # 参数数量匹配，等待 visit 填充
        return annotation, None, True

    @staticmethod
    def undefined_annotation() -> tuple[Annotation, dict]:
        """返回未定义注解的哨兵值"""
        return Annotation("undefined", None, AnnotationCategory.METADATA), {}

    # ==================== 两阶段处理流程 ====================

    def process_pre(
            self,
            raw_annotations: dict[Annotation, dict[str, Any]],
            name: str,
            target: AnnotationTarget,
            meta: Meta
    ) -> tuple[Any, AnnotationContext]:
        """
        PRE_SYMBOL 阶段：符号还未创建，注解可以先做跳过等决策。

        Args:
            raw_annotations: 提取到的注解字典
            name: 符号名
            target: 注解目标类型
            meta: 元数据

        Returns:
            (pre_result, ctx)  ctx 会被复用给 process_post
        """
        if not raw_annotations:
            return None, None

        ctx = self.make_context(name=name, symbol=None, target=target, meta=meta)
        pre = get_registry().process_pre(raw_annotations, ctx)
        return pre, ctx

    def process_post(
            self,
            raw_annotations: dict[Annotation, dict[str, Any]],
            pre_ctx: AnnotationContext,
            symbol: Annotatable
    ) -> Any:
        """
        POST_SYMBOL 阶段：符号已创建，注解可以修改符号属性。

        会自动给符号应用处理结果

        Args:
            raw_annotations: 提取到的注解字典
            pre_ctx: PRE_SYMBOL 阶段的上下文
            symbol: 已创建的符号对象

        Returns:
            post_result（含 attachments、merged 等）
        """
        if not raw_annotations:
            return None

        pre_ctx.symbol = symbol # noqa
        post = get_registry().process_post(raw_annotations, pre_ctx)

        if post.merged.type_override and isinstance(symbol, Function):
            symbol.func_type = post.merged.type_override

        if post:
            symbol.annotations.update(post.attachments)
        return post