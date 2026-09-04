# coding=utf-8
"""
数值提供器提升 Pass 测试

测试策略：手工构造 IR，验证 Pass 将 BINARY_OP 链和函数调用
正确提升为 COMPUTE 指令，provider_tree 结构符合 26.3 格式。
"""
import unittest

from dovetail.core.compile_config import CompileConfig
from dovetail.core.enums import (
    OptimizationLevel, PrimitiveDataType, MinecraftVersion, BinaryOps,
)
from dovetail.core.enums.types import StructureType
from dovetail.core.instructions import (
    IRFunction, IRScopeBegin, IRScopeEnd, IRReturn,
    IRBinaryOp, IRCall, IROpCode, IRCompute,
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


def _make_float_var(name: str) -> Variable:
    return Variable(name, PrimitiveDataType.FLOAT)


def _make_int_lit(value: int) -> Literal:
    return Literal(PrimitiveDataType.INT, value)


def _make_float_lit(value: float) -> Literal:
    return Literal(PrimitiveDataType.FLOAT, value)


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


# ━━━━━━━━━━━━━━ 辅助断言 ━━━━━━━━━━━━━━

def _assert_mc_type(tree: dict, expected_short: str):
    """断言 tree 的 type 字段为 minecraft:<expected_short>"""
    assert tree.get("type") == f"minecraft:{expected_short}", (
        f"Expected type 'minecraft:{expected_short}', got {tree.get('type')!r}"
    )


def _assert_multi(tree: dict, expected_short: str, expected_arg_count: int):
    """断言为 multi-arg provider，并验证 inputs 长度"""
    _assert_mc_type(tree, expected_short)
    assert "inputs" in tree, f"Expected 'inputs' key, got keys: {list(tree.keys())}"
    assert len(tree["inputs"]) == expected_arg_count, (
        f"Expected {expected_arg_count} inputs, got {len(tree['inputs'])}"
    )


def _assert_binary(tree: dict, expected_short: str):
    """断言为 binary provider"""
    _assert_mc_type(tree, expected_short)
    assert "left" in tree and "right" in tree, (
        f"Expected 'left'/'right' keys, got keys: {list(tree.keys())}"
    )


# ════════════════════════════════════════════════════
#  基础链提升
# ════════════════════════════════════════════════════

class TestBasicLifting(unittest.TestCase):
    """基础链提升"""

    def test_add_chain_flattened(self):
        """a + b + c → COMPUTE add(inputs=[a, b, c])"""
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
        _assert_multi(tree, "add", 3)

    def test_mixed_ops_nested(self):
        """min(a + b, c * d) → min(inputs=[add(a,b), mul(c,d)])"""
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
        _assert_multi(tree, "min", 2)
        # 左子节点是 add
        _assert_mc_type(tree["inputs"][0], "add")
        # 右子节点是 mul
        _assert_mc_type(tree["inputs"][1], "mul")

    def test_sub_is_independent_binary(self):
        """a - b → COMPUTE sub(left=a, right=b) — 不再包装为 add/product"""
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
        # 单条 SUB 无收益（subtree < 2），不提升
        computes = _find_computes(result)
        self.assertEqual(len(computes), 0)

    def test_add_then_sub_chain(self):
        """a + b - c → sub(left=add(inputs=[a, b]), right=c)"""
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
        # 根是 sub，不是 sum！
        _assert_binary(tree, "sub")
        # left 是 add(a, b)
        left = tree["left"]
        _assert_multi(left, "add", 2)
        # right 是 c（Reference 叶节点）
        self.assertIsInstance(tree["right"], Reference)

    def test_sub_then_sub_chain(self):
        """a - b - c → sub(left=sub(left=a, right=b), right=c)"""
        func = _make_function("test")
        a, b, c = _make_int_var("a"), _make_int_var("b"), _make_int_var("c")
        t1, t2 = _make_int_var("t1"), _make_int_var("t2")

        builder = IRBuilder()
        builder.insert(IRFunction(func))
        builder.insert(IRScopeBegin("test", StructureType.FUNCTION))
        builder.insert(IRBinaryOp(t1, BinaryOps.SUB, Reference(a), Reference(b)))
        builder.insert(IRBinaryOp(t2, BinaryOps.SUB, Reference(t1), Reference(c)))
        builder.insert(IRReturn(Reference(t2)))
        builder.insert(IRScopeEnd("test", StructureType.FUNCTION))

        result = _run_pass(builder)
        computes = _find_computes(result)

        self.assertEqual(len(computes), 1)
        tree = computes[0].operands[1]
        # 根是 sub
        _assert_binary(tree, "sub")
        # left 也是 sub（嵌套）
        _assert_binary(tree["left"], "sub")


# ════════════════════════════════════════════════════
#  同类运算聚合
# ════════════════════════════════════════════════════

class TestFlattening(unittest.TestCase):
    """同类 multi-arg 运算聚合"""

    def test_nested_add_flattened(self):
        """add(add(a,b), add(c,d)) → add(inputs=[a, b, c, d])"""
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
        _assert_multi(tree, "add", 4)

    def test_mul_chain_flattened(self):
        """a * b * c * d → mul(inputs=[a, b, c, d])"""
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
        _assert_multi(tree, "mul", 4)

    def test_min_chain_flattened(self):
        """min(min(a,b), min(c,d)) → min(inputs=[a, b, c, d])"""
        func = _make_function("test")
        a, b, c, d = (_make_int_var("a"), _make_int_var("b"),
                      _make_int_var("c"), _make_int_var("d"))
        t1, t2, t3 = _make_int_var("t1"), _make_int_var("t2"), _make_int_var("t3")

        builder = IRBuilder()
        builder.insert(IRFunction(func))
        builder.insert(IRScopeBegin("test", StructureType.FUNCTION))
        builder.insert(IRBinaryOp(t1, BinaryOps.MIN, Reference(a), Reference(b)))
        builder.insert(IRBinaryOp(t2, BinaryOps.MIN, Reference(c), Reference(d)))
        builder.insert(IRBinaryOp(t3, BinaryOps.MIN, Reference(t1), Reference(t2)))
        builder.insert(IRReturn(Reference(t3)))
        builder.insert(IRScopeEnd("test", StructureType.FUNCTION))

        result = _run_pass(builder)
        computes = _find_computes(result)

        self.assertEqual(len(computes), 1)
        tree = computes[0].operands[1]
        _assert_multi(tree, "min", 4)

    def test_sub_not_flattened(self):
        """sub 不是 multi-arg，不会扁平化：sub(sub(a,b), c) 保持嵌套"""
        func = _make_function("test")
        a, b, c = _make_int_var("a"), _make_int_var("b"), _make_int_var("c")
        t1, t2 = _make_int_var("t1"), _make_int_var("t2")

        builder = IRBuilder()
        builder.insert(IRFunction(func))
        builder.insert(IRScopeBegin("test", StructureType.FUNCTION))
        builder.insert(IRBinaryOp(t1, BinaryOps.SUB, Reference(a), Reference(b)))
        builder.insert(IRBinaryOp(t2, BinaryOps.SUB, Reference(t1), Reference(c)))
        builder.insert(IRReturn(Reference(t2)))
        builder.insert(IRScopeEnd("test", StructureType.FUNCTION))

        result = _run_pass(builder)
        computes = _find_computes(result)

        self.assertEqual(len(computes), 1)
        tree = computes[0].operands[1]
        # 根是 sub，left 也是 sub — 嵌套结构
        _assert_binary(tree, "sub")
        _assert_binary(tree["left"], "sub")


# ════════════════════════════════════════════════════
#  average 反向推导
# ════════════════════════════════════════════════════

class TestAveragePattern(unittest.TestCase):
    """div(add(a,b,c), 3) → avg(inputs=[a, b, c])"""

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
        _assert_multi(tree, "avg", 3)

    def test_sum_div_mismatch_not_average(self):
        """div(add(a,b,c), 2) → div(left=add(a,b,c), right=2)，不合并为 avg"""
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

        # 除数不匹配 → 整体提升为 div(left=add(...), right=2)
        self.assertGreaterEqual(len(computes), 1)
        tree = computes[0].operands[1]
        _assert_binary(tree, "div")
        _assert_mc_type(tree["left"], "add")


# ════════════════════════════════════════════════════
#  函数调用提升
# ════════════════════════════════════════════════════

class TestFunctionCallLifting(unittest.TestCase):
    """多参数函数调用直接提升"""

    def test_avg_call(self):
        """CALL avg(a, b, c) → COMPUTE avg(inputs=[a, b, c])"""
        func = _make_function("test")
        avg_func = _make_function("avg", 3)
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
        _assert_multi(tree, "avg", 3)

    def test_min_call_old_name(self):
        """CALL min(a, b) → COMPUTE min(inputs=[a, b])（旧名兼容）"""
        func = _make_function("test")
        min_func = _make_function("min", 2)
        a, b = _make_int_var("a"), _make_int_var("b")
        result = _make_int_var("result")

        builder = IRBuilder()
        builder.insert(IRFunction(func))
        builder.insert(IRScopeBegin("test", StructureType.FUNCTION))
        builder.insert(IRCall(result, min_func, {
            "p0": Reference(a), "p1": Reference(b)
        }))
        builder.insert(IRReturn(Reference(result)))
        builder.insert(IRScopeEnd("test", StructureType.FUNCTION))

        r = _run_pass(builder)
        computes = _find_computes(r)

        self.assertEqual(len(computes), 1)
        tree = computes[0].operands[1]
        _assert_multi(tree, "min", 2)


# ════════════════════════════════════════════════════
#  不应提升的场景
# ════════════════════════════════════════════════════

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


# ════════════════════════════════════════════════════
#  IRCompute 指令结构
# ════════════════════════════════════════════════════

class TestComputeInstruction(unittest.TestCase):
    """IRCompute 指令本身的结构验证"""

    def test_compute_integer_kind(self):
        """整数 COMPUTE"""
        result = _make_int_var("r")
        tree = {"type": "minecraft:add", "inputs": [Reference(_make_int_var("a")), Reference(_make_int_var("b"))]}
        instr = IRCompute(result, tree, compute_kind="integer")

        self.assertEqual(instr.opcode, IROpCode.COMPUTE)
        self.assertEqual(instr.operands[0], result)
        self.assertEqual(instr.operands[1], tree)
        self.assertEqual(instr.operands[2], "integer")
        self.assertIsNone(instr.operands[3])

    def test_compute_float_kind_with_scale(self):
        """浮点 COMPUTE 带 scale"""
        result = _make_float_var("r")
        tree = {"type": "minecraft:length", "inputs": [Reference(_make_float_var("a"))]}
        instr = IRCompute(result, tree, compute_kind="float", scale=100.0)

        self.assertEqual(instr.operands[2], "float")
        self.assertEqual(instr.operands[3], 100.0)

    def test_compute_repr_readable(self):
        """repr 应生成人可读的伪代码"""
        a = _make_int_var("a")
        tree = {"type": "minecraft:add", "inputs": [Reference(a), 3]}
        instr = IRCompute(_make_int_var("r"), tree, compute_kind="integer")
        r = repr(instr)
        self.assertIn("COMPUTE", r)
        self.assertIn("add", r)


# ════════════════════════════════════════════════════
#  compute_kind 推断
# ════════════════════════════════════════════════════

class TestComputeKindInference(unittest.TestCase):
    """整数/浮点分流推断"""

    def test_int_chain_produces_integer(self):
        """整数链 → compute_kind == "integer" """
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
        self.assertEqual(computes[0].operands[2], "integer")


# ════════════════════════════════════════════════════
#  边界情况
# ════════════════════════════════════════════════════

class TestEdgeCases(unittest.TestCase):
    """边界情况"""

    def test_forked_chain_safe(self):
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
        # 不应有 ASSIGN t1, 0（那会让 t2/t3 的引用悬空）
        for instr in result.get_instructions():
            if instr.opcode == IROpCode.ASSIGN:
                self.assertNotEqual(instr.operands[0].get_name(), "t1")

    def test_chain_with_constant_literal(self):
        """a + 5 + b → add(inputs=[a, 5, b])，常量作为叶节点保留"""
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
        _assert_multi(tree, "add", 3)

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
        self.assertEqual(len(_find_computes(result)), 0)

    def test_div_with_variable_divisor(self):
        """div(add(a,b,c), d) — d 是变量 → div(left=add(...), right=d)"""
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
        computes = _find_computes(result)
        self.assertGreaterEqual(len(computes), 1)
        tree = computes[0].operands[1]
        # 整体提升为 div
        _assert_binary(tree, "div")
        # left 是 add
        _assert_mc_type(tree["left"], "add")

    def test_mod_chain_lifted(self):
        """a + b; (a+b) % c → mod(left=add(a,b), right=c)"""
        func = _make_function("test")
        a, b, c = _make_int_var("a"), _make_int_var("b"), _make_int_var("c")
        t1, t2 = _make_int_var("t1"), _make_int_var("t2")

        builder = IRBuilder()
        builder.insert(IRFunction(func))
        builder.insert(IRScopeBegin("test", StructureType.FUNCTION))
        builder.insert(IRBinaryOp(t1, BinaryOps.ADD, Reference(a), Reference(b)))
        builder.insert(IRBinaryOp(t2, BinaryOps.MOD, Reference(t1), Reference(c)))
        builder.insert(IRReturn(Reference(t2)))
        builder.insert(IRScopeEnd("test", StructureType.FUNCTION))

        result = _run_pass(builder)
        computes = _find_computes(result)
        self.assertEqual(len(computes), 1)
        tree = computes[0].operands[1]
        _assert_binary(tree, "mod")
        _assert_mc_type(tree["left"], "add")

    def test_minecraft_prefix_in_output(self):
        """所有输出的 type 字段必须带 minecraft: 前缀"""
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
        self.assertTrue(tree["type"].startswith("minecraft:"),
                        f"type should have minecraft: prefix, got {tree['type']!r}")

    def test_inputs_key_not_args(self):
        """输出使用 'inputs' 键而非旧 'args' 键"""
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
        self.assertIn("inputs", tree)
        self.assertNotIn("args", tree)
        self.assertNotIn("op", tree)


if __name__ == "__main__":
    unittest.main()