# coding=utf-8
"""
Dovetail 构建编排器

职责：读取 dovetail.toml → 执行 pre_build hook → 调用编译器 → 执行 post_build hook
编译器本身不读取 dovetail.toml，构建工具负责将配置转换为编译器命令行参数。
"""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

from dovetail.build.config import BuildConfig
from dovetail.build.hooks import run_hook
from dovetail.core.config import CACHE_FILE_PREFIX, IR_CACHE_FILE_PREFIX
from dovetail.utils.logger import get_logger
from dovetail.utils.resource import IS_COMPILED

logger = get_logger(__name__)


class Builder:
    """
    项目构建编排器

    负责编排完整的构建流程：
        pre_build hook → 编译器调用 → post_build hook

    不依赖插件系统，直接作为 CLI 程序 dovetail-build 的实现。

    Attributes:
        project_root: 项目根目录（绝对路径）
    """

    def __init__(self, project_root: Path):
        """
        Args:
            project_root: 包含 dovetail.toml 的项目根目录
        """
        self.project_root = project_root.resolve()

    # ── 构建入口 ──────────────────────────────────────────────

    def build(self) -> int:
        """
        执行完整构建流程

        Returns:
            0 表示成功，非 0 表示失败（遵循 DFP-604 §5.3 退出码约定）
        """
        # 解析并验证配置
        try:
            config = BuildConfig(self.project_root)
        except (FileNotFoundError, ValueError) as e:
            logger.error(str(e))
            return 2  # DFP-604 §5.3: 配置错误

        if config.tool not in ("dovetail", "dovetail-build", "default"):
            logger.error(f"项目需要使用构建工具 {config.tool}。")
            return 2  # DFP-604 §5.3: 配置错误

        logger.info(f"构建项目: {config.name} v{config.version}")

        # pre_build hook
        if config.pre_build:
            logger.info("执行 pre_build 钩子")
            if not run_hook(config.pre_build, self.project_root, "pre_build", config):
                logger.error("pre_build hook 失败，中止构建")
                return 3  # DFP-604 §5.3: 钩子失败

        # 调用编译器
        logger.info("编译文件中")
        try:
            args = self._build_compiler_args(config)
        except FileNotFoundError as e:
            logger.error(str(e))
            return 1

        ret = self._invoke_compiler(args)
        if ret != 0:
            logger.error(f"编译失败 (exit {ret})")
            return 1  # DFP-604 §5.3: 编译错误

        # post_build hook
        if config.post_build:
            logger.info("执行 post_build 钩子")
            if not run_hook(config.post_build, self.project_root, "post_build", config):
                logger.error("post_build hook 失败")
                return 3  # DFP-604 §5.3: 钩子失败

        logger.info("构建成功")
        return 0

    # ── 编译器调用 ────────────────────────────────────────────

    def _build_compiler_args(self, config: BuildConfig) -> list[str]:
        """
        将 dovetail.toml 配置转换为编译器命令行参数（DFP-604 §4.3）

        Args:
            config: 构建配置

        Returns:
            编译器命令行参数列表

        Raises:
            FileNotFoundError: 入口文件不存在
        """
        if IS_COMPILED:
            # 打包环境：同目录下的 dovetail.exe
            compiler_exe = Path(sys.executable).parent / "dovetail.exe"
            args = [str(compiler_exe)]
        else:
            # 普通 Python 环境
            import sys as _sys
            _main = Path(_sys.argv[0]).resolve().parent / "main.py"  # build_main和main在同目录
            args = [sys.executable, str(_main)]

        # 入口文件（必需）
        entry = self.project_root / config.entry
        if not entry.exists():
            raise FileNotFoundError(
                f"入口文件不存在: {entry}\n"
                f"  提示: 检查 dovetail.toml 中 [build].entry 配置。"
            )
        args.append(str(entry))

        # 输出目录 → -o
        if config.output:
            args.extend(["-o", str(self.project_root / config.output)])

        # 标准库路径 → --lib-path
        if config.lib_path:
            args.extend(["--lib-path", config.lib_path])

        # 优化级别 → -O
        args.extend(["-O", str(config.optimization)])

        # 后端 → --backend
        if config.backend:
            args.extend(["--backend", config.backend])

        # 命名空间 → --namespace（空则用 package.name）
        namespace = config.namespace or config.name
        if namespace:
            args.extend(["--namespace", namespace])

        # 调试模式 → --debug
        if config.debug:
            args.append("--debug")

        # 实验性功能 → --experimental
        if config.experimental:
            args.append("--experimental")

        # 禁止子进程编译器输出 info 日志（避免双重输出）
        args.append("--disable-info-logger")

        return args

    def _invoke_compiler(self, args: list[str]) -> int:
        """
        以子进程调用编译器（DFP-604 §2）

        Args:
            args: 编译器命令行参数

        Returns:
            编译器退出码
        """
        logger.debug(f"编译器命令: {' '.join(args)}")
        try:
            result = subprocess.run(args)
            return result.returncode
        except FileNotFoundError:
            logger.error("编译器可执行文件未找到")
            return 1
        except Exception as e:
            logger.error(f"编译器调用异常: {e}")
            return 1

    # ── 项目初始化 ────────────────────────────────────────────

    def init(self) -> int:
        """
        初始化项目骨架

        生成标准的 dovetail.toml、src/main.mcdl、hook/ 目录及 .gitignore。

        Returns:
            0 表示成功，非 0 表示失败
        """
        self.project_root.mkdir(parents=True, exist_ok=True)

        # dovetail.toml
        toml_path = self.project_root / "dovetail.toml"
        toml_path.write_text(
            "[package]\n"
            f'name = "{self.project_root.name}"\n'
            'version = "0.1.0"\n'
            "authors = []\n"
            'description = ""\n'
            'license = "MIT"\n'
            "\n"
            "[build]\n"
            'entry = "src/main.mcdl"\n'
            'output = "build"\n'
            'tool = "default"\n'
            'minecraft_version = ""\n'
            "\n"
            "[paths]\n"
            'sources = ["src"]\n'
            'libraries = ["lib"]\n'
            "includes = []\n"
            "\n"
            "[compiler]\n"
            'lib_path = ""\n'
            "optimization = 2\n"
            'backend = ""\n'
            'namespace = ""\n'
            "debug = false\n"
            "experimental = false\n"
            "\n"
            "[hooks]\n"
            'pre_build = "hook/pre_build.py"\n'
            'post_build = "hook/post_build.py"\n',
            encoding="utf-8",
        )
        logger.info(f"创建 {toml_path}")

        # src/main.mcdl
        main_mcdl = self.project_root / "src" / "main.mcdl"
        main_mcdl.parent.mkdir(parents=True, exist_ok=True)
        main_mcdl.write_text(
            "@init\n"
            "fn main() {\n"
            '    print("Hello, Dovetail!")\n'
            "}\n",
            encoding="utf-8",
        )
        logger.info(f"创建 {main_mcdl}")

        # hook/pre_build.py
        hook_dir = self.project_root / "hook"
        hook_dir.mkdir(parents=True, exist_ok=True)

        pre_hook = hook_dir / "pre_build.py"
        pre_hook.write_text(
            "#!/usr/bin/env python3\n"
            "import os\n"
            'print("[pre_build] Ready.")\n'
            'print(f"  项目根目录: {os.environ.get(\'DOVETAIL_PROJECT_ROOT\', \'\')}")\n',
            encoding="utf-8",
        )
        logger.info(f"创建 {pre_hook}")

        # hook/post_build.py
        post_hook = hook_dir / "post_build.py"
        post_hook.write_text(
            "#!/usr/bin/env python3\n"
            "import os\n"
            'print("[post_build] Done.")\n'
            'print(f"  构建输出: {os.environ.get(\'DOVETAIL_BUILD_DIR\', \'\')}")\n',
            encoding="utf-8",
        )
        logger.info(f"创建 {post_hook}")

        # .gitignore
        gitignore = self.project_root / ".gitignore"
        gitignore.write_text(
            "/build/\n"
            "/target/\n"
            "*.mcdc\n",
            encoding="utf-8",
        )
        logger.info(f"创建 {gitignore}")

        logger.info(f"项目初始化完成: {self.project_root}")
        return 0

    # ── 清理垃圾文件 ────────────────────────────────────────────

    def clean(self) -> int:
        """
        清理垃圾文件

        删除 build 等目录。

        Returns:
            0 表示成功，非 0 表示失败
        """
        # 解析并验证配置
        try:
            config = BuildConfig(self.project_root)
            for p in config.output:
                shutil.rmtree(self.project_root / p, ignore_errors=True)
        except (FileNotFoundError, ValueError):
            pass # 跳过以便于清理其他内容

        for file_path in self.project_root.rglob(f"*"):
            if file_path.is_file() and file_path.suffix in (CACHE_FILE_PREFIX, IR_CACHE_FILE_PREFIX):
                try:
                    file_path.unlink()  # 删除文件
                    logger.debug(f"删除了文件 {file_path}")
                except Exception as e:
                    logger.warning(f"删除失败 {file_path}: {e}")
            elif file_path.is_dir() and file_path.name == "__pycache__":
                try:
                    shutil.rmtree(file_path)
                    logger.debug(f"删除了 Python 缓存目录 {file_path}")
                except (OSError, FileNotFoundError):
                    pass
        return 0
