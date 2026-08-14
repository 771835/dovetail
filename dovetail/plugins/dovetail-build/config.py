# coding=utf-8

from __future__ import annotations

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
from typing import Any

from dovetail.utils.logger import get_logger

logger = get_logger(__name__)


class DovetailConfig:
    """dovetail.toml 项目配置解析器 (DFP-401 §3.3.2)

    编译器不直接读取此文件——由本构建插件读取后，
    将参数传递给编译器命令行 (DFP-401 §3.3.4)。
    """

    def __init__(self, project_root: Path):
        self.root = project_root.resolve()
        self._data: dict[str, Any] = {}
        self._load()

    def _load(self) -> None:
        toml_path = self.root / "dovetail.toml"
        if not toml_path.exists():
            logger.warning(f"dovetail.toml not found in {self.root}")
            return
        try:
            with open(toml_path, "rb") as f:
                self._data = tomllib.load(f)
        except Exception as e:
            logger.error(f"Failed to parse dovetail.toml: {e}")

    # ── [package] ─────────────────────────────────────────────

    @property
    def name(self) -> str:
        return self._data.get("package", {}).get("name", "")

    @property
    def version(self) -> str:
        return self._data.get("package", {}).get("version", "0.0.0")

    @property
    def description(self) -> str:
        return self._data.get("package", {}).get("description", "")

    # ── [build] ───────────────────────────────────────────────

    @property
    def entry(self) -> str:
        """入口文件路径，对应编译器 <input>"""
        return self._data.get("build", {}).get("entry", "src/main.mcdl")

    @property
    def output(self) -> str:
        """输出目录，对应 -o"""
        return self._data.get("build", {}).get("output", "target")

    @property
    def tool(self) -> str:
        return self._data.get("build", {}).get("tool", "default")

    # ── [paths] ───────────────────────────────────────────────

    @property
    def sources(self) -> list[str]:
        return self._data.get("paths", {}).get("sources", ["src"])

    @property
    def libraries(self) -> list[str]:
        return self._data.get("paths", {}).get("libraries", ["lib"])

    @property
    def includes(self) -> list[str]:
        """额外搜索路径，未来对应 -I"""
        return self._data.get("paths", {}).get("includes", [])

    # ── [compiler] ────────────────────────────────────────────

    @property
    def lib_path(self) -> str:
        """标准库路径，对应 --lib-path"""
        return self._data.get("compiler", {}).get("lib_path", "")

    @property
    def optimization(self) -> int:
        """优化级别，对应 -O"""
        return self._data.get("compiler", {}).get("optimization", 2)

    @property
    def backend(self) -> str:
        """后端名称，对应 --backend"""
        return self._data.get("compiler", {}).get("backend", "")

    # ── [hooks] ───────────────────────────────────────────────

    @property
    def pre_build(self) -> str:
        return self._data.get("hooks", {}).get("pre_build", "")

    @property
    def post_build(self) -> str:
        return self._data.get("hooks", {}).get("post_build", "")

    # ── 转换为编译器参数 ──────────────────────────────────────

    def to_compiler_args(self) -> list[str]:
        """将 dovetail.toml 配置转换为编译器命令行参数 (DFP-401 §3.3.4)"""
        args = [str(self.root / self.entry)]

        if self.output:
            args.extend(["-o", self.output])

        if self.lib_path:
            args.extend(["--lib-path", self.lib_path])

        if self.optimization is not None:
            args.extend(["-O", str(self.optimization)])

        if self.backend:
            args.extend(["--backend", self.backend])

        return args