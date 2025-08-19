# coding=utf-8
import typing
import uuid
import warnings

from transpiler.core.enums import DataType, ValueType, CompareOps, BinaryOps
from transpiler.core.symbols import Constant, Variable, Reference, Literal
from ._data import DataBuilder
from ._execute import Execute
from ._scoreboard import ScoreboardBuilder
from .base import BasicCommands
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
    def compare_base_type_equality(
            left: Reference[Variable | Constant | Literal],
            left_scope: CodeGeneratorScope,
            left_objective: str,
            op: typing.Literal[CompareOps.EQ, CompareOps.NE],
            right: Reference[Variable | Constant | Literal],
            right_scope: CodeGeneratorScope,
            right_objective: str,
            result: Variable | Constant,
            result_scope: CodeGeneratorScope,
            result_objective: str
    ):
        commands = []
        result_path = result_scope.get_symbol_path(result.get_name())

        # 类型不相等直接判断为不等于
        if left.get_data_type() != right.get_data_type():
            return [
                BasicCommands.Copy.copy_literal_base_type(
                    result,
                    result_scope,
                    result_objective,
                    Literal(
                        DataType.BOOLEAN,
                        False if op == CompareOps.EQ else True,
                    )
                )
            ]
        # 左项为字面量
        if left.value_type == ValueType.LITERAL:
            left_name = uuid.uuid4().hex
            left_path = left_scope.get_symbol_path(left_name)
            commands.append(
                BasicCommands.Copy.copy_literal_base_type(
                    Variable(
                        left_name,
                        left.get_data_type()
                    ),
                    left_scope,
                    left_objective,
                    left.value
                )
            )
        else:
            left_path = left_scope.get_symbol_path(left.get_name())

        # 右项为字面量
        if right.value_type == ValueType.LITERAL:
            right_name = uuid.uuid4().hex
            right_path = right_scope.get_symbol_path(right_name)
            commands.append(
                BasicCommands.Copy.copy_literal_base_type(
                    Variable(
                        right_name,
                        right.get_data_type()
                    ),
                    right_scope,
                    right_objective,
                    right.value
                )
            )
        else:
            right_path = right_scope.get_symbol_path(right.get_name())

        if left.get_data_type() in (DataType.BOOLEAN, DataType.INT):
            # 比较两数是否相等，如果相等向result_path存储结果
            commands.append(
                Execute.execute()
                .if_score_compare(
                    left_path,
                    left_objective,
                    "=",
                    right_path,
                    right_objective
                )
                .run(
                    ScoreboardBuilder.set_score(
                        result_path,
                        result_objective,
                        1 if op == CompareOps.EQ else 0
                    )
                )
            )
            commands.append(
                Execute.execute()
                .unless_score_compare(
                    left_path,
                    left_objective,
                    "=",
                    right_path,
                    right_objective
                )
                .run(
                    ScoreboardBuilder.set_score(
                        result_path,
                        result_objective,
                        0 if op == CompareOps.EQ else 1
                    )
                )
            )
        elif left.get_data_type() == DataType.STRING:
            temp_path = left_scope.get_symbol_path(uuid.uuid4().hex)
            temp_path_2 = uuid.uuid4().hex
            commands.extend(
                [
                    # 将左侧的值复制到临时变量
                    DataBuilder.modify_storage_set_from_storage(
                        left_objective,
                        temp_path,
                        left_objective,
                        left_path
                    ),
                    # 将右侧值复制到左侧，成功即为不同，不成功即为相同
                    Execute.execute()
                    .store_success_score(
                        temp_path_2,
                        result_objective
                    )
                    .run(
                        DataBuilder.modify_storage_set_from_storage(
                            left_objective,
                            temp_path,
                            right_objective,
                            right_path
                        )
                    ),
                    # x = 1-x的方式取反
                    ScoreboardBuilder.set_score(
                        result_path,
                        result_objective,
                        1
                    ),
                    ScoreboardBuilder.sub_op(
                        result_path,
                        result_objective,
                        temp_path_2,
                        result_objective
                    ),

                ]
            )
        return commands

    @staticmethod
    def compare_base_type_relation(
            left: Reference[Variable | Constant | Literal],
            left_scope: CodeGeneratorScope,
            left_objective: str,
            op: typing.Literal[CompareOps.LT, CompareOps.LE, CompareOps.GT, CompareOps.GE],
            right: Reference[Variable | Constant | Literal],
            right_scope: CodeGeneratorScope,
            right_objective: str,
            result: Variable | Constant,
            result_scope: CodeGeneratorScope,
            result_objective: str
    ):
        commands = []
        result_path = result_scope.get_symbol_path(result.get_name())

        # 类型不相等直接判断为不等于
        if left.get_data_type() != right.get_data_type():
            return [
                BasicCommands.Copy.copy_literal_base_type(
                    result,
                    result_scope,
                    result_objective,
                    Literal(
                        DataType.BOOLEAN,
                        False if op == CompareOps.EQ else True,
                    )
                )
            ]
        # 左项为字面量
        if left.value_type == ValueType.LITERAL:
            left_name = uuid.uuid4().hex
            left_path = left_scope.get_symbol_path(left_name)
            commands.append(
                BasicCommands.Copy.copy_literal_base_type(
                    Variable(
                        left_name,
                        left.get_data_type()
                    ),
                    left_scope,
                    left_objective,
                    left.value
                )
            )
        else:
            left_path = left_scope.get_symbol_path(left.get_name())

        # 右项为字面量
        if right.value_type == ValueType.LITERAL:
            right_name = uuid.uuid4().hex
            right_path = right_scope.get_symbol_path(right_name)
            commands.append(
                BasicCommands.Copy.copy_literal_base_type(
                    Variable(
                        right_name,
                        right.get_data_type()
                    ),
                    right_scope,
                    right_objective,
                    right.value
                )
            )
        else:
            right_path = right_scope.get_symbol_path(right.get_name())

        if left.get_data_type() not in (DataType.BOOLEAN, DataType.INT):
            warnings.warn(
                f"It is not possible to compare type {left.get_data_type().get_name()} and type {left.get_data_type().get_name()}")
            raise SystemExit

        commands.extend(
            [
                Execute.execute()
                .if_score_compare(
                    left_path,
                    left_objective,
                    str(op.value),
                    right_path,
                    right_objective
                )
                .run(
                    ScoreboardBuilder.set_score(
                        result_path,
                        result_objective,
                        1
                    )
                ),
                Execute.execute()
                .unless_score_compare(
                    left_path,
                    left_objective,
                    str(op.value),
                    right_path,
                    right_objective
                )
                .run(
                    ScoreboardBuilder.set_score(
                        result_path,
                        result_objective,
                        0
                    )
                ),
            ]
        )

        return commands

    @staticmethod
    def compare_base_type(
            left: Reference[Variable | Constant | Literal],
            left_scope: CodeGeneratorScope,
            left_objective: str,
            op: CompareOps,
            right: Reference[Variable | Constant | Literal],
            right_scope: CodeGeneratorScope,
            right_objective: str,
            result: Variable | Constant,
            result_scope: CodeGeneratorScope,
            result_objective: str
    ) -> list[str] | None:

        commands = []

        if op in (CompareOps.EQ, CompareOps.NE):
            return Composite.compare_base_type_equality(
                left,
                left_scope,
                left_objective,
                op,
                right,
                right_scope,
                right_objective,
                result,
                result_scope,
                result_objective
            )
        else:
            return Composite.compare_base_type_relation(
                left,
                left_scope,
                left_objective,
                op,
                right,
                right_scope,
                right_objective,
                result,
                result_scope,
                result_objective
            )

    @staticmethod
    def op_base_type_literal_literal(
            result: Variable | Constant,
            result_scope: CodeGeneratorScope,
            result_objective: str,
            op: BinaryOps,
            left: Literal,
            right: Literal
    ):
        """
        处理当两边均为字面量的情况

        :param result: 结果变量
        :param result_scope: 结果变量的作用域
        :param result_objective: 结果变量的记分板
        :param op: 运算符
        :param left: 左项
        :param right: 右项
        :return: 生成的指令
        """
        result_path = result_scope.get_symbol_path(result.get_name())
        if left in (DataType.BOOLEAN, DataType.INT):
            return [
                ScoreboardBuilder.set_score(
                    result_path,
                    result_objective,
                    Composite.LITERAL_PAIR_OP_HANDLERS[op](
                        left.value,
                        right.value
                    )
                )
            ]
        elif left == DataType.STRING:
            if op == BinaryOps.ADD:
                return [
                    DataBuilder.modify_storage_set_value(
                        result_objective,
                        result_path,
                        f"{str(left.value)}{str(right.value)}"
                    )
                ]
            return None

        return None

    @staticmethod
    def op_base_type_variable_literal(
            result: Variable | Constant,
            result_scope: CodeGeneratorScope,
            result_objective: str,
            op: BinaryOps,
            left: Variable | Constant,
            left_scope: CodeGeneratorScope,
            left_objective: str,
            right: Literal,
            namespace: str = ""
    ):
        """
        处理当左项为变量/常量，右项为字面量的情况

        :param result: 结果变量
        :param result_scope: 结果变量的作用域
        :param result_objective: 结果变量的记分板
        :param op: 运算符
        :param left: 左项变量
        :param left_scope: 左项的变量的作用域
        :param left_objective: 左项的变量的记分板
        :param right: 右项
        :param namespace: 命名空间(仅结果为字符串时有效)
        :return: 生成的指令
        """
        result_path = result_scope.get_symbol_path(result.get_name())
        # 当左项和右项的类型均为数时
        if left.dtype in (DataType.BOOLEAN, DataType.INT) and right.dtype in (DataType.BOOLEAN, DataType.INT):
            commands = []
            # 如果左项和结果变量不同将左项复制到结果中
            if left.get_name() != result.get_name():
                commands.append(
                    BasicCommands.Copy.copy_variable_base_type(
                        result,
                        result_scope,
                        result_objective,
                        left,
                        left_scope,
                        left_objective
                    )
                )
            commands.extend(
                Composite.VAR_LITERAL_OP_HANDLERS[op](
                    result_path,
                    result_objective,
                    right.value
                )
            )

            return commands
        elif result.dtype == DataType.STRING:
            return BasicCommands.call_macros_function(
                f"{namespace}:builtins/strcat",
                left_objective,
                {
                    "dest": (
                        True,
                        left_scope.get_symbol_path(left.get_name()),
                        left_objective
                    ),
                    "src": (
                        False,
                        str(right.value),
                        None
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

    @staticmethod
    def op_base_type_variable_variable(
            result: Variable | Constant,
            result_scope: CodeGeneratorScope,
            result_objective: str,
            op: BinaryOps,
            left: Variable | Constant,
            left_scope: CodeGeneratorScope,
            left_objective: str,
            right: Variable | Constant,
            right_scope: CodeGeneratorScope,
            right_objective: str,
            namespace: str = ''
    ):
        """
        处理当两边均为变量/常量的情况

        :param result: 结果变量
        :param result_scope: 结果变量的作用域
        :param result_objective: 结果变量的记分板
        :param op: 运算符
        :param left: 左项变量
        :param left_scope: 左项的变量的作用域
        :param left_objective: 左项的变量的记分板
        :param right: 右项变量
        :param right_scope: 右项的变量的作用域
        :param right_objective: 右项的变量的记分板
        :param namespace: 命名空间(仅结果为字符串时有效)
        :return: 生成的指令
        """
        result_path = result_scope.get_symbol_path(result.get_name())
        # 如果右侧与结果相等左右进行交换
        if right == result:
            right, left = left, right
            left_scope, right_scope = right_scope, left_scope
            left_objective, right_objective = right_objective, left_objective

        if left.dtype in (DataType.BOOLEAN, DataType.INT):
            commands = []
            # 如果左项和结果变量不同将左项复制到结果中
            if left.get_name() != result.get_name():
                commands.append(
                    BasicCommands.Copy.copy_variable_base_type(
                        result,
                        result_scope,
                        result_objective,
                        left,
                        left_scope,
                        left_objective
                    )
                )
            commands.append(
                Composite.BINARY_OP_HANDLERS[op](
                    result_path,
                    result_objective,
                    right_scope.get_symbol_path(right.get_name()),
                    result_objective
                )
            )
        elif result.dtype == DataType.STRING:
            # 对左右两项进行拼接然后存储到结果中
            return BasicCommands.call_macros_function(
                f"{namespace}:builtins/strcat",
                left_objective,
                {
                    "dest": (
                        True,
                        left_scope.get_symbol_path(left.get_name()),
                        left_objective
                    ),
                    "src": (
                        True,
                        right_scope.get_symbol_path(right.get_name()),
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

    @staticmethod
    def op_base_type(
            result: Variable | Constant,
            result_scope: CodeGeneratorScope,
            result_objective: str,
            op: BinaryOps,
            left: Reference[Variable | Constant | Literal],
            left_scope: CodeGeneratorScope,
            left_objective: str,
            right: Reference[Variable | Constant | Literal],
            right_scope: CodeGeneratorScope,
            right_objective: str,
            namespace: str = ""
    ) -> list[str] | None:

        if left.value_type == ValueType.LITERAL and right.value_type == ValueType.LITERAL:
            # 左右项均为字面量
            return Composite.op_base_type_literal_literal(
                result,
                result_scope,
                result_objective,
                op,
                left.value,
                right.value
            )
        elif left.value_type != ValueType.LITERAL and right.value_type != ValueType.LITERAL:
            # 左右项均为变量/常量
            return Composite.op_base_type_variable_variable(
                result,
                result_scope,
                result_objective,
                op,
                left.value,
                left_scope,
                left_objective,
                right.value,
                right_scope,
                right_objective,
                namespace
            )
        else:  # 左右项中有一个是变量/常量
            # 如果右项为变量/常量而左项为字面量的话将左右进行交换
            if right.value_type != ValueType.LITERAL:
                right, left = left, right
                left_scope, right_scope = right_scope, left_scope
                left_objective, right_objective = right_objective, left_objective

            return Composite.op_base_type_variable_literal(
                result,
                result_scope,
                result_objective,
                op,
                left.value,
                left_scope,
                left_objective,
                right.value,
                namespace
            )
