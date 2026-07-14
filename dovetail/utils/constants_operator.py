# coding=utf-8
"""
运算符处理表
"""
from typing import Callable

from dovetail.core.enums import BinaryOps, CompareOps, UnaryOps
from dovetail.utils.logger import get_logger

logger = get_logger(__name__)


# ── 安全运算辅助函数 ──────────────────────────────────────────

def _safe_div(a: int | float, b: int | float) -> int | float:
    """除法，除数为 0 时修正为 1"""
    if b == 0:
        logger.error("除数为 0（已自动修正为 1）")
        return a
    return a // b if isinstance(a, int) and isinstance(b, int) else a / b


def _safe_mod(a: int, b: int) -> int:
    """取模，除数为 0 时修正为 1"""
    if b == 0:
        logger.error("除数为 0（已自动修正为 1）")
        return a
    return a % b


def _safe_shl(a: int, b: int) -> int:
    """左移，负位移返回 0"""
    return a << b if b >= 0 else 0


def _safe_shr(a: int, b: int) -> int:
    """右移，负位移返回 0"""
    return a >> b if b >= 0 else 0


BINARY_OP_HANDLERS: dict[BinaryOps, Callable] = {
    BinaryOps.ADD: lambda a, b: a + b,
    BinaryOps.SUB: lambda a, b: a - b,
    BinaryOps.MUL: lambda a, b: a * b,
    BinaryOps.DIV: _safe_div,
    BinaryOps.MOD: _safe_mod,
    BinaryOps.MIN: lambda a, b: min(a, b),
    BinaryOps.MAX: lambda a, b: max(a, b),
    BinaryOps.BIT_AND: lambda a, b: a & b,
    BinaryOps.BIT_OR: lambda a, b: a | b,
    BinaryOps.BIT_XOR: lambda a, b: a ^ b,
    BinaryOps.SHL: _safe_shl,
    BinaryOps.SHR: _safe_shr,
}

COMPARE_OP_HANDLERS: dict[CompareOps, Callable] = {
    CompareOps.EQ: lambda a, b: a == b,
    CompareOps.NE: lambda a, b: a != b,
    CompareOps.GE: lambda a, b: a >= b,
    CompareOps.GT: lambda a, b: a > b,
    CompareOps.LE: lambda a, b: a <= b,
    CompareOps.LT: lambda a, b: a < b,
}

UNARY_OP_HANDLERS: dict[UnaryOps, Callable] = {
    UnaryOps.NEG: lambda a: -a,
    UnaryOps.NOT: lambda a: not a,
    UnaryOps.BIT_NOT: lambda a: ~a,
}
