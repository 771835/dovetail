# coding=utf-8
from dovetail.core.annotations.base import (
    AnnotationProcessor, AnnotationResult
)
from dovetail.core.annotations.decorator import annotation_processor


@annotation_processor(name="since", params={"version": ""})
class SinceProcessor(AnnotationProcessor):

    def process(self, args, context):
        return AnnotationResult(metadata={"since": args.get("version", "")})