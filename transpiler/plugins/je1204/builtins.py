# coding=utf-8
import threading
import warnings
from typing import Callable

from transpiler.core.specification import CodeGeneratorSpec
from transpiler.core.symbols import Reference, Variable, Constant, Literal
from .command_builder import BasicCommands, Execute, ScoreboardBuilder, DataBuilder
from transpiler.utils.escape_processor import auto_escape
from ...core.enums.types import DataType, ValueType

builtin_func = {
    "builtins/exec": "$$(command)",
    "builtins/strcat": "$data modify storage $(target) $(target_path) set value '$(dest)$(src)'",
    "builtins/str2int": "$scoreboard players set $(target) $(objective) $(value)",
    "builtins/oop/get_property_score": "$execute store result score $(target) $(objective) run data get storage $(source) object.$(id).$(property) 1",
    "builtins/oop/get_property_storage": "$data modify storage $(target) $(target_path) set from storage $(source) object.$(id).$(property)",
    "builtins/oop/set_property_storage": "$data modify storage $(target) object.$(id).$(property) set from storage $(source) $(source_path)",
    "builtins/oop/set_property_storage_value": "$data modify storage $(target) object.$(id).$(property) set value \"$(value)\"",
    "builtins/oop/set_property_score_value": "$data modify storage $(target) object.$(id).$(property) set value $(value)",
    "builtins/oop/remove": "$data remove storage $(target) object.$(id)",
    "builtins/tellraw/tellraw_text": "$tellraw $(target) {\"storage\":\"$(objective)\",\"nbt\":\"$(path)\"}",
    "builtins/tellraw/tellraw_json": "$tellraw $(target) $(json)",
    "builtins/tellraw/tellraw_json_a": "$tellraw @a $(json)",
    "builtins/tellraw/tellraw_json_s": "$tellraw @s $(json)",
    "builtins/tellraw/tellraw_json_e": "$tellraw @e $(json)",
    "builtins/tellraw/tellraw_json_p": "$tellraw @p $(json)",
    "builtins/random/random_value_score": "$execute store result score $(target) $(objective) run random value $(min)..$(max)",
    "builtins/random/random_value_storage": "$execute store result storage $(target) $(target_path) int 1.0 run random value $(min)..$(max)",
    "builtins/setblock/setblock_a": "$setblock $(x) $(y) $(z) $(block_id) $(mode)",
    "builtins/setblock/setblock_d": "$setblock $(x) $(y) $(z) $(block_id) destroy",
    "builtins/setblock/setblock_k": "$setblock $(x) $(y) $(z) $(block_id) keep",
    "builtins/setblock/setblock_r": "$setblock $(x) $(y) $(z) $(block_id) replace",
    "builtins/setblock/setblock_s": "$setblock $(x) $(y) $(z) $(block_id) strict",
    "builtins/setblock/setblock_a_air": "$setblock $(x) $(y) $(z) air $(mode)",
    "builtins/setblock/setblock_d_air": "$setblock $(x) $(y) $(z) air destroy",
    "builtins/setblock/setblock_k_air": "$setblock $(x) $(y) $(z) air keep",
    "builtins/setblock/setblock_r_air": "$setblock $(x) $(y) $(z) air replace",
    "builtins/setblock/setblock_s_air": "$setblock $(x) $(y) $(z) air strict",
    "builtins/setblock/setblock_a_lava": "$setblock $(x) $(y) $(z) lava $(mode)",
    "builtins/setblock/setblock_d_lava": "$setblock $(x) $(y) $(z) lava destroy",
    "builtins/setblock/setblock_k_lava": "$setblock $(x) $(y) $(z) lava keep",
    "builtins/setblock/setblock_r_lava": "$setblock $(x) $(y) $(z) lava replace",
    "builtins/setblock/setblock_s_lava": "$setblock $(x) $(y) $(z) lava strict",
    "builtins/data/list_setitem_value": "$data modify storage $(target) object.$(id).value[$(index)] set value $(value)",
    "builtins/data/list_setitem_from": "$data modify storage $(target) object.$(id).value[$(index)] set from storage $(source) $(source_path)",
    "builtins/data/list_getitem_storage": "$data modify storage $(target) $(target_path) set from storage $(source) object.$(id).value[$(index)]",
    "builtins/data/list_getitem_score": "$execute store result score $(target) $(objective) run data get storage $(source) object.$(id).value[$(index)] 1.0",
    "builtins/data/list_remove_item": "$data remove storage $(target) object.$(id).value[$(index)]",
    "builtins/data/list_setitem_value_o": "$data modify storage $(target) $(target_path)[$(index)] set value \"$(value)\"",
    "builtins/data/list_setitem_from_o": "$data modify storage $(target) $(target_path)[$(index)] set from storage $(source) $(source_path)",
    "builtins/data/list_getitem_storage_o": "$data modify storage $(target) $(target_path) set from storage $(source) $(source_path)[$(index)]",
    "builtins/data/list_getitem_score_o": "$execute store result score $(target) $(objective) run data get storage $(source) $(source_path)[$(index)] 1.0",
    "builtins/data/list_remove_o": "$data remove storage $(target) $(target_path)[$(index)]",
}


class Commands:

    @staticmethod
    def exec(result: Variable | Constant, generator,
             args: dict[str, Reference[Variable | Constant | Literal]]):
        command = args["command"]
        if command.value_type == ValueType.LITERAL:
            generator.current_scope.add_command(str(command.value.value))
        else:
            generator.current_scope.add_command(
                BasicCommands.call_macros_function(
                    f"{generator.namespace}:builtins/exec",
                    generator.var_objective,
                    {
                        "command": (
                            True,
                            generator.current_scope.get_symbol_path(command.get_name()),
                            generator.var_objective,
                        )
                    }
                )
            )

    class Tellraw:
        TELLRAW_JSON_HANDLERS = {
            "@a": "builtins/tellraw/tellraw_json_a",
            "@s": "builtins/tellraw/tellraw_json_s",
            "@e": "builtins/tellraw/tellraw_json_e",
            "@p": "builtins/tellraw/tellraw_json_p",
        }

        @staticmethod
        def tellraw_text(
                result: Variable | Constant,
                generator,
                args: dict[str, Reference[Variable | Constant | Literal]]
        ):
            target_ref = args["target"]
            message_ref = args["msg"]
            if message_ref.value_type == ValueType.LITERAL == target_ref.value_type:
                generator.current_scope.add_command(
                    f"tellraw {target_ref.value.value} \"{message_ref.value.value}\"")
            else:
                if target_ref.value_type == ValueType.LITERAL:
                    generator.current_scope.add_command(
                        f'tellraw '
                        f'{target_ref.value.value} '
                        f'{{"storage":"{generator.var_objective}","nbt":"{BasicCommands.get_symbol_path(generator.current_scope, message_ref)}"}}'
                    )
                    return

                generator.current_scope.add_command(
                    BasicCommands.call_macros_function(
                        f"{generator.namespace}:builtins/tellraw/tellraw_text",
                        generator.var_objective,
                        {
                            "target": (
                                target_ref.value_type != ValueType.LITERAL,
                                target_ref.value.value if target_ref.value_type != ValueType.LITERAL
                                else BasicCommands.get_symbol_path(generator.current_scope, target_ref),
                                generator.var_objective,
                            ),
                            "objective": (
                                False,
                                generator.var_objective,
                                None
                            ),
                            "path": (
                                False,
                                BasicCommands.get_symbol_path(generator.current_scope, message_ref),
                                None
                            ),

                        }
                    )
                )

        @staticmethod
        def tellraw_json(
                result: Variable | Constant,
                generator,
                args: dict[str, Reference[Variable | Constant | Literal]]
        ):
            target_ref = args["target"]
            json_ref = args["json"]
            if json_ref.value_type == ValueType.LITERAL == target_ref.value_type:
                generator.current_scope.add_command(f"tellraw {target_ref.value.value} {json_ref.value.value}")
            else:
                if target_ref.value_type == ValueType.LITERAL:
                    # 由于目标选择器是字面量，因此msg绝对不是字面量，故无需判断msg存入存储
                    target_value = str(target_ref.value.value)
                    if target_value in Commands.Tellraw.TELLRAW_JSON_HANDLERS:
                        generator.current_scope.add_command(
                            BasicCommands.call_macros_function(
                                f"{generator.namespace}:{Commands.Tellraw.TELLRAW_JSON_HANDLERS[target_value]}",
                                generator.var_objective,
                                {
                                    "json": (
                                        True,
                                        generator.current_scope.get_symbol_path(json_ref.get_name()),
                                        generator.var_objective,
                                    )
                                }
                            )
                        )
                        return

                generator.current_scope.add_command(
                    BasicCommands.call_macros_function(
                        f"{generator.namespace}:builtins/tellraw/tellraw_json",
                        generator.var_objective,
                        {
                            "target": (
                                target_ref.value_type != ValueType.LITERAL,
                                target_ref.value.value if target_ref.value_type != ValueType.LITERAL else generator.current_scope.get_symbol_path(
                                    target_ref.get_name()),
                                generator.var_objective,
                            ),
                            "json": (
                                json_ref.value_type != ValueType.LITERAL,
                                json_ref.value.value if json_ref.value_type != ValueType.LITERAL else generator.current_scope.get_symbol_path(
                                    json_ref.get_name()),
                                generator.var_objective,
                            )
                        }
                    )
                )

    class Random:
        @staticmethod
        def randint_both_literal(
                result: Variable | Constant,
                generator,
                min_value: int,
                max_value: int
        ):
            # 最小值大于最大值时
            if min_value > max_value:
                warnings.warn("Fucking minimum is greater than maximum, are you sure you're right?")
                # 进行替换
                min_value, max_value = max_value, min_value
            elif min_value == max_value:  # 最小值等于最大值的情况
                generator.current_scope.add_command(
                    ScoreboardBuilder.set_score(
                        generator.current_scope.get_symbol_path(result.get_name()),
                        generator.var_objective,
                        min_value
                    )
                )
                return
            generator.current_scope.add_command(
                Execute.execute()
                .store_result_score(
                    generator.current_scope.get_symbol_path(result.get_name()),
                    generator.var_objective
                )
                .run(
                    f"random value {min_value}..{max_value}",
                )
            )

        @staticmethod
        def randint_both_variable(
                result: Variable | Constant,
                generator,
                min_value: Variable | Constant,
                max_value: Variable | Constant
        ):
            # 将记分板复制到存储中以便于调用宏函数
            generator.current_scope.add_command(
                BasicCommands.Copy.copy_score_to_storage(
                    min_value,
                    generator.current_scope,
                    generator.var_objective
                )
            )
            generator.current_scope.add_command(
                BasicCommands.Copy.copy_score_to_storage(
                    min_value,
                    generator.current_scope,
                    generator.var_objective
                )
            )
            generator.current_scope.add_command(
                BasicCommands.call_macros_function(
                    f"{generator.namespace}:builtins/random/random_value_score",
                    generator.var_objective,
                    {
                        "target": (
                            False,
                            generator.current_scope.get_symbol_path(result.get_name()),
                            generator.var_objective,
                        ),
                        "objective": (
                            False,
                            generator.var_objective,
                            generator.var_objective,
                        ),
                        "min": (
                            True,
                            generator.current_scope.get_symbol_path(min_value.get_name()),
                            generator.var_objective,
                        ),
                        "max": (
                            True,
                            generator.current_scope.get_symbol_path(max_value.get_name()),
                            generator.var_objective,
                        )
                    }
                )
            )

        @staticmethod
        def randint_variable_and_literal(
                result: Variable | Constant,
                generator,
                min_value: Variable | Constant,
                max_value: int
        ):
            # 将记分板复制到存储中以便于调用宏函数
            generator.current_scope.add_command(
                BasicCommands.Copy.copy_score_to_storage(
                    min_value,
                    generator.current_scope,
                    generator.var_objective
                )
            )
            generator.current_scope.add_command(
                BasicCommands.call_macros_function(
                    f"{generator.namespace}:builtins/random/random_value_score",
                    generator.var_objective,
                    {
                        "target": (
                            False,
                            generator.current_scope.get_symbol_path(result.get_name()),
                            generator.var_objective,
                        ),
                        "objective": (
                            False,
                            generator.var_objective,
                            generator.var_objective,
                        ),
                        "min": (
                            True,
                            generator.current_scope.get_symbol_path(min_value.get_name()),
                            generator.var_objective
                        ),
                        "max": (
                            False,
                            max_value,
                            None
                        )
                    }
                )
            )

        @staticmethod
        def randint_literal_and_variable(
                result: Variable | Constant,
                generator,
                min_value: int,
                max_value: Variable | Constant
        ):
            # 将记分板复制到存储中以便于调用宏函数
            generator.current_scope.add_command(
                BasicCommands.Copy.copy_score_to_storage(
                    max_value,
                    generator.current_scope,
                    generator.var_objective
                )
            )
            generator.current_scope.add_command(
                BasicCommands.call_macros_function(
                    f"{generator.namespace}:builtins/random/random_value_score",
                    generator.var_objective,
                    {
                        "target": (
                            False,
                            generator.current_scope.get_symbol_path(result.get_name()),
                            generator.var_objective,
                        ),
                        "objective": (
                            False,
                            generator.var_objective,
                            generator.var_objective,
                        ),
                        "min": (
                            False,
                            min_value,
                            None
                        ),
                        "max": (
                            True,
                            generator.current_scope.get_symbol_path(max_value.get_name()),
                            generator.var_objective
                        )
                    }
                )
            )

        @staticmethod
        def randint(
                result: Variable | Constant,
                generator,
                args: dict[str, Reference[Variable | Constant | Literal]]
        ):
            minn = args["min"]
            maxx = args["max"]
            # 最大值与最小值均为字面量的情况
            if minn.value_type == ValueType.LITERAL == maxx.value_type:
                Commands.Random.randint_both_literal(
                    result,
                    generator,
                    minn.value.value,
                    maxx.value.value
                )
            elif minn.value_type != ValueType.LITERAL != maxx.value_type:
                Commands.Random.randint_both_variable(
                    result,
                    generator,
                    minn.value,
                    maxx.value
                )
            else:
                if minn.value_type == ValueType.LITERAL:
                    Commands.Random.randint_literal_and_variable(
                        result,
                        generator,
                        minn.value.value,
                        maxx.value
                    )
                else:
                    Commands.Random.randint_variable_and_literal(
                        result,
                        generator,
                        minn.value,
                        maxx.value.value
                    )

    class Block:
        SETBLOCK_HANDLERS = {
            "air": {
                "destroy": "builtins/setblock/setblock_d_air",
                "keep": "builtins/setblock/setblock_k_air",
                "replace": "builtins/setblock/setblock_r_air",
                "strict": "builtins/setblock/setblock_s_air",
                None: "builtins/setblock/setblock_a_air",
            },
            "lava": {
                "destroy": "builtins/setblock/setblock_d_lava",
                "keep": "builtins/setblock/setblock_k_lava",
                "replace": "builtins/setblock/setblock_r_lava",
                "strict": "builtins/setblock/setblock_s_lava",
                None: "builtins/setblock/setblock_a_lava",
            },
            None: {
                "destroy": "builtins/setblock/setblock_d",
                "keep": "builtins/setblock/setblock_k",
                "replace": "builtins/setblock/setblock_r",
                "strict": "builtins/setblock/setblock_s",
                None: "builtins/setblock/setblock_a",
            }
        }

        @staticmethod
        def setblock(result: Variable | Constant, generator,
                     args: dict[str, Reference[Variable | Constant | Literal]]):
            x = args["x"]
            y = args["y"]
            z = args["z"]
            block_id_ref = args["block_id"]
            mode_ref = args["mode"]
            if all(arg.value_type == ValueType.LITERAL for arg in args.values()):
                generator.current_scope.add_command(
                    f"setblock {x} {y} {z} {block_id_ref.value.value} {mode_ref.value.value}"
                )

            # 将x,y,z写入数据存储
            if x.value_type != ValueType.LITERAL:
                generator.current_scope.add_command(
                    BasicCommands.Copy.copy_score_to_storage(
                        x.value,
                        generator.current_scope,
                        generator.var_objective
                    )
                )
            if y.value_type != ValueType.LITERAL:
                generator.current_scope.add_command(
                    BasicCommands.Copy.copy_score_to_storage(
                        y.value,
                        generator.current_scope,
                        generator.var_objective
                    )
                )
            if z.value_type != ValueType.LITERAL:
                generator.current_scope.add_command(
                    BasicCommands.Copy.copy_score_to_storage(
                        z.value,
                        generator.current_scope,
                        generator.var_objective
                    )
                )

            block_id = None
            if block_id_ref.value_type == ValueType.LITERAL:
                block_id = block_id_ref.value.value
                # 检查方块id是否存在命名空间
                if ":" in block_id:
                    namespace, block_id_ = block_id.split(":")[:2]
                    if namespace == "minecraft":
                        block_id = block_id_

            mode_id = None
            if mode_ref.value_type == ValueType.LITERAL:
                mode_id = mode_ref.value.value
                if mode_id not in ["destroy", "keep", "replace", "strict"]:
                    # 提示填充类型不存在
                    warnings.warn(
                        f"Mode '{mode_id}' is not supported, are you sure it exists?\nuse --disable-warnings to block the warning")

            handler = Commands.Block.SETBLOCK_HANDLERS.get(block_id) or Commands.Block.SETBLOCK_HANDLERS.get(None)
            func_name = handler.get(mode_id) or handler.get(None)

            generator.current_scope.add_command(
                BasicCommands.call_macros_function(
                    f"{generator.namespace}:{func_name}",
                    generator.var_objective,
                    {
                        "x": (
                            x.value_type != ValueType.LITERAL,
                            generator.current_scope.get_symbol_path(
                                x.get_name()) if x.value_type != ValueType.LITERAL else x.value.value,
                            generator.var_objective,
                        ),
                        "y": (
                            y.value_type != ValueType.LITERAL,
                            generator.current_scope.get_symbol_path(
                                y.get_name()) if y.value_type != ValueType.LITERAL else y.value.value,
                            generator.var_objective,
                        ),
                        "z": (
                            z.value_type != ValueType.LITERAL,
                            generator.current_scope.get_symbol_path(
                                z.get_name()) if z.value_type != ValueType.LITERAL else z.value.value,
                            generator.var_objective,
                        ),
                        "mode" if mode_id not in handler or mode_id is None else None: (
                            mode_ref.value_type != ValueType.LITERAL,
                            generator.current_scope.get_symbol_path(
                                mode_ref.get_name()) if mode_ref.value_type != ValueType.LITERAL else mode_ref.value.value,
                            generator.var_objective,
                        ),
                        "block_id" if block_id not in Commands.Block.SETBLOCK_HANDLERS or block_id is None else None: (
                            block_id_ref.value_type != ValueType.LITERAL,
                            generator.current_scope.get_symbol_path(
                                block_id_ref.get_name()) if block_id_ref.value_type != ValueType.LITERAL else block_id_ref.value.value,
                            generator.var_objective,
                        ),
                    }
                )
            )

        @staticmethod
        def get_block(result: Variable | Constant, generator: CodeGeneratorSpec,
                      args: dict[str, Reference[Variable | Constant | Literal]]):
            pass

    @staticmethod
    def item_spawn(result: Variable | Constant, generator: CodeGeneratorSpec,
                   args: dict[str, Reference[Variable | Constant | Literal]]):
        pass

    @staticmethod
    def tp(result: Variable | Constant, generator: CodeGeneratorSpec,
           args: dict[str, Reference[Variable | Constant | Literal]]):
        pass

    @staticmethod
    def give(result: Variable | Constant, generator: CodeGeneratorSpec,
             args: dict[str, Reference[Variable | Constant | Literal]]):
        pass

    @staticmethod
    def summon(result: Variable | Constant, generator: CodeGeneratorSpec,
               args: dict[str, Reference[Variable | Constant | Literal]]):
        pass

    @staticmethod
    def kill(result: Variable | Constant, generator: CodeGeneratorSpec,
             args: dict[str, Reference[Variable | Constant | Literal]]):
        pass

    @staticmethod
    def time_set(result: Variable | Constant, generator: CodeGeneratorSpec,
                 args: dict[str, Reference[Variable | Constant | Literal]]):
        pass

    @staticmethod
    def weather(result: Variable | Constant, generator: CodeGeneratorSpec,
                args: dict[str, Reference[Variable | Constant | Literal]]):
        pass

    @staticmethod
    def difficulty(result: Variable | Constant, generator: CodeGeneratorSpec,
                   args: dict[str, Reference[Variable | Constant | Literal]]):
        pass

    @staticmethod
    def gamerule(result: Variable | Constant, generator: CodeGeneratorSpec,
                 args: dict[str, Reference[Variable | Constant | Literal]]):
        pass

    @staticmethod
    def fill(result: Variable | Constant, generator: CodeGeneratorSpec,
             args: dict[str, Reference[Variable | Constant | Literal]]):
        pass

    @staticmethod
    def effect(result: Variable | Constant, generator: CodeGeneratorSpec,
               args: dict[str, Reference[Variable | Constant | Literal]]):
        pass

    @staticmethod
    def attribute(result: Variable | Constant, generator: CodeGeneratorSpec,
                  args: dict[str, Reference[Variable | Constant | Literal]]):
        pass

    @staticmethod
    def tag(result: Variable | Constant, generator: CodeGeneratorSpec,
            args: dict[str, Reference[Variable | Constant | Literal]]):
        pass

    @staticmethod
    def damage(result: Variable | Constant, generator: CodeGeneratorSpec,
               args: dict[str, Reference[Variable | Constant | Literal]]):
        pass

    @staticmethod
    def scoreboard(result: Variable | Constant, generator: CodeGeneratorSpec,
                   args: dict[str, Reference[Variable | Constant | Literal]]):
        pass

    @staticmethod
    def bossbar(result: Variable | Constant, generator: CodeGeneratorSpec,
                args: dict[str, Reference[Variable | Constant | Literal]]):
        pass

    class Math:
        @staticmethod
        def abs(
                result: Variable | Constant,
                generator,
                args: dict[str, Reference[Variable | Constant | Literal]]
        ):
            value = args["value"]
            if value.value_type == ValueType.LITERAL:
                generator.current_scope.add_command(
                    BasicCommands.Copy.copy_literal_base_type(
                        result,
                        generator.current_scope,
                        generator.var_objective,
                        Literal(DataType.INT, abs(value.value.value))
                    )
                )
            else:
                generator.current_scope.add_command(
                    ScoreboardBuilder.set_score(
                        "-1",
                        generator.var_objective,
                        -1
                    )
                )
                if result.get_name() != value.get_name():
                    generator.current_scope.add_command(
                        BasicCommands.Copy.copy_base_type(
                            result,
                            generator.current_scope,
                            generator.var_objective,
                            value.value,
                            generator.current_scope,
                            generator.var_objective,
                        )
                    )
                generator.current_scope.add_command(
                    Execute.execute()
                    .if_score_matches(
                        BasicCommands.get_symbol_path(
                            generator.current_scope,
                            result,
                        ),
                        generator.var_objective,
                        "..-1"
                    )
                    .run(
                        ScoreboardBuilder.mul_op(
                            BasicCommands.get_symbol_path(
                                generator.current_scope,
                                result
                            ),
                            generator.var_objective,
                            "-1",
                            generator.var_objective,
                        )
                    )
                )

        @staticmethod
        def min(
                result: Variable | Constant,
                generator,
                args: dict[str, Reference[Variable | Constant | Literal]]
        ):
            a = args["a"]
            b = args["b"]
            if a.value_type == ValueType.LITERAL == b.value_type:
                generator.current_scope.add_command(
                    BasicCommands.Copy.copy_literal_base_type(
                        result,
                        generator.current_scope,
                        generator.var_objective,
                        Literal(DataType.INT, min(a.value.value, b.value.value))
                    )
                )
            elif a.value_type != ValueType.LITERAL != b.value_type:
                # 对于a与b相等的特殊情况
                if a.get_name() == b.get_name():
                    if a.get_name() != result.get_name():
                        generator.current_scope.add_command(
                            BasicCommands.Copy.copy_base_type(
                                result,
                                generator.current_scope,
                                generator.var_objective,
                                a.value,
                                generator.current_scope,
                                generator.var_objective
                            )
                        )
                    return
                # 如果b等于结果则a与b交换
                if b.get_name() == result.get_name():
                    a, b = b, a
                if a.get_name() != result.get_name():
                    # 将a的值复制到结果
                    generator.current_scope.add_command(
                        BasicCommands.Copy.copy_base_type(
                            result,
                            generator.current_scope,
                            generator.var_objective,
                            a.value,
                            generator.current_scope,
                            generator.var_objective,
                        )
                    )
                # 将结果与b进行比较
                generator.current_scope.add_command(
                    ScoreboardBuilder.min_op(
                        BasicCommands.get_symbol_path(
                            generator.current_scope,
                            result,
                        ),
                        generator.var_objective,
                        BasicCommands.get_symbol_path(
                            generator.current_scope,
                            b,
                        ),
                        generator.var_objective
                    )
                )
            else:  # 有一个是常量
                if a.value_type == ValueType.LITERAL:
                    a, b = b, a
                # 如果a等于结果
                if a.get_name() == result.get_name():
                    generator.current_scope.add_command(
                        ScoreboardBuilder.min_score(
                            BasicCommands.get_symbol_path(
                                generator.current_scope,
                                result,
                            ),
                            generator.var_objective,
                            b.value.value
                        )
                    )
                    return
                else:
                    # 否则将b复制到结果并与a进行比较
                    generator.current_scope.add_command(
                        BasicCommands.Copy.copy_literal_base_type(
                            result,
                            generator.current_scope,
                            generator.var_objective,
                            b.value,
                        )
                    )
                    generator.current_scope.add_command(
                        ScoreboardBuilder.min_op(
                            BasicCommands.get_symbol_path(
                                generator.current_scope,
                                result
                            ),
                            generator.var_objective,
                            BasicCommands.get_symbol_path(
                                generator.current_scope,
                                a
                            ),
                            generator.var_objective
                        )
                    )

        @staticmethod
        def max(
                result: Variable | Constant,
                generator,
                args: dict[str, Reference[Variable | Constant | Literal]]
        ):
            a = args["a"]
            b = args["b"]
            if a.value_type == ValueType.LITERAL == b.value_type:
                generator.current_scope.add_command(
                    BasicCommands.Copy.copy_literal_base_type(
                        result,
                        generator.current_scope,
                        generator.var_objective,
                        Literal(DataType.INT, max(a.value.value, b.value.value))
                    )
                )
            elif a.value_type != ValueType.LITERAL != b.value_type:
                # 对于a与b相等的特殊情况
                if a.get_name() == b.get_name():
                    if a.get_name() != result.get_name():
                        generator.current_scope.add_command(
                            BasicCommands.Copy.copy_base_type(
                                result,
                                generator.current_scope,
                                generator.var_objective,
                                a.value,
                                generator.current_scope,
                                generator.var_objective
                            )
                        )
                    return
                # 如果b等于结果则a与b交换
                if b.get_name() == result.get_name():
                    a, b = b, a
                if a.get_name() != result.get_name():
                    # 将a的值复制到结果
                    generator.current_scope.add_command(
                        BasicCommands.Copy.copy_base_type(
                            result,
                            generator.current_scope,
                            generator.var_objective,
                            a.value,
                            generator.current_scope,
                            generator.var_objective,
                        )
                    )
                # 将结果与b进行比较
                generator.current_scope.add_command(
                    ScoreboardBuilder.max_op(
                        BasicCommands.get_symbol_path(
                            generator.current_scope,
                            result,
                        ),
                        generator.var_objective,
                        BasicCommands.get_symbol_path(
                            generator.current_scope,
                            b,
                        ),
                        generator.var_objective
                    )
                )
            else:  # 有一个是常量
                if a.value_type == ValueType.LITERAL:
                    a, b = b, a
                # 如果a等于结果
                if a.get_name() == result.get_name():
                    generator.current_scope.add_command(
                        ScoreboardBuilder.max_score(
                            BasicCommands.get_symbol_path(
                                generator.current_scope,
                                result,
                            ),
                            generator.var_objective,
                            b.value.value
                        )
                    )
                    return
                else:
                    # 否则将b复制到结果并与a进行比较
                    generator.current_scope.add_command(
                        BasicCommands.Copy.copy_literal_base_type(
                            result,
                            generator.current_scope,
                            generator.var_objective,
                            b.value,
                        )
                    )
                    generator.current_scope.add_command(
                        ScoreboardBuilder.max_op(
                            BasicCommands.get_symbol_path(
                                generator.current_scope,
                                result
                            ),
                            generator.var_objective,
                            BasicCommands.get_symbol_path(
                                generator.current_scope,
                                a
                            ),
                            generator.var_objective
                        )
                    )

    class List:
        @staticmethod
        def init(result: Variable | Constant, generator, args: dict[str, Reference[Variable | Constant | Literal]]):
            list_var = args["list"]
            # 删除旧列表并创建新列表
            generator.current_scope.add_command(
                DataBuilder.remove_storage(
                    generator.var_objective,
                    BasicCommands.get_symbol_path(generator.current_scope, list_var.value)
                )
            )
            generator.current_scope.add_command(
                DataBuilder.modify_storage_set_value(
                    generator.var_objective,
                    BasicCommands.get_symbol_path(generator.current_scope, list_var.value),
                    "[]"
                )
            )

        @staticmethod
        def append(result: Variable | Constant, generator, args: dict[str, Reference[Variable | Constant | Literal]]):
            list_var = args["list"]
            value = args["value"]
            if value.value_type == ValueType.LITERAL:
                generator.current_scope.add_command(
                    DataBuilder.modify_storage_append_value(
                        generator.var_objective,
                        BasicCommands.get_symbol_path(generator.current_scope, list_var),
                        value.value.value if value.get_data_type() != DataType.STRING
                        else f'"{auto_escape(value.value.value)}"'
                    )
                )
            else:
                generator.current_scope.add_command(
                    DataBuilder.modify_storage_append_from_storage(
                        generator.var_objective,
                        BasicCommands.get_symbol_path(generator.current_scope, list_var),
                        generator.var_objective,
                        BasicCommands.get_symbol_path(generator.current_scope, value),
                    )
                )

        @staticmethod
        def setitem(result: Variable | Constant, generator, args: dict[str, Reference[Variable | Constant | Literal]]):
            list_var = args["list"]
            index = args["index"]
            value = args["value"]
            if index.value_type == ValueType.LITERAL:
                if value.value_type != ValueType.LITERAL:
                    if value.get_data_type() in (DataType.INT, DataType.BOOLEAN):
                        generator.current_scope.add_command(
                            BasicCommands.Copy.copy_score_to_storage(
                                value.value,
                                generator.current_scope,
                                generator.var_objective,
                            )
                        )
                    generator.current_scope.add_command(
                        DataBuilder.modify_storage_set_from_storage(
                            generator.var_objective,
                            f"{BasicCommands.get_symbol_path(generator.current_scope, list_var)}[{index.value.value}]",
                            generator.var_objective,
                            BasicCommands.get_symbol_path(generator.current_scope, value),
                        )
                    )
                else:
                    generator.current_scope.add_command(
                        DataBuilder.modify_storage_set_value(
                            generator.var_objective,
                            f"{BasicCommands.get_symbol_path(generator.current_scope, list_var)}[{index.value.value}]",
                            value.value.value if value.get_data_type() != DataType.STRING
                            else f'"{auto_escape(value.value.value)}"'
                        )
                    )
            else:
                if index.get_data_type() in (DataType.INT, DataType.BOOLEAN):
                    generator.current_scope.add_command(
                        BasicCommands.Copy.copy_score_to_storage(
                            index.value,
                            generator.current_scope,
                            generator.var_objective,
                        )
                    )

                if value.value_type != ValueType.LITERAL:
                    if value.get_data_type() in (DataType.INT, DataType.BOOLEAN):
                        generator.current_scope.add_command(
                            BasicCommands.Copy.copy_score_to_storage(
                                value.value,
                                generator.current_scope,
                                generator.var_objective,
                            )
                        )
                    generator.current_scope.add_command(
                        BasicCommands.call_macros_function(
                            f"{generator.namespace}:builtins/data/list_setitem_from",
                            generator.var_objective,
                            {
                                "target": (
                                    False,
                                    generator.var_objective,
                                    None
                                ),
                                "target_path": (
                                    False,
                                    BasicCommands.get_symbol_path(generator.current_scope, list_var),
                                    None
                                ),
                                "index": (
                                    True,
                                    BasicCommands.get_symbol_path(generator.current_scope, index),
                                    generator.var_objective
                                ),
                                "source": (
                                    False,
                                    generator.var_objective,
                                    None
                                ),
                                "source_path": (
                                    False,
                                    BasicCommands.get_symbol_path(generator.current_scope, value),
                                    None
                                )
                            }
                        )
                    )
                else:
                    generator.current_scope.add_command(
                        BasicCommands.call_macros_function(
                            f"{generator.namespace}:builtins/data/list_setitem_value",
                            generator.var_objective,
                            {
                                "target": (
                                    False,
                                    generator.var_objective,
                                    None
                                ),
                                "target_path": (
                                    False,
                                    BasicCommands.get_symbol_path(generator.current_scope, list_var),
                                    None
                                ),
                                "index": (
                                    True,
                                    BasicCommands.get_symbol_path(generator.current_scope, index),
                                    generator.var_objective
                                ),
                                "value": (
                                    False,
                                    auto_escape(value.value.value),
                                    None
                                )
                            }
                        )
                    )

        @staticmethod
        def getitem(result: Variable | Constant, generator, args: dict[str, Reference[Variable | Constant | Literal]]):
            list_var = args["list"]
            index = args["index"]
            if index.value_type == ValueType.LITERAL:
                if result.dtype == DataType.STRING:
                    generator.current_scope.add_command(
                        DataBuilder.modify_storage_set_from_storage(
                            generator.var_objective,
                            BasicCommands.get_symbol_path(generator.current_scope, result),
                            generator.var_objective,
                            f"{BasicCommands.get_symbol_path(generator.current_scope, list_var)}[{index.value.value}]",
                        )
                    )
                elif result.dtype in (DataType.INT, DataType.BOOLEAN):
                    generator.current_scope.add_command(
                        Execute.execute()
                        .store_result_score(
                            BasicCommands.get_symbol_path(generator.current_scope, result),
                            generator.var_objective
                        )
                        .run(
                            DataBuilder.get_storage(
                                generator.var_objective,
                                f"{BasicCommands.get_symbol_path(generator.current_scope, list_var)}[{index.value.value}]",
                            )
                        )
                    )
            else:
                if index.get_data_type() in (DataType.INT, DataType.BOOLEAN):
                    generator.current_scope.add_command(
                        BasicCommands.Copy.copy_score_to_storage(
                            index.value,
                            generator.current_scope,
                            generator.var_objective,
                        )
                    )

                if result.dtype == DataType.STRING:
                    generator.current_scope.add_command(
                        BasicCommands.call_macros_function(
                            f"{generator.namespace}:builtins/data/list_getitem_storage",
                            generator.var_objective,
                            {
                                "target": (
                                    False,
                                    generator.var_objective,
                                    None
                                ),
                                "target_path": (
                                    False,
                                    BasicCommands.get_symbol_path(generator.current_scope, result),
                                    None
                                ),
                                "index": (
                                    True,
                                    BasicCommands.get_symbol_path(generator.current_scope, index),
                                    generator.var_objective
                                ),
                                "source": (
                                    False,
                                    generator.var_objective,
                                    None
                                ),
                                "source_path": (
                                    False,
                                    BasicCommands.get_symbol_path(generator.current_scope, list_var),
                                    None
                                ),
                            }
                        )
                    )
                else:
                    generator.current_scope.add_command(
                        BasicCommands.call_macros_function(
                            f"{generator.namespace}:builtins/data/list_getitem_score",
                            generator.var_objective,
                            {
                                "objective": (
                                    False,
                                    generator.var_objective,
                                    None
                                ),
                                "target": (
                                    False,
                                    BasicCommands.get_symbol_path(generator.current_scope, result),
                                    None
                                ),
                                "index": (
                                    True,
                                    BasicCommands.get_symbol_path(generator.current_scope, index),
                                    generator.var_objective
                                ),
                                "source": (
                                    False,
                                    generator.var_objective,
                                    None
                                ),
                                "source_path": (
                                    False,
                                    BasicCommands.get_symbol_path(generator.current_scope, list_var),
                                    None
                                ),
                            }
                        )
                    )

        @staticmethod
        def clear(result: Variable | Constant, generator, args: dict[str, Reference[Variable | Constant | Literal]]):
            list_var = args["list"]
            generator.current_scope.add_command(
                DataBuilder.remove_storage(
                    generator.var_objective,
                    BasicCommands.get_symbol_path(generator.current_scope, list_var),
                )
            )

        @staticmethod
        def pop(result: Variable | Constant, generator, args: dict[str, Reference[Variable | Constant | Literal]]):
            list_var = args["list"]
            index = args["index"]

            if result:
                Commands.List.getitem(result, generator, args)

            if index.value_type == ValueType.LITERAL:
                generator.current_scope.add_command(
                    DataBuilder.remove_storage(
                        generator.var_objective,
                        f"{BasicCommands.get_symbol_path(generator.current_scope, list_var)}[{index.value.value}]",
                    )
                )
            else:
                if index.get_data_type() in (DataType.INT, DataType.BOOLEAN):
                    generator.current_scope.add_command(
                        BasicCommands.Copy.copy_score_to_storage(
                            index.value,
                            generator.current_scope,
                            generator.var_objective,
                        )
                    )

                generator.current_scope.add_command(
                    BasicCommands.call_macros_function(
                        f"{generator.namespace}:builtins/data/list_remove",
                        generator.var_objective,
                        {
                            "target": (
                                False,
                                generator.var_objective,
                                None
                            ),
                            "target_path": (
                                False,
                                BasicCommands.get_symbol_path(generator.current_scope, list_var),
                                None
                            ),
                            "index": (
                                True,
                                BasicCommands.get_symbol_path(generator.current_scope, index),
                                generator.var_objective
                            )
                        }
                    )
                )


class BuiltinFuncMapping:
    _lock = threading.Lock()
    builtin_map: dict[str, Callable[[Variable | Constant, CodeGeneratorSpec, dict[str, Reference]], None]] = {
        'exec': Commands.exec,
        'tellraw_text': Commands.Tellraw.tellraw_text,
        'tellraw_json': Commands.Tellraw.tellraw_json,
        'randint': Commands.Random.randint,
        'setblock': Commands.Block.setblock,
        'get_block': Commands.Block.get_block,
        'item_spawn': Commands.item_spawn,
        'tp': Commands.tp,
        'give': Commands.give,
        'summon': Commands.summon,
        'kill': Commands.kill,
        'time_set': Commands.time_set,
        'weather': Commands.weather,
        'difficulty': Commands.difficulty,
        'gamerule': Commands.gamerule,
        'fill': Commands.fill,
        'effect': Commands.effect,
        'attribute': Commands.attribute,
        'tag': Commands.tag,
        'damage': Commands.damage,
        'scoreboard': Commands.scoreboard,
        'bossbar': Commands.bossbar,
        'abs': Commands.Math.abs,
        'min': Commands.Math.min,
        'max': Commands.Math.max,
        'list_init': Commands.List.init,
        'list_append': Commands.List.append,
        'list_setitem': Commands.List.setitem,
        'list_getitem': Commands.List.getitem,
        'list_clear': Commands.List.clear,
        'list_pop': Commands.List.pop,

    }

    @classmethod
    def registry(cls, name: str, func: Callable[[Variable | Constant, CodeGeneratorSpec, dict[str, Reference]], None]):
        """
        注册函数

        Args:
            name : 函数名
            func : 函数实现
        """
        with cls._lock:
            cls.builtin_map[name] = func

    @classmethod
    def get(cls, name: str):
        """
        获得函数名对应的函数实现

        Args:
            name : 函数名
        """
        func = cls.builtin_map.get(name, None)
        if func:
            return func
        else:
            # 没有函数实现返回空实现
            return lambda result, generator, args: warnings.warn(f"Builtin function '{name}' not found.", )
