# coding=utf-8
"""
作用域 Mixin 系统协议定义

定义所有 mixin 必须遵循的接口契约，确保类型安全和互操作性。
"""
from typing import Self, Protocol

from dovetail.core.enums.types import StructureType
from dovetail.core.symbols.base import Symbol


class ScopeCore(Protocol):
    """作用域核心属性协议"""
    name: str
    parent: Self | None
    stype: StructureType

    def __init__(self, name: str, parent: Self | None, structure_type: StructureType):
        """初始化核心属性"""
        ...  # 由 mixin 实现


class SymbolContainer(Protocol):
    """符号容器协议"""
    symbols: dict[str, Symbol]


class HierarchyContainer(Protocol):
    """层级容器协议"""
    children: list[Self]


class SymbolResolver(Protocol):
    """符号解析协议"""

    def find_symbol(self, name: str) -> Symbol | None: ...

    def resolve_symbol(self, name: str) -> Symbol | None: ...
