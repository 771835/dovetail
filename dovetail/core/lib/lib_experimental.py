# coding=utf-8
from dovetail.core.lib.lib_factory import LibraryBase

class Experimental(LibraryBase):
    def __init__(self, context):
        self._init(context)

    def __str__(self) -> str:
        return "experimental"
