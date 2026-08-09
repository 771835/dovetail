# coding=utf-8
from dovetail.core.lib.lib_factory import LibraryBase, builtin_func

class Random(LibraryBase):
    def __init__(self, context):
        self._init(context)

    def __str__(self) -> str:
        return "random"

    @builtin_func(returns=int)
    def randint(self, min: int, max: int): ...