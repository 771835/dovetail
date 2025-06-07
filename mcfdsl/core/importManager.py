from __future__ import annotations

import os


class ImportManager:
    def __init__(self):
        self.imported = set()  # 已导入文件

    def resolve_path(self, import_path: str):
        return os.path.abspath(import_path)

    def add_import(self, import_path: str) -> None:
        self.imported.add(self.resolve_path(import_path))
        return

    def is_exist(self, import_path: str):
        return self.resolve_path(import_path) in self.imported
