# coding=utf-8
from pathlib import Path


class IncludeManager:
    """
    包含文件管理器

    负责跟踪和管理已导入的文件路径，避免重复导入。
    """

    def __init__(self):
        """初始化包含管理器"""
        self._included_paths = set()  # 存储实际导入的路径
        self._import_history = []  # 导入历史记录

    def add_include_path(self, include_path: Path) -> None:
        """
        添加已导入的文件路径

        Args:
            include_path: 要添加的包含文件路径
        """
        resolved_path = str(include_path.resolve())
        if resolved_path not in self._included_paths:
            self._included_paths.add(resolved_path)
            self._import_history.append(resolved_path)  # 记录导入历史

    def has_path(self, include_path: Path) -> bool:
        """
        检查文件是否已导入

        Args:
            include_path: 要检查的文件路径

        Returns:
            bool: 如果文件已导入则返回True，否则返回False
        """
        return str(include_path.resolve()) in self._included_paths

    def get_imported_paths(self) -> list[str]:
        """
        获取所有已导入的文件路径列表

        Returns:
            list[str]: 已导入文件路径的列表
        """
        return list(self._import_history)

    def clear(self) -> None:
        """清除所有导入记录"""
        self._included_paths.clear()
        self._import_history.clear()

    def __len__(self) -> int:
        """返回已导入文件的数量"""
        return len(self._included_paths)

    def __contains__(self, include_path: Path) -> bool:
        """支持 'in' 操作符"""
        return self.has_path(include_path)
