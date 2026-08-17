# coding=utf-8

import sys
from pathlib import Path

__all__ = ["resolve_project_path", "project_root", "IS_COMPILED"]

# Nuitka 打包后存在 __compiled__ 属性，不设置 sys.frozen
# PyInstaller 打包后设置 sys.frozen = True
try:
    __compiled__ # noqa
    IS_COMPILED = True
except NameError:
    IS_COMPILED = bool(getattr(sys, "frozen", False))


def _get_project_root() -> Path:
    """获取项目资源根目录，兼容所有部署模式"""
    if IS_COMPILED:
        if hasattr(sys, "_MEIPASS"):
            # PyInstaller
            return Path(sys._MEIPASS)
        else:
            # Nuitka
            return Path(sys.executable).parent
    else:
        # 普通 Python：入口脚本所在目录
        return Path(sys.argv[0]).resolve().parent


project_root = _get_project_root()  # 被导入时计算一次


def resolve_project_path(relative: str | Path) -> Path:
    """将项目相对路径解析为绝对路径"""
    return project_root / relative