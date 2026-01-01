# coding=utf-8
"""
未使用函数消除 Pass

移除从未被调用的函数。
"""
from __future__ import annotations

from transpiler.core.compile_config import CompileConfig
from transpiler.core.enums import OptimizationLevel
from transpiler.core.instructions import *
from transpiler.core.ir_builder import IRBuilder
from transpiler.core.optimize.base import IROptimizationPass
from transpiler.core.optimize.pass_metadata import PassMetadata, PassPhase
from transpiler.core.optimize.pass_registry import register_pass
from transpiler.core.symbols import Function


@register_pass(PassMetadata(
    name="unused_function_elimination",
    display_name="未使用函数消除",
    description="移除从未被调用的函数",
    level=OptimizationLevel.O1,
    phase=PassPhase.CLEANUP,
    provided_features=("removed_unused_functions",)
))
class UnusedFunctionEliminationPass(IROptimizationPass):
    """未使用函数消除优化 Pass"""

    def __init__(self, builder: IRBuilder, config: CompileConfig):
        super().__init__(builder, config)
        self.function_calls = {}
        self.function_declarations: dict[str, Function] = {}
        self._changed = False

    def execute(self) -> bool:
        """执行未使用函数消除优化"""
        self._changed = False
        self._analyze_functions()
        self._remove_unused_functions()
        return self._changed

    def _analyze_functions(self):
        """分析函数调用和声明"""
        iterator = self.builder.__iter__()

        while True:
            try:
                instr = next(iterator)
            except StopIteration:
                break

            if isinstance(instr, IRFunction):
                func = instr.get_operands()[0]
                self.function_declarations[func.name] = func

            elif isinstance(instr, IRCall):
                func = instr.get_operands()[1]
                self.function_calls[func.name] = self.function_calls.get(func.name, 0) + 1

            elif isinstance(instr, IRCallMethod):
                func = instr.get_operands()[2]
                method_name = func.name
                self.function_calls[method_name] = self.function_calls.get(method_name, 0) + 1

    def _remove_unused_functions(self):
        """删除未使用的函数"""

        for func_name, func in self.function_declarations.items():
            if func_name not in self.function_calls:
                if not func.annotations:  # 保留带有注解的函数
                    self._remove_function(func_name)

    def _remove_function(self, func_name):
        """删除指定函数"""
        iterator = self.builder.__iter__()
        in_function = False
        level = 0

        while True:
            try:
                instr = next(iterator)
            except StopIteration:
                break

            if isinstance(instr, IRFunction):
                func = instr.get_operands()[0]
                if func.name == func_name:
                    iterator.remove_current()
                    self._changed = True
                    in_function = True
                    continue

            if in_function:
                if isinstance(instr, IRScopeBegin):
                    level += 1
                elif isinstance(instr, IRScopeEnd):
                    level -= 1
                    if level == 0:
                        in_function = False
                        continue

                iterator.remove_current()
                self._changed = True
