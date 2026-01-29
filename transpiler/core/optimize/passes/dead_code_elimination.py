# coding=utf-8
"""
死代码消除 Pass

移除永远不会使用的变量赋值和计算结果。
"""
from __future__ import annotations

from collections import deque

from transpiler.core.compile_config import CompileConfig
from transpiler.core.enums import OptimizationLevel
from transpiler.core.enums.types import ValueType, VariableType
from transpiler.core.instructions import *
from transpiler.core.ir_builder import IRBuilder
from transpiler.core.optimize.base import IROptimizationPass
from transpiler.core.optimize.pass_metadata import PassMetadata, PassPhase
from transpiler.core.optimize.pass_registry import register_pass
from transpiler.core.symbols import Reference


# FIXME:不同作用域下定义的同名变量都会被标记为活跃

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
        iterator = self.builder.__iter__()

        for instr in iterator:
            if isinstance(instr, IRAssign):
                target, source = instr.get_operands()
                self.def_use_graph[target.name] = []
                if isinstance(source, Reference) and source.value_type == ValueType.VARIABLE:
                    if source.get_name() not in self.use_def_graph:
                        self.use_def_graph[source.get_name()] = []
                    self.use_def_graph[source.get_name()].append(target.get_name())
                    self.def_use_graph[target.get_name()].append(source.get_name())

            elif isinstance(instr, (IRBinaryOp, IRCompare, IRUnaryOp)):
                operands = instr.get_operands()
                result = operands[0]
                self.def_use_graph[result.name] = []

                for op in operands[2:]:
                    if isinstance(op, Reference) and op.value_type == ValueType.VARIABLE:
                        if op.get_name() not in self.use_def_graph:
                            self.use_def_graph[op.get_name()] = []
                        self.use_def_graph[op.get_name()].append(result.get_name())
                        self.def_use_graph[result.get_name()].append(op.get_name())
            elif isinstance(instr, IRCast):
                result, dtype, value_ref = instr.get_operands()
                self.def_use_graph[result.name] = []

                if isinstance(value_ref, Reference) and value_ref.value_type == ValueType.VARIABLE:
                    var_name = value_ref.get_name()
                    if var_name not in self.use_def_graph:
                        self.use_def_graph[var_name] = []
                    self.use_def_graph[var_name].append(result.get_name())
                    self.def_use_graph[result.get_name()].append(var_name)

    def _propagate_liveness(self):
        """传播活跃变量"""
        work_list = deque()

        for instr in self.builder.get_instructions():
            if isinstance(instr, IRDeclare):
                var = instr.get_operands()[0]
                if var.var_type in (VariableType.PARAMETER, VariableType.RETURN):
                    self.live_vars.add(var.name)
                    work_list.append(var.name)
            elif isinstance(instr, IRCall):
                # 标记所有参数为活跃
                args = instr.get_operands()[2]
                for param_name, arg_ref in args.items():
                    if isinstance(arg_ref, Reference) and arg_ref.value_type == ValueType.VARIABLE:
                        var_name = arg_ref.get_name()
                        if var_name not in self.live_vars:
                            self.live_vars.add(var_name)
            elif isinstance(instr, IRCondJump):
                cond_var = instr.get_operands()[0]
                if isinstance(cond_var, type(instr.get_operands()[0])):
                    if cond_var.name not in self.live_vars:
                        self.live_vars.add(cond_var.name)
                        work_list.append(cond_var.name)
            elif isinstance(instr, IRCast):
                result, dtype, value_ref = instr.get_operands()
                if (isinstance(value_ref, Reference) and value_ref.value_type == ValueType.VARIABLE and
                        value_ref.get_name() in self.live_vars and result.name not in self.live_vars):
                    self.live_vars.add(result.name)
                    work_list.append(result.name)
            elif self._has_side_effect(instr):
                for op in instr.get_operands():
                    if isinstance(op, Reference) and op.value_type == ValueType.VARIABLE:
                        if op.get_name() not in self.live_vars:
                            self.live_vars.add(op.get_name())
                            work_list.append(op.get_name())

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

            if isinstance(instr, IRAssign):
                target, source = instr.get_operands()
                if not self._is_declaration_exists(target.name):
                    iterator.remove_current()
                    self._changed = True
                elif target.name not in self.live_vars:
                    iterator.remove_current()
                    self._changed = True

            elif isinstance(instr, (IRBinaryOp, IRCompare, IRUnaryOp, IRCast)):
                result = instr.get_operands()[0]
                if result.name not in self.live_vars:
                    iterator.remove_current()
                    self._changed = True

    def _has_side_effect(self, instr):
        """判断指令是否有副作用"""
        return isinstance(instr, (
            IRAssign, IRCast, IRReturn, IRCall, IRCallMethod, IRNewObj,
            IRGetProperty, IRSetProperty, IRBinaryOp, IRCompare, IRUnaryOp
        ))

    def _is_declaration_exists(self, var_name):
        """检查变量声明是否存在"""
        for instr in self.builder.get_instructions():
            if isinstance(instr, IRDeclare) and instr.get_operands()[0].name == var_name:
                return True
        return False
