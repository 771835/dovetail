# coding=utf-8
"""
AST解析的作用域
"""
from __future__ import annotations
from dovetail.core.enums import StructureType
from dovetail.core.scope.mixins.base import CoreMixin, SymbolStorageMixin, SymbolResolutionMixin, HierarchyMixin


class Scope(
    CoreMixin, SymbolStorageMixin,
    SymbolResolutionMixin, HierarchyMixin
):
    def __init__(self, name: str, parent: Scope | None, structure_type: StructureType):
        super().__init__(name, parent, structure_type)
        SymbolStorageMixin.__init__(self)
        HierarchyMixin.__init__(self)
