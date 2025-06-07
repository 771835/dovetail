from __future__ import annotations

from main import ScopeType, Symbol


class Scope:  # 每层作用域在生成时都会生成为一个函数文件
    def __init__(self, name: str, parent: Scope = None, scope_type: ScopeType = None, namespace: str = "mcfdsl"):
        self.namespace = namespace
        self.name = name
        self.parent = parent
        self.type = scope_type
        self.symbols: dict[str, Symbol] = dict()  # 符号表（变量/函数/类）
        self.classes = {}  # 类定义
        self.children = []  # 子作用域
        self.scope_counter = 0  # 用于生成唯一子作用域名
        self.cmd = list()

    def get_name(self):
        return self.name

    def get_file_path(self):
        return f"{self.namespace}/functions/{self.get_unique_name()}.mcfunction"

    def get_minecraft_function_path(self):
        return f"{self.namespace}:{self.get_unique_name()}".replace("\\", "/")

    def get_unique_name(self):
        if self.type == ScopeType.GLOBAL or self.type is None:
            return "global"
        return self.parent.get_unique_name() + '_' + self.name

    def create_child(self, name: str, scope_type: ScopeType):
        child = Scope(name=name, parent=self, scope_type=scope_type, namespace=self.namespace)
        self.children.append(child)
        return child

    def add_symbol(self, symbol: Symbol):
        if symbol.name in self.symbols:
            raise NameError(f"Symbol {symbol.name} already exists in this scope")
        self.symbols[symbol.name] = symbol

    def set_symbol(self, symbol: Symbol):
        if symbol.name not in self.symbols:
            raise NameError(f"Symbol {symbol.name} does not exist in this scope")
        self.symbols[symbol.name] = symbol

    def resolve_symbol(self, name: str) -> Symbol:
        """逐级向上查找符号"""
        name = str(name)
        current = self
        while current:
            if name in current.symbols:
                return current.symbols[name]
            current = current.parent
        raise NameError(f"Undefined symbol: {name}")

    def resolve_scope(self, name: str) -> Scope:
        """逐级向上查找该作用域可访问到的作用域"""
        name = str(name)
        current = self
        while current:
            if name in [i.name for i in current.children]:
                return [i for i in current.children if i.name == name][0]
            current = current.parent
        raise NameError(f"Undefined scope: {name}")

    def get_parent(self):
        if self.parent:
            return self.parent
        else:
            return self

    def is_exist_parent(self):
        if self.parent:
            return True
        else:
            return False
