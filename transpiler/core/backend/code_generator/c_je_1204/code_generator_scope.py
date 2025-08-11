# coding=utf-8
from __future__ import annotations

from transpiler.core.enums import StructureType
from transpiler.core.symbols import Symbol


class CodeGeneratorScope:
    def __init__(self, name: str, parent: CodeGeneratorScope | None,
                 structure_type: StructureType, namespace: str):
        self.namespace = namespace
        self.name = name
        self.parent = parent
        self.type = structure_type
        self.symbols: dict[str, Symbol] = dict()  # 符号表（变量/函数/类）
        self.children: list[CodeGeneratorScope] = list()  # 子作用域
        self.commands: list[str] = list()

    def add_command(self, commands: str | list[str]):
        if isinstance(commands, str):
            self.commands.append(commands)
        else:
            self.commands.extend(commands)

    def get_name(self):
        return self.name

    def get_file_path(self):
        return f"{self.namespace}/functions/{self.get_unique_name()}.mcfunction"

    def get_minecraft_function_path(self):
        return f"{self.namespace}:{self.get_unique_name()}".replace("\\", "/")

    def get_unique_name(self, separator='/'):
        if self.type == StructureType.GLOBAL or self.type is None:
            return "global"
        return self.parent.get_unique_name(separator) + separator + self.name

    def get_symbol_path(self, name: str):
        name = str(name)
        current = self
        while current:
            if name in current.symbols:
                break
            current = current.parent
        if current:
            return f"{current.get_unique_name('.')}.{name}"
        else:
            return name

    def create_child(self, name: str, type_: StructureType) -> CodeGeneratorScope:
        child = CodeGeneratorScope(name, self, type_, self.namespace)
        self.children.append(child)
        return child

    def add_symbol(self, symbol: Symbol, force=False):
        if symbol.get_name() in self.symbols and not force:
            raise NameError(
                f"Symbol {symbol.get_name()} already exists in this scope")
        self.symbols[symbol.get_name()] = symbol

    def has_symbol(self, name: str):
        return name in self.symbols

    def set_symbol(self, symbol: Symbol, force=False):
        if symbol.get_name() not in self.symbols and not force:
            raise NameError(
                f"Symbol {symbol.get_name()} does not exist in this scope")
        self.symbols[symbol.get_name()] = symbol

    def resolve_symbol(self, name: str) -> Symbol:
        """逐级向上查找符号"""
        name = str(name)
        current = self
        while current:
            if name in current.symbols:
                return current.symbols[name]
            current = current.parent
        raise ValueError(f"Undefined symbol: {name}")

    def find_symbol(self, name: str) -> Symbol:
        """只在单层查找符号"""
        name = str(name)
        if name in self.symbols:
            return self.symbols[name]
        else:
            raise ValueError(f"Undefined symbol: {name}")

    def find_scope(self, name: str) -> CodeGeneratorScope:
        """只在单层查找作用域"""
        name = str(name)
        for i in self.children:
            if i.name == name:
                return i
        raise ValueError(f"Undefined symbol: {name}")

    def resolve_scope(self, name: str) -> CodeGeneratorScope:
        """逐级向上查找该作用域可访问到的作用域"""
        name = str(name)
        current = self
        while current:
            if name in [i.name for i in current.children]:
                return [i for i in current.children if i.name == name][0]
            current = current.parent
        raise ValueError(f"Undefined scope: {name}")

    def get_parent(self) -> CodeGeneratorScope:
        if self.parent:
            return self.parent
        else:
            return self

    def exist_parent(self) -> bool:
        if self.parent:
            return True
        else:
            return False
