# coding=utf-8
import uuid

from ..code_generator_scope import CodeGeneratorScope
from . import BasicCommands, FunctionBuilder
from ._data import DataBuilder
from ._execute import Execute
from ._scoreboard import ScoreboardBuilder
from transpiler.core.language_enums import DataType, ValueType, CompareOps, BinaryOps
from transpiler.core.symbols import Constant, Variable, Reference, Literal
import typing


class Composite:
    @staticmethod
    def var_compare_base_type(left: Reference[Variable | Constant | Literal], left_scope: CodeGeneratorScope,
                              left_objective: str, op: CompareOps, right: Reference[Variable | Constant | Literal],
                              right_scope: CodeGeneratorScope, right_objective: str, result: Variable | Constant,
                              result_scope: CodeGeneratorScope, result_objective: str) -> list[str] | None:

        commands = []

        op_value: typing.Literal["=", "<", "<=", ">", ">="]
        op_value = op.value  # NOQA

        result_path = result_scope.get_symbol_path(result.get_name())

        # 自动将==替换为游戏支持的=
        if op.value == "==":
            op_value = "="

        if left.get_data_type() != right.get_data_type():
            return [BasicCommands.Copy.copy_literal_base_type(result, result_scope, result_objective,
                                                              Literal(DataType.BOOLEAN, False))]

        if left.get_data_type() in (DataType.INT, DataType.BOOLEAN):
            if left.value_type == ValueType.LITERAL:  # 左为字面量
                left_name = uuid.uuid4().hex
                left_path = left_scope.get_symbol_path(left_name)
                commands.append(ScoreboardBuilder.set_score(left_path, left_objective, left.value.value))
            else:
                left_path = left_scope.get_symbol_path(left.get_name())

            if right.value_type == ValueType.LITERAL:  # 右为字面量
                right_name = uuid.uuid4().hex
                right_path = right_scope.get_symbol_path(right_name)
                commands.append(ScoreboardBuilder.set_score(right_path, right_objective, right.value.value))
            else:
                right_path = right_scope.get_symbol_path(right.get_name())

            commands.append(Execute.execute().if_score_compare(left_path, left_objective,
                                                               op_value if op_value != "!=" else "=", right_path,
                                                               right_objective).run(
                ScoreboardBuilder.set_score(result_path, result_objective,
                                            1 if op_value != "!=" else 0)))
            commands.append(
                Execute.execute().unless_score_compare(left_path, left_objective,
                                                       op_value if op_value != "!=" else "=", right_path,
                                                       right_objective).run(
                    ScoreboardBuilder.set_score(result_path, result_objective,
                                                0 if op_value != "!=" else 1)))
        elif left.get_data_type() == DataType.STRING:
            if left.value_type == ValueType.LITERAL:  # 左为字面量
                left_name = uuid.uuid4().hex
                left_path = left_scope.get_symbol_path(left_name)
                commands.append(DataBuilder.modify_storage_set_value(left_path, left_objective, left.value.value))
            else:
                left_path = left_scope.get_symbol_path(left.get_name())

            if right.value_type == ValueType.LITERAL:  # 右为字面量
                right_name = uuid.uuid4().hex
                right_path = right_scope.get_symbol_path(right_name)
                commands.append(DataBuilder.modify_storage_set_value(right_path, right_objective, right.value.value))
            else:
                right_path = right_scope.get_symbol_path(right.get_name())

            temp_path = left_scope.get_symbol_path(uuid.uuid4().hex)
            commands.append(
                DataBuilder.modify_storage_set_from_storage(left_objective, temp_path, left_objective, left_path))
            commands.append(Execute.execute().store_success_score(result_path, result_objective).run(
                DataBuilder.modify_storage_set_from_storage(left_objective, temp_path, right_objective, right_path)))
            if op_value == "==":
                commands.append(Execute.execute().if_score_matches(result_path, result_objective, "1").run(
                    ScoreboardBuilder.set_score(result_path, result_objective, 0)))
                commands.append(Execute.execute().unless_score_matches(result_path, result_objective, "1").run(
                    ScoreboardBuilder.set_score(result_path, result_objective, 1)))

        return commands

    @staticmethod
    def op_base_type(result: Variable | Constant, result_scope: CodeGeneratorScope, result_objective: str,
                     op: BinaryOps, left: Reference[Variable | Constant | Literal],
                     left_scope: CodeGeneratorScope, left_objective: str,
                     right: Reference[Variable | Constant | Literal], right_scope: CodeGeneratorScope,
                     right_objective: str,
                     namespace: str = "") -> list[str] | None:
        result_path = result_scope.get_symbol_path(result.get_name())
        handlers = {
            BinaryOps.ADD: lambda target_scope, target, target_obj, source_scope, source, source_obj:
            ScoreboardBuilder.add_op(
                target_scope.get_symbol_path(target.get_name()),
                target_obj,
                source_scope.get_symbol_path(source.get_name()),
                source_obj
            ),
            BinaryOps.SUB: lambda target_scope, target, target_obj, source_scope, source, source_obj:
            ScoreboardBuilder.sub_op(
                target_scope.get_symbol_path(target.get_name()),
                target_obj,
                source_scope.get_symbol_path(source.get_name()),
                source_obj
            ),
            BinaryOps.MUL: lambda target_scope, target, target_obj, source_scope, source, source_obj:
            ScoreboardBuilder.mul_op(
                target_scope.get_symbol_path(target.get_name()),
                target_obj,
                source_scope.get_symbol_path(source.get_name()),
                source_obj
            ),
            BinaryOps.DIV: lambda target_scope, target, target_obj, source_scope, source, source_obj:
            ScoreboardBuilder.div_op(
                target_scope.get_symbol_path(target.get_name()),
                target_obj,
                source_scope.get_symbol_path(source.get_name()),
                source_obj
            ),
            BinaryOps.MOD: lambda target_scope, target, target_obj, source_scope, source, source_obj:
            ScoreboardBuilder.mod_op(
                target_scope.get_symbol_path(target.get_name()),
                target_obj,
                source_scope.get_symbol_path(source.get_name()),
                source_obj
            ),
            BinaryOps.MIN: lambda target_scope, target, target_obj, source_scope, source, source_obj:
            ScoreboardBuilder.min_op(
                target_scope.get_symbol_path(target.get_name()),
                target_obj,
                source_scope.get_symbol_path(source.get_name()),
                source_obj
            ),
            BinaryOps.MAX: lambda target_scope, target, target_obj, source_scope, source, source_obj:
            ScoreboardBuilder.max_op(
                target_scope.get_symbol_path(target.get_name()),
                target_obj,
                source_scope.get_symbol_path(source.get_name()),
                source_obj
            )
        }
        if right.value == result:
            right, left = left, right
            left_scope, right_scope = right_scope, left_scope
            left_objective, right_objective = right_objective, left_objective
        if result.dtype in (DataType.INT, DataType.BOOLEAN):
            if left.value == result:  # 因为该比较，所以left绝对为Variable 或 Constant
                if right.value_type in (ValueType.VARIABLE, ValueType.CONSTANT):
                    return [handlers[op](left_scope, left, left_objective, right_scope, right, right_objective)]
                else:  # right=literal
                    literal_handlers = {
                        # 加法操作
                        BinaryOps.ADD: lambda target_scope, target, target_objective, score:
                        ScoreboardBuilder.add_score(
                            target_scope.get_symbol_path(target.get_name()),
                            target_objective,
                            score
                        ),

                        # 减法操作
                        BinaryOps.SUB: lambda target_scope, target, target_objective, score:
                        ScoreboardBuilder.sub_score(
                            target_scope.get_symbol_path(target.get_name()),
                            target_objective,
                            score
                        ),

                        # 乘法操作
                        BinaryOps.MUL: lambda target_scope, target, target_objective, score:
                        ScoreboardBuilder.mul_score(
                            target_scope.get_symbol_path(target.get_name()),
                            target_objective,
                            score
                        ),

                        # 除法操作
                        BinaryOps.DIV: lambda target_scope, target, target_objective, score:
                        ScoreboardBuilder.div_score(
                            target_scope.get_symbol_path(target.get_name()),
                            target_objective,
                            score
                        ),

                        # 取模操作
                        BinaryOps.MOD: lambda target_scope, target, target_objective, score:
                        ScoreboardBuilder.mod_score(
                            target_scope.get_symbol_path(target.get_name()),
                            target_objective,
                            score
                        ),
                        # 取最大值操作
                        BinaryOps.MAX: lambda target_scope, target, target_objective, score:
                        ScoreboardBuilder.max_score(
                            target_scope.get_symbol_path(target.get_name()),
                            target_objective,
                            score
                        ),
                        # 取最小值操作
                        BinaryOps.MIN: lambda target_scope, target, target_objective, score:
                        ScoreboardBuilder.min_score(
                            target_scope.get_symbol_path(target.get_name()),
                            target_objective,
                            score
                        ),
                    }

                    return literal_handlers[op](left_scope, left, left_objective, right.value.value)
            elif left.value_type == ValueType.LITERAL and right.value_type == ValueType.LITERAL:
                # 此处理论上应该是重复的，因为正常情况下这一步会被常量折叠优化(谁那么闲不开优化啊)
                literal_handlers = {BinaryOps.ADD: lambda a, b: ScoreboardBuilder.set_score(
                    result_path, result_objective, a + b),
                                    BinaryOps.SUB: lambda a, b: ScoreboardBuilder.set_score(
                                        result_path, result_objective, a - b),
                                    BinaryOps.MUL: lambda a, b: ScoreboardBuilder.set_score(
                                        result_path, result_objective, a * b),
                                    BinaryOps.DIV: lambda a, b: ScoreboardBuilder.set_score(
                                        result_path, result_objective, a / b),
                                    BinaryOps.MOD: lambda a, b: ScoreboardBuilder.set_score(
                                        result_path, result_objective, a % b),
                                    BinaryOps.BIT_AND: lambda a, b: ScoreboardBuilder.set_score(
                                        result_path, result_objective, a & b),
                                    BinaryOps.BIT_OR: lambda a, b: ScoreboardBuilder.set_score(
                                        result_path, result_objective, a | b),
                                    BinaryOps.BIT_XOR: lambda a, b: ScoreboardBuilder.set_score(
                                        result_path, result_objective, a ^ b),
                                    BinaryOps.SHL: lambda a, b: ScoreboardBuilder.set_score(
                                        result_path, result_objective, a << b),
                                    BinaryOps.SHR: lambda a, b: ScoreboardBuilder.set_score(
                                        result_path, result_objective, a >> b),
                                    BinaryOps.MIN: lambda a, b: ScoreboardBuilder.set_score(
                                        result_path, result_objective, min(a, b)),
                                    BinaryOps.MAX: lambda a, b: ScoreboardBuilder.set_score(
                                        result_path, result_objective, max(a, b))
                                    }
                return [literal_handlers[op](left.value.value, left.value.value)]
            elif left.value_type == ValueType.LITERAL or right.value_type == ValueType.LITERAL:
                commands = []
                if right.value_type == ValueType.LITERAL:
                    right, left = left, right
                    left_scope, right_scope = right_scope, left_scope
                    left_objective, right_objective = right_objective, left_objective
                commands.append(ScoreboardBuilder.set_score(result_path, result_objective, left.value.value))
                commands.append(
                    handlers[op](result_scope, result, result_objective, right_scope, right, right_objective))
                return commands
            else:  # 两操作数均为变量或从常量
                commands = [
                    ScoreboardBuilder.set_op(result_path, result_objective, left_scope.get_symbol_path(left.get_name()),
                                             left_objective)]

                commands.extend(
                    handlers[op](result_scope, result, result_objective, right_scope, right, right_objective))
                return commands
        elif result.dtype == DataType.STRING:
            commands = []
            args_path = f"builtins.strcat.args" + uuid.uuid4().hex

            if left.value_type == ValueType.LITERAL:
                commands.append(DataBuilder.modify_storage_set_value("var", args_path + ".dest", str(left.value.value)))
            else:
                commands.append(DataBuilder.modify_storage_set_from_storage("var", args_path + ".dest", left_objective,
                                                                            left_scope.get_symbol_path(
                                                                                left.get_name())))

            if right.value_type == ValueType.LITERAL:
                commands.append(
                    DataBuilder.modify_storage_set_value("var", args_path + ".dest", str(right.value.value)))
            else:
                commands.append(
                    DataBuilder.modify_storage_set_from_storage("var", args_path + ".src", right_objective,
                                                                right_scope.get_symbol_path(right.get_name())))

            commands.append(
                DataBuilder.modify_storage_set_from_storage("var", args_path + ".target", right_objective,
                                                            result_objective))
            commands.append(
                DataBuilder.modify_storage_set_from_storage("var", args_path + ".target_path", right_objective,
                                                            result_path))

            commands.append(FunctionBuilder.run_with_source(f"{namespace}:builtins/strcat", "storage", args_path))

            return commands


        return None
