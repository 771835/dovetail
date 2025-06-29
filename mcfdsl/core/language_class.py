# coding=utf-8


import dataclasses
from abc import ABCMeta

from mcfdsl.core._interfaces import ISymbol, IScope


@dataclasses.dataclass
class Class(ABCMeta):
    methods: list[ISymbol]
    interfaces: list[ISymbol]
    consts: list[ISymbol]
    scope: IScope
