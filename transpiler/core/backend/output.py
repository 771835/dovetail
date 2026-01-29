# coding=utf-8
"""
输出管理系统
"""
import os
import shutil
import tempfile
import zipfile
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Dict

from transpiler.core.backend.context import GenerationContext, Scope
from transpiler.core.config import PROJECT_NAME, PROJECT_WEBSITE, get_project_logger
from transpiler.utils.download_tool import download_dependencies


class OutputWriter(ABC):
    """输出写入器基类"""

    @abstractmethod
    def write(self, context: GenerationContext):
        """
        写入输出

        Args:
            context: 生成上下文
        """
        raise NotImplementedError()

    @abstractmethod
    def get_name(self) -> str:
        """
        返回写入器名称

        Returns:
            str: 写入器名称
        """
        raise NotImplementedError()


class CommandWriter(OutputWriter):
    """命令文件写入器"""

    def write(self, context: GenerationContext):
        """写入所有mcfunction文件"""
        for scope in context.get_all_scopes():
            if scope.has_commands():
                self._write_scope(scope, context)

    def _write_scope(self, scope: Scope, context: GenerationContext):
        """写入单个作用域的命令文件"""
        file_path = context.target / context.namespace / "data" / context.namespace / "function" / scope.get_file_path()
        file_path.parent.mkdir(parents=True, exist_ok=True)

        with open(file_path, 'w', encoding='utf-8') as f:
            if context.config.debug:
                f.write(f"# Scope: {scope.name} ({scope.scope_type.value})\n")
                f.write(f"# Commands: {len(scope.commands)}\n")
                f.write(f"# Time: {datetime.now()}\n")
                f.write(f"# Maker: {PROJECT_NAME}({PROJECT_WEBSITE})\n\n")

            for command in scope.commands:
                f.write(command + '\n')

    def get_name(self) -> str:
        return "command_writer"


class FunctionWriter(OutputWriter):
    """内置函数写入器"""

    def __init__(self, builtin_functions: Dict[str, str] = None):
        """
        Args:
            builtin_functions: 内置函数映射 {函数名: 函数内容}
        """
        self.builtin_functions = builtin_functions or {}

    def write(self, context: GenerationContext):
        """写入内置函数"""
        if not self.builtin_functions:
            return

        builtin_dir: Path = context.target / context.namespace / "data" / "functions" / "__builtin__"
        builtin_dir.mkdir(parents=True, exist_ok=True)

        for func_name, func_content in self.builtin_functions.items():
            func_path = builtin_dir / f"{func_name}.mcfunction"
            with open(func_path, 'w', encoding='utf-8') as f:
                f.write(func_content)

    def get_name(self) -> str:
        return "function_writer"


class MetadataWriter(OutputWriter):
    """元数据写入器"""

    def __init__(self, pack_format: int = 61, description: str = None):
        self.pack_format = pack_format
        self.description = description

    def write(self, context: GenerationContext):
        """写入 pack.mcmeta 基本结构"""
        context.pack_meta.description = self.description or context.namespace
        context.pack_meta.min_format = self.pack_format
        context.pack_meta.max_format = self.pack_format
        # 写入文件
        context.pack_meta.save_file(context.config.version)

    def get_name(self) -> str:
        return "metadata_writer"


class DependentDatapackWriter(OutputWriter):
    """依赖数据包写入器"""

    def __init__(self, urls: dict[str, tuple[str | None, int]] = None):
        """
        Args:
            urls: 依赖数据包的下载地址及哈希值与依赖版本号
        """
        self.urls = urls or {}

    def write(self, context: GenerationContext):
        """下载和写入依赖文件"""
        for url, (sha256, version) in self.urls.items():
            dependence = download_dependencies(url, sha256)
            name = sha256[:12] if sha256 else str(hash(url))
            dst = context.target / context.namespace / name

            if dependence is None:
                get_project_logger().error(f"Download dependence failed for {url}")
                continue

            context.pack_meta.add_overlay(name, (version, version))

            if dependence.is_file():
                if zipfile.is_zipfile(dependence):
                    self._extract_zipfile(dependence, dst)
                else:
                    get_project_logger().warning(f"Unknown dependency file: {dependence}")
            elif dependence.is_dir():
                shutil.copy(dependence, dst)

        context.pack_meta.save_file(context.config.version)

    @staticmethod
    def _extract_zipfile(zip_path, extract_to) -> bool:
        with zipfile.ZipFile(zip_path) as zip_ref:
            # 创建临时目录
            with tempfile.TemporaryDirectory() as temp_dir:
                # 先解压到临时目录
                zip_ref.extractall(temp_dir)
                # 检查是否需要子目录提取
                if os.path.exists(os.path.join(temp_dir, 'pack.mcmeta')):
                    # 直接移动所有文件
                    shutil.copytree(temp_dir, extract_to, dirs_exist_ok=True)
                else:
                    # 查找包含pack.mcmeta的子目录
                    for item in os.listdir(temp_dir):
                        item_path = os.path.join(temp_dir, item)
                        if os.path.isdir(item_path) and os.path.exists(os.path.join(item_path, 'pack.mcmeta')):
                            shutil.copytree(item_path, extract_to, dirs_exist_ok=True)
                            break
                    else:
                        return False
        return True

    def get_name(self) -> str:
        return "dependent_datapack_writer"


class TagWriter(OutputWriter):
    """标签写入器（用于minecraft:load和minecraft:tick）"""

    def __init__(self, load_functions: list[str] = None, tick_functions: list[str] = None):
        """
        Args:
            load_functions: 需要在load时执行的函数列表
            tick_functions: 需要在tick时执行的函数列表
        """
        self.load_functions = load_functions or []
        self.tick_functions = tick_functions or []

    def write(self, context: GenerationContext):
        """写入标签文件"""
        tags_dir = context.target / context.namespace / "data" / "minecraft" / "tags" / "functions"
        tags_dir.mkdir(parents=True, exist_ok=True)

        # 写入load标签
        if self.load_functions:
            self._write_tag(tags_dir / "load.json", self.load_functions, context)

        # 写入tick标签
        if self.tick_functions:
            self._write_tag(tags_dir / "tick.json", self.tick_functions, context)

    def _write_tag(self, path: Path, functions: list[str], context: GenerationContext):
        """写入单个标签文件"""
        import json

        # 添加命名空间前缀
        values = [f"{context.namespace}:{func}" for func in functions]

        tag_content = {
            "values": values
        }

        with open(path, 'w', encoding='utf-8') as f:
            json.dump(tag_content, f, indent=2)

    def get_name(self) -> str:
        return "tag_writer"


class OutputManager:
    """输出管理器，协调所有写入器"""

    def __init__(self):
        self.writers: Dict[str, OutputWriter] = {}

    def register_writer(self, writer: OutputWriter):
        """注册写入器"""
        self.writers[writer.get_name()] = writer

    def unregister_writer(self, name: str):
        """移除写入器"""
        if name in self.writers:
            del self.writers[name]

    def write_all(self, context: GenerationContext):
        """执行所有写入器"""
        for name, writer in self.writers.items():
            try:
                writer.write(context)
            except Exception as e:
                get_project_logger().error(f"Writer {name}: {e}")
                if context.config.debug:
                    raise

    def get_writer(self, name: str) -> OutputWriter:
        """获取指定写入器"""
        return self.writers.get(name)
