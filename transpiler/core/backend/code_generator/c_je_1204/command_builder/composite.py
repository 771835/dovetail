# coding=utf-8
import uuid

from transpiler.core.enums import DataType, ValueType, CompareOps, BinaryOps
from transpiler.core.symbols import Constant, Variable, Reference, Literal
from . import BasicCommands
from ._data import DataBuilder
from ._execute import Execute
from ._scoreboard import ScoreboardBuilder
from ..code_generator_scope import CodeGeneratorScope


class Composite:
    BINARY_OP_HANDLERS = {
        BinaryOps.ADD: ScoreboardBuilder.add_op,
        BinaryOps.SUB: ScoreboardBuilder.sub_op,
        BinaryOps.MUL: ScoreboardBuilder.mul_op,
        BinaryOps.DIV: ScoreboardBuilder.div_op,
        BinaryOps.MOD: ScoreboardBuilder.mod_op,
        BinaryOps.MIN: ScoreboardBuilder.min_op,
        BinaryOps.MAX: ScoreboardBuilder.max_op,
    }
    VAR_LITERAL_OP_HANDLERS = {
        BinaryOps.ADD: ScoreboardBuilder.add_score,
        BinaryOps.SUB: ScoreboardBuilder.sub_score,
        BinaryOps.MUL: ScoreboardBuilder.mul_score,
        BinaryOps.DIV: ScoreboardBuilder.div_score,
        BinaryOps.MOD: ScoreboardBuilder.mod_score,
        BinaryOps.MIN: ScoreboardBuilder.min_score,
        BinaryOps.MAX: ScoreboardBuilder.max_score,
    }
    LITERAL_PAIR_OP_HANDLERS = {
        BinaryOps.ADD: lambda a, b: a + b,
        BinaryOps.SUB: lambda a, b: a - b,
        BinaryOps.MUL: lambda a, b: a * b,
        BinaryOps.DIV: lambda a, b: a / b,
        BinaryOps.MOD: lambda a, b: a % b,
        BinaryOps.MIN: lambda a, b: min(a, b),
        BinaryOps.MAX: lambda a, b: max(a, b),
        BinaryOps.BIT_AND: lambda a, b: a & b,
        BinaryOps.BIT_OR: lambda a, b: a | b,
        BinaryOps.BIT_XOR: lambda a, b: a ^ b,
        BinaryOps.SHL: lambda a, b: a << b,
        BinaryOps.SHR: lambda a, b: a >> b,
    }

    @staticmethod
    def var_compare_base_type(left: Reference[Variable | Constant | Literal], left_scope: CodeGeneratorScope,
                              left_objective: str, op: CompareOps, right: Reference[Variable | Constant | Literal],
                              right_scope: CodeGeneratorScope, right_objective: str, result: Variable | Constant,
                              result_scope: CodeGeneratorScope, result_objective: str) -> list[str] | None:

        commands = []

        op_value: str = op.value

        result_path = result_scope.get_symbol_path(result.get_name())

        # 自动将==替换为游戏所使用的=
        if op_value == "==":
            op_value = "="

        # 类型不相等直接判断为不等于
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
        if right.value == result:
            right, left = left, right
            left_scope, right_scope = right_scope, left_scope
            left_objective, right_objective = right_objective, left_objective
        if result.dtype in (DataType.INT, DataType.BOOLEAN):
            if left.value == result:  # left绝对为 Variable 或 Constant
                if right.value_type in (ValueType.VARIABLE, ValueType.CONSTANT):
                    return [
                        Composite.BINARY_OP_HANDLERS[op](left_scope.get_symbol_path(left.get_name()), left_objective,
                                                         right_scope.get_symbol_path(right.get_name()),
                                                         right_objective)]
                else:  # right为literal

                    return Composite.VAR_LITERAL_OP_HANDLERS[op](left_scope.get_symbol_path(left.get_name()),
                                                                 left_objective,
                                                                 right.value.value)
            elif left.value_type == ValueType.LITERAL and right.value_type == ValueType.LITERAL:
                # 此处理论上应该是重复的，因为正常情况下这一步会被常量折叠优化(谁那么闲不开优化啊)

                return [ScoreboardBuilder.set_score(result_path, result_objective,
                                                    Composite.LITERAL_PAIR_OP_HANDLERS[op](left.value.value,
                                                                                           left.value.value))]
            elif left.value_type == ValueType.LITERAL or right.value_type == ValueType.LITERAL:
                commands = []
                if right.value_type == ValueType.LITERAL:
                    right, left = left, right
                    left_scope, right_scope = right_scope, left_scope
                    left_objective, right_objective = right_objective, left_objective
                commands.append(ScoreboardBuilder.set_score(result_path, result_objective, left.value.value))
                commands.append(
                    Composite.BINARY_OP_HANDLERS[op](result_scope.get_symbol_path(result.get_name()), result_objective,
                                                     right_scope.get_symbol_path(right.get_name()), right_objective))
                return commands
            else:  # 两操作数均为变量或常量
                commands = [
                    ScoreboardBuilder.set_op(result_path, result_objective, left_scope.get_symbol_path(left.get_name()),
                                             left_objective),
                    Composite.BINARY_OP_HANDLERS[op](result_scope.get_symbol_path(result.get_name()), result_objective,
                                                     right_scope.get_symbol_path(right.get_name()), right_objective)]

                return commands
        elif result.dtype == DataType.STRING:
            return BasicCommands.call_macros_function(
                f"{namespace}:builtins/strcat",
                left_objective,
                {
                    "dest": (
                        left.value_type != ValueType.LITERAL,
                        left_scope.get_symbol_path(left.get_name()) if left.get_name() else str(left.value.value),
                        left_objective
                    ),
                    "src": (
                        right.value_type != ValueType.LITERAL,
                        right_scope.get_symbol_path(right.get_name()) if right.get_name() else str(right.value.value),
                        right_objective
                    ),
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

                }
            )

        return None
