# coding=utf-8
"""
符号解析器模块

负责符号表管理、符号查找、作用域管理等。
"""
from contextlib import contextmanager
from typing import Optional, Any

from lark.tree import Meta

from dovetail.core.enums import StructureType
from dovetail.core.errors import Errors

from dovetail.core.parser.tool.error_reporter import ErrorReporter
from dovetail.core.parser.scope import Scope
from dovetail.utils.string_similarity import suggest_similar


class SymbolResolver:
    """符号解析器 - 管理符号表和作用域"""

    def __init__(
            self,
            top_scope: Scope,
            error_reporter: ErrorReporter
    ):
        self.current_scope = top_scope
        self.scope_stack = [top_scope]
        self.error_reporter = error_reporter

    def resolve_symbol(
            self,
            name: str,
            meta: Meta,
            expected_type: Optional[type] = None
    ) -> Optional[Any]:
        """
        解析符号，未找到时报错并给出建议

        Args:
            name: 符号名
            meta: 元数据
            expected_type: 期望的符号类型（如 Function、Variable）

        Returns:
            找到的符号，未找到则返回 None
        """
        symbol = self.current_scope.resolve_symbol(name)

        if symbol is None:
            # 生成相似名称建议
            all_names = list(self.current_scope.get_all_symbols().keys())
            suggestion = suggest_similar(name, all_names)

            hint = f"你的意思是 '{suggestion}'？" if suggestion else None

            self.error_reporter.report(
                Errors.UndefinedSymbol,
                name,
                meta=meta,
                suggestion=hint
            )
            return None

        # 类型检查（如果指定了期望类型）
        if expected_type and not isinstance(symbol, expected_type):
            self.error_reporter.report(
                Errors.SymbolCategory,
                name,
                expected_type.__name__,
                symbol.__class__.__name__,
                meta=meta
            )
            return None

        return symbol

    def add_symbol(
            self,
            symbol: Any,
            meta: Optional[Meta] = None,
            force: bool = False
    ) -> bool:
        """
        添加符号到当前作用域

        Args:
            symbol: 要添加的符号
            meta: 元数据
            force: 是否强制覆盖同名符号

        Returns:
            True 表示添加成功，False 表示失败（符号重复）
        """
        if not self.current_scope.add_symbol(symbol, force=force):
            self.error_reporter.report(
                Errors.DuplicateDefinition,
                symbol.get_name(),
                meta=meta
            )
            return False
        return True

    @contextmanager
    def push_scope(
            self,
            name: str,
            scope_type: StructureType
    ):
        """
        作用域上下文管理器

        用法:
            with resolver.push_scope("func_body", StructureType.FUNCTION):
                # 这里是新作用域
                resolver.add_symbol(...)

        Args:
            name: 作用域名
            scope_type: 作用域类型

        Yields:
            新创建的作用域
        """
        new_scope = self.current_scope.create_child(name, scope_type)
        self.current_scope = new_scope
        self.scope_stack.append(new_scope)

        try:
            yield new_scope
        finally:
            if self.current_scope.parent:
                self.current_scope = self.current_scope.parent
                self.scope_stack.pop()

    def find_enclosing_scope(
            self,
            *scope_types: StructureType
    ) -> Optional[Scope]:
        """
        向上查找特定类型的作用域

        用法:
            loop_scope = resolver.find_enclosing_scope(
                StructureType.LOOP_CHECK,
                StructureType.LOOP_BODY
            )

        Args:
            *scope_types: 要查找的作用域类型（可以是多个）

        Returns:
            找到的作用域，未找到则返回 None
        """
        for scope in reversed(self.scope_stack):
            if scope.stype in scope_types:
                return scope
        return None
