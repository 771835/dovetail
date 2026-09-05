# coding=utf-8
from typing import Any

from dovetail.core.annotations.base import (
    AnnotationProcessor, AnnotationContext, AnnotationResult
)
from dovetail.core.annotations.category import AnnotationCategory
from dovetail.core.annotations.decorator import annotation_processor
from dovetail.core.enums import MinecraftVersion
from dovetail.core.enums.minecraft import UnknownMinecraftVersionError
from dovetail.core.errors import Errors


@annotation_processor(
    name="version",
    category=AnnotationCategory.CONDITION,
    params={"min": "1.20.4", "max": "1.21.5"},
)
class VersionProcessor(AnnotationProcessor):

    def validate(self, args: dict[str, Any], context: AnnotationContext) -> bool:
        for key in ("min", "max"):
            try:
                MinecraftVersion.instance(args.get(key, "1.20.4"))
            except UnknownMinecraftVersionError:
                context.error_reporter.report(
                    Errors.UnsupportedTargetVersion,
                    str(args.get(key)),
                    meta=context.meta,
                )
                return False
        return True

    def process(self, args: dict[str, Any], context: AnnotationContext) -> AnnotationResult:
        min_ver = MinecraftVersion.instance(args.get("min", "1.20.4"))
        max_ver = MinecraftVersion.instance(args.get("max", "1.21.5"))
        return AnnotationResult(skip=not (min_ver <= context.config.version <= max_ver))