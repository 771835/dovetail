# coding=utf-8
from dovetail.core.annotations.base import (
    AnnotationProcessor, AnnotationResult, AnnotationTiming
)
from dovetail.core.annotations.decorator import annotation_processor


@annotation_processor
class DeprecatedProcessor(AnnotationProcessor):
    annotation_name = "deprecated"
    timing = AnnotationTiming.PRE_SYMBOL  #

    def process(self, args, ctx):
        return AnnotationResult(
            skip=ctx.config.disable_deprecated_function,
            metadata={"deprecated_msg": args.get("msg", "")},
        )


@annotation_processor
class DocProcessor(AnnotationProcessor):
    annotation_name = "doc"
    timing = AnnotationTiming.POST_SYMBOL

    def process(self, args, ctx):
        return AnnotationResult(metadata={"doc": args.get("text", "")})


@annotation_processor
class AuthorProcessor(AnnotationProcessor):
    annotation_name = "author"
    timing = AnnotationTiming.POST_SYMBOL

    def process(self, args, ctx):
        return AnnotationResult(metadata={"author": args.get("name", "")})


@annotation_processor
class SinceProcessor(AnnotationProcessor):
    annotation_name = "since"
    timing = AnnotationTiming.POST_SYMBOL

    def process(self, args, ctx):
        return AnnotationResult(metadata={"since": args.get("version", "")})
