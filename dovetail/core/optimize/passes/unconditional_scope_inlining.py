# coding=utf-8
"""
无条件跳转作用域提升 Pass

将"必然执行"的条件作用域内联展开。

识别模式：
    scope xxx (CONDITIONAL) {
        ...instructions...
    }
    goto xxx

由于 goto 无条件跳入，该作用域必然执行，
直接将其内容提升到外层，消除多余的作用域包装。
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
    name="unconditional_scope_inlining",
    display_name="无条件作用域内联",
    description="将紧随无条件 goto 的条件作用域内容提升到外层，消除冗余作用域包装",
    level=OptimizationLevel.O1,
    phase=PassPhase.CLEANUP,
    provided_features=("inlined_unconditional_scopes",)
))
class UnconditionalScopeInliningPass(IROptimizationPass):
    """
    无条件作用域内联优化 Pass

    算法：两遍扫描
      第一遍：找出所有"后面紧跟 goto 自身"的条件作用域，
              记录其内容指令列表 → inlinable_scopes
      第二遍：遍历 IR，将这些作用域的 SCOPE_BEGIN/SCOPE_END
              以及对应的 JUMP 指令删除，把内容原地展开
    """

    def __init__(self, builder: IRBuilder, config: CompileConfig):
        super().__init__(builder, config)
        self._changed = False

    def execute(self) -> bool:
        self._changed = False

        # 第一遍：收集可内联的作用域
        inlinable = self._find_inlinable_scopes()
        if not inlinable:
            return False

        # 第二遍：展开
        self._inline_scopes(inlinable)
        return self._changed

    # ------------------------------------------------------------------ #
    #  第一遍：找出可内联的作用域                                            #
    # ------------------------------------------------------------------ #

    def _find_inlinable_scopes(self) -> set[str]:
        """
        扫描 IR，找出满足以下条件的作用域名称：
          1. 类型是 CONDITIONAL
          2. 在 SCOPE_END 后紧跟着 JUMP 到自身

        Returns:
            可内联的作用域名称集合
        """
        instructions = list(self.builder.get_instructions())
        inlinable: set[str] = set()

        # 先收集所有 CONDITIONAL 作用域的 end 位置
        # scope_end_idx[scope_name] = index of its SCOPE_END instruction
        conditional_scopes: set[str] = set()
        scope_end_idx: dict[str, int] = {}
        scope_stack: list[str] = []

        for idx, instr in enumerate(instructions):
            if instr.opcode == IROpCode.SCOPE_BEGIN:
                scope_name = instr.get_operands()[0]
                scope_type = instr.get_operands()[1]
                scope_stack.append(scope_name)
                if scope_type == StructureType.CONDITIONAL:
                    conditional_scopes.add(scope_name)

            elif instr.opcode == IROpCode.SCOPE_END:
                if scope_stack:
                    finished = scope_stack.pop()
                    scope_end_idx[finished] = idx

        # 检查每个 CONDITIONAL 作用域的 SCOPE_END 后面是否紧跟 JUMP 到自身
        for idx, instr in enumerate(instructions):
            if instr.opcode == IROpCode.JUMP:
                target = instr.get_operands()[0]
                if target not in conditional_scopes:
                    continue
                # JUMP 前一条（跳过中间可能的空行，这里直接看紧邻）
                # 找到该 scope 的 SCOPE_END 位置，看是否就在 JUMP 的前一条
                end_idx = scope_end_idx.get(target)
                if end_idx is not None and end_idx == idx - 1:
                    inlinable.add(target)

        return inlinable

    # ------------------------------------------------------------------ #
    #  第二遍：展开作用域                                                    #
    # ------------------------------------------------------------------ #

    def _inline_scopes(self, inlinable: set[str]) -> None:
        """
        遍历 IR：
          - 遇到 SCOPE_BEGIN(name in inlinable) → 删除
          - 遇到 SCOPE_END，且当前正在展开 → 删除
          - 遇到 JUMP(target in inlinable) → 删除
          - 作用域内的其他指令 → 原样保留（已在外层，不需要移动）
        """
        iterator = self.builder.__iter__()
        inlining_stack: list[str] = []  # 正在被内联的作用域栈

        for instr in iterator:

            if instr.opcode == IROpCode.SCOPE_BEGIN:
                scope_name = instr.get_operands()[0]
                if scope_name in inlinable:
                    # 删除 SCOPE_BEGIN，开始内联模式
                    inlining_stack.append(scope_name)
                    iterator.remove_current()
                    self._changed = True

            elif instr.opcode == IROpCode.SCOPE_END:
                if inlining_stack:
                    # 对应被内联作用域的 SCOPE_END，删掉
                    inlining_stack.pop()
                    iterator.remove_current()
                    self._changed = True

            elif instr.opcode == IROpCode.JUMP:
                target = instr.get_operands()[0]
                if target in inlinable:
                    # 删除无条件跳转
                    iterator.remove_current()
                    self._changed = True