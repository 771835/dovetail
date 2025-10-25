# coding=utf-8
from __future__ import annotations

import copy
from collections import deque
from enum import Enum, auto
from itertools import count

from attrs import define, field, validators

from transpiler.core import registry
from transpiler.core.enums import ValueType, VariableType, DataTypeBase, DataType, BinaryOps, StructureType, UnaryOps, \
    CompareOps
from transpiler.core.generator_config import GeneratorConfig, OptimizationLevel
from transpiler.core.instructions import *
from transpiler.core.ir_builder import IRBuilder, IRBuilderIterator
from transpiler.core.specification import IROptimizerSpec, \
    IROptimizationPass
from transpiler.core.symbols import Variable, Reference, Constant, Literal, Function, Class


class Optimizer(IROptimizerSpec):

    def __init__(self, builder: IRBuilder, config: GeneratorConfig):
        self.config = config
        self.debug = config.debug
        self.level = config.optimization_level
        self.initial_builder = builder
        self.builder = copy.deepcopy(builder)  # 防止修改初始状态

    def optimize(self) -> IRBuilder:
        # 存储启用的优化通道
        optimization_pass: list[type[IROptimizationPass]] = []
        if self.level == OptimizationLevel.O0:
            return self.builder
        if self.level >= OptimizationLevel.O1:
            optimization_pass.append(ConstantFoldingPass)
            optimization_pass.append(DeadCodeEliminationPass)
            optimization_pass.append(DeclareCleanupPass)
            optimization_pass.append(UnreachableCodeRemovalPass)
            optimization_pass.append(UnusedFunctionEliminationPass)
            optimization_pass.extend(registry.optimization_pass.get(OptimizationLevel.O1, []))
        if self.level >= OptimizationLevel.O2:
            optimization_pass.append(UselessScopeRemovalPass)
            optimization_pass.extend(registry.optimization_pass.get(OptimizationLevel.O2, []))
        if self.level >= OptimizationLevel.O3:
            optimization_pass.extend(registry.optimization_pass.get(OptimizationLevel.O3, []))

        last_hash = hash(tuple(self.builder.get_instructions()))
        iteration = count()
        while True:

            if self.debug:
                print(f"[DEBUG: Optimizer] Optimization iteration {next(iteration)} started.")

            for _ in optimization_pass:
                if self.debug:
                    depth = 0
                    for i in self.builder:
                        if isinstance(i, IRScopeEnd):
                            depth -= 1
                        print(depth * "    " + repr(i))
                        if isinstance(i, IRScopeBegin):
                            depth += 1
                    print(f"[DEBUG: {_.__name__}] Starting optimization pass...")
                pass_ = _(self.builder, self.config)
                pass_.exec()
                if self.debug:
                    print(f"[DEBUG: {_.__name__}] Complete optimization pass...")

            now_hash = hash(tuple(self.builder.get_instructions()))
            if now_hash != last_hash:
                last_hash = now_hash
            else:
                break

        return self.builder


class ConstantFoldingPass(IROptimizationPass):
    BINARY_OP_HANDLERS: dict[BinaryOps, dict[tuple[DataTypeBase, DataTypeBase], ...]] = {
        BinaryOps.ADD: {
            (DataType.INT, DataType.INT): lambda a, b: a + b,
            (DataType.STRING, DataType.STRING): lambda a, b: a + b,
            (DataType.STRING, DataType.INT): lambda a, b: a + str(b),
            (DataType.BOOLEAN, DataType.INT): lambda a, b: int(a) + b,
            (DataType.INT, DataType.BOOLEAN): lambda a, b: a + int(b),
            (DataType.BOOLEAN, DataType.BOOLEAN): lambda a, b: int(a) + int(b)
        },
        BinaryOps.SUB: {
            (DataType.INT, DataType.INT): lambda a, b: a - b,
            (DataType.BOOLEAN, DataType.INT): lambda a, b: int(a) - b,
            (DataType.INT, DataType.BOOLEAN): lambda a, b: a - int(b),
            (DataType.BOOLEAN, DataType.BOOLEAN): lambda a, b: int(a) - int(b)
        },
        BinaryOps.MUL: {
            (DataType.INT, DataType.INT): lambda a, b: a * b,
            (DataType.BOOLEAN, DataType.INT): lambda a, b: int(a) * b,
            (DataType.INT, DataType.BOOLEAN): lambda a, b: a * int(b),
            (DataType.BOOLEAN, DataType.BOOLEAN): lambda a, b: int(a) * int(b)
        },
        BinaryOps.DIV: {
            (DataType.INT, DataType.INT): lambda a, b: a / b,
            (DataType.BOOLEAN, DataType.INT): lambda a, b: int(a) / b,
            (DataType.INT, DataType.BOOLEAN): lambda a, b: a / int(b),
            (DataType.BOOLEAN, DataType.BOOLEAN): lambda a, b: int(a) / int(b)
        },
        BinaryOps.MOD: {
            (DataType.INT, DataType.INT): lambda a, b: a % b,
            (DataType.BOOLEAN, DataType.INT): lambda a, b: int(a) % b,
            (DataType.INT, DataType.BOOLEAN): lambda a, b: a % int(b),
            (DataType.BOOLEAN, DataType.BOOLEAN): lambda a, b: int(a) % int(b)
        },
        BinaryOps.MIN: {
            (DataType.INT, DataType.INT): lambda a, b: min(a, b),
            (DataType.BOOLEAN, DataType.INT): lambda a, b: min(int(a), b),
            (DataType.INT, DataType.BOOLEAN): lambda a, b: min(a, int(b)),
            (DataType.BOOLEAN, DataType.BOOLEAN): lambda a, b: min(int(a), int(b))
        },
        BinaryOps.MAX: {
            (DataType.INT, DataType.INT): lambda a, b: max(a, b),
            (DataType.BOOLEAN, DataType.INT): lambda a, b: max(int(a), b),
            (DataType.INT, DataType.BOOLEAN): lambda a, b: max(a, int(b)),
            (DataType.BOOLEAN, DataType.BOOLEAN): lambda a, b: max(int(a), int(b))
        },
        BinaryOps.BIT_AND: {
            (DataType.INT, DataType.INT): lambda a, b: a & b,
            (DataType.BOOLEAN, DataType.INT): lambda a, b: int(a) & b,
            (DataType.INT, DataType.BOOLEAN): lambda a, b: a & int(b),
            (DataType.BOOLEAN, DataType.BOOLEAN): lambda a, b: int(a) & int(b)
        },
        BinaryOps.BIT_OR: {
            (DataType.INT, DataType.INT): lambda a, b: a | b,
            (DataType.BOOLEAN, DataType.INT): lambda a, b: int(a) | b,
            (DataType.INT, DataType.BOOLEAN): lambda a, b: a | int(b),
            (DataType.BOOLEAN, DataType.BOOLEAN): lambda a, b: int(a) | int(b)
        },
        BinaryOps.BIT_XOR: {
            (DataType.INT, DataType.INT): lambda a, b: a ^ b,
            (DataType.BOOLEAN, DataType.INT): lambda a, b: int(a) ^ b,
            (DataType.INT, DataType.BOOLEAN): lambda a, b: a ^ int(b),
            (DataType.BOOLEAN, DataType.BOOLEAN): lambda a, b: int(a) ^ int(b)
        },
        BinaryOps.SHL: {
            (DataType.INT, DataType.INT): lambda a, b: a << b,
            (DataType.BOOLEAN, DataType.INT): lambda a, b: int(a) << b,
            (DataType.INT, DataType.BOOLEAN): lambda a, b: a << int(b),
            (DataType.BOOLEAN, DataType.BOOLEAN): lambda a, b: int(a) << int(b)
        },
        BinaryOps.SHR: {
            (DataType.INT, DataType.INT): lambda a, b: a >> b,
            (DataType.BOOLEAN, DataType.INT): lambda a, b: int(a) >> b,
            (DataType.INT, DataType.BOOLEAN): lambda a, b: a >> int(b),
            (DataType.BOOLEAN, DataType.BOOLEAN): lambda a, b: int(a) >> int(b)
        }
    }
    COMPARE_OP_HANDLERS: dict[CompareOps, dict[tuple[DataTypeBase, DataTypeBase], ...]] = {
        CompareOps.EQ: {
            (DataType.INT, DataType.INT): lambda a, b: a == b,
            (DataType.STRING, DataType.STRING): lambda a, b: a == b,
            (DataType.BOOLEAN, DataType.INT): lambda a, b: int(a) == b,
            (DataType.INT, DataType.BOOLEAN): lambda a, b: a == int(b),
            (DataType.BOOLEAN, DataType.BOOLEAN): lambda a, b: a == b
        },
        CompareOps.NE: {
            (DataType.INT, DataType.INT): lambda a, b: a != b,
            (DataType.STRING, DataType.STRING): lambda a, b: a != b,
            (DataType.BOOLEAN, DataType.INT): lambda a, b: int(a) != b,
            (DataType.INT, DataType.BOOLEAN): lambda a, b: a != int(b),
            (DataType.BOOLEAN, DataType.BOOLEAN): lambda a, b: a != b
        },
        CompareOps.LT: {
            (DataType.INT, DataType.INT): lambda a, b: a < b,
            (DataType.BOOLEAN, DataType.INT): lambda a, b: int(a) < b,
            (DataType.INT, DataType.BOOLEAN): lambda a, b: a < int(b),
            (DataType.BOOLEAN, DataType.BOOLEAN): lambda a, b: int(a) < int(b)
        },
        CompareOps.LE: {
            (DataType.INT, DataType.INT): lambda a, b: a <= b,
            (DataType.BOOLEAN, DataType.INT): lambda a, b: int(a) <= b,
            (DataType.INT, DataType.BOOLEAN): lambda a, b: a <= int(b),
            (DataType.BOOLEAN, DataType.BOOLEAN): lambda a, b: int(a) <= int(b)
        },
        CompareOps.GT: {
            (DataType.INT, DataType.INT): lambda a, b: a > b,
            (DataType.BOOLEAN, DataType.INT): lambda a, b: int(a) > b,
            (DataType.INT, DataType.BOOLEAN): lambda a, b: a > int(b),
            (DataType.BOOLEAN, DataType.BOOLEAN): lambda a, b: int(a) > int(b)
        },
        CompareOps.GE: {
            (DataType.INT, DataType.INT): lambda a, b: a >= b,
            (DataType.BOOLEAN, DataType.INT): lambda a, b: int(a) >= b,
            (DataType.INT, DataType.BOOLEAN): lambda a, b: a >= int(b),
            (DataType.BOOLEAN, DataType.BOOLEAN): lambda a, b: int(a) >= int(b)
        },
    }
    UNARY_OP_HANDLERS: dict[UnaryOps, dict[DataTypeBase, ...]] = {
        UnaryOps.NEG: {
            DataType.INT: lambda a: -a,
            DataType.BOOLEAN: lambda a: -int(a),
        },
        UnaryOps.NOT: {
            DataType.INT: lambda a: not a,
            DataType.BOOLEAN: lambda a: not a,
        },
        UnaryOps.BIT_NOT: {
            DataType.INT: lambda a: ~a,
            DataType.BOOLEAN: lambda a: ~int(a),
        },
    }

    class FoldingFlags(Enum):
        UNKNOWN = auto()  # 未知/无法追踪变量
        UNDEFINED = auto()  # 未定义的变量

    @define(slots=True)
    class SymbolTable:
        """
        支持父-子结构的符号表。
        在当前作用域及其祖先作用域中查找符号。
        """
        name: str = field(validator=validators.instance_of(str))
        stype: StructureType = field(validator=validators.instance_of(StructureType))
        table: dict[str, Reference | ConstantFoldingPass.FoldingFlags] = field(factory=dict)
        parent: ConstantFoldingPass.SymbolTable | None = field(default=None)

        def find(self, name: str) -> Reference | ConstantFoldingPass.FoldingFlags:
            """在当前作用域及其祖先作用域中查找符号"""
            # 先在当前作用域查找
            if name in self.table:
                # 需要特别注意：如果当前作用域的值是 UNKNOWN/UNDEFINED，不应该继续向上查
                # 它代表在这个作用域内这个变量的状态。
                # 但是，如果当前作用域是 LOOP_CHECK，应该标记为 UNKNOWN 并返回。
                # 当前实现，table 中保存的值即为最终状态。
                return self.table[name]

            # 如果没找到，向上级查找
            if self.parent is not None:
                return self.parent.find(name)

            # 找不到
            return ConstantFoldingPass.FoldingFlags.UNDEFINED

        def set(self, name: str, value: Reference | ConstantFoldingPass.FoldingFlags):
            """在当前作用域设置符号"""
            self.table[name] = value

        def add(self, name: str, value: Reference | ConstantFoldingPass.FoldingFlags):
            """同 set"""
            self.set(name, value)

    def __init__(self, builder: IRBuilder, config: GeneratorConfig):
        self.builder = builder
        # 根符号表，等价于 GLOBAL_SCOPE
        self.global_table = ConstantFoldingPass.SymbolTable("global", StructureType.GLOBAL)
        # 当前作用域的符号表。这是一个栈的概念，但用链表（parent）实现更自然。
        # current_table 始终指向当前正在处理的最内层作用域的符号表。
        self.current_table: ConstantFoldingPass.SymbolTable = self.global_table

    def exec(self):
        """执行常量折叠优化"""
        iterator = self.builder.__iter__()
        instruction_handlers = {
            IROpCode.SCOPE_BEGIN: self._handle_scope_begin,
            IROpCode.SCOPE_END: self._handle_scope_end,
            IROpCode.ASSIGN: self._assign,
            IROpCode.DECLARE: self._declare,
            IROpCode.OP: self._op,
            IROpCode.COMPARE: self._compare,
            IROpCode.UNARY_OP: self._unary_op,
            IROpCode.COND_JUMP: self._cond_jump,
            IROpCode.CALL: self._call,
            IROpCode.CAST: self._cast,
            IROpCode.FUNCTION: self._function
        }
        while True:
            try:
                instr: IRInstruction = next(iterator)
            except StopIteration:
                break

            handler = instruction_handlers.get(instr.opcode)
            if handler:
                handler(iterator, instr)  # NOQA

    def _find(self, name: Variable | Literal | Constant | Reference) -> Reference[Literal] | FoldingFlags:
        """
        从符号表搜索符号的最终值
        :param name: 符号名称
        :return: 符号的最终值
        """
        # 如果是字面量，直接返回
        if isinstance(name, Literal):
            return Reference(ValueType.LITERAL, name)
        # 如果是字面量的引用，直接返回
        if isinstance(name, Reference) and name.value_type == ValueType.LITERAL:
            return name

        # 在 loop_check 中查找任何变量都应视为 UNKNOWN
        # 这可以通过检查 current_table 链来实现
        current_scope = self.current_table
        while current_scope:
            if current_scope.stype == StructureType.LOOP_CHECK:
                return ConstantFoldingPass.FoldingFlags.UNKNOWN
            current_scope = current_scope.parent

        # 否则，从符号表中查找
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
            # 递归解析引用链
            return self._find(value)
        else:
            return ConstantFoldingPass.FoldingFlags.UNKNOWN

    def _resolve_ref(
            self,
            ref: Reference[Variable | Constant | Literal]
    ) -> Reference[Literal] | ConstantFoldingPass.FoldingFlags:
        """解析引用到字面量或标识为未知/未定义"""
        if ref.value_type == ValueType.LITERAL:
            return ref
        else:
            return self._find(ref)

    @staticmethod
    def _is_literal(ref: Reference[Literal] | ConstantFoldingPass.FoldingFlags):
        return False if isinstance(ref, ConstantFoldingPass.FoldingFlags) else ref.value_type == ValueType.LITERAL

    def _handle_scope_end(self, iterator: IRBuilderIterator, instr: IRScopeEnd):
        """处理作用域结束"""
        if self.current_table.parent is not None:
            self.current_table = self.current_table.parent

    def _handle_scope_begin(self, iterator: IRBuilderIterator, instr: IRScopeBegin):
        """处理作用域开始"""
        # 为新的作用域创建新的符号表实例，其父是当前作用域
        new_table = ConstantFoldingPass.SymbolTable(instr.get_operands()[0], instr.get_operands()[1],
                                                    parent=self.current_table)
        self.current_table = new_table

    def _declare(self, iterator: IRBuilderIterator, instr: IRDeclare):
        var: Variable = instr.get_operands()[0]
        # 在当前作用域中声明变量，初始值为 UNKNOWN
        self.current_table.set(var.get_name(), ConstantFoldingPass.FoldingFlags.UNKNOWN)

    def _assign(self, iterator: IRBuilderIterator, instr: IRAssign) -> None:
        target: Variable = instr.get_operands()[0]
        source_ref: Reference[Variable | Constant | Literal] = instr.get_operands()[1]

        resolved_source = source_ref
        # 尝试解析源引用，看能否优化它
        if source_ref.value_type in (ValueType.VARIABLE, ValueType.CONSTANT):
            new_source = self._resolve_ref(source_ref)
            # 如果不能解析或者解析到 UNKNOWN/UNDEFINED，保留原始引用
            if isinstance(new_source, ConstantFoldingPass.FoldingFlags):
                # 无法解析，保持原样
                pass
            elif new_source.value_type == ValueType.LITERAL:
                # 解析成功，用常量值替换新指令中的 source
                new_instr = IRAssign(target, new_source)
                iterator.set_current(new_instr)
                resolved_source = new_source
            # 解析成其它(比如 FUNCTION)，也保留原始引用，不替换。
        # 不管有没有替换指令，都把目标变量在符号表中的值更新
        self.current_table.set(target.get_name(), resolved_source)

    def _op(self, iterator: IRBuilderIterator, instr: IROp):
        result: Variable = instr.get_operands()[0]
        op: BinaryOps = instr.get_operands()[1]
        left_ref: Reference[Variable | Constant | Literal] = instr.get_operands()[2]
        right_ref: Reference[Variable | Constant | Literal] = instr.get_operands()[3]

        # 初始假设无法折叠，先把结果设为 UNKNOWN
        self.current_table.set(result.get_name(), ConstantFoldingPass.FoldingFlags.UNKNOWN)

        left = self._resolve_ref(left_ref)
        right = self._resolve_ref(right_ref)

        # 如果任一操作数无法确认为字面量，则无法折叠
        if not self._is_literal(left) or not self._is_literal(right):
            return

        # 进行类型检查和处理 (这部分保持不变)
        left: Reference[Literal]
        right: Reference[Literal]
        left_dtype = left.get_data_type()
        right_dtype = right.get_data_type()

        # 注意字典可能存在不一致，根据问题描述，假设 handlers 存在匹配项
        handlers = self.BINARY_OP_HANDLERS.get(op)
        if not handlers: return
        handler = handlers.get((left_dtype, right_dtype))
        if not handler: return

        try:
            # 调用处理器计算结果
            folded_value = handler(left.value.value, right.value.value)
            # 创建新的字面量引用
            folded_literal_ref = Reference.literal(folded_value)
            # 用赋值指令替换运算指令
            new_instr = IRAssign(result, folded_literal_ref)
            iterator.set_current(new_instr)
            # 立即在符号表中更新 result 的值，这样后续使用 result 的指令都能看到这个新值
            self._assign(iterator, new_instr)
        except (TypeError, ValueError, ZeroDivisionError):
            # 运算出错，例如类型不匹配，或除零
            pass  # 保持原状

    def _compare(self, iterator: IRBuilderIterator, instr: IRCompare):
        """处理比较运算"""
        # 逻辑与 _op 类似
        result: Variable = instr.get_operands()[0]
        op: CompareOps = instr.get_operands()[1]
        left_ref: Reference[Variable | Constant | Literal] = instr.get_operands()[2]
        right_ref: Reference[Variable | Constant | Literal] = instr.get_operands()[3]

        self.current_table.set(result.get_name(), ConstantFoldingPass.FoldingFlags.UNKNOWN)

        left = self._resolve_ref(left_ref)
        right = self._resolve_ref(right_ref)
        if not self._is_literal(left) or not self._is_literal(right):
            return

        left: Reference[Literal]
        right: Reference[Literal]

        handlers = self.COMPARE_OP_HANDLERS.get(op, {})
        handler = handlers.get((left.get_data_type(), right.get_data_type()))

        if handler:
            try:
                folded_value = handler(left.value.value, right.value.value)
                new_instr = IRAssign(result, Reference.literal(folded_value))
                iterator.set_current(new_instr)
                self._assign(iterator, new_instr)
            except (TypeError, ValueError):
                pass

    def _unary_op(self, iterator: IRBuilderIterator, instr: IRUnaryOp):
        """处理一元运算"""
        result: Variable = instr.get_operands()[0]
        op: UnaryOps = instr.get_operands()[1]
        operand_ref: Reference[Variable | Constant | Literal] = instr.get_operands()[2]

        self.current_table.set(result.get_name(), ConstantFoldingPass.FoldingFlags.UNKNOWN)

        operand = self._resolve_ref(operand_ref)
        if not self._is_literal(operand):
            return

        handlers = self.UNARY_OP_HANDLERS.get(op, {})
        handler = handlers.get(operand.get_data_type())

        if handler:
            try:
                folded_value = handler(operand.value.value)
                new_instr = IRAssign(result, Reference.literal(folded_value))
                iterator.set_current(new_instr)
                self._assign(iterator, new_instr)
            except (TypeError, ValueError):
                pass

    def _cond_jump(self, iterator: IRBuilderIterator, instr: IRCondJump):
        """处理条件跳转，如果条件是常量则可以优化"""
        cond_var: Variable | Literal = instr.get_operands()[0]

        true_scope: str = instr.get_operands()[1]
        false_scope: str = instr.get_operands()[2]

        # 只处理简单变量（非复杂表达式）作为条件
        if isinstance(cond_var, Variable):
            value = self._find(cond_var)

            if isinstance(value, ConstantFoldingPass.FoldingFlags):
                return  # 无法确定条件，保留原跳转

            # 如果条件变量是布尔类型或可以转为布尔
            if cond_var.dtype in (DataType.INT, DataType.BOOLEAN):
                # 注意：这里查找的 value 本身应该已经被折叠成 Literal 类型
                if isinstance(value, Reference) and value.value_type == ValueType.LITERAL:
                    # 如果 value.value.value 是布尔值或能转成布尔值
                    cond_val = bool(value.value.value)  # 0 为 False，非0 为 True
                    jump_scope = true_scope if cond_val else false_scope
                    if jump_scope:
                        # 用直接跳转替代条件跳转
                        iterator.set_current(IRJump(jump_scope))
                    else:
                        # 如果跳转目标为空，则无条件删除该指令？
                        # 删除似乎更合适，表示这个分支不执行
                        iterator.remove_current()
        elif isinstance(cond_var, Literal):
            cond_val = bool(cond_var.value)  # 0 为 False，非0 为 True
            jump_scope = true_scope if cond_val else false_scope
            if jump_scope:
                # 用直接跳转替代条件跳转
                iterator.set_current(IRJump(jump_scope))
            else:
                iterator.remove_current()

    def _call(self, iterator: IRBuilderIterator, instr: IRCall):
        """处理函数调用，优化参数"""
        # 注意：函数调用的常量折叠需要函数是纯函数且有返回值
        # 这里主要做参数的常量传播，而不是结果折叠
        result: Variable | Constant = instr.get_operands()[0]
        func: Function = instr.get_operands()[1]
        args: dict[str, Reference[Variable | Constant | Literal]] = instr.get_operands()[2]

        new_args: dict[str, Reference[Variable | Constant | Literal]] = {}
        changed = False

        for param_name, arg_ref in args.items():
            # 尝试解析实参

            # 如果实参本身已经是字面量，不需要解析
            if arg_ref.value_type == ValueType.LITERAL:
                new_args[param_name] = arg_ref
                continue

            # 如果实参是变量或常量，尝试查找其最终值
            if arg_ref.value_type in (ValueType.VARIABLE, ValueType.CONSTANT):
                arg_value = self._find(arg_ref.value)  # arg_ref.value is the symbol
                if isinstance(arg_value, ConstantFoldingPass.FoldingFlags):
                    # 如果不能确定，保留原引用
                    new_args[param_name] = arg_ref
                else:
                    # 否则，用解析后的值替换引用
                    new_args[param_name] = arg_value
                    changed = True
            else:
                # 不应该出现，因为传参不可能为类或函数的定义
                new_args[param_name] = arg_ref  # 为安全起见，原样保留

        # 如果有任何改变，替换当前指令
        if changed:
            iterator.set_current(IRCall(result, func, new_args))

    def _cast(self, iterator: IRBuilderIterator, instr: IRCast):
        result: Variable | Constant = instr.get_operands()[0]
        dtype: DataType | Class = instr.get_operands()[1]
        value_ref: Reference[Variable | Constant | Literal] = instr.get_operands()[2]

        self.current_table.set(result.get_name(), ConstantFoldingPass.FoldingFlags.UNKNOWN)

        value = self._resolve_ref(value_ref)
        if isinstance(value, ConstantFoldingPass.FoldingFlags):
            return

        # 类型相同
        if isinstance(value, Reference) and value.value_type == ValueType.LITERAL and dtype == value.get_data_type():
            # 类型相同且值已知，直接赋值
            new_assign = IRAssign(result, value)
            iterator.set_current(new_assign)
            # 注意：传递当前的 iterator 和已经创建好的 new_assign 指令
            self._assign(iterator, new_assign)  # 修复：改为传递 current instr，或直接传递已创建的 instr
            return

        # int/bool to string
        if dtype == DataType.STRING and isinstance(value, Reference) and value.value_type == ValueType.LITERAL:
            if value.get_data_type() in (DataType.INT, DataType.BOOLEAN):
                str_val = str(int(value.value.value))  # bool 转 int 再转 str
                str_literal_ref = Reference.literal(str_val)
                self.current_table.set(result.get_name(), str_literal_ref)
                new_assign = IRAssign(result, str_literal_ref)
                iterator.set_current(new_assign)
                # 同样，传递创建好的指令给 _assign
                self._assign(iterator, new_assign)  # 修复
                return

        # 其他情况不能折叠，保持原样

    def _function(self, iterator: IRBuilderIterator, instr: IRFunction):
        """处理函数定义"""
        function: Function = instr.get_operands()[0]
        # 将函数本身存入符号表
        self.current_table.set(function.get_name(), Reference(ValueType.FUNCTION, function))


class DeadCodeEliminationPass(IROptimizationPass):
    def __init__(self, builder: IRBuilder, config: GeneratorConfig):
        self.builder = builder
        self.def_use_graph = {}  # 定义使用图 {var: [uses]}
        self.use_def_graph = {}  # 使用定义图 {var: [defs]}
        self.live_vars = set()  # 活跃变量集合

    def exec(self):
        """执行死代码消除优化"""
        # 第一步：构建依赖图
        self._build_dependency_graph()

        # 第二步：传播活跃变量
        self._propagate_liveness()

        # 第三步：删除死代码
        self._remove_dead_code()

    def _build_dependency_graph(self):
        """构建定义使用/使用定义依赖图"""
        iterator = self.builder.__iter__()

        # 记录所有变量定义
        for instr in iterator:
            if isinstance(instr, IRAssign):
                target, source = instr.get_operands()
                self.def_use_graph[target.name] = []
                if isinstance(source, Reference) and source.value_type == ValueType.VARIABLE:
                    if source.get_name() not in self.use_def_graph:
                        self.use_def_graph[source.get_name()] = []
                    self.use_def_graph[source.get_name()].append(target.get_name())
                    self.def_use_graph[target.get_name()].append(source.get_name())

            elif isinstance(instr, (IROp, IRCompare, IRUnaryOp)):
                operands = instr.get_operands()
                result = operands[0]
                self.def_use_graph[result.name] = []

                # 记录操作数依赖
                for op in operands[2:]:  # 跳过操作符和结果变量
                    if isinstance(op, Reference) and op.value_type == ValueType.VARIABLE:
                        if op.get_name() not in self.use_def_graph:
                            self.use_def_graph[op.get_name()] = []
                        self.use_def_graph[op.get_name()].append(result.get_name())
                        self.def_use_graph[result.get_name()].append(op.get_name())

    def _propagate_liveness(self):
        work_list = deque()
        # 初始活跃变量：函数参数、返回值
        for instr in self.builder.get_instructions():
            if isinstance(instr, IRDeclare):
                var = instr.get_operands()[0]
                if var.var_type in (VariableType.PARAMETER, VariableType.RETURN):
                    self.live_vars.add(var.name)
                    work_list.append(var.name)
            elif self._has_side_effect(instr):
                for op in instr.get_operands():
                    if isinstance(op, Reference) and op.value_type == ValueType.VARIABLE:
                        if op.get_name() not in self.live_vars:
                            self.live_vars.add(op.get_name())
                            work_list.append(op.get_name())
            elif isinstance(instr, IRCondJump):
                cond_var = instr.get_operands()[0]
                if isinstance(cond_var, Variable):
                    if cond_var.name not in self.live_vars:
                        self.live_vars.add(cond_var.name)
                        work_list.append(cond_var.name)
        # 反向传播活跃性
        while work_list:
            current = work_list.popleft()
            if current in self.def_use_graph:
                for user in self.def_use_graph[current]:
                    if user not in self.live_vars:
                        self.live_vars.add(user)
                        work_list.append(user)
            if current in self.use_def_graph:
                for defin in self.use_def_graph[current]:
                    if defin not in self.live_vars:
                        self.live_vars.add(defin)
                        work_list.append(defin)

    def _remove_dead_code(self):
        """删除死代码"""
        iterator = self.builder.__iter__()

        while True:
            try:
                instr: IRInstruction = next(iterator)
            except StopIteration:
                break

            # 处理赋值指令
            if isinstance(instr, IRAssign):
                target, source = instr.get_operands()
                # 如果变量声明已被删除，则强制删除赋值指令
                if not self._is_declaration_exists(target.name):
                    iterator.remove_current()
                elif target.name not in self.live_vars:
                    iterator.remove_current()

            # 处理运算指令
            elif isinstance(instr, (IROp, IRCompare, IRUnaryOp)):
                result = instr.get_operands()[0]
                if result.name not in self.live_vars:
                    iterator.remove_current()

    def _has_side_effect(self, instr):
        """判断指令是否有副作用"""
        return isinstance(instr,
                          (IRAssign, IRCast, IRReturn, IRCall, IRCallMethod, IRNewObj, IRGetProperty, IRSetProperty,
                           IROp,
                           IRCompare, IRUnaryOp))

    def _is_declaration_exists(self, var_name):
        # 检查变量声明是否存在于IR中
        for instr in self.builder.get_instructions():
            if isinstance(instr, IRDeclare) and instr.get_operands()[0].name == var_name:
                return True
        return False

    def _is_dead_assignment(self, target, source):
        """判断是否是无意义的赋值"""
        if target.name in self.live_vars:
            return False

        # 特殊常量赋值保留
        if isinstance(source, Reference) and source.value_type == ValueType.LITERAL:
            return source.value.value == 0  # 保留零初始化

        return True


class DeclareCleanupPass(IROptimizationPass):
    def __init__(self, builder: IRBuilder, config: GeneratorConfig):
        self.builder = builder
        self.scope_tree = {}  # 作用域树 {scope: parent}
        self.var_scopes = {}  # 变量作用域 {var: scope}
        self.var_references = {}  # 变量引用计数 {var: count}
        self.root_vars = set()  # 根变量集合（参数、返回值等）
        self.scope_instructions = {}  # 作用域 -> 指令列表

    def exec(self):
        """执行增强版声明清理"""
        self._build_scope_tree()
        self._analyze_variable_usage()
        self._remove_dead_declarations()

    def _build_scope_tree(self):
        """构建作用域树结构"""
        iterator = self.builder.__iter__()
        scope_stack = []

        while True:
            try:
                instr = next(iterator)
            except StopIteration:
                break

            if isinstance(instr, IRScopeBegin):
                scope_name = instr.get_operands()[0]
                parent = scope_stack[-1] if scope_stack else None
                self.scope_tree[scope_name] = parent
                scope_stack.append(scope_name)

            elif isinstance(instr, IRScopeEnd):
                if scope_stack:
                    scope_stack.pop()

    def _analyze_variable_usage(self):
        """增强版变量使用分析"""
        iterator = self.builder.__iter__()
        scope_stack = []
        current_scope = "global"

        while True:
            try:
                instr = next(iterator)
            except StopIteration:
                break

            # 作用域跟踪
            if isinstance(instr, IRScopeBegin):
                scope_name = instr.get_operands()[0]
                scope_stack.append(scope_name)
                current_scope = scope_stack[-1]
                self.scope_instructions[scope_name] = []
            elif isinstance(instr, IRScopeEnd):
                if scope_stack:
                    scope_stack.pop()
                    current_scope = scope_stack[-1] if scope_stack else "global"

            if current_scope in self.scope_instructions:
                self.scope_instructions[current_scope].append(instr)

            # 处理变量声明
            if isinstance(instr, IRDeclare):
                var = instr.get_operands()[0]
                self.var_scopes[var.name] = current_scope

            # 处理函数参数
            elif isinstance(instr, IRFunction):
                func: Function = instr.get_operands()[0]
                for param in func.params:
                    self.root_vars.add(param.get_name())
                    # 标记函数参数为已使用
                    self.var_references[param.get_name()] = self.var_references.get(param.get_name(), 0) + 1

            # 处理函数调用
            elif isinstance(instr, (IRCall, IRCallMethod)):
                if isinstance(instr, IRCall):
                    result_var, func, args = instr.get_operands()
                else:
                    result_var, _, func, args = instr.get_operands()
                # 标记结果变量为使用
                if result_var:
                    self.var_references[result_var.name] = self.var_references.get(result_var.name, 0) + 1

                # 标记函数参数使用
                for param_name, arg_ref in args.items():
                    if isinstance(arg_ref, Reference) and arg_ref.value_type == ValueType.VARIABLE:
                        self.var_references[arg_ref.get_name()] = self.var_references.get(arg_ref.get_name(), 0) + 1


            # 处理返回值
            elif isinstance(instr, IRReturn):
                value = instr.get_operands()[0]
                if isinstance(value, Reference) and value.value_type == ValueType.VARIABLE:
                    self.var_references[value.get_name()] = self.var_references.get(value.get_name(), 0) + 1

            # 处理条件跳转
            elif isinstance(instr, IRCondJump):
                cond_var = instr.get_operands()[0]
                if isinstance(cond_var, (Variable, Constant)):
                    self.var_references[cond_var.name] = self.var_references.get(cond_var.name, 0) + 1

            # 处理赋值操作
            elif isinstance(instr, IRAssign):
                target, source = instr.get_operands()
                # 标记源变量使用
                if source.value_type == ValueType.VARIABLE:
                    self.var_references[source.get_name()] = self.var_references.get(source.get_name(), 0) + 1
                # 标记目标变量为已声明
                self.var_references[target.name] = self.var_references.get(target.name, 0)

            # 处理运算操作
            elif isinstance(instr, (IROp, IRCompare, IRUnaryOp)):
                operands = instr.get_operands()
                result = operands[0]
                # 标记结果变量
                self.var_references[result.name] = self.var_references.get(result.name, 0)

                # 标记所有操作数使用
                for op in operands[2:]:  # 跳过操作符和结果变量
                    if isinstance(op, Reference) and op.value_type == ValueType.VARIABLE:
                        self.var_references[op.get_name()] = self.var_references.get(op.get_name(), 0) + 1
            elif isinstance(instr, IRCast):
                target, dtype, source = instr.get_operands()
                if isinstance(source, Reference) and source.value_type == ValueType.VARIABLE:
                    self.var_references[source.get_name()] = self.var_references.get(source.get_name(), 0) + 1

    def _remove_dead_declarations(self):
        """删除无效的变量声明"""
        iterator = self.builder.__iter__()
        current_scope = "global"

        while True:
            try:
                instr = next(iterator)
            except StopIteration:
                break

            if isinstance(instr, IRScopeBegin):
                current_scope = instr.get_operands()[0]

            elif isinstance(instr, IRDeclare):
                var = instr.get_operands()[0]
                var_name = var.name

                # 保留条件：
                # 1. 根变量（参数、返回值等）
                # 2. 被使用过的变量
                # 3. 作用域根变量
                # 4. 在嵌套作用域中被使用的变量

                # 如果是根变量或被使用过，保留
                if (var_name in self.root_vars or
                        self.var_references.get(var_name, 0) > 0 or
                        self._is_scope_root(var_name, current_scope) or
                        self._is_used_in_nested_scope(var_name, current_scope)):
                    continue

                # 如果是作用域根变量，保留
                if self._is_scope_root(var_name, current_scope):
                    continue

                # 如果被嵌套作用域使用，保留
                if self._is_used_in_nested_scope(var_name, current_scope):
                    continue

                # 否则删除声明
                iterator.remove_current()

    def _is_scope_root(self, var_name, scope):
        """判断变量是否是作用域根变量"""
        parent = self.scope_tree.get(scope)
        if not parent:
            return False
        return self.var_scopes.get(var_name) == parent

    def _is_used_in_nested_scope(self, var_name, scope):
        """判断变量是否在嵌套作用域中被使用"""
        for nested_scope, parent in self.scope_tree.items():
            if parent == scope:
                if self._is_var_used_in_scope(var_name, nested_scope):
                    return True
        return False

    def _is_var_used_in_scope(self, var_name, scope):
        """
        判断变量是否在特定作用域中被使用。

        :param var_name: 要检查的变量名称
        :param scope: 作用域名称
        :return: 如果变量在该作用域中被使用，返回 True，否则返回 False
        """
        if scope not in self.scope_instructions:
            return False

        for instr in self.scope_instructions[scope]:
            for operand in instr.get_operands():
                if isinstance(operand, Reference) and operand.get_name() == var_name:
                    return True
        return False


class UselessScopeRemovalPass(IROptimizationPass):
    def __init__(self, builder: IRBuilder, debug: bool = False):
        self.builder = builder
        self.debug = debug
        self.scope_reachability = {}  # 作用域可达性 {scope_name: is_reachable}
        self.scope_instructions = {}  # 作用域指令映射 {scope_name: [instructions]}
        self.jump_targets = set()  # 所有跳转目标集合
        self.root_scopes = set()  # 根作用域集合（main 函数等）

    def exec(self):
        """执行无用作用域删除优化"""
        # 第一步：构建作用域结构
        self._build_scope_structure()

        # 第二步：分析控制流可达性
        self._analyze_reachability()

        # 第三步：删除不可达作用域
        self._remove_unreachable_scopes()

    def _build_scope_structure(self):
        """构建作用域结构和跳转目标"""
        iterator = self.builder.__iter__()
        current_scope = "global"
        scope_stack = []

        while True:
            try:
                instr = next(iterator)
            except StopIteration:
                break

            # 记录跳转目标
            if isinstance(instr, (IRJump, IRCondJump)):
                targets = [op for op in instr.get_operands() if isinstance(op, str)]
                self.jump_targets.update(targets)

            # 处理作用域
            if isinstance(instr, IRScopeBegin):
                scope_name = instr.get_operands()[0]
                scope_type = instr.get_operands()[1]

                # 所有定义作用域都标记为根作用域
                if scope_type in (StructureType.FUNCTION, StructureType.LOOP_BODY,
                                  StructureType.LOOP_CHECK, StructureType.CLASS, StructureType.INTERFACE):
                    self.root_scopes.add(scope_name)

                scope_stack.append(scope_name)
                current_scope = scope_name
                self.scope_instructions[scope_name] = []

            elif isinstance(instr, IRScopeEnd):
                if scope_stack:
                    scope_stack.pop()
                    current_scope = scope_stack[-1] if scope_stack else "global"

            # 记录作用域内指令
            if current_scope in self.scope_instructions:
                self.scope_instructions[current_scope].append(instr)

    def _analyze_reachability(self):
        """分析作用域可达性（DFS）"""
        # 初始化可达性
        for scope in self.scope_instructions:
            self.scope_reachability[scope] = False

        # 从所有根作用域开始传播
        for root in self.root_scopes:
            if root in self.scope_instructions:
                self._dfs_reachability(root)

    def _dfs_reachability(self, scope_name):
        """深度优先遍历可达作用域"""
        if self.scope_reachability.get(scope_name, False):
            return

        self.scope_reachability[scope_name] = True

        # 遍历该作用域内的所有指令，查找跳转目标
        for instr in self.scope_instructions.get(scope_name, []):
            if isinstance(instr, (IRJump, IRCondJump)):
                targets = [op for op in instr.get_operands() if isinstance(op, str)]
                for target in targets:
                    if target in self.scope_instructions:
                        self._dfs_reachability(target)

    def _remove_unreachable_scopes(self):
        """删除不可达作用域及其指令（保留函数作用域）"""
        iterator = self.builder.__iter__()
        scopes_to_remove = set()

        # 收集所有不可达且非函数作用域的作用域名称
        for scope, reachable in self.scope_reachability.items():
            if not reachable and scope not in self.root_scopes:
                scopes_to_remove.add(scope)

        delete_level = 0  # 当前删除的嵌套层数

        while True:
            try:
                instr = next(iterator)
            except StopIteration:
                break

            if delete_level == 0 and isinstance(instr, IRScopeBegin):
                scope_name = instr.get_operands()[0]
                if scope_name in scopes_to_remove:
                    # 开始删除该作用域，删除当前 SCOPE_BEGIN
                    iterator.remove_current()
                    delete_level = 1  # 进入删除模式

            elif delete_level > 0:
                if isinstance(instr, IRScopeBegin):
                    delete_level += 1  # 嵌套作用域层级增加
                elif isinstance(instr, IRScopeEnd):
                    delete_level -= 1  # 嵌套作用域层级减少
                    iterator.remove_current()  # 删除对应的 SCOPE_END
                else:
                    iterator.remove_current()  # 删除中间所有指令

    def _remove_scope_content(self, iterator, scope_name):
        """删除指定作用域内的所有指令"""
        content = self.scope_instructions.get(scope_name, [])
        for instr in content:
            try:
                # 尝试从迭代器中移除
                if next(i for i in iterator if i == instr):
                    iterator.remove_current()
            except StopIteration:
                pass


class EmptyScopeRemovalPass(IROptimizationPass):

    def __init__(self, builder: IRBuilder, config: GeneratorConfig):
        # FIXME:当函数嵌套且名称重复时会出现删除错误,故临时放在测试性优化，等待修复
        self.builder = builder
        self.scope_instructions = {}  # 作用域 -> 指令列表
        self.empty_scopes = set()  # 空作用域集合

    def exec(self):
        """执行空作用域及跳转指令删除优化"""
        self._build_scope_structure()
        self._detect_empty_scopes()
        self._remove_jump_to_empty_scopes()
        self._remove_empty_scope_declarations()

    def _build_scope_structure(self):
        """构建作用域结构，记录每个作用域内的指令"""
        iterator = self.builder.__iter__()
        current_scope = "global"
        scope_stack = []

        while True:
            try:
                instr = next(iterator)
            except StopIteration:
                break

            if isinstance(instr, IRScopeBegin):
                scope_name = instr.get_operands()[0]
                scope_stack.append(scope_name)
                current_scope = scope_name
                self.scope_instructions[scope_name] = []
            elif isinstance(instr, IRScopeEnd):
                if scope_stack:
                    scope_stack.pop()
                    current_scope = scope_stack[-1] if scope_stack else "global"
            else:
                # 仅记录非作用域指令
                if current_scope in self.scope_instructions:
                    self.scope_instructions[current_scope].append(instr)

    def _detect_empty_scopes(self):
        """检测空作用域（作用域内没有任何非作用域结构的指令）"""
        for scope, instructions in self.scope_instructions.items():
            # 若指令列表为空，或仅包含作用域结构（如IRScopeBegin/IRScopeEnd），则视为空
            if not instructions:
                self.empty_scopes.add(scope)

    def _remove_jump_to_empty_scopes(self):
        """删除所有跳转到空作用域的指令"""
        iterator = self.builder.__iter__()
        while True:
            try:
                instr = next(iterator)
            except StopIteration:
                break

            if isinstance(instr, (IRJump, IRCondJump)):
                targets = [op for op in instr.get_operands() if isinstance(op, str)]
                for target in targets:
                    if target in self.empty_scopes:
                        iterator.remove_current()
                        break

    def _remove_empty_scope_declarations(self):
        """删除空作用域的IRScopeBegin和IRScopeEnd指令"""
        iterator = self.builder.__iter__()
        deleting_scope = None

        while True:
            try:
                instr = next(iterator)
            except StopIteration:
                break

            if isinstance(instr, IRScopeBegin):
                scope_name = instr.get_operands()[0]
                stype = instr.get_operands()[1]
                if scope_name in self.empty_scopes and stype not in (StructureType.FUNCTION, StructureType.CLASS):
                    iterator.remove_current()
                    deleting_scope = scope_name
            elif isinstance(instr, IRScopeEnd):
                if deleting_scope is not None:
                    iterator.remove_current()
                    deleting_scope = None
            elif isinstance(instr, (IRFunction, IRClass)):
                peek_instr = iterator.peek()
                if isinstance(peek_instr, IRScopeBegin) and peek_instr.get_operands()[0] in self.empty_scopes:
                    iterator.remove_current()
            else:
                if deleting_scope is not None:
                    iterator.remove_current()


class UnreachableCodeRemovalPass(IROptimizationPass):
    def __init__(self, builder: IRBuilder, config: GeneratorConfig):
        self.builder = builder
        self.config = config

    def exec(self):
        iterator = self.builder.__iter__()
        in_unreachable = False
        level = 0
        while True:
            try:
                instr = next(iterator)
            except StopIteration:
                break

            if in_unreachable:
                if isinstance(instr, IRScopeBegin):
                    level += 1
                elif isinstance(instr, IRScopeEnd):
                    if level == 0:
                        in_unreachable = False
                        continue

                    level -= 1
                # 删除当前指令
                iterator.remove_current()
                continue

            # 检查是否进入不可达模式
            if isinstance(instr, (IRReturn, IRBreak, IRContinue)):
                in_unreachable = True


class ChainAssignEliminationPass(IROptimizationPass):
    def __init__(self, builder: IRBuilder, config: GeneratorConfig):
        # FIXME: 对于for循环的优化存在严重问题

        self.builder = builder
        self.config = config

    def exec(self):
        """
        链式赋值消除优化：消除中间变量的无意义链式赋值
        """
        # 第一步：构建作用域树和变量别名映射表
        scope_tree, alias_maps = self._build_scope_tree_and_alias_maps()

        # 第二步：应用别名替换
        self._apply_alias_substitution(alias_maps, scope_tree)

    def _build_scope_tree_and_alias_maps(self) -> tuple[dict, dict]:
        """
        构建作用域树和每个作用域的变量别名映射表
        返回 (scope_tree, alias_maps)
        scope_tree: {scope_name: parent_scope_name}
        alias_maps: {scope_name: {var_name: final_reference}}
        """
        scope_tree = {}  # 作用域树 {scope_name: parent_scope_name}
        alias_maps = {}  # 每个作用域的别名映射 {scope_name: {var_name: final_reference}}

        scope_stack = []  # 当前作用域栈
        current_scope = "global"  # 当前作用域
        alias_maps[current_scope] = {}  # 初始化全局作用域别名映射

        # 遍历所有指令，构建作用域结构和别名映射
        for instr in self.builder.get_instructions():
            if isinstance(instr, IRScopeBegin):
                scope_name = instr.get_operands()[0]
                parent_scope = current_scope
                scope_tree[scope_name] = parent_scope
                scope_stack.append(scope_name)
                current_scope = scope_name
                # 初始化新作用域的别名映射，继承父作用域的映射
                alias_maps[current_scope] = alias_maps[parent_scope].copy()

            elif isinstance(instr, IRScopeEnd):
                if scope_stack:
                    scope_stack.pop()
                    current_scope = scope_stack[-1] if scope_stack else "global"

            elif isinstance(instr, IRDeclare):
                var = instr.get_operands()[0]
                var_name = var.get_name()
                # 每个变量初始时指向自己
                if current_scope in alias_maps:
                    alias_maps[current_scope][var_name] = Reference.variable(var_name, var.dtype)

            elif isinstance(instr, IRAssign):
                target, source = instr.get_operands()
                target_name = target.get_name()

                if isinstance(source, Reference):
                    if current_scope in alias_maps:
                        if source.value_type == ValueType.VARIABLE:
                            source_name = source.get_name()
                            # 如果源变量有别名，使用源变量的别名
                            if source_name in alias_maps[current_scope]:
                                alias_maps[current_scope][target_name] = alias_maps[current_scope][source_name]
                            else:
                                alias_maps[current_scope][target_name] = source
                        elif source.value_type in (ValueType.LITERAL, ValueType.CONSTANT):
                            # 直接值作为别名
                            alias_maps[current_scope][target_name] = source

        return scope_tree, alias_maps

    def _get_visible_aliases(self, scope: str, scope_tree: dict, alias_maps: dict) -> dict:
        """
        获取在指定作用域中可见的所有别名映射
        包括当前作用域及其所有祖先作用域的别名
        """
        visible_aliases = {}
        current = scope

        # 从当前作用域开始，向上遍历到根作用域，收集所有可见的别名
        while current is not None:
            if current in alias_maps:
                # 更新可见别名（内部作用域的别名优先）
                for var_name, alias_ref in alias_maps[current].items():
                    if var_name not in visible_aliases:
                        visible_aliases[var_name] = alias_ref
            current = scope_tree.get(current)

        return visible_aliases

    def _apply_alias_substitution(self, alias_maps: dict, scope_tree: dict):
        """
        应用别名替换到所有使用这些变量的地方
        """
        iterator = self.builder.__iter__()
        scope_stack = []  # 当前作用域栈
        current_scope = "global"  # 当前作用域

        while True:
            try:
                instr = next(iterator)
            except StopIteration:
                break

            # 更新当前作用域
            if isinstance(instr, IRScopeBegin):
                scope_name = instr.get_operands()[0]
                scope_stack.append(scope_name)
                current_scope = scope_name
            elif isinstance(instr, IRScopeEnd):
                if scope_stack:
                    scope_stack.pop()
                    current_scope = scope_stack[-1] if scope_stack else "global"

            # 获取当前作用域可见的别名映射
            visible_aliases = self._get_visible_aliases(current_scope, scope_tree, alias_maps)

            # 处理各种指令类型
            if isinstance(instr, IRAssign):
                self._handle_assign(iterator, instr, visible_aliases)
            elif isinstance(instr, IRCall):
                self._handle_call(iterator, instr, visible_aliases)
            elif isinstance(instr, IRCallMethod):
                self._handle_call_method(iterator, instr, visible_aliases)
            elif isinstance(instr, IRCondJump):
                self._handle_cond_jump(iterator, instr, visible_aliases)
            elif isinstance(instr, IRCompare):
                self._handle_compare(iterator, instr, visible_aliases)
            elif isinstance(instr, IROp):
                self._handle_binary_op(iterator, instr, visible_aliases)
            elif isinstance(instr, IRUnaryOp):
                self._handle_unary_op(iterator, instr, visible_aliases)
            elif isinstance(instr, IRCast):
                self._handle_cast(iterator, instr, visible_aliases)
            elif isinstance(instr, IRGetProperty):
                self._handle_get_field(iterator, instr, visible_aliases)
            elif isinstance(instr, IRSetProperty):
                self._handle_set_field(iterator, instr, visible_aliases)

    def _handle_assign(self, iterator, instr: IRAssign, visible_aliases: dict):
        """处理赋值语句中的别名替换"""
        target, source = instr.get_operands()

        if isinstance(source, Reference) and source.value_type == ValueType.VARIABLE:
            source_name = source.get_name()
            if source_name in visible_aliases:
                final_alias = visible_aliases[source_name]
                # 只有当别名不是自身时才替换
                if (isinstance(final_alias, Reference) and
                        (final_alias.value_type != ValueType.VARIABLE or final_alias.get_name() != source_name)):
                    new_instr = IRAssign(target, final_alias)
                    iterator.set_current(new_instr)

    def _handle_call(self, iterator, instr: IRCall, visible_aliases: dict):
        """处理函数调用中的参数别名替换"""
        result, func, args = instr.get_operands()
        new_args = {}
        changed = False

        for param_name, arg_ref in args.items():
            if isinstance(arg_ref, Reference) and arg_ref.value_type == ValueType.VARIABLE:
                source_name = arg_ref.get_name()
                if source_name in visible_aliases:
                    final_alias = visible_aliases[source_name]
                    # 只有当别名不是自身时才替换
                    if (isinstance(final_alias, Reference) and
                            (final_alias.value_type != ValueType.VARIABLE or final_alias.get_name() != source_name)):
                        new_args[param_name] = final_alias
                        changed = True
                    else:
                        new_args[param_name] = arg_ref
                else:
                    new_args[param_name] = arg_ref
            else:
                new_args[param_name] = arg_ref

        if changed:
            iterator.set_current(IRCall(result, func, new_args))

    def _handle_call_method(self, iterator, instr: IRCallMethod, visible_aliases: dict):
        """处理方法调用中的参数别名替换"""
        result, class_, method, args = instr.get_operands()
        if args is None:
            return

        new_args = {}
        changed = False

        for param_name, arg_ref in args.items():
            if isinstance(arg_ref, Reference) and arg_ref.value_type == ValueType.VARIABLE:
                source_name = arg_ref.get_name()
                if source_name in visible_aliases:
                    final_alias = visible_aliases[source_name]
                    if (isinstance(final_alias, Reference) and
                            (final_alias.value_type != ValueType.VARIABLE or final_alias.get_name() != source_name)):
                        new_args[param_name] = final_alias
                        changed = True
                    else:
                        new_args[param_name] = arg_ref
                else:
                    new_args[param_name] = arg_ref
            else:
                new_args[param_name] = arg_ref

        if changed:
            iterator.set_current(IRCallMethod(result, class_, method, new_args))

    def _handle_cond_jump(self, iterator, instr: IRCondJump, visible_aliases: dict):
        """处理条件跳转中的条件变量替换"""
        cond_ref, true_scope, false_scope = instr.get_operands()

        if isinstance(cond_ref, Variable):
            cond_name = cond_ref.name
            if cond_name in visible_aliases:
                final_alias = visible_aliases[cond_name]
                if (isinstance(final_alias, Reference) and
                        (final_alias.value_type != ValueType.VARIABLE or final_alias.get_name() != cond_name)):
                    # 注意：IRCondJump的第一个操作数需要是Variable类型，不是Reference
                    if isinstance(final_alias, Reference) and final_alias.value_type == ValueType.VARIABLE:
                        new_instr = IRCondJump(final_alias.value, true_scope, false_scope)
                        iterator.set_current(new_instr)

    def _handle_compare(self, iterator, instr: IRCompare, visible_aliases: dict):
        """处理比较操作中的操作数替换"""
        result, op, left_ref, right_ref = instr.get_operands()
        changed = False
        new_left = left_ref
        new_right = right_ref

        # 处理左操作数
        if isinstance(left_ref, Reference) and left_ref.value_type == ValueType.VARIABLE:
            left_name = left_ref.get_name()
            if left_name in visible_aliases:
                final_alias = visible_aliases[left_name]
                if (isinstance(final_alias, Reference) and
                        (final_alias.value_type != ValueType.VARIABLE or final_alias.get_name() != left_name)):
                    new_left = final_alias
                    changed = True

        # 处理右操作数
        if isinstance(right_ref, Reference) and right_ref.value_type == ValueType.VARIABLE:
            right_name = right_ref.get_name()
            if right_name in visible_aliases:
                final_alias = visible_aliases[right_name]
                if (isinstance(final_alias, Reference) and
                        (final_alias.value_type != ValueType.VARIABLE or final_alias.get_name() != right_name)):
                    new_right = final_alias
                    changed = True

        if changed:
            new_instr = IRCompare(result, op, new_left, new_right)
            iterator.set_current(new_instr)

    def _handle_binary_op(self, iterator, instr: IROp, visible_aliases: dict):
        """处理二元操作中的操作数替换"""
        result, op, left_ref, right_ref = instr.get_operands()
        changed = False
        new_left = left_ref
        new_right = right_ref

        # 处理左操作数
        if isinstance(left_ref, Reference) and left_ref.value_type == ValueType.VARIABLE:
            left_name = left_ref.get_name()
            if left_name in visible_aliases:
                final_alias = visible_aliases[left_name]
                if (isinstance(final_alias, Reference) and
                        (final_alias.value_type != ValueType.VARIABLE or final_alias.get_name() != left_name)):
                    new_left = final_alias
                    changed = True

        # 处理右操作数
        if isinstance(right_ref, Reference) and right_ref.value_type == ValueType.VARIABLE:
            right_name = right_ref.get_name()
            if right_name in visible_aliases:
                final_alias = visible_aliases[right_name]
                if (isinstance(final_alias, Reference) and
                        (final_alias.value_type != ValueType.VARIABLE or final_alias.get_name() != right_name)):
                    new_right = final_alias
                    changed = True

        if changed:
            new_instr = IROp(result, op, new_left, new_right)
            iterator.set_current(new_instr)

    def _handle_unary_op(self, iterator, instr: IRUnaryOp, visible_aliases: dict):
        """处理一元操作中的操作数替换"""
        result, op, operand_ref = instr.get_operands()

        if isinstance(operand_ref, Reference) and operand_ref.value_type == ValueType.VARIABLE:
            operand_name = operand_ref.get_name()
            if operand_name in visible_aliases:
                final_alias = visible_aliases[operand_name]
                if (isinstance(final_alias, Reference) and
                        (final_alias.value_type != ValueType.VARIABLE or final_alias.get_name() != operand_name)):
                    new_instr = IRUnaryOp(result, op, final_alias)
                    iterator.set_current(new_instr)

    def _handle_cast(self, iterator, instr: IRCast, visible_aliases: dict):
        """处理类型转换中的操作数替换"""
        result, dtype, value_ref = instr.get_operands()

        if isinstance(value_ref, Reference) and value_ref.value_type == ValueType.VARIABLE:
            value_name = value_ref.get_name()
            if value_name in visible_aliases:
                final_alias = visible_aliases[value_name]
                if (isinstance(final_alias, Reference) and
                        (final_alias.value_type != ValueType.VARIABLE or final_alias.get_name() != value_name)):
                    new_instr = IRCast(result, dtype, final_alias)
                    iterator.set_current(new_instr)

    def _handle_get_field(self, iterator, instr: IRGetProperty, visible_aliases: dict):
        """处理字段获取中的对象引用替换"""
        result, obj_ref, field = instr.get_operands()

        if isinstance(obj_ref, Reference) and obj_ref.value_type == ValueType.VARIABLE:
            obj_name = obj_ref.get_name()
            if obj_name in visible_aliases:
                final_alias = visible_aliases[obj_name]
                if (isinstance(final_alias, (Variable, Constant)) and
                        final_alias.get_name() != obj_name):
                    new_instr = IRGetProperty(result, final_alias, field)
                    iterator.set_current(new_instr)

    def _handle_set_field(self, iterator, instr: IRSetProperty, visible_aliases: dict):
        """处理字段设置中的对象引用和值引用替换"""
        obj_ref, field, value_ref = instr.get_operands()
        changed = False
        new_obj = obj_ref
        new_value = value_ref

        # 处理对象引用
        if isinstance(obj_ref, Reference) and obj_ref.value_type == ValueType.VARIABLE:
            obj_name = obj_ref.get_name()
            if obj_name in visible_aliases:
                final_alias = visible_aliases[obj_name]
                if (isinstance(final_alias, Reference) and
                        (final_alias.value_type != ValueType.VARIABLE or final_alias.get_name() != obj_name)):
                    new_obj = final_alias
                    changed = True

        # 处理值引用
        if isinstance(value_ref, Reference) and value_ref.value_type == ValueType.VARIABLE:
            value_name = value_ref.get_name()
            if value_name in visible_aliases:
                final_alias = visible_aliases[value_name]
                if (isinstance(final_alias, Reference) and
                        (final_alias.value_type != ValueType.VARIABLE or final_alias.get_name() != value_name)):
                    new_value = final_alias
                    changed = True

        if changed:
            new_instr = IRSetProperty(new_obj, field, new_value)
            iterator.set_current(new_instr)


class UnusedFunctionEliminationPass(IROptimizationPass):
    """未使用函数消除优化管道 - 正确处理同名嵌套函数"""

    def __init__(self, builder: IRBuilder, config: GeneratorConfig):
        self.builder = builder
        self.config = config
        self.debug = config.debug

    def exec(self):
        """执行未使用函数的消除优化"""
        if self.debug:
            print(f"[DEBUG: {self.__class__.__name__}] Starting unused function elimination...")

        self._eliminate_unused_functions()

        if self.debug:
            print(f"[DEBUG: {self.__class__.__name__}] Unused function elimination completed.")

    def _eliminate_unused_functions(self):
        """消除未被调用的函数定义及其完整函数体，正确处理同名嵌套函数"""
        # 第一步：构建函数层次结构，生成唯一标识符
        function_hierarchy = self._build_function_hierarchy()

        # 第二步：统计函数调用，使用唯一标识符
        function_call_counts = self._count_function_calls(function_hierarchy)

        # 第三步：标记需要移除的函数
        functions_to_remove = self._identify_unused_functions(function_hierarchy, function_call_counts)

        # 第四步：执行移除操作
        self._remove_functions(functions_to_remove, function_hierarchy)

    def _build_function_hierarchy(self):
        """构建函数的层次结构，为每个函数生成唯一标识符"""
        instructions = self.builder.get_instructions()
        hierarchy = {}
        function_stack = []  # 用于追踪嵌套层次
        function_counter = {}  # 用于同名函数计数

        for i, instr in enumerate(instructions):
            if isinstance(instr, IRFunction):
                func_name = instr.operands[0].name

                # 生成唯一标识符：包含路径和计数
                parent_path = function_stack[-1]['unique_id'] if function_stack else ""
                scope_key = f"{parent_path}::{func_name}" if parent_path else func_name

                # 处理同名函数
                if scope_key not in function_counter:
                    function_counter[scope_key] = 0
                else:
                    function_counter[scope_key] += 1

                unique_id = f"{scope_key}#{function_counter[scope_key]}" if function_counter[
                                                                                scope_key] > 0 else scope_key

                parent_func = function_stack[-1]['unique_id'] if function_stack else None

                func_info = {
                    'unique_id': unique_id,
                    'name': func_name,
                    'start_idx': i,
                    'end_idx': None,
                    'parent': parent_func,
                    'children': [],
                    'depth': len(function_stack),
                    'instruction': instr  # 保存指令引用用于调用匹配
                }

                hierarchy[unique_id] = func_info

                if parent_func:
                    hierarchy[parent_func]['children'].append(unique_id)

                function_stack.append(func_info)

            elif isinstance(instr, IRScopeEnd):
                # 检查是否是函数结束
                if function_stack and self._is_function_end_scope(instructions, i, function_stack):
                    current_func = function_stack.pop()
                    hierarchy[current_func['unique_id']]['end_idx'] = i + 1

        # 处理文件末尾的函数
        for func_info in function_stack:
            hierarchy[func_info['unique_id']]['end_idx'] = len(instructions)

        return hierarchy

    def _is_function_end_scope(self, instructions, scope_end_idx, function_stack):
        """判断这个scope end是否真的是当前函数的结束"""
        if not function_stack:
            return False

        current_func_start = function_stack[-1]['start_idx']
        scope_depth = 0

        # 从函数开始到当前位置，计算作用域平衡
        for i in range(current_func_start + 1, scope_end_idx + 1):
            instr = instructions[i]
            if isinstance(instr, IRScopeBegin):
                scope_depth += 1
            elif isinstance(instr, IRScopeEnd):
                scope_depth -= 1
                if scope_depth == 0 and i == scope_end_idx:
                    return True

        return False

    def _count_function_calls(self, hierarchy):
        """统计函数调用，正确匹配到具体的函数实例"""
        call_counts = {unique_id: 0 for unique_id in hierarchy.keys()}
        instructions = self.builder.get_instructions()

        for i, instr in enumerate(instructions):
            if isinstance(instr, IRCall):
                called_func = instr.operands[1]  # Function对象
                target_func_id = self._resolve_function_call(called_func, i, hierarchy)
                if target_func_id:
                    call_counts[target_func_id] += 1

            elif isinstance(instr, IRCallMethod):
                method_func = instr.operands[2]  # Function对象
                target_func_id = self._resolve_function_call(method_func, i, hierarchy)
                if target_func_id:
                    call_counts[target_func_id] += 1

        return call_counts

    def _resolve_function_call(self, func_obj, call_position, hierarchy):
        """
        解析函数调用，确定调用的是哪个具体的函数实例
        根据作用域规则和调用位置来确定目标函数
        """
        func_name = func_obj.name

        # 找到调用点所在的作用域
        call_scope = self._find_call_scope(call_position, hierarchy)

        # 从调用作用域开始，向上查找可见的同名函数
        candidates = self._find_visible_functions(func_name, call_scope, hierarchy)

        if not candidates:
            # 没找到匹配的函数，可能是外部函数或内置函数
            if self.debug:
                print(
                    f"[DEBUG: {self.__class__.__name__}] Could not resolve function call: {func_name} at position {call_position}")
            return None

        # 选择最近的匹配函数（作用域链中最近的）
        return candidates[0]

    def _find_call_scope(self, call_position, hierarchy):
        """找到调用点所在的函数作用域"""
        current_scope = None

        for unique_id, func_info in hierarchy.items():
            start_idx = func_info['start_idx']
            end_idx = func_info['end_idx'] or len(self.builder.get_instructions())

            if start_idx <= call_position < end_idx:
                # 调用在这个函数范围内
                if current_scope is None or func_info['depth'] > hierarchy[current_scope]['depth']:
                    # 选择嵌套层次最深的函数（最内层的作用域）
                    current_scope = unique_id

        return current_scope

    def _find_visible_functions(self, func_name, call_scope, hierarchy):
        """
        根据作用域规则查找可见的同名函数
        返回按优先级排序的候选函数列表
        """
        candidates = []
        current_scope = call_scope

        # 向上遍历作用域链
        while current_scope:
            func_info = hierarchy[current_scope]

            # 检查当前作用域的兄弟函数（同级定义的函数）
            parent = func_info['parent']
            if parent:
                siblings = hierarchy[parent]['children']
            else:
                # 顶级函数
                siblings = [uid for uid, info in hierarchy.items() if info['parent'] is None]

            for sibling_id in siblings:
                if hierarchy[sibling_id]['name'] == func_name and sibling_id != current_scope:
                    candidates.append(sibling_id)

            # 检查父作用域中定义的函数
            if parent:
                parent_info = hierarchy[parent]
                if parent_info['name'] == func_name:
                    candidates.append(parent)

            # 移动到父作用域
            current_scope = parent

        # 检查全局作用域的函数
        for unique_id, func_info in hierarchy.items():
            if func_info['parent'] is None and func_info['name'] == func_name:
                if unique_id not in candidates:
                    candidates.append(unique_id)

        return candidates

    def _identify_unused_functions(self, hierarchy, call_counts):
        """识别未使用的函数"""
        functions_to_remove = []

        for unique_id, func_info in hierarchy.items():
            if func_info['instruction'].operands[0].annotations:
                if self.debug:
                    print(
                        f"[DEBUG: {self.__class__.__name__}] Skipping protected function: {func_info['name']} [{unique_id}]")
                continue
            if call_counts.get(unique_id, 0) == 0:
                functions_to_remove.append(unique_id)

                if self.debug:
                    parent = func_info['parent']
                    depth_str = "  " * func_info['depth']
                    parent_str = f" (nested in {hierarchy[parent]['name']})" if parent else ""
                    print(
                        f"[DEBUG: {self.__class__.__name__}] {depth_str}Marking unused function: {func_info['name']} [{unique_id}]{parent_str}")

        return functions_to_remove

    def _remove_functions(self, functions_to_remove, hierarchy):
        """移除指定的函数"""
        if not functions_to_remove:
            return

        instructions = self.builder.get_instructions()

        # 按照在代码中的位置逆序移除（避免索引偏移问题）
        removal_ranges = []
        for unique_id in functions_to_remove:
            func_info = hierarchy[unique_id]
            removal_ranges.append((func_info['start_idx'], func_info['end_idx'], func_info['name'], unique_id))

        # 按start_idx逆序排序
        removal_ranges.sort(key=lambda x: x[0], reverse=True)

        removed_count = 0
        for start_idx, end_idx, func_name, unique_id in removal_ranges:
            if self.debug:
                print(
                    f"[DEBUG: {self.__class__.__name__}] Removing function {func_name} [{unique_id}]: instructions {start_idx}-{end_idx}")

            del instructions[start_idx:end_idx]
            removed_count += (end_idx - start_idx)

        # 更新指令列表
        self.builder._instructions = instructions

        if self.debug:
            print(
                f"[DEBUG: {self.__class__.__name__}] Total removed {len(functions_to_remove)} functions, {removed_count} instructions")
