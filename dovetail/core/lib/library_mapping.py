# coding=utf-8
"""
内置库映射表
"""
import threading
from functools import lru_cache

from dovetail.core.ir_builder import IRBuilder
from dovetail.core.lib.builtins import Builtins
from dovetail.core.lib.experimental import Experimental
from dovetail.core.lib.lib_int_list import IntList
from dovetail.core.lib.lib_math import Math
from dovetail.core.lib.lib_random import Random
from dovetail.core.lib.library import Library
from dovetail.core.lib.strlib import Strlib


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
