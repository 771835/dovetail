# coding=utf-8
from dovetail.utils.logger import get_logger
from ._data import DataBuilder
from ._function import FunctionBuilder
from .copy import Copy
from .tools import DataPath, StorageLocation, LiteralPoolTools

logger = get_logger(__name__)

def strcat_literal(result: DataPath, a: str, b: str):
    return Copy.copy_literals(result, str(a) + str(b))


def strcat_variable(result: DataPath, a: DataPath, b: DataPath):
    return [
        DataBuilder.modify_storage_set_value(
            "dnt:ram",
            "in",
            "[]"
        ),
        DataBuilder.modify_storage_append_from_storage(
            "dnt:ram",
            "in",
            *reversed(a)
        ), DataBuilder.modify_storage_append_from_storage(
            "dnt:ram",
            "in",
            *reversed(b)
        ), FunctionBuilder.run("dnt:concat")
        , Copy.copy(
            result,
            DataPath(
                "out",
                "dnt:ram",
                StorageLocation.STORAGE
            )
        )
    ]


def strcat(result: DataPath, a: DataPath | str, b: DataPath | str):
    if isinstance(a, str) and isinstance(b, str):
        return [strcat_literal(result, a, b)]
    else:
        if isinstance(a, str):
            assert isinstance(b, DataPath)
            a = LiteralPoolTools.get_literal_path(a, b.target)
        elif isinstance(b, str):
            assert isinstance(a, DataPath)
            b = LiteralPoolTools.get_literal_path(b, a.target)
        return strcat_variable(result, a, b)


def to_str(result: DataPath, value: DataPath | int):
    if isinstance(value, int):
        return [Copy.copy_literals(result, str(value))]

    if value.location == StorageLocation.SCORE:
        return [Copy.copy_score_to_storage(value, value),
                DataBuilder.modify_storage_set_string_storage(*reversed(result), *reversed(value))
                ]
    else:
        return [DataBuilder.modify_storage_set_string_storage(*reversed(result), *reversed(value))]
