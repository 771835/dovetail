# coding=utf-8
"""
构建 Hook 执行器

通过子进程调用 `dovetail-build script <脚本>` 执行钩子。
环境变量由本模块在启动子进程前注入（DFP-604 §6.2），
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

from dovetail.build.config import BuildConfig
from dovetail.utils.logger import get_logger
from dovetail.utils.resource import IS_COMPILED

logger = get_logger(__name__)


def _build_env(config: BuildConfig, project_root: Path, hook_stage: str) -> dict[str, str]:
    """
    构造 DFP-604 §6.2 规定的环境变量字典

    基于当前进程环境变量，叠加构建工具注入的变量。
    所有路径均为绝对路径，空值设为空字符串。

    Args:
        config: 构建配置
        project_root: 项目根目录（绝对路径）
        hook_stage: 钩子执行阶段

    Returns:
        完整的环境变量字典，可直接传给 subprocess.run(env=...)
    """
    env = os.environ.copy()
    env.update({
        "DOVETAIL_PROJECT_ROOT": str(project_root),
        "DOVETAIL_PROJECT_CONFIG": str(config.root / "dovetail.toml"),
        "DOVETAIL_PROJECT_NAME": config.name,
        "DOVETAIL_BUILD_DIR": str(project_root / config.output),
        "DOVETAIL_ENTRY_FILE": str(project_root / config.entry),
        "DOVETAIL_BACKEND": config.backend,
        "DOVETAIL_OPTIMIZATION": str(config.optimization),
        "DOVETAIL_NAMESPACE": config.namespace or config.name,
        "DOVETAIL_LIB_PATH": config.lib_path,
        "DOVETAIL_VERSION": config.version,
        "DOVETAIL_MINECRAFT_VERSION": config.minecraft_version,
        "DOVETAIL_DEBUG": "1" if config.debug else "0",
        "DOVETAIL_EXPERIMENTAL": "1" if config.experimental else "0",
        "DOVETAIL_HOOK_STAGE": hook_stage,
    })
    return env


def run_hook(hook_path: str, project_root: Path, hook_stage: str, config: BuildConfig) -> bool:
    """
    执行构建钩子脚本（DFP-604 §6）

    通过子进程调用自身（dovetail-build script <脚本路径>），
    在启动子进程前注入环境变量，script 子命令直接执行脚本。

    Args:
        hook_path: 相对于 project_root 的脚本路径
        project_root: 项目根目录
        hook_stage: 钩子执行阶段
        config: 构建配置（用于生成环境变量）

    Returns:
        True 表示成功或脚本不存在（视为可选），False 表示失败
    """
    if not hook_path:
        return True

    script = (project_root / hook_path).resolve()

    if not script.exists():
        logger.warning(f"Hook 脚本未找到，跳过: {script}")
        return True

    logger.info(f"执行 Hook: {script}")

    # 构造子进程命令
    if IS_COMPILED:
        # 打包环境：sys.executable 就是 dovetail-build.exe
        cmd = [sys.argv[0], "script", str(script)]
    else:
        # 普通 Python 环境
        cmd = [sys.executable, sys.argv[0], "script", str(script)]

    logger.debug(f"执行参数：{cmd}")

    # 注入环境变量
    env = _build_env(config, project_root, hook_stage)

    try:
        result = subprocess.run(cmd, cwd=str(project_root), env=env, timeout=120)

        if result.returncode != 0:
            logger.error(f"Hook 执行失败 (exit {result.returncode}): {script}")
            return False

        return True

    except subprocess.TimeoutExpired:
        logger.error(f"Hook 执行超时: {script}")
        return False

    except FileNotFoundError as e:
        logger.error(f"执行器未找到: {e}")
        return False
    except Exception as e:
        logger.error(f"Hook 执行异常: {e}")
        return False
