# coding=utf-8
from dovetail.core.lib.library import Library, LibraryContext

# TODO: 实现 data_get和 scoreboard_get 的内建函数形式
class GettingCommands(Library):
    def __init__(self, context: LibraryContext):
        self.context = context
    def __str__(self) -> str:
        return "getting commands"
