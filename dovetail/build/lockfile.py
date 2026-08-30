# coding=utf-8
"""
dovetail.lock 管理

Lock 文件记录依赖的精确 commit hash，确保构建可复现。
- tag/rev: 不可变，lock 主要用于跳过网络请求（缓存加速）
- branch: 可变，lock 确保可复现性（锁定某次构建的精确 commit）
"""
from __future__ import annotations

import sys
from pathlib import Path

if sys.version_info >= (3, 11):
    import tomllib
else:
    try:
        import tomli as tomllib
    except ImportError:
        raise ImportError("Python < 3.11 环境需安装 tomli: pip install tomli")

from dovetail.build.dependencies import ResolvedDependency
from dovetail.utils.logger import get_logger

logger = get_logger(__name__)

LOCK_FILENAME = "dovetail.lock"


def load_lock(project_root: Path) -> dict[str, str]:
    """
    读取 lock 文件，返回 {name: resolved_commit} 映射

    文件不存在时返回空字典（首次构建）。
    """
    lock_path = project_root / LOCK_FILENAME
    if not lock_path.exists():
        return {}

    try:
        with open(lock_path, "rb") as f:
            data = tomllib.load(f)
    except Exception as e:
        logger.warning(f"dovetail.lock 解析失败，将重新解析依赖: {e}")
        return {}

    result = {}
    for entry in data.get("dependency", []):
        name = entry.get("name", "")
        resolved = entry.get("resolved", "")
        if name and resolved:
            result[name] = resolved
    return result


def write_lock(project_root: Path, resolved: list[ResolvedDependency]) -> None:
    """
    写入 lock 文件

    仅在依赖列表非空时写入。
    """
    if not resolved:
        return

    lock_path = project_root / LOCK_FILENAME
    lines = [
        '# 此文件由 dovetail-build 自动生成，请勿手动编辑\n',
        "\n",
    ]

    for dep in resolved:
        lines.append("[[dependency]]\n")
        for key, value in dep.to_lock_entry().items():
            lines.append(f'{key} = "{value}"\n')
        lines.append("\n")

    lock_path.write_text("".join(lines), encoding="utf-8")
    logger.debug(f"已更新 {LOCK_FILENAME}")