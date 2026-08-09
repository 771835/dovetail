# coding=utf-8
from dovetail.core.lib.lib_factory import LibraryBase, lib_var, builtin_func

class Math(LibraryBase):
    INT_MAX = lib_var(int, 2147483647)
    INT_MIN = lib_var(int, -2147483648)

    def __init__(self, context):
        self._init(context)

    def __str__(self) -> str:
        return "math"

    @builtin_func(returns=int)
    def abs(self, value: int): ...

    @builtin_func(returns=int)
    def min(self, a: int, b: int): ...

    @builtin_func(returns=int)
    def max(self, a: int, b: int): ...