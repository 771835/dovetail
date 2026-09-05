# coding=utf-8
from typing import Any

from dovetail.core.annotations.base import (
    AnnotationProcessor, AnnotationContext, AnnotationResult
)
from dovetail.core.annotations.category import AnnotationCategory
from dovetail.core.annotations.decorator import annotation_processor
from dovetail.core.enums import MinecraftEdition


@annotation_processor(
    name="target",
    category=AnnotationCategory.CONDITION,
    params={"edition": "java"},
)
class TargetProcessor(AnnotationProcessor):

    def process(self, args: dict[str, Any], context: AnnotationContext) -> AnnotationResult:
        target_edition = MinecraftEdition.from_str(args.get("edition", "java"))
        return AnnotationResult(skip=target_edition != context.config.version.edition)