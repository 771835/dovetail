# coding=utf-8
from dovetail.core.lib.lib_factory import LibraryBase, builtin_func
from dovetail.core.lib.library import LibraryContext


class GettingCommands(LibraryBase):
    def __init__(self, context: LibraryContext):
        self.context = context
        self._init(context)

    @builtin_func()
    def data_get_block(self, x: int, y: int, z: int, path: str = "", scale: str = "") -> str: ...

    @builtin_func()
    def data_get_entity(self, target: str, path: str = "", scale: str = "") -> str: ...

    @builtin_func()
    def data_get_storage(self, target: str, path: str = "", scale: str = "") -> str: ...

    @builtin_func()
    def scoreboard_players_get(self, target: str, objective: str) -> int: ...

    @builtin_func()
    def attribute_base_get(self, target: str, attribute: str, scale: str = "") -> str: ...

    @builtin_func()
    def attribute_get(self, target: str, attribute: str, scale: str = "") -> str: ...

    @builtin_func()
    def attribute_modifier_value_get(self, target: str, attribute: str, id_: str, scale: str = "") -> str: ...

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
