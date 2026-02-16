# coding=utf-8
from ._scoreboard import ScoreboardBuilder
from .tools import DataPath, LiteralPoolTools


class UnaryOp:

    @staticmethod
    def not_(result: DataPath, value: DataPath):
        # result = 1-x
        return [
            ScoreboardBuilder.set_score(*result, 1),
            ScoreboardBuilder.sub_op(
                *result,
                *value
            )
        ]

    @staticmethod
    def not_self(value: DataPath):
        # x = (x-1)*(-1)
        return [
            ScoreboardBuilder.sub_op(
                *value,
                *LiteralPoolTools.get_literal_path(1, value.target)
            ),
            ScoreboardBuilder.mul_op(
                *value,
                *LiteralPoolTools.get_literal_path(-1, value.target)
            ),
        ]
