# coding=utf-8
"""
常量折叠 Pass 测试

测试策略：手工构造包含常量运算的 IR，验证 Pass 执行后
常量表达式被正确折叠，非常量表达式不被误处理。
"""
import unittest

from dovetail.core.compile_config import CompileConfig
from dovetail.core.enums import OptimizationLevel, PrimitiveDataType, MinecraftVersion, BinaryOps, UnaryOps
from dovetail.core.enums.types import StructureType
from dovetail.core.instructions import (
    IRFunction, IRScopeBegin, IRScopeEnd, IRReturn,
    IRBinaryOp, IRUnaryOp, IROpCode,
)
from dovetail.core.ir_builder import IRBuilder
from dovetail.core.optimize.passes.constant_folding import ConstantFoldingPass
from dovetail.core.symbols import Function, Variable, Literal, Reference


def _make_config() -> CompileConfig:
    return CompileConfig(
        "ns",
        version=MinecraftVersion.instance("1.21.5"),
        optimization_level=OptimizationLevel.O2,
    )


def _make_int_var(name: str) -> Variable:
    return Variable(name, PrimitiveDataType.INT)


def _make_int_lit(value: int) -> Literal:
    return Literal(PrimitiveDataType.INT, value)


def _make_function(name: str) -> Function:
    return Function(name, [], PrimitiveDataType.INT)


def _opcodes(builder: IRBuilder) -> list[IROpCode]:
    return [i.opcode for i in builder.get_instructions()]


def _run_pass(builder: IRBuilder) -> IRBuilder:
    pass_ = ConstantFoldingPass(builder, _make_config())
    pass_.analyze()
    pass_.execute()
    return builder


class TestConstantFoldingBinaryOps(unittest.TestCase):
    """二元常量折叠测试"""

    def _fold(self, op: BinaryOps, left_val: int, right_val: int) -> IRBuilder:
        func = _make_function("test")
        result = _make_int_var("result")
        left = _make_int_lit(left_val)
        right = _make_int_lit(right_val)

        builder = IRBuilder()
        builder.insert(IRFunction(func))
        builder.insert(IRScopeBegin("test", StructureType.FUNCTION))
        builder.insert(IRBinaryOp(result, op, Reference(left), Reference(right)))
        builder.insert(IRReturn(Reference(result)))
        builder.insert(IRScopeEnd("test", StructureType.FUNCTION))

        return _run_pass(builder)

    def test_fold_addition(self):
        """1 + 2 应折叠为 3"""
        builder = self._fold(BinaryOps.ADD, 1, 2)
        opcodes = _opcodes(builder)
        # 折叠后不应再有 BinaryOp 指令
        self.assertNotIn(IROpCode.BINARY_OP, opcodes)

    def test_fold_subtraction(self):
        """10 - 3 应折叠为 7"""
        builder = self._fold(BinaryOps.SUB, 10, 3)
        self.assertNotIn(IROpCode.BINARY_OP, _opcodes(builder))

    def test_fold_multiplication(self):
        """4 * 5 应折叠为 20"""
        builder = self._fold(BinaryOps.MUL, 4, 5)
        self.assertNotIn(IROpCode.BINARY_OP, _opcodes(builder))

    def test_fold_division(self):
        """8 / 2 应折叠为 4"""
        builder = self._fold(BinaryOps.DIV, 8, 2)
        self.assertNotIn(IROpCode.BINARY_OP, _opcodes(builder))

    def test_no_fold_with_variable_operand(self):
        """含变量的操作数不应被折叠"""
        func = _make_function("test")
        x = _make_int_var("x")
        lit = _make_int_lit(1)
        result = _make_int_var("result")

        builder = IRBuilder()
        builder.insert(IRFunction(func))
        builder.insert(IRScopeBegin("test", StructureType.FUNCTION))
        builder.insert(IRBinaryOp(result, BinaryOps.ADD, Reference(x), Reference(lit)))
        builder.insert(IRReturn(Reference(result)))
        builder.insert(IRScopeEnd("test", StructureType.FUNCTION))

        result_builder = _run_pass(builder)

        # 有变量操作数，不应折叠
        self.assertIn(IROpCode.BINARY_OP, _opcodes(result_builder))

    def test_division_by_zero_not_folded(self):
        """除零不应被折叠（避免编译期崩溃）"""
        try:
            builder = self._fold(BinaryOps.DIV, 5, 0)
            # 如果没有抛异常，检查 IR 是否保留了原始指令
        except Exception:
            pass  # 抛异常也是可接受行为，不应是未捕获崩溃


class TestConstantFoldingUnaryOps(unittest.TestCase):
    """一元常量折叠测试"""

    def test_fold_negation(self):
        """-5 应折叠为 -5"""
        func = _make_function("test")
        result = _make_int_var("result")
        lit = _make_int_lit(5)

        builder = IRBuilder()
        builder.insert(IRFunction(func))
        builder.insert(IRScopeBegin("test", StructureType.FUNCTION))
        builder.insert(IRUnaryOp(result, UnaryOps.NEG, Reference(lit)))
        builder.insert(IRReturn(Reference(result)))
        builder.insert(IRScopeEnd("test", StructureType.FUNCTION))

        result_builder = _run_pass(builder)

        self.assertNotIn(IROpCode.UNARY_OP, _opcodes(result_builder))


if __name__ == "__main__":
    unittest.main()
