# coding=utf-8
from __future__ import annotations

from typing import Dict, Type, Any

from attrs import define, field

from dovetail.core.annotations.base import (
    AnnotationProcessor, AnnotationContext, AnnotationResult, AnnotationTiming, AnnotationAttachment
)
from dovetail.core.annotations.spec import Annotation
from dovetail.core.errors import Errors


@define(slots=True)
class PreSymbolResult:
    """process_pre 的返回值，只含 skip"""
    skip: bool = False


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

    def register_class(self, cls: Type[AnnotationProcessor]):
        self.register(cls())

    def get(self, name: str) -> AnnotationProcessor | None:
        return self._processors.get(name)

    def process_pre(
            self,
            raw: dict,
            ctx: AnnotationContext,  # ctx.symbol 为 None
    ) -> PreSymbolResult:
        """
        处理所有 PRE_SYMBOL 注解。
        ctx.symbol 此时为 None，处理器不得访问。
        每个 PRE_SYMBOL 处理器只在此处被调用，不会出现在 process_post 中。
        """
        out = PreSymbolResult()
        for annotation, args in raw.items():
            processor = self._processors.get(annotation.name)
            if processor is None or processor.timing != AnnotationTiming.PRE_SYMBOL:
                continue
            result = self._execute(annotation.name, args, ctx, processor)
            out.skip = out.skip or result.skip
        return out

    def process_post(
            self,
            raw: dict,
            ctx: AnnotationContext,  # ctx.symbol 已存在
    ) -> PostSymbolResult:
        """
        处理所有 POST_SYMBOL 注解。
        ctx.symbol 此时已构造完毕，处理器可安全访问。
        每个 POST_SYMBOL 处理器只在此处被调用，不会出现在 process_pre 中。
        """
        out = PostSymbolResult()
        for annotation, args in raw.items():
            processor = self._processors.get(annotation.name)
            if processor is None or processor.timing != AnnotationTiming.POST_SYMBOL:
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
        """唯一执行入口，私有。process_pre 和 process_post 都经过这里。"""
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

    def validate_and_process_group(
            self,
            raw: dict[Annotation, dict[str, Any]],
            ctx: AnnotationContext,
            timing: AnnotationTiming,
    ) -> AnnotationResult:
        """处理指定时机的所有注解，返回合并结果。"""
        merged = AnnotationResult()
        for annotation, args in raw.items():
            processor = self._processors.get(annotation.name)
            if processor is None or processor.timing != timing:
                continue
            result = self.do_validate_and_process(annotation.name, args, ctx, processor)
            merged = merged.merge(result)
        return merged

    @staticmethod
    def do_validate_and_process(name, args, ctx: AnnotationContext,
                                processor: AnnotationProcessor) -> AnnotationResult:
        """实际执行校验+处理，内部复用。"""
        if processor.experimental and not ctx.config.experimental:
            ctx.error_reporter.report(
                Errors.AnnotationArgumentError,
                name, "此注解需要 --experimental 参数启用", meta=ctx.meta,
            )
            return AnnotationResult()

        if (processor.applicable_targets is not None
                and ctx.symbol_target not in processor.applicable_targets):
            ctx.error_reporter.report(
                Errors.AnnotationNotApplicable, name,
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
