# coding=utf-8
from ._execute import Execute
from ._scoreboard import Scoreboard
from ._function import Function
from .composite import Composite
from .base import BasicCommands
from ._data import Data

__all__ = ['Execute', 'Scoreboard', 'Composite', 'BasicCommands', 'Function', 'Data']
MINECRAFT_VERSION = ['1.20.4']
