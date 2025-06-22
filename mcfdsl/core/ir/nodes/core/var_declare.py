# coding=utf-8
from mcfdsl.core.ir.base import IRNode


class VarDeclare(IRNode):

    def __init__(self, symbol, result):
        self.result = result
        self.symbol = symbol

    def __repr__(self):
        pass

    def generate_commands(self) -> list[str]:
        pass