# coding=utf-8
from dovetail.core.annotations.base import (
    AnnotationProcessor, AnnotationResult
)
from dovetail.core.annotations.decorator import annotation_processor


@annotation_processor(name="doc", params={"text": ""})
class DocProcessor(AnnotationProcessor):

    def process(self, args, context):
        return AnnotationResult(metadata={"doc": args.get("text", "")})