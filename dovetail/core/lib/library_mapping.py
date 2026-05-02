# coding=utf-8
"""
内置库映射表
"""
import threading
from functools import lru_cache

from dovetail.core.compile_config import CompileConfig
from dovetail.core.lib.builtins import Builtins
from dovetail.core.lib.experimental import Experimental
from dovetail.core.lib.lib_assertion import Assertion
from dovetail.core.lib.lib_math import Math
from dovetail.core.lib.lib_random import Random
from dovetail.core.lib.library import Library, LibraryContext
from dovetail.core.lib.lib_string import Strlib
from dovetail.core.parser.components.error_reporter import ErrorReporter
from dovetail.core.parser.components.ir_emitter import IREmitter
from dovetail.core.parser.components.symbol_resolver import SymbolResolver


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
        # "int_list": IntList,
        # "dovetail.list.int_list": IntList,
        "strlib": Strlib,
        "dovetail.strlib": Strlib,
        "assert": Assertion,
        "dovetail.assertion": Assertion,
    }

    @classmethod
    def registry(cls, name: str, lib: type[Library]):
        with cls._lock:
            cls.builtin_map[name] = lib

    @classmethod
    @lru_cache(maxsize=None)  # 无限缓存
    def get(cls, name: str, symbol_resolver: SymbolResolver, emitter: IREmitter,
            error_reporter: ErrorReporter, config: CompileConfig) -> Library | None:
        lib: type[Library] | None = cls.builtin_map.get(name, None)
        if lib is not None:
            return lib(LibraryContext(symbol_resolver, emitter, error_reporter, config))
        return None
