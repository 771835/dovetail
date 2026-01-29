# coding=utf-8
"""
生成上下文，存储后端生成过程中的所有状态
"""
import json
import shutil
from pathlib import Path
from typing import Optional

from attrs import define, field

from transpiler.core.compile_config import CompileConfig
from transpiler.core.enums import StructureType, MinecraftVersion
from transpiler.core.ir_builder import IRBuilder
from transpiler.core.symbols import Symbol


class PackMcmeta:
    def __init__(
            self,
            path: Path,
            data: dict[str, dict[str, str | int | list[dict[str, str | int | dict] | int]]] = None
    ):
        data = data or {}
        self._path = path
        self._description: str | dict = data.get("pack", {}).get("description", "")
        self._format: tuple[int, int] = self._parser_format(data.get("pack", {}))
        self._overlays: list[tuple[str, tuple[int, int]]] = self._parser_overlays(data.get("overlays", []))

    @staticmethod
    def _parser_format(pack: dict[str, int | list[int]]) -> tuple[int, int]:
        if pack.get("min_format") and pack.get("max_format"):
            return pack["min_format"], pack["max_format"]
        elif formats := pack.get("supported_formats") or pack.get("formats"):
            if isinstance(formats, list):
                if len(formats) == 1:
                    return formats[0], 127
                elif len(formats) == 2:
                    return formats[0], formats[1]
            elif isinstance(formats, dict):
                if formats.get("min_inclusive") and formats.get("max_inclusive"):
                    return formats["min_inclusive"], formats["max_inclusive"]
        else:
            if pack.get("pack_format"):
                return pack["pack_format"], pack["pack_format"]
        return 0, 127  # 无结果默认返回(0, 127)

    @staticmethod
    def _parser_overlay(entry: dict[str, str | int | list | dict]) -> tuple[str, tuple[int, int]]:
        return entry.get("directory") or '', PackMcmeta._parser_format(entry)

    @staticmethod
    def _parser_overlays(entries: list[dict[str, str | int | list | dict]]) -> list[tuple[str, tuple[int, int]]]:
        return [PackMcmeta._parser_overlay(entry) for entry in entries]

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, path: Path):
        if self._path is not None and self._path.is_file():
            if path.exists():
                raise FileExistsError
            shutil.move(self._path, path)
        self._path = path

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, description: str | list | dict):
        self._description = description

    @property
    def min_format(self):
        return self._format[0]

    @min_format.setter
    def min_format(self, min_format: int):
        self._format = (min_format, self._format[1])

    @property
    def max_format(self):
        return self._format[1]

    @max_format.setter
    def max_format(self, max_format: int):
        self._format = (self._format[0], max_format)

    def add_overlay(self, directory: str, formats: dict | tuple[int, int]) -> None:
        if isinstance(formats, dict):
            formats = self._parser_format(formats)
        self._overlays.append((directory, formats))

    def _pickle(self, version: MinecraftVersion):
        if version >= MinecraftVersion.instance("1.21.9"):
            return {
                'pack': {
                    'description': self.description,
                    'min_format': self.min_format,
                    'max_format': self.max_format
                },
                'overlays': {
                    'entries': [
                        {
                            'directory': overlay[0],
                            'min_format': overlay[1][0],
                            'max_format': overlay[1][1]
                        } for overlay in self._overlays
                    ]
                }
            }
        elif version >= MinecraftVersion.instance("1.20.2"):
            return {
                'pack': {
                    'description': self.description,
                    'pack_format': self._format[0],
                    'supported_formats': self._format
                },
                'overlays': {
                    'entries': [
                        {
                            'directory': overlay[0],
                            'formats': overlay[1]
                        } for overlay in self._overlays
                    ]
                }
            }
        else:
            return {
                'pack': {
                    'description': self.description,
                    'pack_format': self._format[0]
                }
            }

    def save_file(self, version: MinecraftVersion):
        with open(self.path, "wt") as f:
            json.dump(self._pickle(version), f)


@define
class Scope:
    """作用域数据结构"""
    name: str
    scope_type: StructureType
    parent: Optional['Scope'] = field(default=None)
    children: list['Scope'] = field(factory=list)
    commands: list[str] = field(factory=list)
    symbols: dict[str, Symbol] = field(factory=dict)
    flags: dict[str, ...] = field(factory=dict)

    def add_command(self, command: str):
        """添加命令"""
        self.commands.append(command)

    def has_commands(self) -> bool:
        """是否有命令"""
        return len(self.commands) > 0

    def get_absolute_path(self) -> str:
        """获取完整作用域路径"""
        if self.parent is None:
            return "global"

        count = 0
        for child in self.parent.children:
            if child.name == self.name:
                count += 1
                if child is self:
                    break
        if count == 1:
            return f"{self.parent.get_absolute_path()}.{self.name}"
        else:
            return f"{self.parent.get_absolute_path()}.{self.name}${count}"

    def get_file_path(self) -> Path:
        """获取文件相对路径"""
        # 构建相对路径
        parts = []
        current = self
        while current:
            parts.append(current.name)
            current = current.parent

        parts.reverse()
        return Path(*parts).with_suffix('.mcfunction')

    def add_symbol(self, symbol: Symbol):
        self.symbols[symbol.get_name()] = symbol

    def get_symbol_path(self, symbol_name: str) -> str:
        current = self
        while current:
            if symbol_name in current.symbols:
                break
            current = current.parent
        if current:
            return f"{current.get_absolute_path()}.{symbol_name}"
        else:
            return symbol_name

    def resolve_scope(self, name: str) -> 'Scope':
        """逐级向上查找该作用域可访问到的作用域"""
        current = self
        while current:
            if name in [i.name for i in current.children]:
                return [i for i in current.children if i.name == name][0]
            current = current.parent
        raise ValueError(f"Undefined scope: {name}")


@define
class GenerationContext:
    """后端生成上下文"""
    config: CompileConfig
    target: Path
    ir_builder: IRBuilder

    # 作用域管理
    root_scope: Optional[Scope] = field(default=None)
    current_scope: Optional[Scope] = field(default=None)
    scope_stack: list[Scope] = field(factory=list)

    # 全局状态
    namespace: str = ""
    objective: str = "dovetail"
    temp_var_counter: int = 0

    # 缓存和优化
    scope_cache: dict[str, Scope] = field(factory=dict)

    # 其他文件
    pack_meta: PackMcmeta = None

    def __attrs_post_init__(self):
        """初始化根作用域"""
        self.namespace = self.config.namespace
        self.root_scope = Scope(
            name=self.namespace,
            scope_type=StructureType.GLOBAL,
        )
        self.current_scope = self.root_scope
        self.scope_stack = [self.root_scope]
        self.scope_cache[self.namespace] = self.root_scope
        self.pack_meta = PackMcmeta(self.target / self.namespace / 'pack.mcmeta')

    def create_scope(self, name: str, scope_type: StructureType) -> Scope:
        """创建新作用域"""
        scope = Scope(
            name=name,
            scope_type=scope_type,
            parent=self.current_scope
        )
        self.current_scope.children.append(scope)
        self.scope_cache[name] = scope
        return scope

    def push_scope(self, scope: Scope):
        """进入作用域"""
        self.scope_stack.append(scope)
        self.current_scope = scope

    def pop_scope(self) -> Scope:
        """退出作用域"""
        if len(self.scope_stack) <= 1:
            raise RuntimeError("Cannot pop root scope")

        popped = self.scope_stack.pop()
        self.current_scope = self.scope_stack[-1]
        return popped

    def get_scope(self, name: str) -> Optional[Scope]:
        """通过名称获取作用域（使用缓存）"""
        return self.scope_cache.get(name)

    def get_scope_no_cache(self, name: str, start_scope=None) -> Optional[Scope]:
        """通过名称获取作用域"""
        if start_scope is None:
            start_scope = self.current_scope

        while self.current_scope:
            if name in (child.name for child in start_scope.children):
                return next(child for child in start_scope.children if child.name == name)
            start_scope = start_scope.parent
        return None

    def get_all_scopes(self) -> list[Scope]:
        """获取所有作用域（广度优先）"""
        result = []
        queue = [self.root_scope]

        while queue:
            scope = queue.pop(0)
            result.append(scope)
            queue.extend(scope.children)

        return result

    def allocate_temp_var(self, prefix: str = "temp") -> str:
        """分配临时变量名"""
        self.temp_var_counter += 1
        return f"{prefix}_{self.temp_var_counter}"

    def add_command(self, command: str):
        """在当前作用域添加命令"""
        assert isinstance(command, str)
        self.current_scope.add_command(command)

    def add_commands(self, commands: list[str]):
        """在当前作用域添加多条命令"""
        for command in commands:
            self.add_command(command)
