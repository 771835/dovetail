# coding=utf-8
"""
递归调用分析测试

测试策略：手工构造 IRBuilder（不走完整编译流水线），
验证调用图构建、SCC 检测和 IRCall 标记逻辑。
"""
import unittest

from dovetail.core.enums import PrimitiveDataType
from dovetail.core.enums.types import StructureType
from dovetail.core.instructions import (
    IRFunction, IRCall, IRReturn, IRScopeBegin, IRScopeEnd,
    IROpCode, IRInstruction,
)
from dovetail.core.ir_builder import IRBuilder
from dovetail.core.symbols import Function, Variable, Reference, Parameter

# ── 导入被测模块 ──────────────────────────────────────────────────────────────

from dovetail.plugins.je1215.backend.recursive_call_analysis import (
    build_call_graph,
    find_recursive_sccs,
    tag_recursive_calls,
    META_KEY_NEEDS_STACK_SAVE,
)


# ─── 工具函数 ─────────────────────────────────────────────────────────────────

def _make_int_var(name: str) -> Variable:
    """构造一个 int 类型的 Variable"""
    return Variable(name, PrimitiveDataType.INT)


def _make_function(name: str, params: list[Variable], return_type=PrimitiveDataType.INT) -> Function:
    """构造一个函数符号"""
    func_params = [Parameter(var=v) for v in params]
    return Function(name, func_params, return_type)


def _build_simple_function(name: str) -> tuple[IRBuilder, Function, Variable]:
    """构造一个最简单的非递归函数 fn name(n: int) -> int { return n }"""
    n = _make_int_var("n")
    func = _make_function(name, [n])
    builder = IRBuilder()
    builder.insert(IRFunction(func))
    builder.insert(IRScopeBegin(name, StructureType.FUNCTION))
    builder.insert(IRReturn(Reference(n)))
    builder.insert(IRScopeEnd(name, StructureType.FUNCTION))
    return builder, func, n


def _build_self_recursive_function(name: str) -> tuple[IRBuilder, Function, Variable]:
    """构造一个直接递归函数 fn name(n: int) -> int { return name(n) }"""
    n = _make_int_var("n")
    func = _make_function(name, [n])
    result_var = _make_int_var("__tmp")
    builder = IRBuilder()
    builder.insert(IRFunction(func))
    builder.insert(IRScopeBegin(name, StructureType.FUNCTION))
    builder.insert(IRCall(result_var, func, {"n": Reference(n)}))
    builder.insert(IRReturn(Reference(result_var)))
    builder.insert(IRScopeEnd(name, StructureType.FUNCTION))
    return builder, func, n


def _find_calls(builder: IRBuilder) -> list[IRInstruction]:
    """提取所有 IRCall 指令"""
    return [i for i in builder if i.opcode is IROpCode.CALL]


# ─── 调用图构建测试 ──────────────────────────────────────────────────────────

class TestBuildCallGraph(unittest.TestCase):
    """测试 build_call_graph()"""

    def test_non_recursive_function(self):
        """非递归函数：调用图为空边"""
        builder, func, n = _build_simple_function("foo")
        graph = build_call_graph(builder)
        self.assertIn("foo", graph.all_functions)
        self.assertEqual(graph.edges.get("foo", set()), set())

    def test_direct_recursive_function(self):
        """直接递归：调用图有自环"""
        builder, func, n = _build_self_recursive_function("fact")
        graph = build_call_graph(builder)
        self.assertIn("fact", graph.edges)
        self.assertIn("fact", graph.edges["fact"])

    def test_two_functions_call_chain(self):
        """A 调 B，B 不调 A：无环"""
        n = _make_int_var("n")
        a = _make_function("a", [n])
        b = _make_function("b", [n])
        result = _make_int_var("__tmp")

        builder = IRBuilder()
        builder.insert(IRFunction(a))
        builder.insert(IRScopeBegin("a", StructureType.FUNCTION))
        builder.insert(IRCall(result, b, {"n": Reference(n)}))
        builder.insert(IRReturn(Reference(result)))
        builder.insert(IRScopeEnd("a", StructureType.FUNCTION))

        builder.insert(IRFunction(b))
        builder.insert(IRScopeBegin("b", StructureType.FUNCTION))
        builder.insert(IRReturn(Reference(n)))
        builder.insert(IRScopeEnd("b", StructureType.FUNCTION))

        graph = build_call_graph(builder)
        self.assertEqual(graph.edges["a"], {"b"})
        self.assertNotIn("b", graph.edges)

    def test_mutual_recursive_pair(self):
        """A 调 B，B 调 A：双向边"""
        n = _make_int_var("n")
        a = _make_function("a", [n])
        b = _make_function("b", [n])
        result = _make_int_var("__tmp")

        builder = IRBuilder()
        builder.insert(IRFunction(a))
        builder.insert(IRScopeBegin("a", StructureType.FUNCTION))
        builder.insert(IRCall(result, b, {"n": Reference(n)}))
        builder.insert(IRReturn(Reference(result)))
        builder.insert(IRScopeEnd("a", StructureType.FUNCTION))

        builder.insert(IRFunction(b))
        builder.insert(IRScopeBegin("b", StructureType.FUNCTION))
        builder.insert(IRCall(result, a, {"n": Reference(n)}))
        builder.insert(IRReturn(Reference(result)))
        builder.insert(IRScopeEnd("b", StructureType.FUNCTION))

        graph = build_call_graph(builder)
        self.assertEqual(graph.edges["a"], {"b"})
        self.assertEqual(graph.edges["b"], {"a"})

    def test_empty_builder(self):
        """空 IR：调用图为空"""
        builder = IRBuilder()
        graph = build_call_graph(builder)
        self.assertEqual(graph.edges, {})
        self.assertEqual(graph.all_functions, set())


# ─── SCC 检测测试 ────────────────────────────────────────────────────────────

class TestFindRecursiveSCCs(unittest.TestCase):
    """测试 find_recursive_sccs()"""

    def test_no_recursion(self):
        """无递归：结果为空"""
        builder, _, _ = _build_simple_function("foo")
        graph = build_call_graph(builder)
        sccs = find_recursive_sccs(graph)
        self.assertEqual(sccs, [])

    def test_direct_recursion(self):
        """直接递归：检测为 is_direct=True"""
        builder, _, _ = _build_self_recursive_function("fact")
        graph = build_call_graph(builder)
        sccs = find_recursive_sccs(graph)
        self.assertEqual(len(sccs), 1)
        self.assertEqual(sccs[0].members, frozenset({"fact"}))
        self.assertTrue(sccs[0].is_direct)

    def test_mutual_recursion(self):
        """互递归：检测为 is_direct=False"""
        n = _make_int_var("n")
        a = _make_function("a", [n])
        b = _make_function("b", [n])
        result = _make_int_var("__tmp")

        builder = IRBuilder()
        builder.insert(IRFunction(a))
        builder.insert(IRScopeBegin("a", StructureType.FUNCTION))
        builder.insert(IRCall(result, b, {"n": Reference(n)}))
        builder.insert(IRReturn(Reference(result)))
        builder.insert(IRScopeEnd("a", StructureType.FUNCTION))

        builder.insert(IRFunction(b))
        builder.insert(IRScopeBegin("b", StructureType.FUNCTION))
        builder.insert(IRCall(result, a, {"n": Reference(n)}))
        builder.insert(IRReturn(Reference(result)))
        builder.insert(IRScopeEnd("b", StructureType.FUNCTION))

        graph = build_call_graph(builder)
        sccs = find_recursive_sccs(graph)
        self.assertEqual(len(sccs), 1)
        self.assertEqual(sccs[0].members, frozenset({"a", "b"}))
        self.assertFalse(sccs[0].is_direct)

    def test_three_way_cycle(self):
        """三函数环 A→B→C→A"""
        n = _make_int_var("n")
        a = _make_function("a", [n])
        b = _make_function("b", [n])
        c = _make_function("c", [n])
        result = _make_int_var("__tmp")

        builder = IRBuilder()
        for func, callee in [(a, b), (b, c), (c, a)]:
            builder.insert(IRFunction(func))
            builder.insert(IRScopeBegin(func.get_name(), StructureType.FUNCTION))
            builder.insert(IRCall(result, callee, {"n": Reference(n)}))
            builder.insert(IRReturn(Reference(result)))
            builder.insert(IRScopeEnd(func.get_name(), StructureType.FUNCTION))

        graph = build_call_graph(builder)
        sccs = find_recursive_sccs(graph)
        self.assertEqual(len(sccs), 1)
        self.assertEqual(sccs[0].members, frozenset({"a", "b", "c"}))
        self.assertFalse(sccs[0].is_direct)

    def test_scc_with_outgoing_edge(self):
        """递归 SCC 内的函数调用 SCC 外函数，外部函数不应被纳入"""
        n = _make_int_var("n")
        a = _make_function("a", [n])
        b = _make_function("b", [n])
        helper = _make_function("helper", [n])
        result = _make_int_var("__tmp")

        builder = IRBuilder()
        # a 调 b（递归）和 helper（非递归）
        builder.insert(IRFunction(a))
        builder.insert(IRScopeBegin("a", StructureType.FUNCTION))
        builder.insert(IRCall(result, b, {"n": Reference(n)}))
        builder.insert(IRCall(result, helper, {"n": Reference(n)}))
        builder.insert(IRReturn(Reference(result)))
        builder.insert(IRScopeEnd("a", StructureType.FUNCTION))

        # b 调 a（递归）
        builder.insert(IRFunction(b))
        builder.insert(IRScopeBegin("b", StructureType.FUNCTION))
        builder.insert(IRCall(result, a, {"n": Reference(n)}))
        builder.insert(IRReturn(Reference(result)))
        builder.insert(IRScopeEnd("b", StructureType.FUNCTION))

        # helper 不调任何人
        builder.insert(IRFunction(helper))
        builder.insert(IRScopeBegin("helper", StructureType.FUNCTION))
        builder.insert(IRReturn(Reference(n)))
        builder.insert(IRScopeEnd("helper", StructureType.FUNCTION))

        graph = build_call_graph(builder)
        sccs = find_recursive_sccs(graph)
        scc_members = [s.members for s in sccs]

        # helper 不在任何递归 SCC 内
        self.assertNotIn(frozenset({"helper"}), scc_members)
        # a, b 在同一个递归 SCC 内
        self.assertIn(frozenset({"a", "b"}), scc_members)

    def test_two_independent_recursive_functions(self):
        """两个独立的直接递归函数：应检出两个 SCC"""
        builder1, _, _ = _build_self_recursive_function("f")
        builder2, _, _ = _build_self_recursive_function("g")

        # 合并到同一个 builder
        combined = IRBuilder()
        for instr in builder1:
            combined.insert(instr)
        for instr in builder2:
            combined.insert(instr)

        graph = build_call_graph(combined)
        sccs = find_recursive_sccs(graph)
        self.assertEqual(len(sccs), 2)
        members = {s.members for s in sccs}
        self.assertIn(frozenset({"f"}), members)
        self.assertIn(frozenset({"g"}), members)


# ─── IRCall 标记测试 ─────────────────────────────────────────────────────────

class TestTagRecursiveCalls(unittest.TestCase):
    """测试 tag_recursive_calls()"""

    def test_non_recursive_not_tagged(self):
        """非递归函数的 IRCall 不应被打标签"""
        n = _make_int_var("n")
        a = _make_function("a", [n])
        b = _make_function("b", [n])
        result = _make_int_var("__tmp")

        builder = IRBuilder()
        builder.insert(IRFunction(a))
        builder.insert(IRScopeBegin("a", StructureType.FUNCTION))
        builder.insert(IRCall(result, b, {"n": Reference(n)}))
        builder.insert(IRReturn(Reference(result)))
        builder.insert(IRScopeEnd("a", StructureType.FUNCTION))

        builder.insert(IRFunction(b))
        builder.insert(IRScopeBegin("b", StructureType.FUNCTION))
        builder.insert(IRReturn(Reference(n)))
        builder.insert(IRScopeEnd("b", StructureType.FUNCTION))

        tag_recursive_calls(builder)

        calls = _find_calls(builder)
        self.assertEqual(len(calls), 1)
        self.assertNotIn(META_KEY_NEEDS_STACK_SAVE, calls[0].metadata)

    def test_direct_recursive_tagged(self):
        """直接递归调用应被打标签"""
        builder, _, _ = _build_self_recursive_function("fact")
        tag_recursive_calls(builder)

        calls = _find_calls(builder)
        self.assertEqual(len(calls), 1)
        self.assertTrue(calls[0].metadata.get(META_KEY_NEEDS_STACK_SAVE))

    def test_mutual_recursive_both_tagged(self):
        """互递归：A 调 B 和 B 调 A 都应打标签"""
        n = _make_int_var("n")
        a = _make_function("a", [n])
        b = _make_function("b", [n])
        result = _make_int_var("__tmp")

        builder = IRBuilder()
        builder.insert(IRFunction(a))
        builder.insert(IRScopeBegin("a", StructureType.FUNCTION))
        builder.insert(IRCall(result, b, {"n": Reference(n)}))
        builder.insert(IRReturn(Reference(result)))
        builder.insert(IRScopeEnd("a", StructureType.FUNCTION))

        builder.insert(IRFunction(b))
        builder.insert(IRScopeBegin("b", StructureType.FUNCTION))
        builder.insert(IRCall(result, a, {"n": Reference(n)}))
        builder.insert(IRReturn(Reference(result)))
        builder.insert(IRScopeEnd("b", StructureType.FUNCTION))

        tag_recursive_calls(builder)

        calls = _find_calls(builder)
        self.assertEqual(len(calls), 2)
        for call in calls:
            self.assertTrue(call.metadata.get(META_KEY_NEEDS_STACK_SAVE))

    def test_call_outside_scc_not_tagged(self):
        """递归 SCC 内的函数调用 SCC 外的函数，外部调用不应打标签"""
        n = _make_int_var("n")
        a = _make_function("a", [n])
        b = _make_function("b", [n])
        helper = _make_function("helper", [n])
        result = _make_int_var("__tmp")

        builder = IRBuilder()
        # a 调 b（递归）和 helper（非递归）
        builder.insert(IRFunction(a))
        builder.insert(IRScopeBegin("a", StructureType.FUNCTION))
        builder.insert(IRCall(result, b, {"n": Reference(n)}))
        builder.insert(IRCall(result, helper, {"n": Reference(n)}))
        builder.insert(IRReturn(Reference(result)))
        builder.insert(IRScopeEnd("a", StructureType.FUNCTION))

        # b 调 a（递归）
        builder.insert(IRFunction(b))
        builder.insert(IRScopeBegin("b", StructureType.FUNCTION))
        builder.insert(IRCall(result, a, {"n": Reference(n)}))
        builder.insert(IRReturn(Reference(result)))
        builder.insert(IRScopeEnd("b", StructureType.FUNCTION))

        # helper 不调任何人
        builder.insert(IRFunction(helper))
        builder.insert(IRScopeBegin("helper", StructureType.FUNCTION))
        builder.insert(IRReturn(Reference(n)))
        builder.insert(IRScopeEnd("helper", StructureType.FUNCTION))

        tag_recursive_calls(builder)

        calls = _find_calls(builder)
        self.assertEqual(len(calls), 3)

        tagged_callees = set()
        untagged_callees = set()
        for call in calls:
            callee_name: str = call.operands[1].get_name()
            if call.metadata.get(META_KEY_NEEDS_STACK_SAVE):
                tagged_callees.add(callee_name)
            else:
                untagged_callees.add(callee_name)

        # a→b 和 b→a 应标，a→helper 不应标
        self.assertEqual(tagged_callees, {"a", "b"})
        self.assertEqual(untagged_callees, {"helper"})

    def test_empty_builder_no_crash(self):
        """空 IR 不应崩溃"""
        builder = IRBuilder()
        tag_recursive_calls(builder)

    def test_no_recursion_no_tags(self):
        """无递归时，所有 IRCall 都不应被打标签"""
        n = _make_int_var("n")
        a = _make_function("a", [n])
        b = _make_function("b", [n])
        c = _make_function("c", [n])
        result = _make_int_var("__tmp")

        builder = IRBuilder()
        # a→b→c，无环
        builder.insert(IRFunction(a))
        builder.insert(IRScopeBegin("a", StructureType.FUNCTION))
        builder.insert(IRCall(result, b, {"n": Reference(n)}))
        builder.insert(IRReturn(Reference(result)))
        builder.insert(IRScopeEnd("a", StructureType.FUNCTION))

        builder.insert(IRFunction(b))
        builder.insert(IRScopeBegin("b", StructureType.FUNCTION))
        builder.insert(IRCall(result, c, {"n": Reference(n)}))
        builder.insert(IRReturn(Reference(result)))
        builder.insert(IRScopeEnd("b", StructureType.FUNCTION))

        builder.insert(IRFunction(c))
        builder.insert(IRScopeBegin("c", StructureType.FUNCTION))
        builder.insert(IRReturn(Reference(n)))
        builder.insert(IRScopeEnd("c", StructureType.FUNCTION))

        tag_recursive_calls(builder)

        calls = _find_calls(builder)
        for call in calls:
            self.assertNotIn(META_KEY_NEEDS_STACK_SAVE, call.metadata)

    def test_idempotent(self):
        """重复调用 tag_recursive_calls 不应产生重复标签或副作用"""
        builder, _, _ = _build_self_recursive_function("fact")
        tag_recursive_calls(builder)
        tag_recursive_calls(builder)

        calls = _find_calls(builder)
        self.assertEqual(len(calls), 1)
        # 仍然是 True，不是 True 被覆盖两次
        self.assertTrue(calls[0].metadata.get(META_KEY_NEEDS_STACK_SAVE))


# ─── Tarjan 算法测试 ─────────────────────────────────────────────────────────

class TestTarjanSCC(unittest.TestCase):
    """单独测试 Tarjan 算法的正确性"""

    def _tarjan(self, graph: dict[str, set[str]]) -> list[frozenset[str]]:
        """便捷入口"""
        from dovetail.plugins.je1215.backend.recursive_call_analysis import _tarjan_scc
        return _tarjan_scc(graph)

    def test_single_node_no_self_loop(self):
        graph = {"a": set()}
        sccs = self._tarjan(graph)
        self.assertEqual(len(sccs), 1)
        self.assertEqual(sccs[0], frozenset({"a"}))

    def test_single_node_self_loop(self):
        graph = {"a": {"a"}}
        sccs = self._tarjan(graph)
        self.assertEqual(len(sccs), 1)
        self.assertEqual(sccs[0], frozenset({"a"}))

    def test_two_cycles_isolated(self):
        graph = {
            "a": {"b"}, "b": {"a"},
            "c": {"d"}, "d": {"c"},
        }
        sccs = self._tarjan(graph)
        members = {s for s in sccs}
        self.assertEqual(len(sccs), 2)
        self.assertIn(frozenset({"a", "b"}), members)
        self.assertIn(frozenset({"c", "d"}), members)

    def test_dag(self):
        """DAG：每个节点自身就是一个 SCC"""
        graph = {"a": {"b"}, "b": {"c"}, "c": set()}
        sccs = self._tarjan(graph)
        self.assertEqual(len(sccs), 3)
        members = {s for s in sccs}
        self.assertEqual(members, {frozenset({"a"}), frozenset({"b"}), frozenset({"c"})})


if __name__ == "__main__":
    unittest.main()