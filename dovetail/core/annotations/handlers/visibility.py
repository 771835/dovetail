# coding=utf-8
from dovetail.core.annotations import annotation_processor
from dovetail.core.annotations.base import (
    AnnotationProcessor, AnnotationResult, AnnotationTarget, AnnotationTiming
)


@annotation_processor
class InternalProcessor(AnnotationProcessor):
    annotation_name = "internal"
    applicable_targets = [AnnotationTarget.FUNCTION]
    timing = AnnotationTiming.POST_SYMBOL

    def process(self, args, ctx):
        return AnnotationResult(flags={"aggressive_opt"})


@annotation_processor
class NoinlineProcessor(AnnotationProcessor):
    annotation_name = "noinline"
    applicable_targets = [AnnotationTarget.FUNCTION]
    timing = AnnotationTiming.POST_SYMBOL

    def process(self, args, ctx):
        return AnnotationResult(flags={"no_inline"})


@annotation_processor
class RecursiveProcessor(AnnotationProcessor):
    annotation_name = "recursive"
    applicable_targets = [AnnotationTarget.FUNCTION]
    timing = AnnotationTiming.POST_SYMBOL

    def process(self, args, ctx):
        return AnnotationResult(flags={"allow_recursion", "no_inline"})
