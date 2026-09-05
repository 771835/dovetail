# coding=utf-8
from typing import Any

from dovetail.core.annotations.base import (
    AnnotationProcessor, AnnotationContext, AnnotationResult
)
from dovetail.core.annotations.category import AnnotationCategory
from dovetail.core.annotations.decorator import annotation_processor


@annotation_processor(name="if_not_exists", category=AnnotationCategory.CONDITION)
class IfNotExistsProcessor(AnnotationProcessor):
    repeatable = True

    def process(self, args: dict[str, Any], context: AnnotationContext) -> AnnotationResult:
        return AnnotationResult(skip=context.symbol_resolver.current_scope.resolve_symbol(
            context.symbol_name
        ) is not None)