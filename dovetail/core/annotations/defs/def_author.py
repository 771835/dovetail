# coding=utf-8
from dovetail.core.annotations.base import (
    AnnotationProcessor, AnnotationResult
)
from dovetail.core.annotations.decorator import annotation_processor


@annotation_processor(name="author", params={"name": ""})
class AuthorProcessor(AnnotationProcessor):

    def process(self, args, context):
        return AnnotationResult(metadata={"author": args.get("name", "")})