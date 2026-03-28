# coding=utf-8
"""
错误报告器模块

提供上下文感知的错误报告能力，作为全局 report 函数的门面。
"""
from contextlib import contextmanager
from pathlib import Path
from typing import Optional

from lark.tree import Meta

from dovetail.core.errors import report, Errors


class ErrorReporter:
    """错误报告器 - 提供上下文感知的错误报告"""

    def __init__(self, filepath: Path):
        self.filepath = filepath
        self.error_count = 0
        self.warning_count = 0
        self._context_stack: list[str] = []

    def report(
            self,
            error: Errors,
            *args: str,
            meta: Optional[Meta] = None,
            suggestion: Optional[str] = None
    ) -> None:
        """
        报告错误

        Args:
            error: 错误类型
            *args: 错误参数
            meta: 语法树元数据（包含行列号）
            suggestion: 修复建议
        """
        line, column = self._extract_position(meta)
        enhanced_suggestion = self._build_suggestion(suggestion)

        # 委托给全局 report 函数
        report(
            error,
            *args,
            filepath=self.filepath,
            line=line,
            column=column,
            suggestion=enhanced_suggestion
        )
        self.error_count += 1

    @contextmanager
    def context(self, description: str):
        """
        错误上下文管理器

        用法:
            with error_reporter.context("处理函数声明"):
                # 这里的错误会自动包含上下文信息
                ...

        Args:
            description: 上下文描述
        """
        self._context_stack.append(description)
        try:
            yield
        finally:
            self._context_stack.pop()

    def _build_suggestion(self, suggestion: Optional[str]) -> Optional[str]:
        """构建包含上下文的建议信息"""
        if not self._context_stack:
            return suggestion

        context_info = " → ".join(self._context_stack)
        context_hint = f"\n[上下文: {context_info}]"

        if suggestion:
            return f"{suggestion}{context_hint}"
        return context_hint

    def _extract_position(self, meta: Optional[Meta]) -> tuple[int, int]:
        """从 Meta 对象提取位置信息"""
        if meta is None:
            return -1, -1
        return meta.line, meta.column

    def has_errors(self) -> bool:
        """检查是否有错误"""
        return self.error_count > 0

    def set_filepath(self, filepath: Path) -> None:
        """更新当前文件路径（用于 include 处理）"""
        self.filepath = filepath