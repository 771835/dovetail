# coding=utf-8
from __future__ import annotations

import copy
from collections import deque
from enum import Enum, auto
from itertools import count

from attrs import define, field, validators

from transpiler.core.backend.ir_builder import IRBuilder, IRBuilderIterator
from transpiler.core.backend.specification import IROptimizerSpec, \
    IROptimizationPass, MinecraftVersion
from transpiler.core.enums import ValueType, VariableType, DataTypeBase
from transpiler.core.generator_config import GeneratorConfig, MinecraftEdition, OptimizationLevel
from transpiler.core.instructions import *
from transpiler.core.symbols import Variable, Reference, Constant, Literal, Parameter


class Optimizer(IROptimizerSpec):
    def __init__(self, builder: IRBuilder,
                 config: GeneratorConfig):
        self.config = config
        self.debug = config.debug
        self.level = config.optimization_level
        self.initial_builder = builder
        self.builder = copy.deepcopy(builder)  # 防止修改初始状态
        self.passes = []  # 存储启用的优化通道

    @classmethod
    def is_support(
            cls, version: MinecraftVersion) -> bool:

        if version.major == 1 and version.minor == 20 and version.patch == 4 and version.edition == MinecraftEdition.JAVA_EDITION:
            return True
        else:
            return False

    def optimize(self) -> IRBuilder:
        optimization_pass: list[type[IROptimizationPass]] = []
        if self.level == OptimizationLevel.O0:
            return self.builder

        if self.level >= OptimizationLevel.O1:
            optimization_pass.append(ConstantFoldingPass)
            optimization_pass.append(DeadCodeEliminationPass)
            optimization_pass.append(DeclareCleanupPass)
            optimization_pass.append(UnreachableCodeRemovalPass)
        if self.level >= OptimizationLevel.O2:
            optimization_pass.append(UselessScopeRemovalPass)

        if self.level >= OptimizationLevel.O3:  # 测试性优化
            # FIXME:当函数嵌套且名称重复时会出现删除错误,故临时放在测试性优化，等待修复
            optimization_pass.append(EmptyScopeRemovalPass)
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
            (DataType.STRING, DataType.INT): lambda a, b: a + str(b)
        },
        BinaryOps.SUB: {
            (DataType.INT, DataType.INT): lambda a, b: a - b
        },
        BinaryOps.MUL: {
            (DataType.INT, DataType.INT): lambda a, b: a * b
        },
        BinaryOps.DIV: {
            (DataType.INT, DataType.INT): lambda a, b: a / b
        },
        BinaryOps.MOD: {
            (DataType.INT, DataType.INT): lambda a, b: a % b
        },
        BinaryOps.MIN: {
            (DataType.INT, DataType.INT): lambda a, b: min(a, b)
        },
        BinaryOps.MAX: {
            (DataType.INT, DataType.INT): lambda a, b: max(a, b)
        },
        BinaryOps.BIT_AND: {
            (DataType.INT, DataType.INT): lambda a, b: a & b
        },
        BinaryOps.BIT_OR: {
            (DataType.INT, DataType.INT): lambda a, b: a | b
        },
        BinaryOps.BIT_XOR: {
            (DataType.INT, DataType.INT): lambda a, b: a ^ b
        },
        BinaryOps.SHL: {
            (DataType.INT, DataType.INT): lambda a, b: a << b
        },
        BinaryOps.SHR: {
            (DataType.INT, DataType.INT): lambda a, b: a >> b
        }
    }
    COMPARE_OP_HANDLERS: dict[CompareOps, dict[tuple[DataTypeBase, DataTypeBase], ...]] = {
        CompareOps.EQ: {
            (DataType.INT, DataType.INT): lambda a, b: a == b,
            (DataType.STRING, DataType.STRING): lambda a, b: a == b,
        },
        CompareOps.NE: {
            (DataType.INT, DataType.INT): lambda a, b: a != b,
            (DataType.STRING, DataType.STRING): lambda a, b: a != b,
        },
        CompareOps.LT: {
            (DataType.INT, DataType.INT): lambda a, b: a < b,
        },
        CompareOps.LE: {
            (DataType.INT, DataType.INT): lambda a, b: a <= b,
        },
        CompareOps.GT: {
            (DataType.INT, DataType.INT): lambda a, b: a > b,
        },
        CompareOps.GE: {
            (DataType.INT, DataType.INT): lambda a, b: a >= b,
        },
    }
    UNARY_OP_HANDLERS: dict[UnaryOps, dict[DataTypeBase, ...]] = {
        UnaryOps.NEG: {
            DataType.INT: lambda a: -a,
        },
        UnaryOps.NOT: {
            DataType.INT: lambda a: not a,
        },
        UnaryOps.BIT_NOT: {
            DataType.INT: lambda a: ~a,
        },
    }

    class FoldingFlags(Enum):
        UNKNOWN = auto()  # 未知/无法追踪变量
        UNDEFINED = auto()  # 未定义的变量

    @define(slots=True)
    class SymbolTable:
        """
            符号表实现，使用嵌套字典结构

            属性:

            table : 字典类型，映射符号名称到以下两种类型之一:
                Reference: 变量/函数的直接引用
                SymbolTable: 嵌套的作用域/子语言符号表
        """
        name: str = field(validator=validators.instance_of(str))
        stype: StructureType = field(validator=validators.instance_of(StructureType))
        table: dict[str, Reference | ConstantFoldingPass.FoldingFlags | ConstantFoldingPass.SymbolTable] = field(
            validator=validators.instance_of(dict), factory=dict)
        parent: ConstantFoldingPass.SymbolTable | None = field(default=None)

        def set(self, name: str, value: Reference | ConstantFoldingPass.FoldingFlags, depth=1) -> bool:
            if name in self.table:
                self.table[name] = value
                return True
            if self.parent is None:
                if depth > 1:
                    return False
                else:
                    self.table[name] = value
                    return True
            success = self.parent.set(name, value, depth + 1)
            if not success and depth == 1:
                self.table[name] = value
                return True
            else:
                return success

        def add(self, name: str, value: Reference | ConstantFoldingPass.FoldingFlags):
            self.table[name] = value

        def create_child(self, name: str, stype: StructureType) -> ConstantFoldingPass.SymbolTable:
            return ConstantFoldingPass.SymbolTable(name, parent=self, stype=stype)

        def find(self, name: str):
            if self.stype == StructureType.LOOP_CHECK:
                return ConstantFoldingPass.FoldingFlags.UNKNOWN
            if name in self.table:
                return self.table[name]
            if self.parent is None:
                return ConstantFoldingPass.FoldingFlags.UNDEFINED
            return self.parent.find(name)

    def __init__(self, builder: IRBuilder, config: GeneratorConfig):
        self.builder = builder
        self.symbol_table = ConstantFoldingPass.SymbolTable("global", StructureType.GLOBAL)
        self.current_table: ConstantFoldingPass.SymbolTable = self.symbol_table

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
        if isinstance(name, Literal):
            return Reference(ValueType.LITERAL, name)
        if isinstance(name, Reference) and name.value_type == ValueType.LITERAL:
            return name

        value = self.current_table.find(name.get_name())
        if value == ConstantFoldingPass.FoldingFlags.UNKNOWN:
            return value
        elif value == ConstantFoldingPass.FoldingFlags.UNDEFINED:
            return value
        elif value.value_type == ValueType.LITERAL:
            return value
        elif value.value_type == ValueType.FUNCTION:
            return value
        elif value.value_type in (ValueType.CONSTANT, ValueType.VARIABLE):
            return self._find(value)
        else:
            return ConstantFoldingPass.FoldingFlags.UNKNOWN

    def _resolve_ref(
            self,
            ref: Reference[Variable | Constant | Literal]
    ) -> Reference[Literal] | ConstantFoldingPass.FoldingFlags:
        if ref.value_type == ValueType.LITERAL:
            return ref
        else:
            return self._find(ref)

    @staticmethod
    def _is_literal(ref: Reference[Literal] | ConstantFoldingPass.FoldingFlags):
        return False if isinstance(ref, ConstantFoldingPass.FoldingFlags) else ref.value_type == ValueType.LITERAL

    def _handle_scope_end(self, iterator: IRBuilderIterator, instr: IRScopeEnd):
        self.current_table = self.current_table.parent

    def _handle_scope_begin(self, iterator: IRBuilderIterator, instr: IRScopeBegin):
        self.current_table: ConstantFoldingPass.SymbolTable = self.current_table.create_child(instr.get_operands()[0],
                                                                                              instr.get_operands()[1])

    def _assign(self, iterator: IRBuilderIterator, instr: IRAssign) -> None:
        """处理赋值"""
        target: Variable = instr.get_operands()[0]
        source: Reference[Variable | Constant | Literal] = instr.get_operands()[1]
        if source.value_type in (ValueType.VARIABLE, ValueType.CONSTANT):
            new_source = self._find(source)
            if new_source == ConstantFoldingPass.FoldingFlags.UNKNOWN:
                pass
            elif new_source == ConstantFoldingPass.FoldingFlags.UNDEFINED:
                raise RuntimeError(f"未定义的符号{source}")
            else:
                iterator.set_current(IRAssign(target, new_source))
                source = new_source

        self.current_table.set(target.get_name(), source)

    def _declare(self, iterator: IRBuilderIterator, instr: IRDeclare):
        var: Variable = instr.get_operands()[0]
        self.current_table.set(var.get_name(), ConstantFoldingPass.FoldingFlags.UNKNOWN)

    def _op(self, iterator: IRBuilderIterator, instr: IROp):
        result: Variable = instr.get_operands()[0]
        op: BinaryOps = instr.get_operands()[1]
        left_ref: Reference[Variable | Constant | Literal] = instr.get_operands()[2]
        right_ref: Reference[Variable | Constant | Literal] = instr.get_operands()[3]
        # 操作前将结果设为未知
        self.current_table.set(result.get_name(), ConstantFoldingPass.FoldingFlags.UNKNOWN)

        left = self._resolve_ref(left_ref)
        right = self._resolve_ref(right_ref)
        if not self._is_literal(left) or not self._is_literal(right):
            return
        left: Reference[Literal]
        right: Reference[Literal]
        handlers = self.BINARY_OP_HANDLERS.get(op, {})
        handler = handlers.get((DataType.INT if left.get_data_type() == DataType.BOOLEAN else left.get_data_type(),
                                DataType.INT if right.get_data_type() == DataType.BOOLEAN else right.get_data_type()))

        if handler:
            folded_value = handler(left.value.value, right.value.value)
            new_instr = IRAssign(result, Reference.literal(folded_value))
            iterator.set_current(new_instr)
            self._assign(iterator, new_instr)

    def _compare(self, iterator: IRBuilderIterator, instr: IRCompare):
        result: Variable = instr.get_operands()[0]
        op: CompareOps = instr.get_operands()[1]
        left_ref: Reference[Variable | Constant | Literal] = instr.get_operands()[2]
        right_ref: Reference[Variable | Constant | Literal] = instr.get_operands()[3]
        # 操作前将结果设为未知
        self.current_table.set(result.get_name(), ConstantFoldingPass.FoldingFlags.UNKNOWN)

        left = self._resolve_ref(left_ref)
        right = self._resolve_ref(right_ref)
        if not self._is_literal(left) or not self._is_literal(right):
            return
        left: Reference[Literal]
        right: Reference[Literal]
        handlers = self.COMPARE_OP_HANDLERS.get(op, {})
        handler = handlers.get((DataType.INT if left.get_data_type() == DataType.BOOLEAN else left.get_data_type(),
                                DataType.INT if right.get_data_type() == DataType.BOOLEAN else right.get_data_type()))

        if handler:
            folded_value = handler(left.value.value, right.value.value)
            new_instr = IRAssign(result, Reference.literal(folded_value))
            iterator.set_current(new_instr)
            self._assign(iterator, new_instr)

    def _unary_op(self, iterator: IRBuilderIterator, instr: IRUnaryOp):
        result: Variable = instr.get_operands()[0]
        op: UnaryOps = instr.get_operands()[1]
        operand_ref: Reference[Variable | Constant | Literal] = instr.get_operands()[2]
        # 操作前将结果设为未知
        self.current_table.set(result.get_name(), ConstantFoldingPass.FoldingFlags.UNKNOWN)

        operand = self._resolve_ref(operand_ref)
        if not self._is_literal(operand):
            return

        handlers = self.UNARY_OP_HANDLERS.get(op, {})
        handler = handlers.get(DataType.INT if operand.get_data_type() == DataType.BOOLEAN else operand.get_data_type())

        if handler:
            folded_value = handler(operand.value.value)
            new_instr = IRAssign(result, Reference.literal(folded_value))
            iterator.set_current(new_instr)
            self._assign(iterator, new_instr)

    def _cond_jump(self, iterator: IRBuilderIterator, instr: IRCondJump):
        cond_var: Variable = instr.get_operands()[0]
        true_scope: str = instr.get_operands()[1]
        false_scope: str = instr.get_operands()[2]
        value = self._find(cond_var)
        if isinstance(value, ConstantFoldingPass.FoldingFlags):
            return

        if cond_var.dtype in (DataType.INT, DataType.BOOLEAN):
            jump_scope = true_scope if value.value.value else false_scope
            if jump_scope:
                iterator.set_current(IRJump(jump_scope))
            else:
                iterator.remove_current()

    def _call(self, iterator: IRBuilderIterator, instr: IRCall):
        result: Variable | Constant = instr.get_operands()[0]
        func: Function = instr.get_operands()[1]
        args: dict[str, Reference[Variable | Constant | Literal]] = instr.get_operands()[2]
        new_args: dict[str, Reference[Variable | Constant | Literal]] = {}
        for param_name, arg_ref in args.items():
            arg = arg_ref.value

            if arg_ref.value_type in (ValueType.VARIABLE, ValueType.CONSTANT):
                arg_value = self._find(arg)
                if isinstance(arg_value, ConstantFoldingPass.FoldingFlags):  # 如果搜不到最终值
                    new_args[param_name] = arg_ref
                else:
                    new_args[param_name] = arg_value
            elif arg_ref.value_type == ValueType.LITERAL:
                new_args[param_name] = arg_ref
            else:  # 不应该出现，因为传参不可能为类或函数的定义
                raise
        iterator.set_current(instr.__class__(result, func, new_args))

    def _cast(self, iterator: IRBuilderIterator, instr: IRCast):
        result: Variable | Constant = instr.get_operands()[0]
        dtype: DataType | Class = instr.get_operands()[1]
        value_ref: Reference[Variable | Constant | Literal] = instr.get_operands()[2]

        # 操作前将结果设为未知
        self.current_table.set(result.get_name(), ConstantFoldingPass.FoldingFlags.UNKNOWN)

        value = self._resolve_ref(value_ref)
        if isinstance(value, ConstantFoldingPass.FoldingFlags):
            return

        if dtype == value_ref.get_data_type():
            iterator.set_current(IRAssign(result, value_ref))
            self._assign(iterator, iterator.current())  # NOQA
            return  # NOQA

        if dtype == DataType.STRING:
            if value.get_data_type() in (DataType.INT, DataType.BOOLEAN):
                self.current_table.set(result.get_name(),
                                       Reference(ValueType.LITERAL, Literal(DataType.STRING, str(value.value.value))))
                iterator.set_current(
                    IRAssign(result, Reference(ValueType.LITERAL, Literal(DataType.STRING, str(value.value.value)))))
                self._assign(iterator, iterator.current())  # NOQA

    def _function(self, iterator: IRBuilderIterator, instr: IRFunction):
        function: Function = instr.get_operands()[0]
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
                          (IRAssign, IRCast, IRReturn, IRCall, IROp, IRCompare, IRUnaryOp))

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
            elif isinstance(instr, IRCall):
                result_var, func, args = instr.get_operands()
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
                if scope_name in self.empty_scopes:
                    iterator.remove_current()
                    deleting_scope = scope_name
            elif isinstance(instr, IRScopeEnd):
                if deleting_scope is not None:
                    iterator.remove_current()
                    deleting_scope = None
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
