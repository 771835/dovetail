# coding=utf-8
from typing import Any

from dovetail.core.annotations.base import AnnotationProcessor, AnnotationContext, AnnotationResult
from dovetail.core.annotations.decorator import annotation_processor
from dovetail.core.enums.minecraft import UnknownMinecraftVersionError
from dovetail.core.enums import MinecraftVersion, MinecraftEdition
from dovetail.core.errors import Errors
from dovetail.core.symbols import Function, Variable, Class


@annotation_processor
class VersionProcessor(AnnotationProcessor):
    annotation_name = "version"

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
        max_ver = MinecraftVersion.instance(args.get("max", "1.21.4"))
        return AnnotationResult(skip=not (min_ver <= context.config.version <= max_ver))


@annotation_processor
class TargetProcessor(AnnotationProcessor):
    annotation_name = "target"

    def process(self, args: dict[str, Any], context: AnnotationContext) -> AnnotationResult:
        target_edition = MinecraftEdition.from_str(args.get("edition", "java"))
        return AnnotationResult(skip=target_edition != context.config.version.edition)


@annotation_processor
class IfNotExistsProcessor(AnnotationProcessor):
    annotation_name = "if_not_exists"
    repeatable = True

    def process(self, args: dict[str, Any], context: AnnotationContext) -> AnnotationResult:
        return AnnotationResult(skip=context.symbol_resolver.current_scope.resolve_symbol(
            context.symbol_name
        ) is not None)


@annotation_processor
class IfSymbolProcessor(AnnotationProcessor):
    annotation_name = "if_symbol"
    repeatable = True

    def process(self, args: dict[str, Any], context: AnnotationContext) -> AnnotationResult:
        name = args.get("name", "")
        type_ = args.get("type", "any")
        symbol = context.symbol_resolver.current_scope.resolve_symbol(name)

        if symbol is None:
            return AnnotationResult(skip=True)  # 符号不存在 → 跳过

        if type_ == "any":
            return AnnotationResult()  # 符号存在，不跳过

        type_map = {"class": Class, "function": Function, "variable": Variable}
        expected_cls = type_map.get(type_)

        # 符号存在但类型不匹配 → 跳过
        return AnnotationResult(
            skip=expected_cls is not None and not isinstance(symbol, expected_cls)
        )

@annotation_processor
class IfFeatureProcessor(AnnotationProcessor):
    annotation_name = "if_feature"
    repeatable = True

    def process(self, args: dict[str, Any], context: AnnotationContext) -> AnnotationResult:
        feature = args.get("feature", "")
        if getattr(AnnotationContext.config, feature, None):
            return AnnotationResult(skip=True)
        return AnnotationResult()
