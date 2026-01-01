# coding=utf-8
"""
生成上下文，存储后端生成过程中的所有状态
"""
from pathlib import Path
from typing import Optional

from attrs import define, field

from transpiler.core.compile_config import CompileConfig
from transpiler.core.enums import StructureType


@define
class Scope:
    """作用域数据结构"""
    name: str
    scope_type: StructureType
    parent: Optional['Scope'] = field(default=None)
    children: list['Scope'] = field(factory=list)
    commands: list[str] = field(factory=list)
    metadata: dict = field(factory=dict)

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
        if count == 0:
            return f"{self.parent.get_absolute_path()}.{self.name}"
        else:
            return f"{self.parent.get_absolute_path()}.{self.name}${count}"

    def get_file_path(self) -> Path:
        """获取文件路径"""
        # 构建相对路径
        parts = []
        current = self
        while current and current.parent:
            parts.append(current.name)
            current = current.parent

        parts.reverse()
        return Path("function") / Path(*parts).with_suffix('.mcfunction')


@define
class GenerationContext:
    """后端生成上下文"""
    config: CompileConfig
    target: Path

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
        self.current_scope.add_command(command)
