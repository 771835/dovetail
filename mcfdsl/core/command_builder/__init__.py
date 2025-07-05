# coding=utf-8
from ._data import Data
from ._execute import Execute
from ._function import Function
from ._scoreboard import Scoreboard
from .base import BasicCommands
from .composite import Composite

__all__ = ['Execute', 'Scoreboard', 'Composite', 'BasicCommands', 'Function', 'Data']
MINECRAFT_VERSION = ['1.20.4']
