# coding=utf-8
"""
死代码消除 Pass

移除永远不会使用的变量赋值和计算结果。
"""
from collections import deque

from dovetail.core.compile_config import CompileConfig
from dovetail.core.enums import OptimizationLevel
from dovetail.core.enums.types import ValueType, VariableType
from dovetail.core.instructions import *
from dovetail.core.ir_builder import IRBuilder
from dovetail.core.optimize.base import IROptimizationPass
from dovetail.core.optimize.pass_metadata import PassMetadata, PassPhase
from dovetail.core.optimize.pass_registry import register_pass
from dovetail.core.symbols import Reference


@register_pass(PassMetadata(
    name="dead_code_elimination",
    display_name="死代码消除",
    description="移除永远不会使用的变量赋值和计算结果",
    level=OptimizationLevel.O1,
    phase=PassPhase.CLEANUP,
    provided_features=("cleaned_dead_code",)
))
class DeadCodeEliminationPass(IROptimizationPass):
    """死代码消除优化 Pass"""

    def __init__(self, builder: IRBuilder, config: CompileConfig):
        super().__init__(builder, config)
        self.def_use_graph = {}
        self.use_def_graph = {}
        self.live_vars = set()
        self.declared_vars = set()
        self._changed = False

    def execute(self) -> bool:
        """执行死代码消除优化"""
        self._changed = False
        self._build_dependency_graph()
        self._propagate_liveness()
        self._remove_dead_code()
        return self._changed

    def _build_dependency_graph(self):
        """构建定义使用/使用定义依赖图"""
        for instr in self.builder.get_instructions():
            if instr.opcode == IROpCode.DECLARE:
                var = instr.get_operands()[0]
                self.declared_vars.add(id(var))
                continue

            if instr.opcode == IROpCode.ASSIGN:
                target, source = instr.get_operands()
                target_id = id(target)
                self.def_use_graph[target_id] = []
                if isinstance(source, Reference) and source.value_type == ValueType.VARIABLE:
                    source_id = id(source.value)
                    if source_id not in self.use_def_graph:
                        self.use_def_graph[source_id] = []
                    self.use_def_graph[source_id].append(target_id)
                    self.def_use_graph[target_id].append(source_id)

            elif instr.opcode in (IROpCode.BINARY_OP, IROpCode.COMPARE, IROpCode.UNARY_OP):
                operands = instr.get_operands()
                result = operands[0]
                result_id = id(result)
                self.def_use_graph[result_id] = []

                for op in operands[2:]:
                    if isinstance(op, Reference) and op.value_type == ValueType.VARIABLE:
                        op_id = id(op.value)
                        if op_id not in self.use_def_graph:
                            self.use_def_graph[op_id] = []
                        self.use_def_graph[op_id].append(result_id)
                        self.def_use_graph[result_id].append(op_id)

            elif instr.opcode == IROpCode.CAST:
                result, dtype, value_ref = instr.get_operands()
                result_id = id(result)
                self.def_use_graph[result_id] = []

                if isinstance(value_ref, Reference) and value_ref.value_type == ValueType.VARIABLE:
                    var_id = id(value_ref.value)
                    if var_id not in self.use_def_graph:
                        self.use_def_graph[var_id] = []
                    self.use_def_graph[var_id].append(result_id)
                    self.def_use_graph[result_id].append(var_id)

    def _propagate_liveness(self):
        """传播活跃变量"""
        work_list = deque()

        for instr in self.builder.get_instructions():
            if instr.opcode == IROpCode.DECLARE:
                var = instr.get_operands()[0]
                if var.var_type in (VariableType.PARAMETER, VariableType.RETURN):
                    var_id = id(var)
                    self.live_vars.add(var_id)
                    work_list.append(var_id)
            elif instr.opcode == IROpCode.CALL:
                # 标记所有参数为活跃
                args = instr.get_operands()[2]
                for param_name, arg_ref in args.items():
                    if isinstance(arg_ref, Reference) and arg_ref.value_type == ValueType.VARIABLE:
                        var_id = id(arg_ref.value)
                        if var_id not in self.live_vars:
                            self.live_vars.add(var_id)
                            work_list.append(var_id)
            elif instr.opcode == IROpCode.COND_JUMP:
                cond_var = instr.get_operands()[0]
                if isinstance(cond_var, Reference) and cond_var.value_type == ValueType.VARIABLE:
                    var_id = id(cond_var.value)
                    if var_id not in self.live_vars:
                        self.live_vars.add(var_id)
                        work_list.append(var_id)
            elif instr.opcode == IROpCode.CAST:
                result, dtype, value_ref = instr.get_operands()
                if (isinstance(value_ref, Reference) and value_ref.value_type == ValueType.VARIABLE and
                        id(value_ref.value) in self.live_vars and id(result) not in self.live_vars):
                    self.live_vars.add(id(result))
                    work_list.append(id(result))
            elif self._has_side_effect(instr):
                for op in instr.get_operands():
                    if isinstance(op, Reference) and op.value_type == ValueType.VARIABLE:
                        var_id = id(op.value)
                        if var_id not in self.live_vars:
                            self.live_vars.add(var_id)
                            work_list.append(var_id)

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
                instr = next(iterator)
            except StopIteration:
                break

            if instr.opcode == IROpCode.ASSIGN:
                target, source = instr.get_operands()
                target_id = id(target)
                if not self._is_declaration_exists(target) or target_id not in self.live_vars:
                    iterator.remove_current()
                    self._changed = True

            elif instr.opcode in (IROpCode.BINARY_OP, IROpCode.COMPARE, IROpCode.UNARY_OP, IROpCode.CAST):
                result = instr.get_operands()[0]
                result_id = id(result)
                if result_id not in self.live_vars:
                    iterator.remove_current()
                    self._changed = True

    def _has_side_effect(self, instr):
        """判断指令是否有副作用"""
        return instr.opcode in (
            IROpCode.ASSIGN, IROpCode.CAST, IROpCode.RETURN, IROpCode.RETURN,
            IROpCode.CALL, IROpCode.CALL_METHOD, IROpCode.NEW_OBJ, IROpCode.GET_PROPERTY, IROpCode.SET_PROPERTY,
            IROpCode.BINARY_OP, IROpCode.UNARY_OP, IROpCode.COMPARE
        )

    def _is_declaration_exists(self, var):
        """检查变量声明是否存在"""
        return id(var) in self.declared_vars
