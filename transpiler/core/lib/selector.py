# coding=utf-8
from transpiler.core.lib.library import Library
from transpiler.core.safe_enum import SafeEnum


class TargetSelectorVariables(SafeEnum):
    NEAREST_PLAYER = "@p"
    RANDOM_PLAYER = "@r"
    ALL_PLAYER = "@a"
    ALL_ENTITIES = "@e"
    ENTITY_EXECUTING_COMMAND = "@s"
    NEAREST_ENTITY = "@n"


class Selector(Library):
    pass