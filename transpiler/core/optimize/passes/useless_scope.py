# coding=utf-8
"""
无用作用域移除 Pass

移除不可达的作用域及其内容。
"""
from __future__ import annotations

from transpiler.core.compile_config import CompileConfig
from transpiler.core.enums import OptimizationLevel
from transpiler.core.instructions import *
from transpiler.core.ir_builder import IRBuilder
from transpiler.core.optimize.base import IROptimizationPass
from transpiler.core.optimize.pass_metadata import PassMetadata, PassPhase
from transpiler.core.optimize.pass_registry import register_pass


@register_pass(PassMetadata(
    name="useless_scope_removal",
    display_name="无用作用域移除",
    description="移除不可达的作用域及其内容",
    level=OptimizationLevel.O2,
    phase=PassPhase.CLEANUP,
    provided_features=("removed_useless_scopes",)
))
class UselessScopeRemovalPass(IROptimizationPass):
    """无用作用域移除优化 Pass"""

    def __init__(self, builder: IRBuilder, config: CompileConfig):
        super().__init__(builder, config)
        self.scope_reachability = {}
        self.scope_instructions = {}
        self.jump_targets = set()
        self.root_scopes = set()
        self._changed = False

    def execute(self) -> bool:
        """执行无用作用域删除优化"""
        self._changed = False
        self._build_scope_structure()
        self._analyze_reachability()
        self._remove_unreachable_scopes()
        return self._changed

    def _build_scope_structure(self):
        """构建作用域结构"""
        iterator = self.builder.__iter__()
        current_scope = "global"
        scope_stack = []

        while True:
            try:
                instr = next(iterator)
            except StopIteration:
                break

            if isinstance(instr, (IRJump, IRCondJump)):
                targets = [op for op in instr.get_operands() if isinstance(op, str)]
                self.jump_targets.update(targets)

            if isinstance(instr, IRScopeBegin):
                scope_name = instr.get_operands()[0]
                scope_type = instr.get_operands()[1]

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

            if current_scope in self.scope_instructions:
                self.scope_instructions[current_scope].append(instr)

    def _analyze_reachability(self):
        """分析作用域可达性"""
        for scope in self.scope_instructions:
            self.scope_reachability[scope] = False

        for root in self.root_scopes:
            if root in self.scope_instructions:
                self._dfs_reachability(root)

    def _dfs_reachability(self, scope_name):
        """深度优先遍历可达作用域"""
        if self.scope_reachability.get(scope_name, False):
            return

        self.scope_reachability[scope_name] = True

        for instr in self.scope_instructions.get(scope_name, []):
            if isinstance(instr, (IRJump, IRCondJump)):
                targets = [op for op in instr.get_operands() if isinstance(op, str)]
                for target in targets:
                    if target in self.scope_instructions:
                        self._dfs_reachability(target)

    def _remove_unreachable_scopes(self):
        """删除不可达作用域及其指令"""
        iterator = self.builder.__iter__()
        scopes_to_remove = set()

        for scope, reachable in self.scope_reachability.items():
            if not reachable and scope not in self.root_scopes:
                scopes_to_remove.add(scope)

        delete_level = 0

        while True:
            try:
                instr = next(iterator)
            except StopIteration:
                break

            if delete_level == 0 and isinstance(instr, IRScopeBegin):
                scope_name = instr.get_operands()[0]
                if scope_name in scopes_to_remove:
                    iterator.remove_current()
                    self._changed = True
                    delete_level = 1

            elif delete_level > 0:
                if isinstance(instr, IRScopeBegin):
                    delete_level += 1
                elif isinstance(instr, IRScopeEnd):
                    delete_level -= 1
                    iterator.remove_current()
                    self._changed = True
                else:
                    iterator.remove_current()
                    self._changed = True
