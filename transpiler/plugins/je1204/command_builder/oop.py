# coding=utf-8
"""
面对对象特性的指令生成函数
"""
from transpiler.core.enums import DataType, ValueType
from transpiler.core.symbols import Variable, Constant, Reference, Literal
from transpiler.utils.escape_processor import auto_escape
from . import BasicCommands
from ..code_generator_scope import CodeGeneratorScope


class OOP:
    """
    面对对象特性生成
    """

    @staticmethod
    def get_property(
            result: Variable,
            result_scope: CodeGeneratorScope,
            result_objective: str,
            obj: Variable | Constant,
            obj_scope: CodeGeneratorScope,
            obj_objective: str,
            property_name: str
    ) -> list[str]:
        obj_path = BasicCommands.get_symbol_path(obj_scope, obj)
        result_path = BasicCommands.get_symbol_path(result_scope, result)
        commands = [BasicCommands.Copy.copy_score_to_storage(obj, obj_scope, obj_objective)]
        if result.dtype == DataType.STRING:
            commands.extend(
                BasicCommands.call_macros_function(
                    f"{obj_scope.namespace}:builtins/oop/get_property_storage",
                    result_objective,
                    {
                        "target": (
                            False,
                            result_objective,
                            None
                        ),
                        "target_path": (
                            False,
                            result_path,
                            None
                        ),
                        "source": (
                            False,
                            obj_objective,
                            None
                        ),
                        "id": (
                            True,
                            obj_path,
                            obj_objective
                        ),
                        "property": (
                            False,
                            property_name,
                            None
                        )
                    }
                )
            )
        else:  # 类/整数/布尔值
            commands.extend(
                BasicCommands.call_macros_function(
                    f"{obj_scope.namespace}:builtins/oop/get_property_score",
                    result_objective,
                    {
                        "objective": (
                            False,
                            result_objective,
                            None
                        ),
                        "target": (
                            False,
                            result_path,
                            None
                        ),
                        "source": (
                            False,
                            obj_objective,
                            None
                        ),
                        "id": (
                            True,
                            obj_path,
                            obj_objective
                        ),
                        "property": (
                            False,
                            property_name,
                            None
                        )
                    }
                )
            )
        return commands

    @staticmethod
    def set_property(
            obj: Variable | Constant,
            obj_scope: CodeGeneratorScope,
            obj_objective: str,
            value: Reference[Variable | Constant | Literal],
            value_scope: CodeGeneratorScope,
            value_objective: str,
            property_name: str
    ) -> list[str]:
        obj_path = BasicCommands.get_symbol_path(obj_scope, obj)
        commands = [BasicCommands.Copy.copy_score_to_storage(obj, obj_scope, obj_objective)]

        if value.get_data_type() == DataType.STRING:  # 字符串
            if value.value_type != Literal:
                commands.extend(
                    BasicCommands.call_macros_function(
                        f"{obj_scope.namespace}:builtins/oop/set_property_storage",
                        obj_objective,
                        {
                            "target": (
                                False,
                                obj_objective,
                                None
                            ),
                            "id": (
                                True,
                                obj_path,
                                obj_objective
                            ),
                            "property": (
                                False,
                                property_name,
                                None
                            ),
                            "source": (
                                False,
                                value_objective,
                                None
                            ),
                            "source_path": (
                                False,
                                BasicCommands.get_symbol_path(value_scope, value),
                                None
                            )
                        }
                    )
                )
            else:
                commands.extend(
                    BasicCommands.call_macros_function(
                        f"{obj_scope.namespace}:builtins/oop/set_property_storage_value",
                        obj_objective,
                        {
                            "target": (
                                False,
                                obj_objective,
                                None
                            ),
                            "id": (
                                True,
                                obj_path,
                                obj_objective
                            ),
                            "property": (
                                False,
                                property_name,
                                None
                            ),
                            "value": (
                                False,
                                auto_escape(value.value.value),
                                None
                            )
                        }
                    )
                )
        else:  # 整数/布尔值/实例

            if value.value_type != ValueType.LITERAL:
                commands.append(BasicCommands.Copy.copy_score_to_storage(value.value, value_scope, value_objective))

            commands.extend(
                BasicCommands.call_macros_function(
                    f"{obj_scope.namespace}:builtins/oop/set_property_score_value",
                    obj_objective,
                    {
                        "target": (
                            False,
                            obj_objective,
                            None
                        ),
                        "id": (
                            True,
                            obj_path,
                            obj_objective
                        ),
                        "property": (
                            False,
                            property_name,
                            None
                        ),
                        "value": (
                            value.value_type != ValueType.LITERAL,
                            (
                                BasicCommands.get_symbol_path(value_scope, value)
                                if value.value_type != ValueType.LITERAL else
                                auto_escape(value.value.value)
                            ),
                            value_objective
                        )
                    }
                )
            )

        return commands
