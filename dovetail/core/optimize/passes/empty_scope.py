# coding=utf-8
"""
空作用域移除 Pass

移除没有任何指令的空作用域。
"""
from __future__ import annotations

from dovetail.core.compile_config import CompileConfig
from dovetail.core.enums import OptimizationLevel
from dovetail.core.instructions import *
from dovetail.core.ir_builder import IRBuilder
from dovetail.core.optimize.base import IROptimizationPass
from dovetail.core.optimize.pass_metadata import PassMetadata, PassPhase
from dovetail.core.optimize.pass_registry import register_pass


@register_pass(PassMetadata(
    name="empty_scope_removal",
    display_name="空作用域移除",
    description="移除没有任何指令的空作用域",
    level=OptimizationLevel.O1,
    phase=PassPhase.CLEANUP,
    provided_features=("removed_empty_scopes",)
))
class EmptyScopeRemovalPass(IROptimizationPass):
    """空作用域移除优化 Pass"""

    def __init__(self, builder: IRBuilder, config: CompileConfig):
        super().__init__(builder, config)
        self.scope_instructions = {}
        self.empty_scopes = set()
        self._changed = False

    def execute(self) -> bool:
        """执行空作用域及跳转指令删除优化"""
        self._changed = False
        self._build_scope_structure()
        self._detect_empty_scopes()
        self._remove_jump_to_empty_scopes()
        self._remove_empty_scope_declarations()
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

            if instr.opcode == IROpCode.SCOPE_BEGIN:
                scope_name = instr.get_operands()[0]
                scope_stack.append(scope_name)
                current_scope = scope_name
                self.scope_instructions[scope_name] = []
            elif instr.opcode == IROpCode.SCOPE_END:
                if scope_stack:
                    scope_stack.pop()
                    current_scope = scope_stack[-1] if scope_stack else "global"
            else:
                if current_scope in self.scope_instructions:
                    self.scope_instructions[current_scope].append(instr)

    def _detect_empty_scopes(self):
        """检测空作用域"""
        for scope, instructions in self.scope_instructions.items():
            if not instructions:
                self.empty_scopes.add(scope)

    def _remove_jump_to_empty_scopes(self):
        iterator = self.builder.__iter__()
        while True:
            try:
                instr = next(iterator)
            except StopIteration:
                break

            if instr.opcode == IROpCode.JUMP:
                if instr.operands[0] in self.empty_scopes:
                    iterator.remove_current()
                    self._changed = True

            elif instr.opcode == IROpCode.COND_JUMP:
                a = None if instr.operands[1] in self.empty_scopes else instr.operands[1]
                b = None if instr.operands[2] in self.empty_scopes else instr.operands[2]
                if a is None and b is None:
                    iterator.remove_current()
                    self._changed = True
                elif a != instr.operands[1] or b != instr.operands[2]:
                    # 有操作数发生变化，原地更新，不触碰迭代器位置
                    instr.operands[1] = a
                    instr.operands[2] = b
                    self._changed = True

    def _remove_empty_scope_declarations(self):
        """删除空作用域的指令"""
        iterator = self.builder.__iter__()
        deleting_stack = []  # 用栈记录

        while True:
            try:
                instr = next(iterator)
            except StopIteration:
                break

            if instr.opcode == IROpCode.SCOPE_BEGIN:
                scope_name = instr.get_operands()[0]
                stype = instr.get_operands()[1]
                if deleting_stack:
                    # 已在删除模式中，子作用域也一并删除
                    iterator.remove_current()
                    self._changed = True
                    deleting_stack.append(scope_name)  # 压栈，追踪嵌套层数
                elif scope_name in self.empty_scopes and stype not in (StructureType.FUNCTION, StructureType.CLASS):
                    iterator.remove_current()
                    self._changed = True
                    deleting_stack.append(scope_name)  # 开始删除模式

            elif instr.opcode == IROpCode.SCOPE_END:
                if deleting_stack:
                    iterator.remove_current()
                    self._changed = True
                    deleting_stack.pop()  # 出栈，正确对应嵌套层数

            elif instr.opcode in (IROpCode.FUNCTION, IROpCode.CLASS):
                pass
            else:
                if deleting_stack:
                    iterator.remove_current()
                    self._changed = True
