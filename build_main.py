# coding=utf-8
"""
dovetail-build — Dovetail 构建工具

独立可执行程序，负责项目级构建编排。
与编译器核心（dovetail）完全分离，通过子进程调用编译器。

用法：
    dovetail-build build [path]          读取 dovetail.toml 构建项目
    dovetail-build init [path]           初始化新项目骨架
    dovetail-build clean [path]          清理临时文件和构建文件
    dovetail-build script <script_path>  执行钩子脚本
"""
import argparse
import runpy
import shutil
import subprocess
import sys
from contextlib import chdir
from pathlib import Path

from dovetail.build import Builder
from dovetail.utils.logger import get_logger

script_run_timeout = 75

# 将 sys.argv[0] 设置为绝对路径
sys.argv[0] = str(Path(sys.argv[0]).resolve())

def main():
    parser = argparse.ArgumentParser(
        prog="dovetail-build",
        description="Dovetail 构建工具",
    )

    parser.add_argument('--debug', action='store_true', help='启用调试模式')

    sub = parser.add_subparsers(dest="command", metavar="command")
    sub.required = True

    # ── build ──────────────────────────────────────────────────
    build_p = sub.add_parser("build", help="构建项目（读取 dovetail.toml）")
    build_p.add_argument(
        "project_root",
        nargs="?",
        default=".",
        metavar="path",
        help="项目根目录，默认当前目录",
    )

    # ── init ───────────────────────────────────────────────────
    init_p = sub.add_parser("init", help="初始化新项目骨架")
    init_p.add_argument(
        "project_root",
        nargs="?",
        default=".",
        metavar="path",
        help="项目目录，默认当前目录",
    )

    # ── clean ──────────────────────────────────────────────────
    clean_p = sub.add_parser("clean", help="清理临时文件和构建文件")
    clean_p.add_argument(
        "project_root",
        nargs="?",
        default=".",
        metavar="path",
        help="项目目录，默认当前目录",
    )

    # ── script ─────────────────────────────────────────────────
    script_p = sub.add_parser(
        "script",
        help="注入环境变量后执行钩子脚本（DFP-604 §6.2）",
    )
    script_p.add_argument(
        "script_path",
        metavar="script",
        help="钩子脚本路径（.py 或 .sh）",
    )
    script_p.add_argument(
        "project_root",
        nargs="?",
        default=".",
        metavar="path",
        help="项目根目录，默认当前目录",
    )

    args = parser.parse_args()

    logger = get_logger("dovetail-build")

    # ── 处理 build ─────────────────────────────────────────────
    if args.command == "build":
        root = Path(args.project_root).resolve()
        sys.exit(Builder(root).build())

    # ── 处理 init ──────────────────────────────────────────────
    elif args.command == "init":
        root = Path(args.project_root).resolve()
        if root.exists() and any(root.iterdir()):
            logger.error(
                f"目录 '{root}' 已存在且非空，无法初始化。\n"
                f"  提示：请在空目录中运行，或指定新目录名。"
            )
            sys.exit(1)
        sys.exit(Builder(root).init())

    # ── 处理 clean ─────────────────────────────────────────────
    elif args.command == "clean":
        root = Path(args.project_root).resolve()
        sys.exit(Builder(root).clean())

    # ── 处理 script ────────────────────────────────────────────
    elif args.command == "script":
        script = Path(args.script_path).resolve()

        if not script.exists():
            logger.error(f"脚本不存在: {script}")
            sys.exit(1)

        with chdir(args.project_root):
            try:
                # 环境变量已由父进程（run_hook）注入，此处直接执行即可
                if script.suffix == ".py":
                    # python 脚本这里因为不是一个子进程在跑，所以就不是采用 script_run_timeout 来限时，而是调用这个程序的 timeout 决定
                    # 因此 python 脚本有着更长的可运行时间
                    runpy.run_path(str(script), run_name="__main__")
                    sys.exit(0)
                elif script.suffix == ".sh":
                    shell_path = shutil.which("bash")
                    if shell_path:
                        result = subprocess.run([shell_path, str(script)], timeout=script_run_timeout)
                        sys.exit(result.returncode)
                    else:
                        logger.error("未找到 bash，无法执行 .sh 脚本")
                        sys.exit(1)
                elif script.suffix in (".bat", ".cmd"):
                    shell_path = shutil.which("cmd")
                    if shell_path:
                        result = subprocess.run(["cmd", "/c", str(script)], timeout=script_run_timeout)
                        sys.exit(result.returncode)
                    else:
                        logger.error(f"未找到 cmd，无法执行 {script.suffix} 脚本")
                        sys.exit(1)
                elif script.suffix == ".ps1":
                    # 1. 检查系统是否安装了 pwsh
                    if shell_path := shutil.which("pwsh"):
                        # 2. 如果有，使用 pwsh 运行
                        result = subprocess.run([shell_path, str(script)], timeout=script_run_timeout)
                    elif shell_path := shutil.which("powershell"):
                        # 3. 如果没有，回退到传统的 powershell
                        result = subprocess.run([shell_path, str(script)], timeout=script_run_timeout)
                    else:
                        logger.error(f"未找到 pwsh/powershell，无法执行 {script.suffix} 脚本")
                        sys.exit(1)
                    sys.exit(result.returncode)
                else:
                    logger.error(f"不支持的脚本类型: {script.suffix}")
                    sys.exit(1)
            except subprocess.TimeoutExpired:
                logger.error(f"脚本 '{script}' 运行超时")
                sys.exit(1)
            except SystemExit as e:
                sys.exit(e.code if e.code is not None else 0)
            except Exception as e:
                logger.error(f"脚本执行异常: {e}")
                sys.exit(1)


if __name__ == "__main__":
    main()
