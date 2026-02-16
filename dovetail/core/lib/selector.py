# coding=utf-8
from dovetail.core.lib.library import Library
from dovetail.utils.safe_enum import SafeEnum


class TargetSelectorVariables(SafeEnum):
    NEAREST_PLAYER = "@p"
    RANDOM_PLAYER = "@r"
    ALL_PLAYER = "@a"
    ALL_ENTITIES = "@e"
    ENTITY_EXECUTING_COMMAND = "@s"
    NEAREST_ENTITY = "@n"


class Selector(Library):
    pass
