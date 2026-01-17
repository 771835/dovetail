# coding=utf-8
"""
常量折叠 Pass

在编译时计算常量表达式，减少运行时计算开销。
支持控制流敏感的常量传播分析。
"""
from __future__ import annotations

from enum import Enum, auto
from typing import Any, Callable

from attrs import define, field

from transpiler.core.compile_config import CompileConfig
from transpiler.core.enums import OptimizationLevel
from transpiler.core.enums.operations import BinaryOps, CompareOps, UnaryOps
from transpiler.core.enums.types import DataType, StructureType, ValueType
from transpiler.core.instructions import *
from transpiler.core.ir_builder import IRBuilder, IRBuilderIterator
from transpiler.core.optimize.base import IROptimizationPass
from transpiler.core.optimize.pass_metadata import PassMetadata, PassPhase
from transpiler.core.optimize.pass_registry import register_pass
from transpiler.core.symbols import Variable, Constant, Literal, Reference, Function, Class


@register_pass(PassMetadata(
    name="constant_folding",
    display_name="常量折叠",
    description="在编译时计算常量表达式，支持控制流敏感分析",
    level=OptimizationLevel.O1,
    phase=PassPhase.TRANSFORM,
    provided_features=("simplified_arithmetic",)
))
class ConstantFoldingPass(IROptimizationPass):
    """
    常量折叠优化 Pass

    核心策略：
    1. 顺序遍历 IR，维护符号表
    2. 遇到 CONDITIONAL 作用域时，保存当前状态
    3. 在条件分支内使用临时符号表
    4. 遇到 COND_JUMP 时，合并所有分支的状态
    """
    BINARY_OP_HANDLERS: dict[BinaryOps, Callable[[int | bool, int | bool], int | bool]] = {
        BinaryOps.ADD: lambda a, b: a + b,
        BinaryOps.SUB: lambda a, b: a - b,
        BinaryOps.MUL: lambda a, b: a * b,
        BinaryOps.DIV: lambda a, b: a / b,
        BinaryOps.MOD: lambda a, b: a % b,
        BinaryOps.MIN: lambda a, b: min(a, b),
        BinaryOps.MAX: lambda a, b: max(a, b),
        BinaryOps.BIT_AND: lambda a, b: a & b,
        BinaryOps.BIT_OR: lambda a, b: a | b,
        BinaryOps.BIT_XOR: lambda a, b: a ^ b,
        BinaryOps.SHL: lambda a, b: a << b,
        BinaryOps.SHR: lambda a, b: a >> b,
    }

    COMPARE_OP_HANDLERS: dict[CompareOps, Callable[[int | bool, int | bool], bool]] = {
        CompareOps.EQ: lambda a, b: a == b,
        CompareOps.NE: lambda a, b: a != b,
        CompareOps.GE: lambda a, b: a >= b,
        CompareOps.GT: lambda a, b: a > b,
        CompareOps.LE: lambda a, b: a <= b,
        CompareOps.LT: lambda a, b: a < b,

    }

    UNARY_OP_HANDLERS: dict[UnaryOps, Callable[[int | bool], int]] = {
        UnaryOps.NEG: lambda a: -a,
        UnaryOps.NOT: lambda a: not a,
        UnaryOps.BIT_NOT: lambda a: ~a,
    }

    class FoldingFlags(Enum):
        """常量折叠标志"""
        UNKNOWN = auto()  # 未知/无法追踪变量
        UNDEFINED = auto()  # 未定义的变量

    @define(slots=True)
    class SymbolTable:
        """
        支持父-子结构的符号表。
        在当前作用域及其祖先作用域中查找符号。
        """
        name: str = field()
        stype: StructureType = field()
        table: dict[str, Reference | ConstantFoldingPass.FoldingFlags] = field(factory=dict)
        parent: "ConstantFoldingPass.SymbolTable | None" = field(default=None)

        def find(self, name: str) -> Reference | ConstantFoldingPass.FoldingFlags:
            """在当前作用域及其祖先作用域中查找符号"""
            if name in self.table:
                return self.table[name]

            if self.parent is not None:
                return self.parent.find(name)

            return ConstantFoldingPass.FoldingFlags.UNDEFINED

        def set(self, name: str, value: Reference | ConstantFoldingPass.FoldingFlags) -> None:
            """在当前作用域设置符号"""
            self.table[name] = value

        def copy_state(self) -> dict[str, Reference | ConstantFoldingPass.FoldingFlags]:
            """复制当前符号表状态（包括父级）"""
            state = {}
            current = self
            while current:
                state.update(current.table)
                current = current.parent
            return state

    def __init__(self, builder: IRBuilder, config: CompileConfig):
        super().__init__(builder, config)
        self.global_table = self.SymbolTable("global", StructureType.GLOBAL)
        self.current_table: ConstantFoldingPass.SymbolTable = self.global_table

        # 控制流分析相关
        self.pending_branches: dict[str, list[dict]] = {}  # 等待处理的分支: {jump_target: [branch_states]}
        self.branch_base_state: dict[str, dict] = {}  # 分支开始前的状态

    def execute(self) -> bool:
        """执行常量折叠优化"""
        self.changed = False
        # 预扫描，识别条件分支结构
        self._prescan_branches()

        # 第二步：执行常量折叠
        self._perform_folding()

        return self.changed

    def _prescan_branches(self):
        """预扫描，识别所有条件分支及其父作用域"""
        self.conditional_branches = {}  # {branch_name: parent_scope}
        self.branch_groups = {}  # {parent_scope: [branch1, branch2]}

        scope_stack = []

        for instr in self.builder.get_instructions():
            if isinstance(instr, IRScopeBegin):
                scope_name = instr.get_operands()[0]
                scope_type = instr.get_operands()[1]

                if scope_type == StructureType.CONDITIONAL:
                    parent = scope_stack[-1] if scope_stack else "global"
                    self.conditional_branches[scope_name] = parent

                    if parent not in self.branch_groups:
                        self.branch_groups[parent] = []
                    self.branch_groups[parent].append(scope_name)

                scope_stack.append(scope_name)

            elif isinstance(instr, IRScopeEnd):
                if scope_stack:
                    scope_stack.pop()

    def _perform_folding(self):
        """执行常量折叠"""
        iterator = self.builder.__iter__()
        instruction_handlers = {
            IROpCode.SCOPE_BEGIN: self._handle_scope_begin,
            IROpCode.SCOPE_END: self._handle_scope_end,
            IROpCode.ASSIGN: self._assign,
            IROpCode.DECLARE: self._declare,
            IROpCode.BINARY_OP: self._op,
            IROpCode.COMPARE: self._compare,
            IROpCode.UNARY_OP: self._unary_op,
            IROpCode.COND_JUMP: self._cond_jump,
            IROpCode.CALL: self._call,
            IROpCode.CAST: self._cast,
            IROpCode.FUNCTION: self._function
        }

        # ✅ 跟踪当前所在的作用域路径
        self.scope_path = []

        while True:
            try:
                instr = next(iterator)
            except StopIteration:
                break

            handler = instruction_handlers.get(instr.opcode)
            if handler:
                if handler(iterator, instr):  # NOQA
                    self._changed = True

    def _find(self, name: Variable | Literal | Constant | Reference) -> Reference[Literal] | FoldingFlags:
        """从符号表搜索符号的最终值"""
        if isinstance(name, Literal):
            return Reference(ValueType.LITERAL, name)
        if isinstance(name, Reference) and name.value_type == ValueType.LITERAL:
            return name

        # 在 loop_check 中查找任何变量都应视为 UNKNOWN
        current_scope = self.current_table
        while current_scope:
            if current_scope.stype == StructureType.LOOP_CHECK:
                return ConstantFoldingPass.FoldingFlags.UNKNOWN
            current_scope = current_scope.parent

        value = self.current_table.find(name.get_name())
        if value == ConstantFoldingPass.FoldingFlags.UNKNOWN:
            return value
        elif value == ConstantFoldingPass.FoldingFlags.UNDEFINED:
            return value
        elif value.value_type == ValueType.LITERAL:
            return value
        elif value.value_type == ValueType.FUNCTION:
            return value
        elif value.value_type in (ValueType.VARIABLE, ValueType.CONSTANT):
            return self._find(value)
        else:
            return ConstantFoldingPass.FoldingFlags.UNKNOWN

    def _resolve_ref(
            self,
            ref: Reference[Variable | Constant | Literal]
    ) -> Reference[Literal] | FoldingFlags:
        """解析引用到字面量或标识为未知/未定义"""
        if ref.value_type == ValueType.LITERAL:
            return ref
        else:
            return self._find(ref)

    @staticmethod
    def _is_literal(ref: Reference[Literal] | FoldingFlags) -> bool:
        """判断是否为字面量"""
        return (
                not isinstance(ref, ConstantFoldingPass.FoldingFlags) and
                ref.value_type == ValueType.LITERAL
        )

    def _handle_scope_begin(self, iterator: IRBuilderIterator, instr: IRScopeBegin) -> bool:
        """处理作用域开始"""
        scope_name = instr.get_operands()[0]
        scope_type = instr.get_operands()[1]

        self.scope_path.append(scope_name)

        # ✅ 如果是条件分支
        if scope_type == StructureType.CONDITIONAL:
            parent_scope = self.conditional_branches.get(scope_name)

            # 第一次遇到这个父作用域的条件分支
            if parent_scope and parent_scope not in self.branch_base_state:
                # 保存当前符号表状态
                self.branch_base_state[parent_scope] = self.current_table.copy_state()

            # ✅ 从基础状态创建新的符号表
            if parent_scope and parent_scope in self.branch_base_state:
                base_state = self.branch_base_state[parent_scope]
                new_table = ConstantFoldingPass.SymbolTable(
                    scope_name,
                    scope_type,
                    parent=self.current_table.parent
                )
                # 恢复基础状态到新表
                for var_name, value in base_state.items():
                    new_table.set(var_name, value)

                self.current_table = new_table
                return False

        # 普通作用域
        new_table = ConstantFoldingPass.SymbolTable(
            scope_name,
            scope_type,
            parent=self.current_table
        )
        self.current_table = new_table
        return False

    def _handle_scope_end(self, iterator: IRBuilderIterator, instr: IRScopeEnd) -> bool:
        """处理作用域结束"""
        scope_name = self.current_table.name
        scope_type = self.current_table.stype

        # ✅ 如果是条件分支结束，保存完整状态
        if scope_type == StructureType.CONDITIONAL:
            full_state = {}
            current = self.current_table
            while current:
                for var_name, value in current.table.items():
                    if var_name not in full_state:
                        full_state[var_name] = value
                current = current.parent

            if scope_name not in self.pending_branches:
                self.pending_branches[scope_name] = []
            self.pending_branches[scope_name].append(full_state)

        if self.current_table.parent is not None:
            self.current_table = self.current_table.parent

        if self.scope_path:
            self.scope_path.pop()

        return False

    def _declare(self, iterator: IRBuilderIterator, instr: IRDeclare) -> bool:
        """处理变量声明"""
        var: Variable = instr.get_operands()[0]
        self.current_table.set(var.get_name(), ConstantFoldingPass.FoldingFlags.UNKNOWN)
        return False

    def _assign(self, iterator: IRBuilderIterator, instr: IRAssign) -> bool:
        """处理赋值指令"""
        target: Variable = instr.get_operands()[0]
        source_ref: Reference[Variable | Constant | Literal] = instr.get_operands()[1]

        resolved_source = source_ref
        changed = False

        if source_ref.value_type in (ValueType.VARIABLE, ValueType.CONSTANT):
            new_source = self._resolve_ref(source_ref)
            if isinstance(new_source, ConstantFoldingPass.FoldingFlags):
                pass
            elif new_source.value_type == ValueType.LITERAL:
                new_instr = IRAssign(target, new_source)
                iterator.set_current(new_instr)
                resolved_source = new_source
                changed = True

        self.current_table.set(target.get_name(), resolved_source)
        return changed

    def _op(self, iterator: IRBuilderIterator, instr: IRBinaryOp) -> bool:
        """处理二元运算"""
        result: Variable = instr.get_operands()[0]
        op: BinaryOps = instr.get_operands()[1]
        left_ref: Reference[Variable | Constant | Literal] = instr.get_operands()[2]
        right_ref: Reference[Variable | Constant | Literal] = instr.get_operands()[3]

        self.current_table.set(result.get_name(), ConstantFoldingPass.FoldingFlags.UNKNOWN)

        left = self._resolve_ref(left_ref)
        right = self._resolve_ref(right_ref)

        # 两边任意一方非常量跳过
        if not self._is_literal(left) or not self._is_literal(right):
            return False

        left_dtype = left.get_data_type()
        right_dtype = right.get_data_type()

        # 两边有任意一方非基本类型跳过
        if not isinstance(left_dtype, DataType) or not isinstance(right_dtype, DataType):
            return False

        if op == BinaryOps.ADD and (left_dtype == DataType.STRING or right_dtype == DataType.STRING):
            new_value = str(left.value.value) + str(right.value.value)
        else:
            new_value = int(self.BINARY_OP_HANDLERS[op](left.value.value, right.value.value))

        try:
            # 用新指令替换原始指令
            new_instr = IRAssign(result, Reference.literal(new_value))
            iterator.set_current(new_instr)
            self._assign(iterator, new_instr)
            return True
        except (TypeError, ValueError, ZeroDivisionError):
            return False

    def _compare(self, iterator: IRBuilderIterator, instr: IRCompare) -> bool:
        """处理比较运算"""
        result: Variable = instr.get_operands()[0]
        op: CompareOps = instr.get_operands()[1]
        left_ref: Reference[Variable | Constant | Literal] = instr.get_operands()[2]
        right_ref: Reference[Variable | Constant | Literal] = instr.get_operands()[3]

        self.current_table.set(result.get_name(), ConstantFoldingPass.FoldingFlags.UNKNOWN)

        left = self._resolve_ref(left_ref)
        right = self._resolve_ref(right_ref)

        # 两边任意一方非常量跳过
        if not self._is_literal(left) or not self._is_literal(right):
            return False

        left_dtype = left.get_data_type()
        right_dtype = right.get_data_type()

        # 两边有任意一方非基本类型跳过
        if not isinstance(left_dtype, DataType) or not isinstance(right_dtype, DataType):
            return False

        new_value = self.COMPARE_OP_HANDLERS[op](left.value.value, right.value.value)
        try:
            new_instr = IRAssign(result, Reference.literal(new_value))
            iterator.set_current(new_instr)
            self._assign(iterator, new_instr)
            return True
        except (TypeError, ValueError):
            return False

    def _unary_op(self, iterator: IRBuilderIterator, instr: IRUnaryOp) -> bool:
        """处理一元运算"""
        result: Variable = instr.get_operands()[0]
        op: UnaryOps = instr.get_operands()[1]
        operand_ref: Reference[Variable | Constant | Literal] = instr.get_operands()[2]

        self.current_table.set(result.get_name(), ConstantFoldingPass.FoldingFlags.UNKNOWN)

        operand = self._resolve_ref(operand_ref)
        if not self._is_literal(operand) or not isinstance(operand.get_data_type(), DataType):
            return False

        try:
            folded_value = self.UNARY_OP_HANDLERS[op](operand.value.value)
            new_instr = IRAssign(result, Reference.literal(folded_value))
            iterator.set_current(new_instr)
            self._assign(iterator, new_instr)
            return True
        except (TypeError, ValueError):
            return False

    def _cond_jump(self, iterator: IRBuilderIterator, instr: IRCondJump) -> bool:
        """
        处理条件跳转

        关键：此时所有分支已经"执行"完毕，需要合并状态
        """
        cond_var: Variable | Literal = instr.get_operands()[0]
        true_scope: str = instr.get_operands()[1]
        false_scope: str = instr.get_operands()[2]

        # 1. 先尝试优化条件本身
        changed = False

        if isinstance(cond_var, Variable):
            value = self._find(cond_var)

            if not isinstance(value, ConstantFoldingPass.FoldingFlags):
                if cond_var.dtype in (DataType.INT, DataType.BOOLEAN):
                    if isinstance(value, Reference) and value.value_type == ValueType.LITERAL:
                        cond_val = bool(value.value.value)
                        jump_scope = true_scope if cond_val else false_scope

                        # ✅ 条件是常量，选择对应分支的状态
                        selected_state = self.pending_branches.get(jump_scope, [{}])[
                            0] if jump_scope in self.pending_branches else {}

                        # 将选中分支的状态应用到当前符号表
                        for var_name, val in selected_state.items():
                            self.current_table.set(var_name, val)

                        # 替换为直接跳转
                        if jump_scope:
                            iterator.set_current(IRJump(jump_scope))
                        else:
                            iterator.remove_current()

                        # 清理
                        self.pending_branches.pop(true_scope, None)
                        self.pending_branches.pop(false_scope, None)
                        self.branch_base_state.pop(self.conditional_branches.get(true_scope), None)
                        self.branch_base_state.pop(self.conditional_branches.get(false_scope), None)

                        return True

        elif isinstance(cond_var, Literal):
            cond_val = bool(cond_var.value)
            jump_scope = true_scope if cond_val else false_scope

            # ✅ 条件是字面量，选择对应分支的状态
            selected_state = self.pending_branches.get(jump_scope, [{}])[
                0] if jump_scope in self.pending_branches else {}

            # 将选中分支的状态应用到当前符号表
            for var_name, val in selected_state.items():
                self.current_table.set(var_name, val)

            # 替换为直接跳转
            if jump_scope:
                iterator.set_current(IRJump(jump_scope))
            else:
                iterator.remove_current()

            # 清理
            self.pending_branches.pop(true_scope, None)
            self.pending_branches.pop(false_scope, None)
            self.branch_base_state.pop(self.conditional_branches.get(true_scope), None)
            self.branch_base_state.pop(self.conditional_branches.get(false_scope), None)

            return True

        # 2. 条件不确定，合并两个分支的完整状态
        true_state = self.pending_branches.get(true_scope, [{}])[0] if true_scope in self.pending_branches else {}
        false_state = self.pending_branches.get(false_scope, [{}])[0] if false_scope in self.pending_branches else {}

        # ✅ 找出所有变量（两个完整状态的并集）
        all_vars = set(true_state.keys()) | set(false_state.keys())

        for var_name in all_vars:
            true_val = true_state.get(var_name, self.FoldingFlags.UNKNOWN)
            false_val = false_state.get(var_name, self.FoldingFlags.UNKNOWN)

            # 如果两个分支的值相同，使用该值
            if self._values_equal(true_val, false_val):
                self.current_table.set(var_name, true_val)
            else:
                # 值不同，标记为 UNKNOWN
                self.current_table.set(var_name, self.FoldingFlags.UNKNOWN)

        # 清理已处理的分支
        self.pending_branches.pop(true_scope, None)
        self.pending_branches.pop(false_scope, None)

        # 清理基础状态（从 conditional_branches 中查找父作用域）
        parent_scope = self.conditional_branches.get(true_scope)
        if parent_scope:
            self.branch_base_state.pop(parent_scope, None)

        return changed

    def _values_equal(self, v1: Any, v2: Any) -> bool:
        """比较两个值是否相等"""
        if isinstance(v1, self.FoldingFlags) or isinstance(v2, self.FoldingFlags):
            return v1 == v2

        if not isinstance(v1, Reference) or not isinstance(v2, Reference):
            return False

        if v1.value_type != v2.value_type:
            return False

        if v1.value_type == ValueType.LITERAL:
            return v1.value.value == v2.value.value

        if v1.value_type in (ValueType.VARIABLE, ValueType.CONSTANT):
            return v1.get_name() == v2.get_name()

        return False

    def _call(self, iterator: IRBuilderIterator, instr: IRCall) -> bool:
        """处理函数调用，优化参数"""
        result: Variable | Constant = instr.get_operands()[0]
        func: Function = instr.get_operands()[1]
        args: dict[str, Reference[Variable | Constant | Literal]] = instr.get_operands()[2]

        new_args: dict[str, Reference[Variable | Constant | Literal]] = {}
        changed = False

        for param_name, arg_ref in args.items():
            if arg_ref.value_type == ValueType.LITERAL:
                new_args[param_name] = arg_ref
                continue

            if arg_ref.value_type in (ValueType.VARIABLE, ValueType.CONSTANT):
                arg_value = self._find(arg_ref.value)
                if isinstance(arg_value, ConstantFoldingPass.FoldingFlags):
                    new_args[param_name] = arg_ref
                else:
                    new_args[param_name] = arg_value
                    changed = True
            else:
                new_args[param_name] = arg_ref

        if changed:
            iterator.set_current(IRCall(result, func, new_args))

        return changed

    def _cast(self, iterator: IRBuilderIterator, instr: IRCast) -> bool:
        """处理类型转换"""
        result: Variable | Constant = instr.get_operands()[0]
        dtype: DataType | Class = instr.get_operands()[1]
        value_ref: Reference[Variable | Constant | Literal] = instr.get_operands()[2]

        self.current_table.set(result.get_name(), ConstantFoldingPass.FoldingFlags.UNKNOWN)

        value = self._resolve_ref(value_ref)
        if isinstance(value, ConstantFoldingPass.FoldingFlags):
            return False

        if isinstance(value, Reference) and value.value_type == ValueType.LITERAL:
            if dtype == value.get_data_type():
                new_assign = IRAssign(result, value)
                iterator.set_current(new_assign)
                self._assign(iterator, new_assign)
                return True

            if dtype == DataType.STRING and value.get_data_type() in (DataType.INT, DataType.BOOLEAN):
                str_val = str(int(value.value.value))
                str_literal_ref = Reference.literal(str_val)
                new_assign = IRAssign(result, str_literal_ref)
                iterator.set_current(new_assign)
                self._assign(iterator, new_assign)
                return True

        return False

    def _function(self, iterator: IRBuilderIterator, instr: IRFunction) -> bool:
        """处理函数定义"""
        function: Function = instr.get_operands()[0]
        self.current_table.set(function.get_name(), Reference(ValueType.FUNCTION, function))
        return False
