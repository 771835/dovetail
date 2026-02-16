# coding=utf-8
"""
基础功能 Mixins - 作用域系统的构建块
"""
from dovetail.core.symbols.base import Symbol
from dovetail.core.enums.types import StructureType
from dovetail.core.scope.protocols import ScopeCore


class CoreMixin:
    """核心属性初始化 mixin"""

    def __init__(self, name: str, parent: ScopeCore | None, structure_type: StructureType):
        """初始化核心属性"""
        self.name = name
        self.parent = parent
        self.stype = structure_type


class SymbolStorageMixin:
    """
    符号存储与单层查询功能

    提供符号的添加、修改、删除和单层查找能力。
    """

    def __init__(self):
        """初始化符号表"""
        if not hasattr(self, 'symbols'):
            self.symbols: dict[str, Symbol] = {}

    def add_symbol(self, symbol: Symbol, force: bool = False) -> bool:
        """
        添加符号到当前作用域

        Args:
            symbol: 要添加的符号对象
            force: 是否强制覆盖同名符号

        Returns:
            bool: 添加成功返回 True，符号已存在且未强制时返回 False
        """
        symbol_name = symbol.get_name()
        if symbol_name in self.symbols and not force:
            return False
        self.symbols[symbol_name] = symbol
        return True

    def has_symbol(self, name: str) -> bool:
        """检查当前作用域是否存在符号"""
        return name in self.symbols

    def set_symbol(self, symbol: Symbol, force: bool = False) -> bool:
        """
        修改已存在的符号

        Args:
            symbol: 要修改的符号对象
            force: 是否允许添加新符号

        Returns:
            bool: 操作成功返回 True
        """
        symbol_name = symbol.get_name()
        if symbol_name not in self.symbols and not force:
            return False
        self.symbols[symbol_name] = symbol
        return True

    def remove_symbol(self, name: str) -> bool:
        """从当前作用域移除符号"""
        if name in self.symbols:
            del self.symbols[name]
            return True
        return False

    def get_symbols(self) -> dict[str, Symbol]:
        """获取当前作用域的所有符号"""
        return self.symbols.copy()

    def find_symbol(self, name: str) -> Symbol | None:
        """
        在当前作用域查找符号（单层查找）

        Args:
            name: 符号名称

        Returns:
            Symbol | None: 找到的符号或 None
        """
        return self.symbols.get(str(name), None)


class SymbolResolutionMixin:
    """
    符号解析功能 - 向上链式查找

    提供跨越作用域边界的符号解析能力。
    """

    def resolve_symbol(self: ScopeCore, name: str) -> Symbol | None:
        """
        逐级向上解析符号

        Args:
            name: 要解析的符号名称

        Returns:
            Symbol | None: 找到的符号或 None
        """
        name = str(name)
        current = self

        while current:
            if hasattr(current, 'find_symbol'):
                symbol = current.find_symbol(name)
                if symbol:
                    return symbol
            current = current.parent

        return None

    def resolve_symbol_in_chain(self: ScopeCore, name: str, chain: list[type] | None = None) -> Symbol | None:
        """
        在指定类型的作用域链中解析符号

        Args:
            name: 符号名称
            chain: 限制的作用域类型列表，None 表示不限制

        Returns:
            Symbol | None: 找到的符号或 None
        """
        name = str(name)
        current = self

        while current:
            if hasattr(current, 'find_symbol'):
                if chain is None or current.stype in chain:
                    symbol = current.find_symbol(name)
                    if symbol:
                        return symbol
            current = current.parent

        return None

    def get_all_symbols(self: ScopeCore) -> dict[str, Symbol]:
        """
        获得完整符号表

        Returns: 返回从当前作用域开始向上直到根作用域的符号表

        """
        scope_stack: list[ScopeCore] = []
        current = self
        while current:
            scope_stack.append(current)
            current = current.parent
        symbols: dict[str, Symbol] = {}
        while scope_stack:
            current = scope_stack.pop()
            if hasattr(current, 'symbols'):
                symbols.update(current.symbols)
        return symbols



class HierarchyMixin:
    """
    层级管理功能 - 作用域树的构建与导航
    """

    def __init__(self):
        """初始化子作用域列表"""
        if not hasattr(self, 'children'):
            self.children: list[ScopeCore] = []

    def create_child(self: ScopeCore, name: str, stype: StructureType) -> ScopeCore:
        """
        创建子作用域

        Args:
            name: 子作用域名称
            stype: 子作用域类型

        Returns:
            ScopeCore: 新创建的子作用域
        """
        # 使用当前类创建子作用域，保持类型一致性
        child = self.__class__(name, self, stype)
        self.children.append(child)
        return child

    def find_scope(self: ScopeCore, name: str) -> ScopeCore | None:
        """
        在直接子作用域中查找

        Args:
            name: 作用域名称

        Returns:
            ScopeCore | None: 找到的子作用域或 None
        """
        name = str(name)
        for child in self.children:
            if child.name == name:
                return child
        return None

    def resolve_scope(self: ScopeCore, name: str) -> ScopeCore | None:
        """
        逐级向上解析可访问的子作用域

        Args:
            name: 要解析的作用域名称

        Returns:
            ScopeCore | None: 找到的作用域或 None
        """
        name = str(name)
        current = self

        while current:
            if hasattr(current, 'find_scope'):
                scope = current.find_scope(name)
                if scope:
                    return scope
            current = current.parent

        return None

    def get_ancestors(self: ScopeCore) -> list[ScopeCore]:
        """
        获取所有祖先作用域（从父作用域到根）

        Returns:
            list[ScopeCore]: 祖先作用域列表
        """
        ancestors = []
        current = self.parent

        while current:
            ancestors.append(current)
            current = current.parent

        return ancestors

    def get_depth(self: ScopeCore) -> int:
        """
        获取当前作用域的深度（根作用域为 0）

        Returns:
            int: 作用域深度
        """
        return len(self.get_ancestors())