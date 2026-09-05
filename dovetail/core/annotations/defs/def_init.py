# coding=utf-8
from dovetail.core.annotations.base import (
    AnnotationProcessor, AnnotationResult, AnnotationTarget
)
from dovetail.core.annotations.category import AnnotationCategory
from dovetail.core.annotations.decorator import annotation_processor


@annotation_processor(name="init", category=AnnotationCategory.LIFECYCLE)
class InitProcessor(AnnotationProcessor):
    applicable_targets = [AnnotationTarget.FUNCTION]

    def process(self, args, context):
        return AnnotationResult(
            flags={"load_hook", "no_dce"},
            metadata={"hook_type": "load"},
        )