# coding=utf-8

import sys
from pathlib import Path

__all__ = ["resolve_project_path", "install_root", "IS_COMPILED", "COMPILED_BY", "IS_BROWSER"]

# Nuitka 打包后存在 __compiled__ 属性，不设置 sys.frozen
if "__compiled__" in globals():
    COMPILED_BY = "Nuitka"
elif getattr(sys, "frozen", False):
    # PyInstaller 打包后设置 sys.frozen = True
    COMPILED_BY = "PyInstaller"
else:
    COMPILED_BY = None

IS_COMPILED = COMPILED_BY is not None


IS_BROWSER = sys.platform == 'emscripten'

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
        # 普通 Python：入口脚本所在目录，根据此文件所在的位置计算
        return Path(__file__).resolve().parent.parent.parent


install_root = _get_project_root()  # 被导入时计算一次


def resolve_project_path(relative: str | Path) -> Path:
    """将项目相对路径解析为绝对路径"""
    return install_root / relative