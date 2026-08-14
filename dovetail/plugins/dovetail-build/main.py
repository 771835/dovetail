# coding=utf-8
import subprocess
import sys
from pathlib import Path

from dovetail.plugins.plugin_api.plugin import Plugin
from dovetail.utils.logger import get_logger
from .config import DovetailConfig
from .hooks import run_hook


class PluginMain(Plugin):
    """dovetail-build 默认构建工具插件 (DFP-401 §3)"""

    # 标记为构建工具，供 _find_build_plugin() 发现
    _is_build_tool = True

    def __init__(self):
        super().__init__()
        self._name = "dovetail_build"
        self.logger = get_logger("dovetail-build")

    def validate(self) -> tuple[bool, str | None]:
        return True, None

    def load(self) -> None:
        self.logger.info("dovetail-build 插件已加载")

    def unload(self) -> bool:
        return True

    # ── 构建入口 ──────────────────────────────────────────────

    def build(self, project_root: "Path") -> int:
        """pre_build hook → 调用编译器 → post_build hook"""
        config = DovetailConfig(project_root)

        # pre_build 钩子
        if config.pre_build and not run_hook(config.pre_build, project_root):
            self.logger.error("pre_build hook 失败，中止构建")
            return -1

        # 拼命令行，调用编译器
        args = self._build_compiler_args(config, project_root)
        ret = self._invoke_compiler(args)

        # post_build 钩子
        if config.post_build:
            if not run_hook(config.post_build, project_root):
                self.logger.warning("post_build hook 失败（构建已完成）")

        return ret

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
        self.logger.info(f"调用编译器: {' '.join(args)}")
        try:
            result = subprocess.run(args)
            return result.returncode
        except Exception as e:
            self.logger.error(f"编译器调用失败: {e}")
            return -1

    # ── 插件间通信 ────────────────────────────────────────────

    def handle_message(self, sender, message):
        if isinstance(message, dict) and message.get("action") == "build":
            root = message.get("project_root", ".")
            return self.build(Path(root).resolve())
        return None