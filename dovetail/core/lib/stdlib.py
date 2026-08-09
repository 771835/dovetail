# coding=utf-8

from dovetail.core.enums.datatypes import ArrayType, ListType
from dovetail.core.lib.lib_factory import builtin_func, LibraryBase


class Stdlib(LibraryBase):
    def __init__(self, context):
        self.context = context
        self._init(context)

    @builtin_func()
    def malloc(self, array: ArrayType | ListType, size: int): ...

    def __str__(self) -> str:
        return "stdlib"
