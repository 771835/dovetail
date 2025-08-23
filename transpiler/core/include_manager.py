# coding=utf-8
from __future__ import annotations

from pathlib import Path


class IncludeManager:
    def __init__(self):
        self._include_registry = set()  # 存储实际导入的路径

    def add_include_path(self, include_path: Path):
        self._include_registry.add(str(include_path.absolute()))

    def has_path(self, include_path: Path) -> bool:
        """检查是否已执行过导入操作"""
        return str(include_path.absolute()) in self._include_registry
