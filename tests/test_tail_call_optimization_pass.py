# coding=utf-8
"""
尾递归优化 Pass 测试

测试策略：直接手工构造 IRBuilder（不走完整编译流水线），
验证 Pass 的识别逻辑与 IR 变换结果。
"""
import unittest

from dovetail.core.compile_config import CompileConfig
from dovetail.core.enums import OptimizationLevel, PrimitiveDataType, MinecraftVersion
from dovetail.core.instructions import (
    IRFunction, IRCall, IRReturn, IRScopeBegin, IRScopeEnd,
    IROpCode,
)
from dovetail.core.enums.types import StructureType
from dovetail.core.ir_builder import IRBuilder
from dovetail.core.symbols import Function, Variable, Reference, Parameter
from dovetail.core.optimize.passes.tail_call_optimization import (
    TailCallOptimizationPass,
    _TCO_SCOPE_SUFFIX,
)


# ─── 工具函数 ─────────────────────────────────────────────────────────────────

def _make_config(level: OptimizationLevel = OptimizationLevel.O3) -> CompileConfig:
    """构造一个最小化 CompileConfig"""
    return CompileConfig("n", version=MinecraftVersion.instance("1.21.5"), optimization_level=level, debug=False)


def _make_int_var(name: str) -> Variable:
    """构造一个 int 类型的 Variable"""
    return Variable(name, PrimitiveDataType.INT)


def _make_function(name: str, params: list[Variable], return_type=PrimitiveDataType.INT) -> Function:
    """构造一个函数符号"""
    func_params = [Parameter(var=v) for v in params]
    return Function(name, func_params, return_type)


def _opcodes(builder: IRBuilder) -> list[IROpCode]:
    """提取 IRBuilder 中所有指令的 opcode，方便断言"""
    return [instr.opcode for instr in builder.get_instructions()]


def _find_all(builder: IRBuilder, opcode: IROpCode) -> list[int]:
    """找出指定 opcode 的所有位置索引"""
    return [i for i, instr in enumerate(builder.get_instructions())
            if instr.opcode is opcode]


# ─── 测试用例 ──────────────────────────────────────────────────────────────────

class TestTCOPassAnalyze(unittest.TestCase):
    """测试 analyze() 的识别逻辑"""

    def _build_simple_tail_recursive_ir(self):
        """
        构造最简单的直接尾递归 IR，对应：

            fn fib(n: int) -> int {
                return fib(n)    # 简化：参数不变，只测结构
            }
        """
        n = _make_int_var("n")
        fib = _make_function("fib", [n])
        result_var = _make_int_var("__tmp")

        builder = IRBuilder()
        builder.insert(IRFunction(fib))
        builder.insert(IRScopeBegin("fib", StructureType.FUNCTION))
        builder.insert(IRCall(result_var, fib, {"n": Reference(n)}))
        builder.insert(IRReturn(Reference(result_var)))
        builder.insert(IRScopeEnd("fib", StructureType.FUNCTION))
        return builder, fib

    def test_detects_direct_tail_recursion(self):
        """analyze() 应识别出直接尾递归候选"""
        builder, fib = self._build_simple_tail_recursive_ir()
        config = _make_config()
        pass_ = TailCallOptimizationPass(builder, config)

        result = pass_.analyze()
        candidates = result.get("candidates", {})

        self.assertIn("fib", candidates)
        self.assertEqual(len(candidates["fib"]), 1)

    def test_no_false_positive_on_non_tail_call(self):
        """
        非尾调用不应被识别。对应：

            fn foo(n: int) -> int {
                let tmp = foo(n)
                return tmp + 1   # return 的不是 tmp，而是表达式结果
            }

        此处用 result_var2 模拟 tmp+1 的中间结果，
        使 return 值与 call 结果不同。
        """
        n = _make_int_var("n")
        foo = _make_function("foo", [n])
        call_result = _make_int_var("__tmp")
        other_result = _make_int_var("__other")  # 与 call_result 不同

        builder = IRBuilder()
        builder.insert(IRFunction(foo))
        builder.insert(IRScopeBegin("foo", StructureType.FUNCTION))
        builder.insert(IRCall(call_result, foo, {"n": Reference(n)}))
        # return 的是另一个变量，不是 call 的结果
        builder.insert(IRReturn(Reference(other_result)))
        builder.insert(IRScopeEnd("foo", StructureType.FUNCTION))

        config = _make_config()
        pass_ = TailCallOptimizationPass(builder, config)
        result = pass_.analyze()
        candidates = result.get("candidates", {})

        self.assertNotIn("foo", candidates)

    def test_no_false_positive_on_mutual_recursion(self):
        """
        互递归不应被识别（foo 调 bar，不是自身）。
        """
        n = _make_int_var("n")
        foo = _make_function("foo", [n])
        bar = _make_function("bar", [n])  # 不同函数
        result_var = _make_int_var("__tmp")

        builder = IRBuilder()
        builder.insert(IRFunction(foo))
        builder.insert(IRScopeBegin("foo", StructureType.FUNCTION))
        # foo 调用 bar，不是 foo 自身
        builder.insert(IRCall(result_var, bar, {"n": Reference(n)}))
        builder.insert(IRReturn(Reference(result_var)))
        builder.insert(IRScopeEnd("foo", StructureType.FUNCTION))

        config = _make_config()
        pass_ = TailCallOptimizationPass(builder, config)
        result = pass_.analyze()
        candidates = result.get("candidates", {})

        self.assertNotIn("foo", candidates)

    def test_detects_multiple_tail_call_sites(self):
        """
        同一函数内有多个尾调用点（多分支都 return 自身），
        应全部识别出来。对应：

            fn f(n: int) -> int {
                if (...) { return f(n) }   # site 1
                return f(n)                # site 2
            }
        """
        n = _make_int_var("n")
        f = _make_function("f", [n])
        tmp1 = _make_int_var("__tmp1")
        tmp2 = _make_int_var("__tmp2")

        builder = IRBuilder()
        builder.insert(IRFunction(f))
        builder.insert(IRScopeBegin("f", StructureType.FUNCTION))

        # 分支 1（模拟 if 体，用嵌套 scope 表示）
        builder.insert(IRScopeBegin("f_if", StructureType.CONDITIONAL))
        builder.insert(IRCall(tmp1, f, {"n": Reference(n)}))
        builder.insert(IRReturn(Reference(tmp1)))
        builder.insert(IRScopeEnd("f_if", StructureType.CONDITIONAL))

        # 分支 2（函数体末尾）
        builder.insert(IRCall(tmp2, f, {"n": Reference(n)}))
        builder.insert(IRReturn(Reference(tmp2)))

        builder.insert(IRScopeEnd("f", StructureType.FUNCTION))

        config = _make_config()
        pass_ = TailCallOptimizationPass(builder, config)
        result = pass_.analyze()
        candidates = result.get("candidates", {})

        self.assertIn("f", candidates)
        self.assertEqual(len(candidates["f"]), 2)

    def test_void_tail_recursion(self):
        """
        void 函数的尾递归：call_result 和 return_value 均为 None。
        """
        n = _make_int_var("n")
        proc = _make_function("proc", [n], return_type=PrimitiveDataType.VOID)

        builder = IRBuilder()
        builder.insert(IRFunction(proc))
        builder.insert(IRScopeBegin("proc", StructureType.FUNCTION))
        # void 调用：result=None，return=None
        builder.insert(IRCall(None, proc, {"n": Reference(n)}))
        builder.insert(IRReturn(None))
        builder.insert(IRScopeEnd("proc", StructureType.FUNCTION))

        config = _make_config()
        pass_ = TailCallOptimizationPass(builder, config)
        result = pass_.analyze()
        candidates = result.get("candidates", {})

        self.assertIn("proc", candidates)


class TestTCOPassExecute(unittest.TestCase):
    """测试 execute() 的 IR 变换结果"""

    def _build_ir(self):
        """
        构造标准测试用 IR：

            fn fib(n: int) -> int {
                return fib(n - 1)
            }

        简化：参数直接传 n，不做减法运算（运算结果在上层已折叠为变量）。
        """
        n = _make_int_var("n")
        fib = _make_function("fib", [n])
        result_var = _make_int_var("__tmp")

        builder = IRBuilder()
        builder.insert(IRFunction(fib))
        builder.insert(IRScopeBegin("fib", StructureType.FUNCTION))
        builder.insert(IRCall(result_var, fib, {"n": Reference(n)}))
        builder.insert(IRReturn(Reference(result_var)))
        builder.insert(IRScopeEnd("fib", StructureType.FUNCTION))
        return builder, fib, n

    def test_execute_returns_true_on_tail_recursive(self):
        """execute() 对含尾递归的 IR 应返回 True（表示发生了变更）"""
        builder, _, _ = self._build_ir()
        pass_ = TailCallOptimizationPass(builder, _make_config())
        self.assertTrue(pass_.execute())

    def test_execute_returns_false_on_no_tail_recursion(self):
        """execute() 对无尾递归的 IR 应返回 False"""
        n = _make_int_var("n")
        foo = _make_function("foo", [n])
        builder = IRBuilder()
        builder.insert(IRFunction(foo))
        builder.insert(IRScopeBegin("foo", StructureType.FUNCTION))
        builder.insert(IRReturn(Reference(n)))  # 直接 return，无递归
        builder.insert(IRScopeEnd("foo", StructureType.FUNCTION))

        pass_ = TailCallOptimizationPass(builder, _make_config())
        self.assertFalse(pass_.execute())

    def test_call_replaced_by_assigns(self):
        """变换后，原 IRCall 应消失，替换为 IRAssign"""
        builder, _, _ = self._build_ir()
        pass_ = TailCallOptimizationPass(builder, _make_config())
        pass_.execute()

        opcodes = _opcodes(builder)
        self.assertNotIn(IROpCode.CALL, opcodes)
        self.assertIn(IROpCode.ASSIGN, opcodes)

    def test_return_replaced_by_jump(self):
        """变换后，尾部 IRReturn 应被替换为 IRJump"""
        builder, _, _ = self._build_ir()
        pass_ = TailCallOptimizationPass(builder, _make_config())
        pass_.execute()

        opcodes = _opcodes(builder)
        # RETURN 应该没了（只有尾部那一条，终止条件分支的不在这个 IR 里）
        self.assertNotIn(IROpCode.RETURN, opcodes)
        self.assertIn(IROpCode.JUMP, opcodes)

    def test_tco_scope_inserted(self):
        """变换后，应插入名为 fib__tco_loop 的循环作用域"""
        builder, fib, _ = self._build_ir()
        loop_name = f"{fib.get_name()}{_TCO_SCOPE_SUFFIX}"

        pass_ = TailCallOptimizationPass(builder, _make_config())
        pass_.execute()

        scope_begins = [
            instr for instr in builder.get_instructions()
            if instr.opcode is IROpCode.SCOPE_BEGIN
        ]
        scope_names = [instr.operands[0] for instr in scope_begins]
        self.assertIn(loop_name, scope_names)

    def test_tco_scope_properly_closed(self):
        """TCO 循环作用域的 SCOPE_BEGIN 和 SCOPE_END 数量应相等"""
        builder, _, _ = self._build_ir()
        pass_ = TailCallOptimizationPass(builder, _make_config())
        pass_.execute()

        instructions = builder.get_instructions()
        begins = sum(1 for i in instructions if i.opcode is IROpCode.SCOPE_BEGIN)
        ends = sum(1 for i in instructions if i.opcode is IROpCode.SCOPE_END)
        self.assertEqual(begins, ends)

    def test_jump_target_matches_tco_scope(self):
        """IRJump 的目标作用域名应与插入的 TCO SCOPE_BEGIN 名一致"""
        builder, fib, _ = self._build_ir()
        loop_name = f"{fib.get_name()}{_TCO_SCOPE_SUFFIX}"

        pass_ = TailCallOptimizationPass(builder, _make_config())
        pass_.execute()

        jumps = [
            instr for instr in builder.get_instructions()
            if instr.opcode is IROpCode.JUMP
        ]
        self.assertEqual(len(jumps), 1)
        self.assertEqual(jumps[0].operands[0], loop_name)

    def test_assign_uses_correct_param(self):
        """IRAssign 的目标变量应是函数的形参，而非临时变量"""
        n = _make_int_var("n")
        fib = _make_function("fib", [n])
        result_var = _make_int_var("__tmp")

        builder = IRBuilder()
        builder.insert(IRFunction(fib))
        builder.insert(IRScopeBegin("fib", StructureType.FUNCTION))
        builder.insert(IRCall(result_var, fib, {"n": Reference(n)}))
        builder.insert(IRReturn(Reference(result_var)))
        builder.insert(IRScopeEnd("fib", StructureType.FUNCTION))

        pass_ = TailCallOptimizationPass(builder, _make_config())
        pass_.execute()

        assigns = [
            instr for instr in builder.get_instructions()
            if instr.opcode is IROpCode.ASSIGN
        ]
        self.assertTrue(len(assigns) > 0)
        # 赋值目标应是 n（函数形参），不是 __tmp（临时变量）
        assign_target_name = assigns[0].operands[0].get_name()
        self.assertEqual(assign_target_name, "n")

    def test_idempotent_on_second_run(self):
        """
        Pass 不应重复转换同一函数。
        第二次 execute() 应返回 False（IR 已无尾递归模式）。
        """
        builder, _, _ = self._build_ir()
        config = _make_config()
        pass1 = TailCallOptimizationPass(builder, config)
        pass1.execute()

        # 第二次用同一个 builder 跑
        pass2 = TailCallOptimizationPass(builder, config)
        self.assertFalse(pass2.execute())

    def test_non_recursive_function_untouched(self):
        """
        无递归的函数，execute() 后 IR 结构不变。
        """
        n = _make_int_var("n")
        foo = _make_function("foo", [n])

        builder = IRBuilder()
        builder.insert(IRFunction(foo))
        builder.insert(IRScopeBegin("foo", StructureType.FUNCTION))
        builder.insert(IRReturn(Reference(n)))
        builder.insert(IRScopeEnd("foo", StructureType.FUNCTION))

        original_opcodes = _opcodes(builder).copy()

        pass_ = TailCallOptimizationPass(builder, _make_config())
        pass_.execute()

        self.assertEqual(_opcodes(builder), original_opcodes)


class TestTCOPassEdgeCases(unittest.TestCase):
    """边界情况"""

    def test_empty_builder(self):
        """空 IR 不应崩溃"""
        builder = IRBuilder()
        pass_ = TailCallOptimizationPass(builder, _make_config())
        self.assertFalse(pass_.execute())

    def test_function_with_no_body(self):
        """只有 FUNCTION 指令、没有 SCOPE_BEGIN 的函数不应崩溃"""
        n = _make_int_var("n")
        foo = _make_function("foo", [n])

        builder = IRBuilder()
        builder.insert(IRFunction(foo))
        # 故意不加 SCOPE_BEGIN/END

        pass_ = TailCallOptimizationPass(builder, _make_config())
        self.assertFalse(pass_.execute())

    def test_multiple_functions_only_recursive_transformed(self):
        """
        多个函数中，只有含尾递归的那个应被变换，其他函数 IR 不变。
        """
        n = _make_int_var("n")
        fib = _make_function("fib", [n])
        bar = _make_function("bar", [n])
        result_var = _make_int_var("__tmp")

        builder = IRBuilder()

        # fib：有尾递归
        builder.insert(IRFunction(fib))
        builder.insert(IRScopeBegin("fib", StructureType.FUNCTION))
        builder.insert(IRCall(result_var, fib, {"n": Reference(n)}))
        builder.insert(IRReturn(Reference(result_var)))
        builder.insert(IRScopeEnd("fib", StructureType.FUNCTION))

        # bar：无递归
        builder.insert(IRFunction(bar))
        builder.insert(IRScopeBegin("bar", StructureType.FUNCTION))
        builder.insert(IRReturn(Reference(n)))
        builder.insert(IRScopeEnd("bar", StructureType.FUNCTION))

        pass_ = TailCallOptimizationPass(builder, _make_config())
        pass_.execute()

        # fib 应有 JUMP，bar 对应区域不应有 JUMP
        instructions = builder.get_instructions()
        jumps = [i for i, instr in enumerate(instructions)
                 if instr.opcode is IROpCode.JUMP]

        # 只应有一个 JUMP，且在 fib 的函数体内
        self.assertEqual(len(jumps), 1)


if __name__ == "__main__":
    unittest.main()
