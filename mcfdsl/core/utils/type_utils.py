# coding=utf-8
from __future__ import annotations

from typing import Any

from mcfdsl.core.language_types import DataType


class TypeUtils:
    @staticmethod
    def infer(value: Any) -> DataType | None:
        # 根据表达式结果的具体值推断
        if isinstance(value, int):
            return DataType.INT
        elif isinstance(value, str):
            return DataType.STRING
        elif isinstance(value, bool):
            return DataType.BOOLEAN
        elif value is None:
            return DataType.VOID
        else:
            return None
