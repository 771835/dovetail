from __future__ import annotations

from pathlib import Path
from typing import Optional


class ImportManager:
    def __init__(self):
        self._search_paths = set()
        self._import_registry = set()  # 存储实际导入的路径

    def add_search_path(self, path: str) -> None:
        """添加搜索路径（自动规范化）"""
        self._search_paths.add(str(Path(path).resolve()))

    def find_candidates(self, import_path: str) -> list[str]:
        """返回所有候选路径（不修改状态）"""
        target = Path(import_path)
        candidates = []

        # 处理绝对路径
        if target.is_absolute():
            try:
                resolved = target.resolve()
                if resolved.is_file():
                    candidates.append(str(resolved))
            except FileNotFoundError:
                pass
            return candidates

        # 处理相对路径
        for base in self._search_paths:
            full_path = Path(base).joinpath(target).resolve()
            try:
                if full_path.is_file():
                    candidates.append(str(full_path))
            except FileNotFoundError:
                continue

        return candidates

    def execute_import(self, import_path: str) -> Optional[str]:
        """执行导入操作，返回实际导入的路径"""
        candidates = self.find_candidates(import_path)
        if not candidates:
            return None

        # 模拟实际导入行为：选择第一个找到的路径
        actual_path = candidates[0]
        self._import_registry.add(actual_path)
        return actual_path

    def has_imported(self, import_path: str) -> bool:
        """检查是否已执行过导入操作"""
        candidates = self.find_candidates(import_path)
        return any(p in self._import_registry for p in candidates)

    def exists_in_search_path(self, import_path: str) -> bool:
        """仅检查文件是否存在（不涉及导入状态）"""
        return bool(self.find_candidates(import_path))
