# coding=utf-8
from dovetail.core.annotations.base import (
    AnnotationProcessor, AnnotationResult, AnnotationTarget
)
from dovetail.core.annotations.category import AnnotationCategory
from dovetail.core.annotations.decorator import annotation_processor


@annotation_processor(name="internal", category=AnnotationCategory.VISIBILITY)
class InternalProcessor(AnnotationProcessor):
    applicable_targets = [AnnotationTarget.FUNCTION]

    def process(self, args, context):
        return AnnotationResult(flags={"aggressive_opt"})