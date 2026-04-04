# coding=utf-8
"""
辅助功能 Mixins - 命名、父访问、缓存等
"""
from typing import Optional

from dovetail.core.enums.types import StructureType
from dovetail.core.scope.protocols import ScopeCore
from dovetail.core.symbols import Symbol


class NamingMixin:
    """命名与路径管理"""

    def get_name(self: ScopeCore) -> str:
        """获取作用域名称"""
        return self.name

    def get_unique_name(self: ScopeCore, separator: str = '/') -> str:
        """
        获取唯一的完整路径名

        Args:
            separator: 路径分隔符，默认 '/'

        Returns:
            str: 完整的唯一路径名

        """
        if self.stype == StructureType.GLOBAL or self.parent is None:
            return "global"

        if hasattr(self.parent, 'get_unique_name'):
            return f"{self.parent.get_unique_name(separator)}{separator}{self.name}"

        return self.name

    def get_full_path(self: ScopeCore) -> str:
        """获取完整路径（同 get_unique_name）"""
        if hasattr(self, 'get_unique_name'):
            return self.get_unique_name()
        else:
            return self.name

    def get_display_name(self: ScopeCore) -> str:
        """
        获取用于显示的作用域名称

        不同类型的作用域可能有不同的显示格式。
        """
        type_prefix = {
            StructureType.GLOBAL: "global",
            StructureType.FUNCTION: "func",
            StructureType.CLASS: "class",
            StructureType.LOOP_CHECK: "loop_check",
            StructureType.LOOP_BODY: "loop_body",
            StructureType.INTERFACE: "interface",
            StructureType.CONDITIONAL: "cond",
        }

        prefix = type_prefix.get(self.stype, "scope")
        return f"{prefix}:{self.name}"


class ParentAccessMixin:
    """父作用域访问功能"""

    def get_parent(self: ScopeCore) -> ScopeCore:
        """
        获取父作用域

        如果不存在父作用域，返回自身（根作用域）

        Returns:
            ScopeCore: 父作用域或自身
        """
        return self.parent if self.parent else self

    def exist_parent(self: ScopeCore) -> bool:
        """
        检查是否存在父作用域

        Returns:
            bool: 存在父作用域返回 True
        """
        return self.parent is not None

    def get_root(self: ScopeCore) -> ScopeCore:
        """
        获取根作用域

        Returns:
            ScopeCore: 根作用域（全局作用域）
        """
        current = self
        while current.parent:
            current = current.parent
        return current

    def is_descendant_of(self: ScopeCore, other: ScopeCore) -> bool:
        """
        检查当前作用域是否是另一个作用域的后代

        Args:
            other: 祖先作用域

        Returns:
            bool: 是后代返回 True
        """
        current = self.parent
        while current:
            if current is other:
                return True
            current = current.parent
        return False


class CachingMixin:
    """
    符号解析缓存 mixin

    缓存解析结果以提升性能，适用于频繁查找的场景。
    """

    def __init__(self):
        """初始化缓存"""
        if not hasattr(self, '_symbol_cache'):
            self._symbol_cache: dict[str, Optional[Symbol]] = {}
        if not hasattr(self, '_cache_enabled'):
            self._cache_enabled = True

    def resolve_symbol(self: ScopeCore, name: str) -> Symbol | None:
        """带缓存的符号解析"""
        if not self._cache_enabled:
            return super().resolve_symbol(name)

        name = str(name)

        # 检查缓存
        if name in self._symbol_cache:
            return self._symbol_cache[name]

        # 解析并缓存
        symbol = super().resolve_symbol(name)
        self._symbol_cache[name] = symbol

        return symbol

    def invalidate_cache(self):
        """清除缓存"""
        self._symbol_cache.clear()

    def invalidate_symbol_cache(self, name: str):
        """清除指定符号的缓存"""
        self._symbol_cache.pop(str(name), None)

    def enable_cache(self):
        """启用缓存"""
        self._cache_enabled = True

    def disable_cache(self):
        """禁用缓存"""
        self._cache_enabled = False
