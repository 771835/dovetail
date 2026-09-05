# coding=utf-8
from typing import Any

from dovetail.core.annotations.base import (
    AnnotationProcessor, AnnotationContext, AnnotationResult
)
from dovetail.core.annotations.category import AnnotationCategory
from dovetail.core.annotations.decorator import annotation_processor
from dovetail.core.symbols import Function, Variable, Class


@annotation_processor(
    name="if_symbol",
    category=AnnotationCategory.CONDITION,
    params={"name": "", "type": "any"},
)
class IfSymbolProcessor(AnnotationProcessor):
    repeatable = True

    def process(self, args: dict[str, Any], context: AnnotationContext) -> AnnotationResult:
        name = args.get("name", "")
        type_ = args.get("type", "any")
        symbol = context.symbol_resolver.current_scope.resolve_symbol(name)

        if symbol is None:
            return AnnotationResult(skip=True)

        if type_ == "any":
            return AnnotationResult()

        type_map = {"class": Class, "function": Function, "variable": Variable}
        expected_cls = type_map.get(type_)

        return AnnotationResult(
            skip=expected_cls is not None and not isinstance(symbol, expected_cls)
        )