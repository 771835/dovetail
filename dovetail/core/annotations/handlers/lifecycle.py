# coding=utf-8

from dovetail.core.annotations import annotation_processor
from dovetail.core.annotations.base import (
    AnnotationProcessor, AnnotationResult, AnnotationTarget, AnnotationTiming
)
from dovetail.core.errors import Errors


@annotation_processor
class InitProcessor(AnnotationProcessor):
    annotation_name = "init"
    applicable_targets = [AnnotationTarget.FUNCTION]
    timing = AnnotationTiming.POST_SYMBOL

    def process(self, args, ctx):
        return AnnotationResult(
            flags={"load_hook", "no_dce"},
            metadata={"hook_type": "load"},
        )


@annotation_processor
class TickProcessor(AnnotationProcessor):
    annotation_name = "tick"
    applicable_targets = [AnnotationTarget.FUNCTION]
    timing = AnnotationTiming.POST_SYMBOL

    def validate(self, args, ctx):
        interval = args.get("interval", 1)
        if not isinstance(interval, int) or interval < 1:
            ctx.error_reporter.report(
                Errors.AnnotationArgumentError,
                "tick", "interval 必须是正整数", meta=ctx.meta,
            )
            return False
        return True

    def process(self, args, ctx):
        return AnnotationResult(
            flags={"tick_hook", "no_dce"},
            metadata={"hook_type": "tick", "interval": args.get("interval", 1)},
        )
