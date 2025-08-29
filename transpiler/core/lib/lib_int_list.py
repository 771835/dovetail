# coding=utf-8
"""
int数组
"""
import uuid
from typing import Callable

from transpiler.core.backend.ir_builder import IRBuilder
from transpiler.core.enums import DataType, FunctionType, VariableType
from transpiler.core.instructions import IRInstruction, IRCall
from transpiler.core.lib.library import Library
from transpiler.core.symbols import Constant, Reference, Function, Variable, Literal, Class, Parameter


class IntList(Library):
    def __init__(self, builder: IRBuilder):
        self.builder = builder
        self.classes: dict[Class, dict[str, Callable[..., Variable | Constant | Literal | None]]] = {}
        # 初始化处理第一个类
        int_list_setitem_params = []
        int_list_getitem_params = []
        int_list_append_params = []

        int_list_init_params = []
        int_list_class = Class(
            "IntList",
            {
                Function(
                    "__setitem__",
                    int_list_setitem_params,
                    DataType.NULL,
                    FunctionType.LIBRARY
                ),
                Function(
                    "__getitem__",
                    int_list_setitem_params,
                    DataType.INT,
                    FunctionType.LIBRARY
                ),
                Function(
                    "append",
                    int_list_append_params,
                    DataType.NULL,
                    FunctionType.LIBRARY
                ),
                Function(
                    "__init__",
                    int_list_init_params,
                    DataType.NULL,
                    FunctionType.LIBRARY
                )
            },
            None,
            None,
            set(),
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
        self.classes[int_list_class] = {"__init__": self._int_list_init, "__getitem__": self._int_list_getitem,
                                        "append": self._int_list_append, "__setitem__": self._int_list_setitem}

    def _int_list_setitem(_self, self: Reference[Variable | Constant | Literal],
                          index: Reference[Variable | Constant | Literal],
                          value: Reference[Variable | Constant | Literal]) -> None:
        _self.builder.insert(
            IRCall(
                self.value,
                Function(
                    "list_setitem",
                    [
                        Parameter(
                            Variable(
                                "list",
                                DataType.NULL,
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
                    DataType.NULL,
                    FunctionType.BUILTIN
                ),
                {
                    "list": self,
                    "index": index,
                    "value": value
                }
            )
        )

    def _int_list_append(_self, self: Reference[Variable | Constant | Literal],
                          value: Reference[Variable | Constant | Literal]) -> None:
        _self.builder.insert(
            IRCall(
                self.value,
                Function(
                    "list_append",
                    [
                        Parameter(
                            Variable(
                                "list",
                                DataType.NULL,
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
                    DataType.NULL,
                    FunctionType.BUILTIN
                ),
                {
                    "list": self,
                    "value": value
                }
            )
        )


    def _int_list_getitem(_self, self: Reference[Variable | Constant | Literal],
                          index: Reference[Variable | Constant | Literal]):
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
                                DataType.NULL,
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
                    DataType.NULL,
                    FunctionType.BUILTIN
                ),
                {
                    "list": self,
                    "index": index,
                }
            )
        )
        return result_var

    def _int_list_init(_self, self: Reference[Variable | Constant]) -> None:
        # 似乎完全没必要初始化，因为有bug
        # _self.builder.insert(
        #     IRCall(
        #         self.value,
        #         Function(
        #             "list_init",
        #             [
        #                 Parameter(
        #                     Variable(
        #                         "list",
        #                         DataType.NULL,
        #                         VariableType.PARAMETER
        #                     )
        #                 )
        #             ],
        #             DataType.NULL,
        #             FunctionType.BUILTIN
        #         ),
        #         {
        #             "list": self
        #         }
        #     )
        # )
        return

    def __str__(self) -> str:
        return "int_list"

    def load(self) -> list[IRInstruction]:
        return []

    def get_functions(self) -> dict[Function, Callable[..., Variable | Constant | Literal]]:
        return {}

    def get_constants(self) -> dict[Constant, Reference]:
        return {}

    def get_classes(self) -> dict[Class, dict[str, Callable[..., Variable | Constant | Literal]]]:
        return self.classes
