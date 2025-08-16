# coding=utf-8
import threading
import warnings
from typing import Callable

from transpiler.core.backend.code_generator.c_je_1204.command_builder import BasicCommands, Execute, ScoreboardBuilder
from transpiler.core.backend.specification import CodeGeneratorSpec
from transpiler.core.enums import ValueType
from transpiler.core.symbols import Reference, Variable, Constant, Literal

builtin_func = {
    "builtins/exec": "$$(command)",
    "builtins/strcat": "$data modify storage $(target) $(target_path) set value '$(dest)$(src)'",
    "builtins/int2str": "$data modify storage $(target) $(target_path) set value '$(value)'",
    "builtins/str2int": "$scoreboard players set $(target) $(objective) $(value)'",
    "builtins/tellraw/tellraw_text": "$tellraw $(target) \"$(msg)\"",
    "builtins/tellraw/tellraw_text_a": "$tellraw @a \"$(msg)\"",
    "builtins/tellraw/tellraw_text_s": "$tellraw @s \"$(msg)\"",
    "builtins/tellraw/tellraw_text_e": "$tellraw @e \"$(msg)\"",
    "builtins/tellraw/tellraw_text_p": "$tellraw @p \"$(msg)\"",
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
}


class Commands:

    @staticmethod
    def exec(result: Variable | Constant, generator,
             args: dict[str, Reference[Variable | Constant | Literal]]):
        command: Reference[Variable | Constant | Literal] = args["command"]
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
        TELLRAW_TEXT_HANDLERS = {
            "@a": "builtins/tellraw/tellraw_text_a",
            "@s": "builtins/tellraw/tellraw_text_s",
            "@e": "builtins/tellraw/tellraw_text_e",
            "@p": "builtins/tellraw/tellraw_text_p",
        }
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
                message = str(message_ref.value.value).replace('"', '\\"')
                generator.current_scope.add_command(f"tellraw {target_ref.value.value} \"{message}\"")
            else:
                if target_ref.value_type == ValueType.LITERAL:
                    # 由于目标选择器是字面量，因此msg绝对不是字面量，故无需判断msg存入存储
                    target_value = str(target_ref.value.value)
                    if target_value in Commands.Tellraw.TELLRAW_TEXT_HANDLERS:
                        generator.current_scope.add_command(
                            BasicCommands.call_macros_function(
                                f"{generator.namespace}:{Commands.Tellraw.TELLRAW_TEXT_HANDLERS[target_value]}",
                                generator.var_objective,
                                {
                                    "msg": (
                                        True,
                                        generator.current_scope.get_symbol_path(message_ref.get_name()),
                                        generator.var_objective,
                                    )
                                }
                            )
                        )
                        return

                generator.current_scope.add_command(
                    BasicCommands.call_macros_function(
                        f"{generator.namespace}:builtins/tellraw/tellraw_text",
                        generator.var_objective,
                        {
                            "target": (
                                True if target_ref.value_type != ValueType.LITERAL else False,
                                target_ref.value.value if target_ref.value_type != ValueType.LITERAL else generator.current_scope.get_symbol_path(
                                    target_ref.get_name()),
                                generator.var_objective,
                            ),
                            "msg": (
                                True if message_ref.value_type != ValueType.LITERAL else False,
                                message_ref.value.value if message_ref.value_type != ValueType.LITERAL else generator.current_scope.get_symbol_path(
                                    message_ref.get_name()),
                                generator.var_objective,
                            )
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
                                True if target_ref.value_type != ValueType.LITERAL else False,
                                target_ref.value.value if target_ref.value_type != ValueType.LITERAL else generator.current_scope.get_symbol_path(
                                    target_ref.get_name()),
                                generator.var_objective,
                            ),
                            "json": (
                                True if json_ref.value_type != ValueType.LITERAL else False,
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
                            True if x.value_type != ValueType.LITERAL else False,
                            generator.current_scope.get_symbol_path(
                                x.get_name()) if x.value_type != ValueType.LITERAL else x.value.value,
                            generator.var_objective,
                        ),
                        "y": (
                            True if y.value_type != ValueType.LITERAL else False,
                            generator.current_scope.get_symbol_path(
                                y.get_name()) if y.value_type != ValueType.LITERAL else y.value.value,
                            generator.var_objective,
                        ),
                        "z": (
                            True if z.value_type != ValueType.LITERAL else False,
                            generator.current_scope.get_symbol_path(
                                z.get_name()) if z.value_type != ValueType.LITERAL else z.value.value,
                            generator.var_objective,
                        ),
                        "mode" if mode_id not in handler or mode_id is None else None: (
                            True if mode_ref.value_type != ValueType.LITERAL else False,
                            generator.current_scope.get_symbol_path(
                                mode_ref.get_name()) if mode_ref.value_type != ValueType.LITERAL else mode_ref.value.value,
                            generator.var_objective,
                        ),
                        "block_id" if block_id not in Commands.Block.SETBLOCK_HANDLERS or block_id is None else None: (
                            True if block_id_ref.value_type != ValueType.LITERAL else False,
                            generator.current_scope.get_symbol_path(
                                block_id_ref.get_name()) if block_id_ref.value_type != ValueType.LITERAL else block_id_ref.value.value,
                            generator.var_objective,
                        ),
                    }
                )
            )

        @staticmethod
        def is_block(result: Variable | Constant, generator: CodeGeneratorSpec,
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


class BuiltinFuncMapping:
    _lock = threading.Lock()
    builtin_map: dict[str, Callable[[Variable | Constant, CodeGeneratorSpec, dict[str, Reference]], None]] = {
        'exec': Commands.exec,
        'tellraw_text': Commands.Tellraw.tellraw_text,
        'tellraw_json': Commands.Tellraw.tellraw_json,
        'randint': Commands.Random.randint,
        'setblock': Commands.Block.setblock,
        'is_block': Commands.Block.is_block,
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
    }

    @classmethod
    def registry(cls, name: str, func: Callable[[Variable | Constant, CodeGeneratorSpec, dict[str, Reference]], None]):
        with cls._lock:
            cls.builtin_map[name] = func

    @classmethod
    def get(cls, name: str):
        func = cls.builtin_map.get(name, None)
        if func:
            return func
        else:
            return lambda result, generator, args: warnings.warn(f"Builtin function '{name}' not found.", )
