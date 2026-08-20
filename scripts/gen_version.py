#!/usr/bin/env python3
# coding=utf-8
"""构建时生成版本信息文件"""
import subprocess

import sys

# 兼容 Python 3.10 及更低版本与 Python 3.11+
if sys.version_info >= (3, 11):
    import tomllib
else:
    try:
        import tomli as tomllib
    except ImportError:
        raise ImportError("请在 Python < 3.11 环境下安装 tomli 库: pip install tomli")

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def get_git_last_commit_date() -> str:
    """获取所在提交的年月日"""
    try:
        return subprocess.check_output(
            ["git", "log", "-1", "--format=%cd", "--date=format:%Y%m%d"],
            stderr=subprocess.DEVNULL
        ).decode().strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "unknown"


def read_project_version() -> str:
    """从 dovetail.toml 读取版本号，dev 版本自动补充最后提交日期"""
    with open(ROOT / "dovetail.toml", "rb") as f:
        data = tomllib.load(f)
    version = data["package"]["version"]

    if version == "dev":
        date = get_git_last_commit_date()
        return f"dev{date}"  # → "dev20260801"

    return version


def get_git_commit_hash() -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            stderr=subprocess.DEVNULL
        ).decode().strip()[:8]
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "unknown"


def generate_version_file(output_path: Path):
    version = read_project_version()
    prev_hash = get_git_commit_hash()
    content = f'''# coding=utf-8
# 此文件由构建脚本自动生成，请勿手动修改
PROJECT_VERSION = "{version}"
COMMIT_HASH = "{prev_hash}"
'''
    output_path.write_text(content, encoding='utf-8')


if __name__ == '__main__':
    generate_version_file(ROOT / "dovetail" / "_version.py")