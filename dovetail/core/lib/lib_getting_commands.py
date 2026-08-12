# coding=utf-8
from dovetail.core.lib.lib_factory import LibraryBase, builtin_func
from dovetail.core.lib.library import LibraryContext


class GettingCommands(LibraryBase):
    def __init__(self, context: LibraryContext):
        self.context = context
        self._init(context)

    # 任何 NBT 类型都能用，但结果是字符串，需要手动解析

    @builtin_func()
    def data_get_block(self, x: int, y: int, z: int, path: str = "") -> str: ...

    @builtin_func()
    def data_get_entity(self, source: str, path: str = "") -> str: ...

    @builtin_func()
    def data_get_storage(self, source: str, path: str = "") -> str: ...

    # data get int — 走 execute store result score，返回 int

    @builtin_func()
    def data_get_block_int(self, x: int, y: int, z: int, path: str, scale: int = 1) -> int: ...

    @builtin_func()
    def data_get_entity_int(self, source: str, path: str, scale: int = 1) -> int: ...

    @builtin_func()
    def data_get_storage_int(self, source: str, path: str, scale: int = 1) -> int: ...

    # 其他返回

    @builtin_func()
    def scoreboard_players_get(self, target: str, objective: str) -> int: ...

    @builtin_func()
    def attribute_base_get(self, target: str, attribute: str, scale: int = 1) -> str: ...

    @builtin_func()
    def attribute_get(self, target: str, attribute: str, scale: int = 1) -> str: ...

    @builtin_func()
    def attribute_modifier_value_get(self, target: str, attribute: str, id_: str, scale: int = 1) -> str: ...

    @builtin_func()
    def bossbar_get_max(self, id_: str) -> int: ...

    @builtin_func()
    def bossbar_get_players(self, id_: str) -> int: ...

    @builtin_func()
    def bossbar_get_value(self, id_: str) -> int: ...

    @builtin_func()
    def bossbar_get_visible(self, id_: str) -> int: ...

    def __str__(self) -> str:
        return "getting commands"
