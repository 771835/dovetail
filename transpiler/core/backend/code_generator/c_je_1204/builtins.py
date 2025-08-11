# coding=utf-8
import threading
import warnings
from typing import Callable

from transpiler.core.backend.code_generator.c_je_1204.command_builder import BasicCommands, Execute
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
    "builtins/tellraw/tellraw_json": "$tellraw $(target) \"$(msg)\"",
    "builtins/tellraw/tellraw_json_a": "$tellraw $(target) \"$(msg)\"",
    "builtins/tellraw/tellraw_json_s": "$tellraw $(target) \"$(msg)\"",
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

}


class Commands:
    SETBLOCK_HANDLERS = {
        "air": {
            "destroy": "builtins/setblock/setblock_d_air",
            "keep": "builtins/setblock/setblock_k_air",
            "replace": "builtins/setblock/setblock_r_air",
            "strict": "builtins/setblock/setblock_s_air",
            None: "builtins/setblock/setblock_a_air",
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

    @staticmethod
    def tellraw_text(result: Variable | Constant, generator, args: dict[str, Reference[Variable | Constant | Literal]]):
        target_ref: Reference[Variable | Constant | Literal] = args["target"]
        message_ref: Reference[Variable | Constant | Literal] = args["msg"]
        if message_ref.value_type == ValueType.LITERAL and target_ref.value_type == ValueType.LITERAL:
            target_value = str(target_ref.value.value)
            message = str(message_ref.value.value).replace('"', '\\"')
            generator.current_scope.add_command(f"tellraw {target_value} {message}")
        else:
            if target_ref.value_type == ValueType.LITERAL:
                target_value = str(target_ref.value.value)
                if target_value == "@a":
                    generator.current_scope.add_command(
                        BasicCommands.call_macros_function(
                            f"{generator.namespace}:builtins/tellraw/tellraw_text_a",
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
                elif target_value == "@s":
                    generator.current_scope.add_command(
                        BasicCommands.call_macros_function(
                            f"{generator.namespace}:builtins/tellraw/tellraw_text_s",
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
                                True,
                                generator.current_scope.get_symbol_path(target_ref.get_name()),
                                generator.var_objective,
                            ),
                            "msg": (
                                True,
                                generator.current_scope.get_symbol_path(message_ref.get_name()),
                                generator.var_objective,
                            )
                        }
                    )
                )

    @staticmethod
    def tellraw_json(result: Variable | Constant, generator,
                     args: dict[str, Reference[Variable | Constant | Literal]]):
        target_ref: Reference[Variable | Constant | Literal] = args["target"]
        json_text_ref: Reference[Variable | Constant | Literal] = args["json"]
        if json_text_ref.value_type == ValueType.LITERAL and target_ref.value_type == ValueType.LITERAL:
            generator.current_scope.add_command(f"tellraw {target_ref.value.value} {json_text_ref.value.value}")
        else:
            if target_ref.value_type == ValueType.LITERAL:
                target_value = str(target_ref.value.value)
                if target_value == "@a":
                    generator.current_scope.add_command(
                        BasicCommands.call_macros_function(
                            f"{generator.namespace}:builtins/tellraw/tellraw_json_a",
                            generator.var_objective,
                            {
                                "msg": (
                                    True,
                                    generator.current_scope.get_symbol_path(json_text_ref.get_name()),
                                    generator.var_objective,
                                )
                            }
                        )
                    )
                    return
                elif target_value == "@s":
                    generator.current_scope.add_command(
                        BasicCommands.call_macros_function(
                            f"{generator.namespace}:builtins/tellraw/tellraw_json_s",
                            generator.var_objective,
                            {
                                "msg": (
                                    True,
                                    generator.current_scope.get_symbol_path(json_text_ref.get_name()),
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
                                True,
                                generator.current_scope.get_symbol_path(target_ref.get_name()),
                                generator.var_objective,
                            ),
                            "msg": (
                                True,
                                generator.current_scope.get_symbol_path(json_text_ref.get_name()),
                                generator.var_objective,
                            )
                        }
                    )
                )

    @staticmethod
    def randint(result: Variable | Constant, generator,
                args: dict[str, Reference[Variable | Constant | Literal]]):
        minn: Reference[Variable | Constant | Literal] = args["min"]
        maxx: Reference[Variable | Constant | Literal] = args["max"]
        if minn.value_type == maxx.value_type == ValueType.LITERAL:
            generator.current_scope.add_command(
                Execute.execute().store_result_score(
                    generator.current_scope.get_symbol_path(result.get_name()),
                    generator.var_objective
                ).run(
                    f"random value {minn.value.value}..{maxx.value.value}"
                )
            )
        else:
            if minn.value_type != ValueType.LITERAL:
                generator.current_scope.add_command(
                    BasicCommands.Copy.copy_score_to_storage(minn.value, generator.current_scope,
                                                             generator.var_objective)
                )
            if maxx.value_type != ValueType.LITERAL:
                generator.current_scope.add_command(
                    BasicCommands.Copy.copy_score_to_storage(maxx.value, generator.current_scope,
                                                             generator.var_objective)
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
                            True if minn.value_type == ValueType.LITERAL else False,
                            minn.value.value if minn.value_type == ValueType.LITERAL else generator.current_scope.get_symbol_path(
                                minn.get_name()),
                            generator.var_objective,
                        ),
                        "max": (
                            True if maxx.value_type == ValueType.LITERAL else False,
                            maxx.value.value if minn.value_type == ValueType.LITERAL else generator.current_scope.get_symbol_path(
                                maxx.get_name()),
                            generator.var_objective,
                        ),

                    }
                )
            )

    @staticmethod
    def setblock(result: Variable | Constant, generator,
                 args: dict[str, Reference[Variable | Constant | Literal]]):
        x = args["x"]
        y = args["y"]
        z = args["z"]
        block_id = args["block_id"]
        mode = args["mode"]
        if all(arg.value_type == ValueType.LITERAL for arg in args.values()):
            generator.current_scope.add_command(f"setblock {x} {y} {z} {block_id} {mode}")

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

        block_id_value = None
        if block_id.value_type == ValueType.LITERAL:
            block_id_value = block_id.value.value

        mode_id_value = None
        if mode.value_type == ValueType.LITERAL:
            mode_id_value = mode.value.value

        handler = Commands.SETBLOCK_HANDLERS.get(block_id_value) or Commands.SETBLOCK_HANDLERS.get(None)
        func_name = handler.get(mode_id_value) or handler.get(None)

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
                    "mode" if mode_id_value not in handler or mode_id_value is None else None: (
                        True if mode.value_type != ValueType.LITERAL else False,
                        generator.current_scope.get_symbol_path(
                            mode.get_name()) if mode.value_type != ValueType.LITERAL else mode.value.value,
                        generator.var_objective,
                    ),
                    "block_id" if block_id_value not in Commands.SETBLOCK_HANDLERS or block_id_value is None else None: (
                        True if block_id.value_type != ValueType.LITERAL else False,
                        generator.current_scope.get_symbol_path(
                            block_id.get_name()) if block_id.value_type != ValueType.LITERAL else block_id.value.value,
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
        'tellraw_text': Commands.tellraw_text,
        'tellraw_json': Commands.tellraw_json,
        'randint': Commands.randint,
        'setblock': Commands.setblock,
        'is_block': Commands.is_block,
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
