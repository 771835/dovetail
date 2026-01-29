# coding=utf-8
from transpiler.core.enums import BinaryOps
from transpiler.core.optimize.passes import ConstantFoldingPass
from transpiler.plugins.je1214.backend.commands import ScoreboardBuilder
from transpiler.plugins.je1214.backend.commands.copy import Copy
from transpiler.plugins.je1214.backend.commands.tools import DataPath, LiteralPoolTools


class BinaryOp:
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

    @staticmethod
    def _op_both_literal(op: BinaryOps, a: int | str, b: int | str):
        return ConstantFoldingPass.BINARY_OP_HANDLERS[op](a, b)

    @staticmethod
    def _select_command(op: BinaryOps, target: DataPath, source: DataPath):
        return BinaryOp.BINARY_OP_HANDLERS[op](*target, *source)

    @staticmethod
    def op_both_variable(result: DataPath, op: BinaryOps, a: DataPath, b: DataPath):
        commands: list[str] = []
        if result == b:
            a, b = b, a
        if result != a:
            commands.append(Copy.copy(result, a))
        commands.append(BinaryOp._select_command(op, result, b))
        return commands

    @staticmethod
    def op_all(result: DataPath, op: BinaryOps, a: DataPath | int | bool, b: DataPath | int | bool):
        if not isinstance(a, DataPath) and not isinstance(b, DataPath):
            return [Copy.copy_literals(result, BinaryOp._op_both_literal(op, a, b))]
        else:
            if not isinstance(a, DataPath):
                a = LiteralPoolTools.get_literal_path(a, result.target)
            if not isinstance(b, DataPath):
                b = LiteralPoolTools.get_literal_path(b, result.target)
            return BinaryOp.op_both_variable(result, op, a, b)
