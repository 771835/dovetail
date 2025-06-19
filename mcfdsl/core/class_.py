# 暂不使用


import dataclasses

from mcfdsl.core._interfaces import ISymbol, IScope


@dataclasses.dataclass
class Class:
    methods:list[ISymbol]
    constructor:ISymbol
    interfaces:list[ISymbol]
    consts:list[ISymbol]
    scope:IScope
