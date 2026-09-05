# coding=utf-8
from dovetail.core.annotations.base import (
    AnnotationProcessor, AnnotationResult
)
from dovetail.core.annotations.category import AnnotationTiming
from dovetail.core.annotations.decorator import annotation_processor


@annotation_processor(name="deprecated", params={"msg": ""})
class DeprecatedProcessor(AnnotationProcessor):
    timing = AnnotationTiming.PRE_SYMBOL  # 显式覆盖：需要 skip 能力

    def process(self, args, context):
        return AnnotationResult(
            skip=context.config.disable_deprecated_function,
            metadata={"deprecated_msg": args.get("msg", "")},
        )