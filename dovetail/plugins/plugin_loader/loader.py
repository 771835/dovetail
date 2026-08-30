# coding=utf-8
"""
插件加载器核心实现

负责插件的实际加载、执行环境构建和生命周期管理。
"""

import json
import os
import re
import traceback
from pathlib import Path
from typing import Dict

import sys

from dovetail.plugins.plugin_api import Plugin, api_version
from dovetail.utils.logger import get_logger
from dovetail.utils.resource import resolve_project_path, install_root

# 兼容 Python 3.10 及更低版本与 Python 3.11+
if sys.version_info >= (3, 11):
    import tomllib
else:
    try:
        import tomli as tomllib
    except ImportError:
        raise ImportError("请在 Python < 3.11 环境下安装 tomli 库: pip install tomli")

__all__ = [
    "plugin_loader",
]

logger = get_logger(__name__)

load_stack = []


# ── 语义化版本工具 ────────────────────────────────────────────

def _parse_semver(version: str) -> tuple[int, int, int]:
    """解析语义化版本字符串 (主.次.修订)"""
    m = re.match(r'^(\d+)\.(\d+)\.(\d+)$', version.strip())
    if not m:
        raise ValueError(f"Invalid semver: {version}")
    return int(m[1]), int(m[2]), int(m[3])


def _parse_api_version(version: str) -> tuple[int, int]:
    """解析 API 版本 (主.次)"""
    m = re.match(r'^(\d+)\.(\d+)$', version.strip())
    if not m:
        raise ValueError(f"Invalid api_version: {version}")
    return int(m[1]), int(m[2])


def _check_semver_constraint(version: str, constraint: str) -> bool:
    """检查版本是否满足约束 (^主.次.修订 格式)"""
    if version.startswith("dev"):  # dev 版本跳过判断
        return True
    elif "rc" in version:  # rc版本去除rc标识后进行比较
        version = version.split("-", 1)[0]
    v = _parse_semver(version)
    c = _parse_semver(constraint.lstrip('^'))
    if constraint.startswith('^'):
        # ^1.2.3 → >=1.2.3 且 <2.0.0
        return v >= c and v[0] == c[0]
    return v == c


def _check_api_version_compatibility(plugin_api_version: str, current_api_version: str) -> bool:
    """检查 api_version 兼容性 (DFP-602 §8.1)"""
    if plugin_api_version == "~":
        return True

    p = _parse_api_version(plugin_api_version)
    c = _parse_api_version(current_api_version)
    return p[0] == c[0] and p[1] <= c[1]


# ── PluginLoader ──────────────────────────────────────────────

class PluginLoader:
    """
    插件加载器

    Attributes:
        plugins_paths (List[str]): 插件搜索路径列表
        plugins_locals (Dict[str, Dict]): 插件的本地变量作用域映射
        plugins_instance (Dict[str, Plugin]): 已加载插件实例映射
    """

    # 插件搜索路径
    plugins_paths = [
        "dovetail/plugins",
        "plugins",
    ]

    def __init__(self):
        """初始化 PluginLoader 实例"""
        self.plugins_locals: dict[str, dict] = {}
        self.plugins_instance: dict[str, Plugin] = {}
        self.plugin_metadata: dict[str, dict] = {}  # 新增：缓存 TOML 元数据
        self._load_order: list[str] = []  # 新增：拓扑排序结果

    def _load_metadata(self, plugin_path: Path) -> dict | None:
        """加载插件元数据，优先 TOML，向后兼容 JSON"""
        toml_path = plugin_path / "plugin.toml"
        json_path = plugin_path / "plugin.metadata"

        if toml_path.exists():
            try:
                with open(toml_path, "rb") as f:
                    return tomllib.load(f)
            except Exception as e:
                logger.error(f"Failed to parse {toml_path}: {e}")
                return None

        if json_path.exists():
            logger.warning(
                f"插件 '{plugin_path.name}' 使用已弃用的 plugin.metadata (JSON) 格式，"
                f"请迁移至 plugin.toml。参见 DFP-602。",
            )
            try:
                with open(json_path, encoding="utf-8") as f:
                    return self._convert_json_metadata(json.load(f))
            except Exception as e:
                logger.error(f"Failed to parse {json_path}: {e}")
                return None

        return None

    def _convert_json_metadata(self, json_meta: dict) -> dict:
        """将旧 JSON 元数据转换为 TOML 等效结构"""
        return {
            "plugin": {
                "name": json_meta.get("display_name", "").lower().replace("-", "_"),
                "version": json_meta.get("plugin_version", "0.0.0"),
                "api_version": api_version(),
                "entry": json_meta.get("plugin_main", "main.py").replace(".py", ""),
                "type": json_meta.get("plugin_type", "plugin"),
                "main_class": json_meta.get("main_class", ""),
            },
            "metadata": {
                "author": ", ".join(json_meta.get("plugin_author", [])),
            },
        }

    def _get_entry_file(self, plugin_path: Path, metadata: dict) -> Path | None:
        """从元数据中获取入口文件路径"""
        entry = metadata.get("plugin", {}).get("entry", "main")
        # 优先不加 .py，也尝试加 .py
        for candidate in [entry, f"{entry}.py"]:
            p = plugin_path / candidate
            if p.exists() and p.is_file():
                return p
        return None

    # ── 依赖解析 (DFP-602 §7.2) ────────────────────────

    def _resolve_dependencies(self, all_metadata: dict[str, dict]) -> list[str]:
        """拓扑排序插件加载顺序"""
        # 构建依赖图
        graph: dict[str, set[str]] = {}
        for name, meta in all_metadata.items():
            deps = meta.get("dependencies", {})
            graph[name] = set(deps.keys())

        # Kahn 拓扑排序
        in_degree = {n: 0 for n in graph}
        adjacency = {n: [] for n in graph}
        for name, deps in graph.items():
            for dep in deps:
                if dep not in graph:
                    logger.warning(f"插件 '{name}' 依赖 '{dep}' 未找到，跳过加载")
                    continue
                adjacency[dep].append(name)
                in_degree[name] += 1

        ready = sorted([n for n, d in in_degree.items() if d == 0])
        result = []
        while ready:
            current = ready.pop(0)
            result.append(current)
            for neighbor in adjacency[current]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    ready.append(neighbor)
                    ready.sort()

        if len(result) != len(graph):
            cycle = [n for n, d in in_degree.items() if d > 0]
            logger.error(f"插件间存在循环依赖：{cycle}")
            # 返回已排好序的部分，跳过循环依赖的插件

        return result

    def _check_version_compatibility(self, plugin_name: str, metadata: dict) -> bool:
        """检查版本兼容性 (DFP-602 §8)"""
        plugin = metadata.get("plugin", {})

        # api_version 检查
        api_ver = plugin.get("api_version", "")
        if not _check_api_version_compatibility(api_ver, api_version()):
            logger.warning(
                f"插件 '{plugin_name}' api_version={api_ver} 与当前插件API版本 {api_version()} 不兼容，跳过加载"
            )
            return False

        # 编译器版本兼容性
        compat = metadata.get("compatibility", {})
        from dovetail.core.config import PROJECT_VERSION
        if compat.get("dovetail_min"):
            if PROJECT_VERSION < compat["dovetail_min"]:
                logger.warning(
                    f"插件 '{plugin_name}' 要求最低编译器版本 {compat['dovetail_min']}，当前 {PROJECT_VERSION}")
                return False
        if compat.get("dovetail_max"):
            if PROJECT_VERSION > compat["dovetail_max"]:
                logger.warning(
                    f"插件 '{plugin_name}' 要求最高编译器版本 {compat['dovetail_max']}，当前 {PROJECT_VERSION}")
                return False

        return True

    # ── 插件加载 ───────────────────────────────────────

    def load_plugin(self, plugin_input: str | Path) -> None:
        """加载指定名称的插件（支持 TOML 和 JSON 元数据）"""
        input_path = Path(plugin_input)
        is_absolute_path = input_path.is_absolute() and input_path.exists() and input_path.is_dir()

        if is_absolute_path:
            plugin_path = input_path
            plugin_name = plugin_path.name
        else:
            plugin_name = plugin_input.name if isinstance(plugin_input, Path) else Path(plugin_input).name

        if plugin_name in self.plugins_instance:
            logger.warning(f"插件重复加载：'{plugin_name}' 已经被加载了")
            return

        # 搜索插件目录
        if is_absolute_path:
            search_paths = [plugin_path]  # noqa
        else:
            search_paths = [resolve_project_path(p) / plugin_name for p in PluginLoader.plugins_paths]

        for p_path in search_paths:
            if p_path.exists() and p_path.is_dir():
                plugin_path = p_path
                metadata = self._load_metadata(plugin_path)
                if metadata is None:
                    continue

                entry_file = self._get_entry_file(plugin_path, metadata)
                if entry_file is None:
                    logger.error(f"Plugin '{plugin_path}' 入口文件未找到")
                    continue

                # 版本兼容性检查
                if not self._check_version_compatibility(plugin_name, metadata):
                    return

                break
        else:
            logger.error(f"No valid plugin found for '{plugin_input}'")
            return

        # 缓存元数据，供配置系统使用
        self.plugin_metadata[plugin_name] = metadata

        logger.info(f"插件 '{plugin_name}' 被从 '{plugin_path}' 加载")

        load_stack.append(plugin_name)
        logger.debug(f"插件加载栈：{' -> '.join(load_stack)}，长度 {len(load_stack)}")

        # 执行插件代码
        plugin_locals = self.plugins_locals.get(plugin_name, {})
        try:
            global_env: dict = dict()

            # 处理相对路径计算，防止绝对路径加载时 relative_to 报错
            try:
                package_path = str(plugin_path.relative_to(install_root)).replace(os.sep, ".")
            except ValueError:
                # 如果绝对路径不在当前工作目录下，则用插件名作为包名
                package_path = plugin_name
                logger.warning("无法解析插件相对路径计算")

            # TOML 元数据中 entry 不含 .py，对应 main_class 在代码中搜索
            plugin_info = metadata.get("plugin", metadata)  # 兼容 JSON 转换后的结构
            main_class_name = plugin_info.get("main_class", "PluginMain")

            global_env.update({
                "__path__": str(plugin_path),
                "__package__": package_path,
                "__name__": plugin_name,
                "__file__": str(entry_file.resolve()),
                "__plugin_name__": plugin_info.get("name", plugin_name),
            })
            with open(entry_file, encoding="utf-8") as f:
                code = f.read()
            exec(code, global_env, plugin_locals)
            global_env.update(plugin_locals)
            self.plugins_locals[plugin_name] = plugin_locals

            # 搜索入口类
            if plugin_main_class := plugin_locals.get(main_class_name, None):
                plugin_main_class: type[Plugin]
                instance = plugin_main_class()
                instance._name = plugin_name
                instance._version = plugin_info.get("version", "0.0.0")
                self.plugins_instance[plugin_name] = instance

                is_validate, reason = instance.validate()
                if not is_validate:
                    logger.warning(f"Plugin '{plugin_name}' validate 失败: {reason}")
                    return

                instance.initialize()
                instance.load()
            else:
                raise ModuleNotFoundError(
                    f"Plugin '{plugin_name}' 入口类 '{main_class_name}' 未找到"
                )

        except Exception as e:
            logger.error(f"加载插件 {plugin_name} 失败：{e}")
            self.plugins_locals.pop(plugin_name, None)
            self.plugins_instance.pop(plugin_name, None)
            if os.environ.get("PLUGIN_DEBUG"):
                traceback.print_tb(e.__traceback__)

        load_stack.pop()


plugin_loader = PluginLoader()
