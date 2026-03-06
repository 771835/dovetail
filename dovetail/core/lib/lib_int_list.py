# coding=utf-8
"""
int数组
"""
import uuid
from typing import Callable

from dovetail.core.enums.types import FunctionType, DataType, VariableType
from dovetail.core.instructions import IRInstruction, IRCall
from dovetail.core.ir_builder import IRBuilder
from dovetail.core.lib.library import Library
from dovetail.core.symbols import Reference, Function, Variable, Literal, Class, Parameter
from dovetail.utils.naming import NameNormalizer


class IntList(Library):
    def __init__(self, builder: IRBuilder):
        self.builder = builder
        self.classes: dict[Class, dict[str, Callable[..., Variable  | Literal | None]]] = {}
        # 初始化处理第一个类
        int_list_setitem_params = []
        int_list_getitem_params = []
        int_list_append_params = []
        int_list_clear_params = []
        int_list_init_params = []
        int_list_pop_params = []
        int_list_class = Class(
            NameNormalizer.normalize("IntList"),
            {
                Function(
                    NameNormalizer.normalize("__setitem__"),
                    int_list_setitem_params,
                    DataType.NULL_TYPE,
                    FunctionType.LIBRARY
                ),
                Function(
                    NameNormalizer.normalize("__getitem__"),
                    int_list_setitem_params,
                    DataType.INT,
                    FunctionType.LIBRARY
                ),
                Function(
                    NameNormalizer.normalize("append"),
                    int_list_append_params,
                    DataType.NULL_TYPE,
                    FunctionType.LIBRARY
                ),
                Function(
                    NameNormalizer.normalize("__init__"),
                    int_list_init_params,
                    DataType.NULL_TYPE,
                    FunctionType.LIBRARY
                ),
                Function(
                    "clear",
                    int_list_init_params,
                    DataType.NULL_TYPE,
                    FunctionType.LIBRARY
                ),
                Function(
                    "pop",
                    int_list_pop_params,
                    DataType.INT,
                    FunctionType.LIBRARY
                )
            },
            None,
            None,
            set()
        )
        int_list_setitem_params.extend(
            [
                Parameter(
                    Variable(
                        "self",
                        int_list_class,
                        VariableType.PARAMETER
                    )
                ),
                Parameter(
                    Variable(
                        "index",
                        DataType.INT,
                        VariableType.PARAMETER
                    )
                ),
                Parameter(
                    Variable(
                        "value",
                        DataType.INT,
                        VariableType.PARAMETER
                    )
                )
            ]
        )
        int_list_append_params.extend(
            [
                Parameter(
                    Variable(
                        "self",
                        int_list_class,
                        VariableType.PARAMETER
                    )
                ),
                Parameter(
                    Variable(
                        "value",
                        DataType.INT,
                        VariableType.PARAMETER
                    )
                )
            ]
        )
        int_list_getitem_params.extend(
            [
                Parameter(
                    Variable(
                        "self",
                        int_list_class,
                        VariableType.PARAMETER
                    )
                ),
                Parameter(
                    Variable(
                        "index",
                        DataType.INT,
                        VariableType.PARAMETER
                    )
                )
            ]
        )

        int_list_init_params.extend(
            [
                Parameter(
                    Variable(
                        "self",
                        int_list_class,
                        VariableType.PARAMETER
                    )
                )
            ]
        )
        int_list_clear_params.extend(
            [
                Parameter(
                    Variable(
                        "self",
                        int_list_class,
                        VariableType.PARAMETER
                    )
                )
            ]
        )
        int_list_pop_params.extend(
            [
                Parameter(
                    Variable(
                        "self",
                        int_list_class,
                        VariableType.PARAMETER
                    )
                ),
                Parameter(
                    Variable(
                        "index",
                        DataType.INT,
                        VariableType.PARAMETER
                    ),
                    True,
                    Reference.literal(-1)
                )
            ]
        )

        self.classes[int_list_class] = {
            "__init__": self._init,
            "__getitem__": self._getitem,
            "__setitem__": self._setitem,
            "append": self._append,
            "clear": self._clear,
            "pop": self._pop
        }

    def _clear(_self, self: Reference[Variable  | Literal]):
        _self.builder.insert(
            IRCall(
                self.value,
                Function(
                    "list_clear",
                    [
                        Parameter(
                            Variable(
                                "list",
                                DataType.NULL_TYPE,
                                VariableType.PARAMETER
                            )
                        )
                    ],
                    DataType.NULL_TYPE,
                    FunctionType.BUILTIN
                ),
                {
                    "list": self
                }
            )
        )

    def _setitem(_self, self: Reference[Variable  | Literal],
                 index: Reference[Variable  | Literal],
                 value: Reference[Variable  | Literal]) -> None:
        _self.builder.insert(
            IRCall(
                self.value,
                Function(
                    "list_setitem",
                    [
                        Parameter(
                            Variable(
                                "list",
                                DataType.NULL_TYPE,
                                VariableType.PARAMETER
                            )
                        ),
                        Parameter(
                            Variable(
                                "index",
                                DataType.INT,
                                VariableType.PARAMETER
                            )
                        ),
                        Parameter(
                            Variable(
                                "value",
                                DataType.INT,
                                VariableType.PARAMETER
                            )
                        )
                    ],
                    DataType.NULL_TYPE,
                    FunctionType.BUILTIN
                ),
                {
                    "list": self,
                    "index": index,
                    "value": value
                }
            )
        )

    def _append(_self, self: Reference[Variable  | Literal],
                value: Reference[Variable  | Literal]) -> None:
        _self.builder.insert(
            IRCall(
                self.value,
                Function(
                    "list_append",
                    [
                        Parameter(
                            Variable(
                                "list",
                                DataType.NULL_TYPE,
                                VariableType.PARAMETER
                            )
                        ),
                        Parameter(
                            Variable(
                                "value",
                                DataType.INT,
                                VariableType.PARAMETER
                            )
                        )
                    ],
                    DataType.NULL_TYPE,
                    FunctionType.BUILTIN
                ),
                {
                    "list": self,
                    "value": value
                }
            )
        )

    def _getitem(_self, self: Reference[Variable  | Literal],
                 index: Reference[Variable  | Literal]):
        result_var = Variable(
            "result_" + uuid.uuid4().hex[:8],
            DataType.INT,
            VariableType.PARAMETER)
        _self.builder.insert(
            IRCall(
                result_var,
                Function(
                    "list_getitem",
                    [
                        Parameter(
                            Variable(
                                "list",
                                DataType.NULL_TYPE,
                                VariableType.PARAMETER
                            )
                        ),
                        Parameter(
                            Variable(
                                "index",
                                DataType.INT,
                                VariableType.PARAMETER
                            )
                        )
                    ],
                    DataType.INT,
                    FunctionType.BUILTIN
                ),
                {
                    "list": self,
                    "index": index,
                }
            )
        )

        return result_var

    def _init(_self, self: Reference[Variable ]) -> None:
        _self.builder.insert(
            IRCall(
                self.value,
                Function(
                    "list_init",
                    [
                        Parameter(
                            Variable(
                                "list",
                                DataType.NULL_TYPE,
                                VariableType.PARAMETER
                            )
                        )
                    ],
                    DataType.NULL_TYPE,
                    FunctionType.BUILTIN
                ),
                {
                    "list": self
                }
            )
        )
        return

    def _pop(_self, self: Reference[Variable ], index: Reference[Variable  | Literal]):
        result_var = Variable(
            "result_" + uuid.uuid4().hex[:8],
            DataType.INT,
            VariableType.PARAMETER)
        _self.builder.insert(
            IRCall(
                result_var,
                Function(
                    "list_pop",
                    [
                        Parameter(
                            Variable(
                                "list",
                                DataType.NULL_TYPE,
                                VariableType.PARAMETER
                            )
                        ),
                        Parameter(
                            Variable(
                                "index",
                                DataType.INT,
                                VariableType.PARAMETER
                            )
                        )
                    ],
                    DataType.INT,
                    FunctionType.BUILTIN
                ),
                {
                    "list": self,
                    "index": index,
                }
            )
        )

        return result_var

    def __str__(self) -> str:
        return "IntList"

    def load(self) -> list[IRInstruction]:
        return []

    def get_functions(self) -> dict[Function, Callable[..., Variable  | Literal]]:
        return {}

    def get_variables(self) -> dict[Variable, Reference]:
        return {}

    def get_classes(self) -> dict[Class, dict[str, Callable[..., Variable  | Literal]]]:
        return self.classes
