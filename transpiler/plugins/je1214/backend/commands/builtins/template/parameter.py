# coding=utf-8
from enum import Enum
from typing import Any, Optional

from attrs import define

from transpiler.core.backend import Scope
from transpiler.core.symbols import Reference
from transpiler.core.enums.types import ValueType, DataTypeBase


class ParamBindingType(Enum):
    """参数绑定类型"""
    LITERAL = "literal"  # 直接值
    REFERENCE = "reference"  # 存储引用


@define(slots=True, frozen=True)
class TemplateParameter:
    """命令参数"""
    name: str
    value: Optional[int | str | bool]
    binding_type: ParamBindingType
    storage_path: str | None = None
    objective: str | None = None
    dtype: DataTypeBase | None = None

    @classmethod
    def from_reference(cls, name: str, ref: Reference, scope: Scope, objective: str):
        """从 Reference 创建参数"""
        if ref.value_type == ValueType.LITERAL:
            return cls(
                name=name,
                value=ref.value.value,
                binding_type=ParamBindingType.LITERAL,
                dtype=ref.get_data_type()
            )
        else:
            return cls(
                name=name,
                value=None,
                binding_type=ParamBindingType.REFERENCE,
                storage_path=scope.get_symbol_path(ref),
                objective=objective,
                dtype=ref.get_data_type()
            )

    @classmethod
    def literal(cls, name: str, value: Any):
        """创建字面量参数"""
        return cls(name=name, value=value, binding_type=ParamBindingType.LITERAL)

    @classmethod
    def reference(cls, name: str, storage_path: str, objective: str):
        """创建引用参数"""
        return cls(
            name=name,
            value=None,
            binding_type=ParamBindingType.REFERENCE,
            storage_path=storage_path,
            objective=objective
        )

    def is_literal(self) -> bool:
        return self.binding_type == ParamBindingType.LITERAL


class ParameterBuilder:
    """参数构建器 - 简化参数创建流程"""

    def __init__(self, scope: Scope, objective: str):
        self.scope = scope
        self.objective = objective

    def build(self, name: str, arg: Reference) -> TemplateParameter:
        """自动构建参数"""
        return TemplateParameter.from_reference(name, arg, self.scope, self.objective)

    def build_all(self, args: dict[str, Reference], param_names: list[str]) -> dict[str, TemplateParameter]:
        """批量构建参数"""
        return {
            name: self.build(name, args[name])
            for name in param_names
            if name in args
        }
