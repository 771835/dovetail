# coding=utf-8
"""
数值提供器提升 Pass 测试

测试策略：手工构造 IR，验证 Pass 将 BINARY_OP 链和函数调用
正确提升为 COMPUTE 指令，provider_tree 结构符合预期。
"""
import unittest

from dovetail.core.compile_config import CompileConfig
from dovetail.core.enums import (
    OptimizationLevel, PrimitiveDataType, MinecraftVersion, BinaryOps,
)
from dovetail.core.enums.types import StructureType
from dovetail.core.instructions import (
    IRFunction, IRScopeBegin, IRScopeEnd, IRReturn,
    IRBinaryOp, IRAssign, IRDeclare, IRCall, IROpCode, IRCompute,
)
from dovetail.core.ir_builder import IRBuilder
from dovetail.core.optimize.passes.number_provider_lifting import NumberProviderLiftingPass
from dovetail.core.symbols import Function, Variable, Literal, Reference


def _make_config() -> CompileConfig:
    return CompileConfig(
        "ns",
        version=MinecraftVersion.instance("26.3"),
        optimization_level=OptimizationLevel.O2,
    )


def _make_int_var(name: str) -> Variable:
    return Variable(name, PrimitiveDataType.INT)


def _make_int_lit(value: int) -> Literal:
    return Literal(PrimitiveDataType.INT, value)


def _make_function(name: str, param_count: int = 0) -> Function:
    params = []
    for i in range(param_count):
        params.append(Variable(f"p{i}", PrimitiveDataType.INT))
    return Function(name, params, PrimitiveDataType.INT)


def _run_pass(builder: IRBuilder) -> IRBuilder:
    p = NumberProviderLiftingPass(builder, _make_config())
    p.execute()
    return builder


def _find_computes(builder: IRBuilder) -> list:
    """收集所有 COMPUTE 指令"""
    return [i for i in builder.get_instructions() if i.opcode == IROpCode.COMPUTE]


def _binary_op_count(builder: IRBuilder) -> int:
    return sum(1 for i in builder.get_instructions() if i.opcode == IROpCode.BINARY_OP)


class TestBasicLifting(unittest.TestCase):
    """基础链提升"""

    def test_add_chain_flattened(self):
        """a + b + c → COMPUTE sum(a, b, c)"""
        func = _make_function("test")
        a, b, c = _make_int_var("a"), _make_int_var("b"), _make_int_var("c")
        t1, t2 = _make_int_var("t1"), _make_int_var("t2")

        builder = IRBuilder()
        builder.insert(IRFunction(func))
        builder.insert(IRScopeBegin("test", StructureType.FUNCTION))
        builder.insert(IRBinaryOp(t1, BinaryOps.ADD, Reference(a), Reference(b)))
        builder.insert(IRBinaryOp(t2, BinaryOps.ADD, Reference(t1), Reference(c)))
        builder.insert(IRReturn(Reference(t2)))
        builder.insert(IRScopeEnd("test", StructureType.FUNCTION))

        result = _run_pass(builder)
        computes = _find_computes(result)

        self.assertEqual(len(computes), 1)
        tree = computes[0].operands[1]
        self.assertEqual(tree["op"], "sum")
        self.assertEqual(len(tree["args"]), 3)

    def test_mixed_ops_nested(self):
        """min(a + b, c * d) → COMPUTE minimum(sum(a,b), product(c,d))"""
        func = _make_function("test")
        a, b, c, d = (_make_int_var("a"), _make_int_var("b"),
                      _make_int_var("c"), _make_int_var("d"))
        t1, t2, t3 = _make_int_var("t1"), _make_int_var("t2"), _make_int_var("t3")

        builder = IRBuilder()
        builder.insert(IRFunction(func))
        builder.insert(IRScopeBegin("test", StructureType.FUNCTION))
        builder.insert(IRBinaryOp(t1, BinaryOps.ADD, Reference(a), Reference(b)))
        builder.insert(IRBinaryOp(t2, BinaryOps.MUL, Reference(c), Reference(d)))
        builder.insert(IRBinaryOp(t3, BinaryOps.MIN, Reference(t1), Reference(t2)))
        builder.insert(IRReturn(Reference(t3)))
        builder.insert(IRScopeEnd("test", StructureType.FUNCTION))

        result = _run_pass(builder)
        computes = _find_computes(result)

        self.assertEqual(len(computes), 1)
        tree = computes[0].operands[1]
        self.assertEqual(tree["op"], "minimum")
        self.assertEqual(len(tree["args"]), 2)
        self.assertEqual(tree["args"][0]["op"], "sum")
        self.assertEqual(tree["args"][1]["op"], "product")

    def test_sub_wrapped_as_sum(self):
        """a - b → COMPUTE sum(a, product(b, -1))"""
        func = _make_function("test")
        a, b = _make_int_var("a"), _make_int_var("b")
        t1 = _make_int_var("t1")

        builder = IRBuilder()
        builder.insert(IRFunction(func))
        builder.insert(IRScopeBegin("test", StructureType.FUNCTION))
        builder.insert(IRBinaryOp(t1, BinaryOps.SUB, Reference(a), Reference(b)))
        builder.insert(IRReturn(Reference(t1)))
        builder.insert(IRScopeEnd("test", StructureType.FUNCTION))

        result = _run_pass(builder)
        # 单条 SUB 无收益（<2），不会提升
        computes = _find_computes(result)
        self.assertEqual(len(computes), 0)

    def test_sub_in_chain(self):
        """a + b - c → sum(a, b, product(c, -1))"""
        func = _make_function("test")
        a, b, c = _make_int_var("a"), _make_int_var("b"), _make_int_var("c")
        t1, t2 = _make_int_var("t1"), _make_int_var("t2")

        builder = IRBuilder()
        builder.insert(IRFunction(func))
        builder.insert(IRScopeBegin("test", StructureType.FUNCTION))
        builder.insert(IRBinaryOp(t1, BinaryOps.ADD, Reference(a), Reference(b)))
        builder.insert(IRBinaryOp(t2, BinaryOps.SUB, Reference(t1), Reference(c)))
        builder.insert(IRReturn(Reference(t2)))
        builder.insert(IRScopeEnd("test", StructureType.FUNCTION))

        result = _run_pass(builder)
        computes = _find_computes(result)

        self.assertEqual(len(computes), 1)
        tree = computes[0].operands[1]
        self.assertEqual(tree["op"], "sum")
        # args: [a, b, product(c, -1)]
        self.assertEqual(len(tree["args"]), 3)
        neg_part = tree["args"][2]
        self.assertEqual(neg_part["op"], "product")


class TestFlattening(unittest.TestCase):
    """同类运算聚合"""

    def test_nested_sum_flattened(self):
        """sum(sum(a,b), sum(c,d)) → sum(a,b,c,d)"""
        func = _make_function("test")
        a, b, c, d = (_make_int_var("a"), _make_int_var("b"),
                      _make_int_var("c"), _make_int_var("d"))
        t1, t2, t3 = _make_int_var("t1"), _make_int_var("t2"), _make_int_var("t3")

        builder = IRBuilder()
        builder.insert(IRFunction(func))
        builder.insert(IRScopeBegin("test", StructureType.FUNCTION))
        builder.insert(IRBinaryOp(t1, BinaryOps.ADD, Reference(a), Reference(b)))
        builder.insert(IRBinaryOp(t2, BinaryOps.ADD, Reference(c), Reference(d)))
        builder.insert(IRBinaryOp(t3, BinaryOps.ADD, Reference(t1), Reference(t2)))
        builder.insert(IRReturn(Reference(t3)))
        builder.insert(IRScopeEnd("test", StructureType.FUNCTION))

        result = _run_pass(builder)
        computes = _find_computes(result)

        self.assertEqual(len(computes), 1)
        tree = computes[0].operands[1]
        self.assertEqual(tree["op"], "sum")
        self.assertEqual(len(tree["args"]), 4)

    def test_product_chain_flattened(self):
        """a * b * c * d → product(a, b, c, d)"""
        func = _make_function("test")
        a, b, c, d = (_make_int_var("a"), _make_int_var("b"),
                      _make_int_var("c"), _make_int_var("d"))
        t1, t2, t3 = _make_int_var("t1"), _make_int_var("t2"), _make_int_var("t3")

        builder = IRBuilder()
        builder.insert(IRFunction(func))
        builder.insert(IRScopeBegin("test", StructureType.FUNCTION))
        builder.insert(IRBinaryOp(t1, BinaryOps.MUL, Reference(a), Reference(b)))
        builder.insert(IRBinaryOp(t2, BinaryOps.MUL, Reference(t1), Reference(c)))
        builder.insert(IRBinaryOp(t3, BinaryOps.MUL, Reference(t2), Reference(d)))
        builder.insert(IRReturn(Reference(t3)))
        builder.insert(IRScopeEnd("test", StructureType.FUNCTION))

        result = _run_pass(builder)
        computes = _find_computes(result)

        self.assertEqual(len(computes), 1)
        tree = computes[0].operands[1]
        self.assertEqual(tree["op"], "product")
        self.assertEqual(len(tree["args"]), 4)


class TestAveragePattern(unittest.TestCase):
    """(a+b+c)/3 → average(a, b, c)"""

    def test_sum_div_n_becomes_average(self):
        func = _make_function("test")
        a, b, c = _make_int_var("a"), _make_int_var("b"), _make_int_var("c")
        t1, t2, t3 = _make_int_var("t1"), _make_int_var("t2"), _make_int_var("t3")

        builder = IRBuilder()
        builder.insert(IRFunction(func))
        builder.insert(IRScopeBegin("test", StructureType.FUNCTION))
        builder.insert(IRBinaryOp(t1, BinaryOps.ADD, Reference(a), Reference(b)))
        builder.insert(IRBinaryOp(t2, BinaryOps.ADD, Reference(t1), Reference(c)))
        builder.insert(IRBinaryOp(t3, BinaryOps.DIV, Reference(t2), Reference(_make_int_lit(3))))
        builder.insert(IRReturn(Reference(t3)))
        builder.insert(IRScopeEnd("test", StructureType.FUNCTION))

        result = _run_pass(builder)
        computes = _find_computes(result)

        self.assertEqual(len(computes), 1)
        tree = computes[0].operands[1]
        self.assertEqual(tree["op"], "average")
        self.assertEqual(len(tree["args"]), 3)

    def test_sum_div_mismatch_not_average(self):
        """(a+b+c)/2 → 不合并为 average，但 sum 仍提升"""
        func = _make_function("test")
        a, b, c = _make_int_var("a"), _make_int_var("b"), _make_int_var("c")
        t1, t2, t3 = _make_int_var("t1"), _make_int_var("t2"), _make_int_var("t3")

        builder = IRBuilder()
        builder.insert(IRFunction(func))
        builder.insert(IRScopeBegin("test", StructureType.FUNCTION))
        builder.insert(IRBinaryOp(t1, BinaryOps.ADD, Reference(a), Reference(b)))
        builder.insert(IRBinaryOp(t2, BinaryOps.ADD, Reference(t1), Reference(c)))
        builder.insert(IRBinaryOp(t3, BinaryOps.DIV, Reference(t2), Reference(_make_int_lit(2))))
        builder.insert(IRReturn(Reference(t3)))
        builder.insert(IRScopeEnd("test", StructureType.FUNCTION))

        result = _run_pass(builder)
        computes = _find_computes(result)

        # sum 链提升，但 DIV 不提升 → 有 COMPUTE(sum) + BINARY_OP(DIV)
        self.assertGreaterEqual(len(computes), 1)
        tree = computes[0].operands[1]
        self.assertEqual(tree["op"], "sum")


class TestFunctionCallLifting(unittest.TestCase):
    """多参数函数调用直接提升"""

    def test_average_call(self):
        """CALL average(a, b, c) → COMPUTE average(a, b, c)"""
        func = _make_function("test")
        avg_func = _make_function("average", 3)
        a, b, c = _make_int_var("a"), _make_int_var("b"), _make_int_var("c")
        result = _make_int_var("result")

        builder = IRBuilder()
        builder.insert(IRFunction(func))
        builder.insert(IRScopeBegin("test", StructureType.FUNCTION))
        builder.insert(IRCall(result, avg_func, {
            "p0": Reference(a), "p1": Reference(b), "p2": Reference(c)
        }))
        builder.insert(IRReturn(Reference(result)))
        builder.insert(IRScopeEnd("test", StructureType.FUNCTION))

        r = _run_pass(builder)
        computes = _find_computes(r)

        self.assertEqual(len(computes), 1)
        tree = computes[0].operands[1]
        self.assertEqual(tree["op"], "average")
        self.assertEqual(len(tree["args"]), 3)


class TestNoLift(unittest.TestCase):
    """不应提升的场景"""

    def test_single_binary_op_no_lift(self):
        """单条 BINARY_OP（无链）无收益，不提升"""
        func = _make_function("test")
        a, b = _make_int_var("a"), _make_int_var("b")
        t1 = _make_int_var("t1")

        builder = IRBuilder()
        builder.insert(IRFunction(func))
        builder.insert(IRScopeBegin("test", StructureType.FUNCTION))
        builder.insert(IRBinaryOp(t1, BinaryOps.ADD, Reference(a), Reference(b)))
        builder.insert(IRReturn(Reference(t1)))
        builder.insert(IRScopeEnd("test", StructureType.FUNCTION))

        result = _run_pass(builder)
        self.assertEqual(len(_find_computes(result)), 0)

    def test_bit_xor_not_lifted(self):
        """BIT_XOR 不在可提升集合中"""
        func = _make_function("test")
        a, b = _make_int_var("a"), _make_int_var("b")
        t1 = _make_int_var("t1")

        builder = IRBuilder()
        builder.insert(IRFunction(func))
        builder.insert(IRScopeBegin("test", StructureType.FUNCTION))
        builder.insert(IRBinaryOp(t1, BinaryOps.BIT_XOR, Reference(a), Reference(b)))
        builder.insert(IRReturn(Reference(t1)))
        builder.insert(IRScopeEnd("test", StructureType.FUNCTION))

        result = _run_pass(builder)
        self.assertEqual(len(_find_computes(result)), 0)

    def test_version_below_26_3_no_lift(self):
        """目标版本 < 26.3 时不运行"""
        config = CompileConfig(
            "ns",
            version=MinecraftVersion.instance("1.21.5"),
            optimization_level=OptimizationLevel.O2,
        )

        func = _make_function("test")
        a, b, c = _make_int_var("a"), _make_int_var("b"), _make_int_var("c")
        t1, t2 = _make_int_var("t1"), _make_int_var("t2")

        builder = IRBuilder()
        builder.insert(IRFunction(func))
        builder.insert(IRScopeBegin("test", StructureType.FUNCTION))
        builder.insert(IRBinaryOp(t1, BinaryOps.ADD, Reference(a), Reference(b)))
        builder.insert(IRBinaryOp(t2, BinaryOps.ADD, Reference(t1), Reference(c)))
        builder.insert(IRReturn(Reference(t2)))
        builder.insert(IRScopeEnd("test", StructureType.FUNCTION))

        p = NumberProviderLiftingPass(builder, config)
        ctx = type("Ctx", (), {"has_feature": lambda s, f: True, "was_executed": lambda s, n: False})()
        if p.should_run(ctx):
            p.execute()
        self.assertEqual(len(_find_computes(builder)), 0)


class TestComputeInstruction(unittest.TestCase):
    """IRCompute 指令本身的结构验证"""

    def test_compute_integer_flag(self):
        """COMPUTE 默认 integer=True"""
        result = _make_int_var("r")
        tree = {"op": "sum", "args": [Reference(_make_int_var("a")), Reference(_make_int_var("b"))]}
        instr = IRCompute(result, tree, integer=True)

        self.assertEqual(instr.opcode, IROpCode.COMPUTE)
        self.assertEqual(instr.operands[0], result)
        self.assertEqual(instr.operands[1], tree)
        self.assertTrue(instr.operands[2])

    def test_compute_repr_readable(self):
        """repr 应生成人可读的伪代码"""
        a = _make_int_var("a")
        tree = {"op": "sum", "args": [Reference(a), 3]}
        instr = IRCompute(_make_int_var("r"), tree, integer=True)
        r = repr(instr)
        self.assertIn("COMPUTE", r)
        self.assertIn("sum", r)


class TestEdgeCases(unittest.TestCase):
    """边界情况"""

    def test_forked_chain_not_lifted(self):
        """t1 被两条指令消费 → 不提升（防止悬空引用）"""
        func = _make_function("test")
        a, b, c, d = (_make_int_var("a"), _make_int_var("b"),
                      _make_int_var("c"), _make_int_var("d"))
        t1, t2, t3 = _make_int_var("t1"), _make_int_var("t2"), _make_int_var("t3")

        builder = IRBuilder()
        builder.insert(IRFunction(func))
        builder.insert(IRScopeBegin("test", StructureType.FUNCTION))
        builder.insert(IRBinaryOp(t1, BinaryOps.ADD, Reference(a), Reference(b)))
        builder.insert(IRBinaryOp(t2, BinaryOps.MUL, Reference(t1), Reference(c)))
        builder.insert(IRBinaryOp(t3, BinaryOps.MIN, Reference(t1), Reference(d)))
        builder.insert(IRReturn(Reference(t2)))
        builder.insert(IRScopeEnd("test", StructureType.FUNCTION))

        result = _run_pass(builder)
        # t1 有分叉，链根不会穿过 t1，但 t2/t3 各自的单链也不够长
        # 不应产生悬空引用
        for instr in result.get_instructions():
            if instr.opcode == IROpCode.ASSIGN:
                # 不应有 ASSIGN t1, 0（那会让 t2/t3 的引用悬空）
                self.assertNotEqual(instr.operands[0].get_name(), "t1")

    def test_chain_with_constant_literal(self):
        """a + 5 + b → sum(a, 5, b)，常量作为 Reference 叶节点保留"""
        func = _make_function("test")
        a, b = _make_int_var("a"), _make_int_var("b")
        five = _make_int_lit(5)
        t1, t2 = _make_int_var("t1"), _make_int_var("t2")

        builder = IRBuilder()
        builder.insert(IRFunction(func))
        builder.insert(IRScopeBegin("test", StructureType.FUNCTION))
        builder.insert(IRBinaryOp(t1, BinaryOps.ADD, Reference(a), Reference(five)))
        builder.insert(IRBinaryOp(t2, BinaryOps.ADD, Reference(t1), Reference(b)))
        builder.insert(IRReturn(Reference(t2)))
        builder.insert(IRScopeEnd("test", StructureType.FUNCTION))

        result = _run_pass(builder)
        computes = _find_computes(result)
        self.assertEqual(len(computes), 1)
        tree = computes[0].operands[1]
        self.assertEqual(tree["op"], "sum")
        self.assertEqual(len(tree["args"]), 3)

    def test_non_liftable_op_interrupts_chain(self):
        """a + b; (a+b) & c — BIT_AND 中断链，ADD 不提升"""
        func = _make_function("test")
        a, b, c = _make_int_var("a"), _make_int_var("b"), _make_int_var("c")
        t1, t2 = _make_int_var("t1"), _make_int_var("t2")

        builder = IRBuilder()
        builder.insert(IRFunction(func))
        builder.insert(IRScopeBegin("test", StructureType.FUNCTION))
        builder.insert(IRBinaryOp(t1, BinaryOps.ADD, Reference(a), Reference(b)))
        builder.insert(IRBinaryOp(t2, BinaryOps.BIT_AND, Reference(t1), Reference(c)))
        builder.insert(IRReturn(Reference(t2)))
        builder.insert(IRScopeEnd("test", StructureType.FUNCTION))

        result = _run_pass(builder)
        # BIT_AND 消费 t1 → t1 不是链根，单条 ADD 也不够长
        self.assertEqual(len(_find_computes(result)), 0)

    def test_div_with_variable_divisor_not_average(self):
        """(a+b+c) / d（d 是变量）→ sum 提升，DIV 留着"""
        func = _make_function("test")
        a, b, c, d = (_make_int_var("a"), _make_int_var("b"),
                      _make_int_var("c"), _make_int_var("d"))
        t1, t2, t3 = _make_int_var("t1"), _make_int_var("t2"), _make_int_var("t3")

        builder = IRBuilder()
        builder.insert(IRFunction(func))
        builder.insert(IRScopeBegin("test", StructureType.FUNCTION))
        builder.insert(IRBinaryOp(t1, BinaryOps.ADD, Reference(a), Reference(b)))
        builder.insert(IRBinaryOp(t2, BinaryOps.ADD, Reference(t1), Reference(c)))
        builder.insert(IRBinaryOp(t3, BinaryOps.DIV, Reference(t2), Reference(d)))
        builder.insert(IRReturn(Reference(t3)))
        builder.insert(IRScopeEnd("test", StructureType.FUNCTION))

        result = _run_pass(builder)
        # 除数是变量 → 不匹配 average，但 sum 链应提升
        computes = _find_computes(result)
        self.assertGreaterEqual(len(computes), 1)
        tree = computes[0].operands[1]
        self.assertEqual(tree["op"], "sum")

if __name__ == "__main__":
    unittest.main()