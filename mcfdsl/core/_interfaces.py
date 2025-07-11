# coding=utf-8
from __future__ import annotations

from dataclasses import dataclass

from mcfdsl.core.language_enums import StructureType
from mcfdsl.core.symbols import NewSymbol


@dataclass
class IScope:
    name: str
    namespace: str
    parent: IScope
    type: StructureType
    symbols: dict[str, NewSymbol]
    classes: dict
    children: list[IScope]
    scope_counter: int

    def get_name(self) -> str: ...

    def get_file_path(self) -> str: ...

    def get_minecraft_function_path(self) -> str: ...

    def get_unique_name(self) -> str: ...

    def create_child(self, name: str, type_: StructureType) -> IScope: ...

    def add_symbol(self, symbol: NewSymbol, force=False) -> None: ...

    def set_symbol(self, symbol: NewSymbol, force=False) -> None: ...

    def resolve_symbol(self, name: str) -> NewSymbol: ...

    def resolve_scope(self, name: str) -> IScope: ...

    def find_symbol(self, name: str) -> NewSymbol: ...

    def find_scope(self, name: str) -> IScope: ...

    def get_parent(self) -> IScope: ...

    def exist_parent(self) -> bool: ...
