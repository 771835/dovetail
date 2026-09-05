# coding=utf-8
from typing import Any

from dovetail.core.annotations.base import (
    AnnotationProcessor, AnnotationContext, AnnotationResult
)
from dovetail.core.annotations.category import AnnotationCategory
from dovetail.core.annotations.decorator import annotation_processor


@annotation_processor(
    name="if_feature",
    category=AnnotationCategory.CONDITION,
    params={"feature": ""},
)
class IfFeatureProcessor(AnnotationProcessor):
    repeatable = True

    def process(self, args: dict[str, Any], context: AnnotationContext) -> AnnotationResult:
        feature = args.get("feature", "")
        if getattr(context.config, feature, None):
            return AnnotationResult(skip=True)
        return AnnotationResult()