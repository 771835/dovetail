# coding=utf-8
"""
内置库映射表
"""
import threading
from functools import lru_cache

from transpiler.core.ir_builder import IRBuilder
from transpiler.core.lib.builtins import Builtins
from transpiler.core.lib.experimental import Experimental
from transpiler.core.lib.lib_int_list import IntList
from transpiler.core.lib.lib_math import Math
from transpiler.core.lib.lib_random import Random
from transpiler.core.lib.library import Library
from transpiler.core.lib.strlib import Strlib


class LibraryMapping:
    _lock = threading.Lock()
    builtin_map: dict[str, type[Library]] = {
        "builtins": Builtins,
        "builtin.builtins": Builtins,
        "experimental": Experimental,
        "builtin.experimental": Experimental,
        "random": Random,
        "builtin.math.random": Random,
        "math": Math,
        "builtin.math": Math,
        "int_list": IntList,
        "builtin.list.int_list": IntList,
        "strlib": Strlib,
        "builtin.strlib": Strlib
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
