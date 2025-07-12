"""# coding=utf-8
import uuid

from mcfdsl.core.backend.code_generator.c_je_1204.command_builder._data import Data
from mcfdsl.core.backend.code_generator.c_je_1204.command_builder._execute import Execute, ScoreOperation
from mcfdsl.core.backend.code_generator.c_je_1204.command_builder._scoreboard import Scoreboard
from mcfdsl.core.backend.code_generator.c_je_1204.command_builder.base import BasicCommands
from mcfdsl.core.language_enums import DataType, ValueType, SymbolType
from mcfdsl.core.result import Result


class Composite:
    @staticmethod
    def var_init(var: ISymbol, value: int | str = None):
        if var.data_type == DataType.INT:
            if value is not None:
                value = 0
            if var.data_type == DataType.BOOLEAN:
                value = 1 if value else 0
            return Scoreboard.set_score(
                var.get_unique_name(), var.objective, int(value))
        elif var.data_type == DataType.STRING:
            if value is not None:
                value = ''
            return Data.modify_storage_set_value(
                var.get_unique_name(), var.get_storage_path(), str(value))
        else:
            return None

    @staticmethod
    def var_assignment(var: ISymbol, expr: ISymbol | Result) -> str | None:
        if isinstance(expr, Result):
            var2 = expr.to_symbol(objective=var.objective)
            if var2 is None:
                return None
        else:
            assert isinstance(expr, ISymbol)
            var2: ISymbol = expr

        if var2.value_type == ValueType.LITERAL:
            return BasicCommands.Copy.copy_literal(var, var2.value)
        elif var2.value_type == ValueType.VARIABLE:
            return BasicCommands.Copy.copy_variable(var2, var)
        return None

    @staticmethod
    def var_compare(
            left: ISymbol | Result,
            op: str,
            right: ISymbol | Result,
            result_var: ISymbol,
            objective: str = None
    ):
        if isinstance(left, Result) and isinstance(
                right, ISymbol):  # 如果left是Result且right是ISymbol
            left = left.to_symbol(objective=right.objective)
        # 如果right是Result且left是ISymbol
        elif isinstance(right, Result) and isinstance(left, ISymbol):
            right = right.to_symbol(objective=left.objective)
        elif isinstance(left, Result) and isinstance(right, Result):
            if objective:
                left = left.to_symbol(objective=objective)
                right = right.to_symbol(objective=objective)
            else:
                return None
        # 自动将==替换为游戏支持的=
        if op == "==":
            op = "="

        if left.data_type in (
                DataType.INT,
                DataType.BOOLEAN) and right.data_type in (
                DataType.INT,
                DataType.BOOLEAN):
            if left.value_type == ValueType.VARIABLE and right.value_type == ValueType.VARIABLE:  # 左右都是变量引用
                return [
                    Composite._variable_compare(
                        left, op, right, result_var)]
            elif left.value_type == ValueType.LITERAL and right.value_type == ValueType.LITERAL:  # 左右都是字面量
                assert isinstance(left.value, (int, bool))
                assert isinstance(right.value, (int, bool))
                return [
                    Scoreboard.set_score(
                        result_var.get_unique_name(),
                        result_var.objective,
                        1 if Composite._literal_compare(
                            left.value,
                            op,
                            right.value) else 0)]
            else:  # 左右有任意一边是变量引用
                cmd = []
                temp = '#' + uuid.uuid4().hex
                if left.value_type == ValueType.LITERAL:
                    assert isinstance(left.value, (int, bool))
                    cmd.append(
                        Scoreboard.set_score(temp,
                                             left.objective, left.value
                                             )
                    )
                    left = Symbol(
                        temp,
                        SymbolType.VARIABLE,
                        None,
                        left.data_type,
                        left.objective,
                        left.value,
                        ValueType.VARIABLE)
                elif right.value_type == ValueType.LITERAL:
                    assert isinstance(right.value, (int, bool))
                    cmd.append(
                        Scoreboard.set_score(temp,
                                             right.objective, right.value)
                    )
                    right = Symbol(
                        temp,
                        SymbolType.VARIABLE,
                        None,
                        right.data_type,
                        right.objective,
                        right.value,
                        ValueType.VARIABLE)
                else:
                    return None
                cmd.append(
                    Composite._variable_compare(
                        left, op, right, result_var))
                cmd.append(Scoreboard.reset_score(temp, result_var.objective))
                return cmd
        elif left.data_type == DataType.STRING and right.data_type == DataType.STRING:
            cmd = []
            # TODO: 依然待实现
            return cmd
        elif isinstance(left.data_type, DataType) and isinstance(right.data_type, DataType):
            return [
                Scoreboard.set_score(
                    result_var.get_unique_name(),
                    result_var.objective,
                    0)]
        else:  # 其他
            return None

    @staticmethod
    def _variable_compare(
            left: ISymbol,
            op: str,
            right: ISymbol,
            result_var: ISymbol):
        ops = ["=", "<", "<=", ">", ">="]
        if op in ops:
            op: ScoreOperation
            return Execute.execute().if_score_compare(
                left.get_unique_name(),
                left.objective,
                op,
                right.get_unique_name(),
                right.objective).run(
                Scoreboard.set_score(
                    result_var.get_unique_name(),
                    result_var.objective,
                    1))
        elif op == "!=":
            return Execute.execute().unless_score_compare(
                left.get_unique_name(),
                left.objective,
                "=",
                right.get_unique_name(),
                right.objective).run(
                Scoreboard.set_score(
                    result_var.get_unique_name(),
                    result_var.objective,
                    1))
        else:
            return None

    @staticmethod
    def _literal_compare(left: int | bool, op: str, right: int | bool):
        result = False
        if op == '<':
            result = left < right
        elif op == '>':
            result = left > right
        elif op == '<=':
            result = left <= right
        elif op == '>=':
            result = left >= right
        elif op == '=' or op == '==':
            result = left == right
        elif op == '!=':
            result = left != right
        return True if result else False
"""
