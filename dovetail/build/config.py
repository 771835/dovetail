# coding=utf-8
"""
dovetail.toml 项目配置解析器（DFP-604 §4.2）

编译器核心不读取此文件——由构建工具读取后，
将参数转换为编译器命令行传递。
"""
from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any

if sys.version_info >= (3, 11):
    import tomllib
else:
    try:
        import tomli as tomllib
    except ImportError:
        raise ImportError(
            "Python < 3.11 环境需安装 tomli: pip install tomli"
        )

from dovetail.utils.logger import get_logger

logger = get_logger(__name__)

_SEMVER_RE = re.compile(r'^\d+\.\d+\.\d+$')


class BuildConfig:
    """
    dovetail.toml 配置解析器（DFP-604 §4.2）

    Attributes:
        root: 项目根目录（绝对路径）
    """

    def __init__(self, project_root: Path):
        """
        Args:
            project_root: 包含 dovetail.toml 的项目根目录

        Raises:
            FileNotFoundError: dovetail.toml 不存在
            ValueError: TOML 解析失败或字段验证失败
        """
        self.root = project_root.resolve()
        self._data: dict[str, Any] = {}
        self._load()
        self._validate()

    def _load(self) -> None:
        """读取并解析 dovetail.toml"""
        toml_path = self.root / "dovetail.toml"
        if not toml_path.exists():
            raise FileNotFoundError(
                f"dovetail.toml 未找到: {toml_path}\n"
                f"  提示: 请在项目根目录运行，或使用 dovetail-build init 初始化项目。"
            )
        try:
            with open(toml_path, "rb") as f:
                self._data = tomllib.load(f)
        except Exception as e:
            raise ValueError(f"dovetail.toml 解析失败: {e}") from e

    def _validate(self) -> None:
        """验证必需字段（DFP-604 §4.4）"""
        if not self.name:
            raise ValueError("dovetail.toml: [package].name 不能为空")
        if not _SEMVER_RE.match(self.version):
            raise ValueError(
                f"dovetail.toml: [package].version 格式无效: {self.version!r}\n"
                f"  提示: 应为语义化版本，如 '1.0.0'"
            )
        if not self.entry:
            raise ValueError("dovetail.toml: [build].entry 不能为空")
        entry_path = self.root / self.entry
        if not entry_path.exists():
            raise ValueError(
                f"dovetail.toml: [build].entry 文件不存在: {entry_path}"
            )
        if not (0 <= self.optimization <= 3):
            raise ValueError(
                f"dovetail.toml: [compiler].optimization 必须为 0-3，当前: {self.optimization}"
            )

    # ── [package] ─────────────────────────────────────────────

    @property
    def name(self) -> str:
        """项目名称"""
        return self._data.get("package", {}).get("name", "")

    @property
    def version(self) -> str:
        """项目版本"""
        return self._data.get("package", {}).get("version", "0.0.0")

    @property
    def description(self) -> str:
        """项目描述"""
        return self._data.get("package", {}).get("description", "")

    # ── [build] ───────────────────────────────────────────────

    @property
    def entry(self) -> str:
        """入口文件路径（相对项目根目录），对应编译器 <input>"""
        return self._data.get("build", {}).get("entry", "src/main.mcdl")

    @property
    def output(self) -> str:
        """输出目录，对应编译器 -o"""
        return self._data.get("build", {}).get("output", ["build"])

    @property
    def tool(self) -> str:
        """构建工具名称"""
        return self._data.get("build", {}).get("tool", "default")

    @property
    def minecraft_version(self) -> str:
        """构建游戏版本"""
        return self._data.get("build", {}).get("minecraft_version", "")

    # ── [paths] ───────────────────────────────────────────────

    @property
    def source(self) -> str:
        """源码目录列表"""
        return self._data.get("paths", {}).get("source", "src")

    @property
    def library(self) -> str:
        """库目录列表"""
        return self._data.get("paths", {}).get("library", "")

    @property
    def includes(self) -> list[str]:
        """额外头文件搜索路径"""
        return self._data.get("paths", {}).get("includes", [])

    # ── [compiler] ────────────────────────────────────────────

    @property
    def lib_path(self) -> str:
        """标准库路径，对应编译器 --lib-path"""
        return self._data.get("compiler", {}).get("lib_path", "")

    @property
    def optimization(self) -> int:
        """优化级别，对应编译器 -O"""
        return int(self._data.get("compiler", {}).get("optimization", 2))

    @property
    def backend(self) -> str:
        """后端名称，对应编译器 --backend"""
        return self._data.get("compiler", {}).get("backend", "")

    @property
    def namespace(self) -> str:
        """数据包命名空间，对应编译器 --namespace；空则使用 package.name"""
        return self._data.get("compiler", {}).get("namespace", "")

    @property
    def debug(self) -> bool:
        """调试模式，对应编译器 --debug"""
        return bool(self._data.get("compiler", {}).get("debug", False))

    @property
    def experimental(self) -> bool:
        """实验性功能，对应编译器 --experimental"""
        return bool(self._data.get("compiler", {}).get("experimental", False))

    # ── [hooks] ───────────────────────────────────────────────

    @property
    def pre_build(self) -> str:
        """pre_build 钩子脚本路径（相对项目根目录）"""
        return self._data.get("hooks", {}).get("pre_build", "")

    @property
    def post_build(self) -> str:
        """post_build 钩子脚本路径（相对项目根目录）"""
        return self._data.get("hooks", {}).get("post_build", "")

    # ── [dependencies] ────────────────────────────────────────

    @property
    def dependencies(self) -> dict:
        """依赖声明（原始字典，由 dependencies.py 解析）"""
        return self._data.get("dependencies", {})

    def __repr__(self) -> str:
        return (
            f"BuildConfig(name={self.name!r}, version={self.version!r}, "
            f"entry={self.entry!r}, output={self.output!r})"
        )
