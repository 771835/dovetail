# coding=utf-8
"""
包含文件管理器模块

该模块提供 IncludeManager 类，用于跟踪和管理项目中已包含的文件路径，
以避免重复包含。主要功能包括记录包含历史、检查是否已包含某路径、检测循环依赖等。
"""

from pathlib import Path
from typing import Optional
from contextlib import contextmanager

from dovetail.core.errors import Errors
from dovetail.core.parser.components import ErrorReporter

class CircularIncludeException(Exception):
    """
    循环依赖异常

    当出现循环依赖时抛出
    """
    pass

class IncludeManager:
    """
    包含文件管理器

    负责跟踪和管理已包含的文件路径，避免重复包含和循环依赖。

    Attributes:
        error_reporter (ErrorReporter): 错误报告器
        entry_file (Optional[Path]): 编译入口文件路径
        _included_paths (set): 存储已包含的路径（已解析的绝对路径）。
        _include_history (list): 包含历史记录，保持插入顺序。
        _include_stack (list): 当前包含栈，用于检测循环依赖。
    """

    def __init__(self, error_reporter: ErrorReporter, entry_file: Optional[Path] = None):
        """
        初始化包含管理器

        Args:
            error_reporter (ErrorReporter): 错误报告器
            entry_file (Optional[Path]): 编译入口文件路径，如果提供则会自动添加到包含栈底部
        """
        self.error_reporter = error_reporter
        self.entry_file = entry_file.resolve() if entry_file else None
        self._included_paths = set()  # 存储已包含的路径
        self._include_history = []  # 包含历史记录
        self._include_stack = []  # 包含栈，用于循环依赖检测

        # 如果提供了入口文件，将其作为栈底
        if self.entry_file:
            self._include_stack.append(str(self.entry_file))

    @contextmanager
    def including(self, include_path: Path):
        """
        上下文管理器：在包含文件时使用

        检测循环依赖，并在包含期间维护包含栈。

        Args:
            include_path (Path): 正在包含的文件路径

        Raises:
            CircularIncludeException: 检测到循环依赖时抛出

        Usage:
            with include_manager.including(some_path):
                # 处理包含逻辑
                pass
        """
        resolved_path = str(include_path.resolve())

        with self.error_reporter.context(f"包含文件 {resolved_path}"):

            # 检测循环依赖
            if resolved_path in self._include_stack:
                self._report_circular_dependency(resolved_path)
                raise CircularIncludeException(f"Circular dependency detected: {resolved_path}")

            # 进入包含：将路径压入栈
            self._include_stack.append(resolved_path)

            try:
                yield self
            finally:
                # 退出包含：将路径弹出栈
                if self._include_stack and self._include_stack[-1] == resolved_path:
                    self._include_stack.pop()

    def _report_circular_dependency(self, current_path: str) -> None:
        """
        报告循环依赖错误

        Args:
            current_path (str): 触发循环的文件路径
        """
        # 找到循环开始的位置
        cycle_start_index = self._include_stack.index(current_path)

        # 完整的包含链（从入口到触发循环的文件）
        full_chain = self._include_stack + [current_path]

        # 构建易读的错误信息
        error_msg = "详细信息如下\n\n"

        # 显示完整的包含链
        error_msg += "包含链条:\n"
        for i, path in enumerate(full_chain):
            file_name = Path(path).name

            # 标记循环开始的位置
            if i == cycle_start_index:
                error_msg += f"  {i + 1}. {file_name}  ← 循环从这里开始\n"
            # 标记循环闭合的位置
            elif i == len(full_chain) - 1:
                error_msg += f"  {i + 1}. {file_name}  ← 尝试再次包含（错误）\n"
            else:
                error_msg += f"  {i + 1}. {file_name}\n"

        # 添加简短的解释
        error_msg += f"\n文件 '{Path(current_path).name}' 已被包含。"
        error_msg += "移除循环包含文件以修复此错误。"

        self.error_reporter.report(
                Errors.CircularInclude,
                error_msg,
            )

    def add_include_path(self, include_path: Path) -> None:
        """
        添加已包含的文件路径

        如果指定的路径尚未被包含，则将其加入内部集合和历史列表中。
        使用 resolve() 方法确保路径标准化。

        Args:
            include_path (Path): 要添加的包含文件路径。

        Returns:
            None: 无返回值。
        """
        resolved_path = str(include_path.resolve())
        if resolved_path not in self._included_paths:
            self._included_paths.add(resolved_path)
            self._include_history.append(resolved_path)  # 记录包含历史

    def has_path(self, include_path: Path) -> bool:
        """
        检查文件是否已包含

        Args:
            include_path (Path): 要检查的文件路径。

        Returns:
            bool: 如果文件已包含则返回True，否则返回False。
        """
        if not isinstance(include_path, Path):
            return False
        return str(include_path.resolve()) in self._included_paths

    def get_included_paths(self) -> list[str]:
        """
        获取所有已包含的文件路径列表

        Returns:
            list[str]: 已包含文件路径的列表。
        """
        return list(self._include_history)

    def get_include_stack(self) -> list[str]:
        """
        获取当前包含栈

        Returns:
            list[str]: 当前的包含调用栈。
        """
        return list(self._include_stack)

    def get_entry_file(self) -> Optional[Path]:
        """
        获取入口文件路径

        Returns:
            Optional[Path]: 入口文件路径，如果未设置则返回 None
        """
        return Path(self.entry_file) if self.entry_file else None

    def clear(self) -> None:
        """
        清除所有包含记录

        将已包含路径集合、包含历史列表和包含栈置为空。
        注意：入口文件会被保留在栈底。

        Returns:
            None: 无返回值。
        """
        self._included_paths.clear()
        self._include_history.clear()
        self._include_stack.clear()

        # 重新添加入口文件
        if self.entry_file:
            self._include_stack.append(str(self.entry_file))
            self._included_paths.add(str(self.entry_file))
            self._include_history.append(str(self.entry_file))

    def __len__(self) -> int:
        """
        返回已包含文件的数量

        Returns:
            int: 已包含文件的数量。
        """
        return len(self._included_paths)

    def __contains__(self, include_path: Path) -> bool:
        """
        支持 'in' 操作符

        判断指定路径是否已在已包含路径集合中。

        Args:
            include_path (Path): 要检查的路径。

        Returns:
            bool: 若路径存在于已包含集合中，返回 True；否则返回 False。
        """
        return self.has_path(include_path)