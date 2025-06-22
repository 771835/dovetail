# coding=utf-8
from mcfdsl.core.ir.base import IRNode


class RawCommand(IRNode):

    def __init__(self, commands:list[str]):
        self.commands = commands

    def generate_commands(self) -> list[str]:
        return self.commands

    def __repr__(self):
        return \
f"""{self.__class__.__name__}(
    commands = {self.commands}
)
"""