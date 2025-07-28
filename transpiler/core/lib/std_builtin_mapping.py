# coding=utf-8
import threading
from functools import lru_cache

from transpiler.core.backend.ir_builder import IRBuilder
from transpiler.core.lib.experimental import Experimental
from transpiler.core.lib.builtins import Builtins
from transpiler.core.lib.library import Library


class StdBuiltinMapping:
    _lock = threading.Lock()
    builtin_map: dict[str, type[Library]] = {
        "builtins": Builtins,
        "experimental": Experimental,
    }

    @classmethod
    def registry(cls, name: str, lib: type[Library]):
        with cls._lock:
            cls.builtin_map[name] = lib

    @classmethod
    @lru_cache(maxsize=None)  # 无限缓存
    def get(cls, name: str, builder: IRBuilder) -> Library | None:
        lib: type[Library] = cls.builtin_map.get(name, None)
        if lib:
            return lib(builder)
        else:
            return None
