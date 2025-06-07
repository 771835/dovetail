from __future__ import annotations

from mcfdsl.core.result import Result
from mcfdsl.core.types import Type


class TypeUtils:
    @staticmethod
    def infer(expr_result: Result) -> Type | None:
        if expr_result is None:
            return None
        if expr_result.type_ != Type.TYPE_ANY:
            return expr_result.type_
        # 根据表达式结果的具体值推断
        if isinstance(expr_result.value, int):
            return Type.TYPE_INT
        elif isinstance(expr_result.value, str):
            return Type.TYPE_STRING
        elif isinstance(expr_result.value, bool):
            return Type.TYPE_BOOLEAN
        elif expr_result.value is None:
            return Type.TYPE_VOID
        else:
            return None
