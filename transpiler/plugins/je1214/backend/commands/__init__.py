# coding=utf-8
"""
命令构造模块

给定参数并构造命令
转义应在底层命令构造完成
以_开头的模块为基础命令，直接映射游戏原始命令
其他模块为组合命令，以目标为导向
"""
from ._data import DataBuilder
from ._execute import Execute
from ._function import FunctionBuilder
from ._return import ReturnBuilder
from ._scoreboard import ScoreboardBuilder
from ._summon import SummonBuilder

MINECRAFT_VERSION = ["1.21.4"]
__all__ = [
    "ReturnBuilder",
    "DataBuilder",
    "Execute",
    "ScoreboardBuilder",
    "SummonBuilder",
    "FunctionBuilder",
]
