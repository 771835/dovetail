# coding=utf-8
from __future__ import annotations

from typing import Dict, Any

from attrs import define, field

from dovetail.core.annotations.base import (
    AnnotationProcessor, AnnotationContext, AnnotationResult, AnnotationAttachment
)
from dovetail.core.annotations.category import AnnotationTiming
from dovetail.core.errors import Errors


@define(slots=True)
class PreSymbolResult:
    """process_pre 的返回值，含 skip 和 metadata"""
    skip: bool = False
    metadata: dict[str, Any] = field(factory=dict)


@define(slots=True)
class PostSymbolResult:
    """process_post 的返回值，含符号写入所需的全部信息"""
    merged: AnnotationResult = field(factory=AnnotationResult)
    attachments: dict[str, AnnotationAttachment] = field(factory=dict)


class AnnotationRegistry:

    def __init__(self):
        self._processors: Dict[str, AnnotationProcessor] = {}

    def register(self, processor: AnnotationProcessor):
        if not processor.annotation_name:
            raise ValueError(f"{type(processor).__name__} 未指定 annotation_name")
        self._processors[processor.annotation_name] = processor

    def register_class(self, cls: type[AnnotationProcessor]):
        self.register(cls())

    def get(self, name: str) -> AnnotationProcessor | None:
        return self._processors.get(name)

    def process_pre(
            self,
            raw: dict,
            ctx: AnnotationContext,
    ) -> PreSymbolResult:
        """
        处理所有 PRE_SYMBOL 注解。
        ctx.symbol 此时为 None，处理器不得访问。
        修复：现在保留 metadata，不再丢弃。
        """
        out = PreSymbolResult()
        for annotation, args in raw.items():
            processor = self._processors.get(annotation.name)
            if processor is None or processor.effective_timing != AnnotationTiming.PRE_SYMBOL:
                continue
            result = self._execute(annotation.name, args, ctx, processor)
            out.skip = out.skip or result.skip
            out.metadata.update(result.metadata)  # ← 修复：保留 metadata
        return out

    def process_post(
            self,
            raw: dict,
            ctx: AnnotationContext,
    ) -> PostSymbolResult:
        """
        处理所有 POST_SYMBOL 注解。
        ctx.symbol 此时已构造完毕，处理器可安全访问。
        """
        out = PostSymbolResult()
        for annotation, args in raw.items():
            processor = self._processors.get(annotation.name)
            if processor is None or processor.effective_timing != AnnotationTiming.POST_SYMBOL:
                continue
            result = self._execute(annotation.name, args, ctx, processor)
            out.merged = out.merged.merge(result)
            out.attachments[annotation.name] = AnnotationAttachment(
                name=annotation.name,
                args=args,
                result=result,
            )
        return out

    def _execute(
            self,
            name: str,
            args: dict[str, Any],
            ctx: AnnotationContext,
            processor: AnnotationProcessor,
    ) -> AnnotationResult:
        """唯一执行入口，私有。"""
        if processor.experimental and not ctx.config.experimental:
            ctx.error_reporter.report(
                Errors.AnnotationArgumentError,
                name, "此注解需要 --experimental 参数启用", meta=ctx.meta,
            )
            return AnnotationResult()

        if (processor.applicable_targets is not None
                and ctx.symbol_target not in processor.applicable_targets):
            ctx.error_reporter.report(
                Errors.AnnotationNotApplicable,
                name,
                ctx.symbol_target.value if ctx.symbol_target else "unknown",
                meta=ctx.meta,
            )
            return AnnotationResult()

        if not processor.validate(args, ctx):
            return AnnotationResult()

        return processor.process(args, ctx)


_registry = AnnotationRegistry()


def get_registry() -> AnnotationRegistry:
    return _registry