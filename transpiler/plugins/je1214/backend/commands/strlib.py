# coding=utf-8
from transpiler.core.config import get_project_logger
from . import DataBuilder, FunctionBuilder
from .copy import Copy
from .tools import DataPath, StorageLocation, LiteralPoolTools


def strcat_literal(result: DataPath, a: str, b: str):
    return Copy.copy_literals(result, str(a) + str(b))


def strcat_variable(result: DataPath, a: DataPath, b: DataPath):
    return [
        DataBuilder.modify_storage_set_from_storage(
            "stringlib:input",
            "concat[0]",
            *reversed(a)
        ), DataBuilder.modify_storage_set_from_storage(
            "stringlib:input",
            "concat[1]",
            *reversed(b)
        ), FunctionBuilder.run("stringlib:util/concat"), Copy.copy(
            result,
            DataPath(
                "concat",
                "stringlib:output",
                StorageLocation.STORAGE
            )
        )
    ]


def strcat(result: DataPath, a: DataPath | str, b: DataPath | str):
    if isinstance(a, str) and isinstance(b, str):
        return [strcat_literal(result, a, b)]
    else:
        if isinstance(a, str):
            a = LiteralPoolTools.get_literal_path(a, b.target)
        elif isinstance(b, str):
            b = LiteralPoolTools.get_literal_path(b, a.target)
        return strcat_variable(result, a, b)


def to_str(result: DataPath, value: DataPath | int):
    if isinstance(value, int):
        return [Copy.copy_literals(result, str(value))]

    return [
        Copy.copy(
            DataPath(
                "to_string.Input",
                "stringlib:input",
                StorageLocation.STORAGE
            ),
            value
        ),
        FunctionBuilder.run_with_source(
            "stringlib:util/to_string",
            "storage",
            "stringlib:input",
            "to_string"
        ),
        Copy.copy(
            result,
            DataPath(
                "to_string",
                "stringlib:output",
                StorageLocation.STORAGE
            )
        )
    ]


def to_int(result: DataPath, value: DataPath | str):
    if isinstance(value, str):
        try:
            return [Copy.copy_literals(result, int(value))]
        except ValueError:
            get_project_logger().error(f"'{value}' is not a number")
            return []

    return [
        DataBuilder.modify_storage_set_from_storage(
            "stringlib:input",
            "to_number.Input",
            *value
        ),
        FunctionBuilder.run_with_source(
            "stringlib:util/to_number",
            "storage",
            "stringlib:input",
            "to_number"
        ),
        Copy.copy(
            result,
            DataPath(
                "to_number",
                "stringlib:output",
                StorageLocation.STORAGE
            )
        )
    ]
