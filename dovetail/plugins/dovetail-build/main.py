# coding=utf-8
import subprocess
import sys
from pathlib import Path

from dovetail.plugins.plugin_api.plugin import Plugin
from dovetail.utils.logger import get_logger
from .config import DovetailConfig
from .hooks import run_hook

logger = get_logger("dovetail-build")


class PluginMain(Plugin):
    """dovetail-build 默认构建工具插件 (DFP-401 §3)"""

    # 标记为构建工具，供 _find_build_plugin() 发现
    _is_build_tool = True

    def __init__(self):
        super().__init__()
        self._name = "dovetail_build"

    def validate(self) -> tuple[bool, str | None]:
        return True, None

    def load(self) -> None:
        logger.info("dovetail-build 插件已加载")

    def unload(self) -> bool:
        return True

    # ── 构建入口 ──────────────────────────────────────────────

    def build(self, project_root: "Path") -> int:
        """pre_build hook → 调用编译器 → post_build hook"""
        config = DovetailConfig(project_root)

        # pre_build 钩子
        if config.pre_build and not run_hook(config.pre_build, project_root):
            logger.error("pre_build hook 失败，中止构建")
            return -1

        # 拼命令行，调用编译器
        args = self._build_compiler_args(config, project_root)
        ret = self._invoke_compiler(args)

        # post_build 钩子
        if config.post_build:
            if not run_hook(config.post_build, project_root):
                logger.warning("post_build hook 失败（构建已完成）")

        return ret

    def init_project(self, project_root: "Path") -> int:
        """初始化项目骨架"""
        project_root.mkdir(parents=True, exist_ok=True)

        # dovetail.toml
        toml_path = project_root / "dovetail.toml"
        toml_path.write_text(
            '[package]\n'
            f'name = "{project_root.name}"\n'
            'version = "0.1.0"\n'
            'authors = []\n'
            'description = ""\n'
            'license = "MIT"\n'
            '\n'
            '[build]\n'
            'tool = "default"\n'
            'entry = "src/main.mcdl"\n'
            'output = "target"\n'
            '\n'
            '[paths]\n'
            'sources = ["src"]\n'
            'libraries = ["lib"]\n'
            'includes = []\n'
            '\n'
            '[compiler]\n'
            'lib_path = ""\n'
            'optimization = 2\n'
            'backend = ""\n'
            '\n'
            '[hooks]\n'
            'pre_build = "hook/pre_build.py"\n'
            'post_build = "hook/post_build.py"\n',
            encoding="utf-8",
        )
        logger.info(f"创建文件 {toml_path}")

        # src/main.mcdl
        main_mcdl = project_root / "src" / "main.mcdl"
        main_mcdl.parent.mkdir(parents=True, exist_ok=True)
        main_mcdl.write_text(
            '@init\n'
            'fn main() {\n'
            '    print("Hello, Dovetail!")\n'
            '}\n',
            encoding="utf-8",
        )
        logger.info(f"创建文件 {main_mcdl}")

        # hook/
        hook_dir = project_root / "hook"
        hook_dir.mkdir(parents=True, exist_ok=True)

        pre_hook = hook_dir / "pre_build.py"
        pre_hook.write_text(
            '#!/usr/bin/env python3\n'
            'print("[pre_build] Ready.")\n',
            encoding="utf-8",
        )
        logger.info(f"创建文件 {pre_hook}")

        post_hook = hook_dir / "post_build.py"
        post_hook.write_text(
            '#!/usr/bin/env python3\n'
            'print("[post_build] Done.")\n',
            encoding="utf-8",
        )
        logger.info(f"创建文件 {post_hook}")

        # .gitignore
        gitignore = project_root / ".gitignore"
        gitignore.write_text(
            'target/\n'
            'build/\n'
            '*.mcdc\n',
            encoding="utf-8",
        )
        logger.info(f"创建文件 {gitignore}")

        logger.info(f"项目初始化完成: {project_root}")
        return 0

    # ── 命令行构建 ────────────────────────────────────────────

    @staticmethod
    def _build_compiler_args(config: "DovetailConfig", project_root: "Path") -> list[str]:
        """将 dovetail.toml 配置转换为编译器命令行 (DFP-401 §3.3.4)"""

        # 冻结环境 (PyInstaller/Nuitka): sys.executable 就是编译器本体
        # 普通环境: sys.executable 是 python 解释器，需要加 main.py
        if getattr(sys, 'frozen', False):
            args = [sys.executable]
        else:
            main_py = sys.argv[0]
            args = [sys.executable, main_py]

        # 入口文件 → <input>
        args.append(str(project_root / config.entry))

        # 输出目录 → -o
        if config.output:
            args.extend(["-o", str(project_root / config.output)])

        # 标准库路径 → --lib-path
        if config.lib_path:
            args.extend(["--lib-path", config.lib_path])

        # 优化级别 → -O
        args.extend(["-O", str(config.optimization)])

        # 后端 → --backend
        if config.backend:
            args.extend(["--backend", config.backend])

        # 禁止子编译器进程日志输出
        args.append("--disable-info-logger")

        return args

    def _invoke_compiler(self, args: list[str]) -> int:
        """以子进程调用编译器"""
        logger.info(f"调用编译器: {' '.join(args)}")
        try:
            result = subprocess.run(args)
            return result.returncode
        except Exception as e:
            logger.error(f"编译器调用失败: {e}")
            return -1

    # ── 插件间通信 ────────────────────────────────────────────

    def handle_message(self, sender, message):
        if isinstance(message, dict) and message.get("action") == "build":
            root = message.get("project_root", ".")
            return self.build(Path(root).resolve())
        elif isinstance(message, dict) and message.get("action") == "init":
            root = Path(message.get("project_root", ".")).resolve()
            if root.exists() and any(root.iterdir()):
                logger.error(
                    f"'{root}' 已存在且非空，无法初始化。\n"
                    f"  提示：请在空目录中运行 dovetail init，或指定新目录。"
                )
                sys.exit(1)

            return self.init_project(root)
        return None