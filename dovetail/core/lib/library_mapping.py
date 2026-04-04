# coding=utf-8
"""
内置库映射表
"""
import threading
from functools import lru_cache

from dovetail.core.lib.builtins import Builtins
from dovetail.core.lib.experimental import Experimental
from dovetail.core.lib.lib_int_list import IntList
from dovetail.core.lib.lib_math import Math
from dovetail.core.lib.lib_random import Random
from dovetail.core.lib.library import Library
from dovetail.core.lib.strlib import Strlib
from dovetail.core.parser.tools.error_reporter import ErrorReporter
from dovetail.core.parser.tools.ir_emitter import IREmitter
from dovetail.core.parser.tools.symbol_resolver import SymbolResolver


class LibraryMapping:
    _lock = threading.Lock()
    builtin_map: dict[str, type[Library]] = {
        "builtins": Builtins,
        "dovetail.builtins": Builtins,
        "experimental": Experimental,
        "dovetail.experimental": Experimental,
        "random": Random,
        "dovetail.minecraft.random": Random,
        "math": Math,
        "dovetail.math": Math,
        "int_list": IntList,
        "dovetail.list.int_list": IntList,
        "strlib": Strlib,
        "dovetail.strlib": Strlib,
    }

    @classmethod
    def registry(cls, name: str, lib: type[Library]):
        with cls._lock:
            cls.builtin_map[name] = lib

    @classmethod
    @lru_cache(maxsize=None)  # 无限缓存
    def get(cls, name: str, symbol_resolver: SymbolResolver, emitter: IREmitter,
            error_reporter: ErrorReporter) -> Library | None:
        lib: type[Library] | None = cls.builtin_map.get(name, None)
        if lib is not None:
            return lib(symbol_resolver, emitter, error_reporter)
        return None
