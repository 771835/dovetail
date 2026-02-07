# coding=utf-8
import uuid

from transpiler.core.enums import CompareOps
from transpiler.core.optimize.passes import ConstantFoldingPass
from ._execute import Execute
from ._scoreboard import ScoreboardBuilder
from .copy import Copy
from .tools import DataPath, StorageLocation, LiteralPoolTools
from .unary_op import UnaryOp


class Compare:
    @staticmethod
    def _compare_literals(op: CompareOps, a: int | bool, b: int | bool) -> bool:
        return ConstantFoldingPass.COMPARE_OP_HANDLERS[op](a, b)

    @staticmethod
    def compare_literals(result: DataPath, op: CompareOps, a: int | bool, b: int | bool) -> str | None:
        return Copy.copy_literals(result, Compare._compare_literals(op, a, b))

    @staticmethod
    def compare_equality_storage(
            result: DataPath,
            op: CompareOps,
            a: DataPath,
            b: DataPath,
    ):
        temp = DataPath(uuid.uuid4().hex, result.target, StorageLocation.STORAGE)
        commands = [
            # 将左侧的值复制到临时变量
            Copy.copy(temp, a),
            # 将右侧值复制到左侧，成功即为不同，不成功即为相同
            Execute.execute().store_success_score(*result).run(Copy.copy(temp, b))
        ]

        if op == CompareOps.EQ:
            commands.extend(UnaryOp.not_(result, result))
        return commands

    @staticmethod
    def compare_equality_score(
            result: DataPath,
            op: CompareOps,
            a: DataPath,
            b: DataPath,
    ):
        return [
            ScoreboardBuilder.set_score(*result, int(op == CompareOps.NE)),
            Execute.execute()
            .if_score_compare(*a, "=", *b)
            .run(ScoreboardBuilder.set_score(*result, int(op == CompareOps.EQ))),
        ]

    @staticmethod
    def compare_equality_variables(
            result: DataPath,
            op: CompareOps,
            a: DataPath,
            b: DataPath,
    ):

        if a.location != b.location:  # 如果两者不存储于同一存储空间则在存储比较
            commands: list[str] = []
            # 将待比较的两项复制到存储中
            if a.location == StorageLocation.SCORE:
                a = DataPath(a.path, a.target, StorageLocation.STORAGE)
                commands.append(Copy.copy_score_to_storage(a, a))
            else:
                b = DataPath(b.path, b.target, StorageLocation.STORAGE)
                commands.append(Copy.copy_score_to_storage(b, b))
            # 比较是否相等
            commands.extend(Compare.compare_equality_storage(result, op, a, b))
            return commands
        else:
            if a.location == StorageLocation.SCORE:
                return Compare.compare_equality_score(result, op, a, b)
            else:
                return Compare.compare_equality_storage(result, op, a, b)

    @staticmethod
    def compare_equality(
            result: DataPath,
            op: CompareOps,
            a: DataPath | int | bool | str,
            b: DataPath | int | bool | str,
    ) -> list[str]:
        if isinstance(a, DataPath):
            if isinstance(b, DataPath):
                return Compare.compare_equality_variables(result, op, a, b)
            else:
                return Compare.compare_equality_variables(result, op, a, LiteralPoolTools.get_literal_path(b, a.target))
        else:
            if isinstance(b, DataPath):
                return Compare.compare_equality_variables(result, op, LiteralPoolTools.get_literal_path(a, b.target), b)
            else:
                # 两方均为常数时直接计算
                return [Compare.compare_literals(result, op, a, b)]

    @staticmethod
    def compare_relation_score(
            result: DataPath,
            op: CompareOps,
            a: DataPath,
            b: DataPath,
    ):
        return [
            ScoreboardBuilder.set_score(*result, 0),
            Execute.execute()
            .if_score_compare(*a, str(op.value), *b)
            .run(ScoreboardBuilder.set_score(*result, 1))
        ]

    @staticmethod
    def compare_relation(
            result: DataPath,
            op: CompareOps,
            a: DataPath | int | bool,
            b: DataPath | int | bool,
    ) -> list[str]:
        # 常量提前计算
        if not isinstance(a, DataPath) and not isinstance(b, DataPath):
            return [Compare.compare_literals(result, op, a, b)]
        else:
            commands: list[str] = []
            if not isinstance(a, DataPath):
                a = LiteralPoolTools.get_literal_path(a, b.target)
            elif not isinstance(b, DataPath):
                b = LiteralPoolTools.get_literal_path(b, a.target)
            commands.extend(Compare.compare_relation_score(result, op, a, b))
            return commands

    @staticmethod
    def compare(
            result: DataPath,
            op: CompareOps,
            a: DataPath | int | bool | str,
            b: DataPath | int | bool | str,
    ) -> list[str]:
        if op in (CompareOps.EQ, CompareOps.NE):
            return Compare.compare_equality(result, op, a, b)
        else:
            return Compare.compare_relation(result, op, a, b)
