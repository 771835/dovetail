# coding=utf-8
from dovetail.core.annotations.base import (
    AnnotationProcessor, AnnotationResult, AnnotationTarget
)
from dovetail.core.annotations.category import AnnotationCategory
from dovetail.core.annotations.decorator import annotation_processor
from dovetail.core.errors import Errors


@annotation_processor(
    name="tick",
    category=AnnotationCategory.LIFECYCLE,
    params={"interval": 1},
)
class TickProcessor(AnnotationProcessor):
    applicable_targets = [AnnotationTarget.FUNCTION]

    def validate(self, args, context):
        interval = args.get("interval", 1)
        if not isinstance(interval, int) or interval < 1:
            context.error_reporter.report(
                Errors.AnnotationArgumentError,
                "tick", "interval 必须是正整数", meta=context.meta,
            )
            return False
        return True

    def process(self, args, context):
        return AnnotationResult(
            flags={"tick_hook", "no_dce"},
            metadata={"hook_type": "tick", "interval": args.get("interval", 1)},
        )