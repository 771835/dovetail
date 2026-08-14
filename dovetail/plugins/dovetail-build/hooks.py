# coding=utf-8

import subprocess
from pathlib import Path

from dovetail.utils.logger import get_logger

logger = get_logger(__name__)


def run_hook(hook_path: str, project_root: Path) -> bool:
    """执行编译钩子脚本 (DFP-401 §3.4)

    支持 .sh 和 .py 钩子。
    返回 True 表示成功，False 表示失败。
    """
    if not hook_path:
        return True

    script = project_root / hook_path
    if not script.exists():
        logger.warning(f"Hook script not found: {script}")
        return True

    logger.info(f"Running hook: {script}")

    try:
        if script.suffix == ".py":
            result = subprocess.run(
                ["python", str(script)],
                cwd=str(project_root),
                capture_output=True, text=True,
            )
        else:
            result = subprocess.run(
                ["bash", str(script)],
                cwd=str(project_root),
                capture_output=True, text=True,
            )

        if result.returncode != 0:
            logger.error(f"Hook failed (exit {result.returncode}): {result.stderr}")
            return False

        if result.stdout:
            logger.debug(f"Hook output: {result.stdout}")
        return True

    except Exception as e:
        logger.error(f"Hook execution error: {e}")
        return False
