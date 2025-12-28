# coding=utf-8
from typing import SupportsIndex

from transpiler.core.instructions import IRInstruction, IROpCode


class IRBuilder:
    def __init__(self):
        self._instructions: list[IRInstruction] = []

    def insert(self, instruction: IRInstruction, index: SupportsIndex = None):
        if index is None:
            # 默认插入到末尾
            self._instructions.append(instruction)
        else:
            # 使用整数索引插入
            self._instructions.insert(index, instruction)

    def get_instructions(self):
        return self._instructions

    def __iter__(self):
        return IRBuilderIterator(self._instructions)

    def __reversed__(self):
        """返回可反转迭代器"""
        return IRBuilderReversibleIterator(self._instructions)

    def print(self):
        """格式化打印"""
        depth = 0
        for i in self:
            if i.opcode == IROpCode.SCOPE_END:
                depth -= 1
            print(depth * "    " + repr(i))
            if i.opcode == IROpCode.SCOPE_BEGIN:
                depth += 1


class IRBuilderIterator:
    def __init__(self, instructions: list[IRInstruction], index: int = 0):
        self.instructions = instructions
        self.index = index
        self._last_index = -1  # 跟踪最后返回的指令索引

    def __iter__(self):
        return self

    def __next__(self):
        if self.index >= len(self.instructions):
            raise StopIteration

        self._last_index = self.index
        item = self.instructions[self.index]
        self.index += 1
        return item

    def __reversed__(self):
        """转换为反向迭代器，保持当前位置"""
        # 计算反向迭代器的起始位置
        if self.index > 0:
            reverse_start_index = self.index - 1
        else:
            reverse_start_index = -1
        return IRBuilderReversibleIterator(self.instructions, reverse_start_index)

    def peek(self) -> IRInstruction:
        """
        查看下一条指令但不移动迭代器
        """
        if self.index >= len(self.instructions):
            raise StopIteration
        return self.instructions[self.index]

    def rollback(self, steps=1):
        """回退迭代位置"""
        self.index = min(max(0, self.index - steps), len(self.instructions))
        self._last_index = -1  # 重置最后返回位置

    def current(self) -> IRInstruction:
        """
            返回当前迭代到的指令（最后返回的指令）
        """
        if self._last_index == -1:
            raise IndexError(
                "No current instruction to remove (call next() first)")
        return self.instructions[self._last_index]

    def set_current(self, instr: IRInstruction):
        """
             设置当前迭代到的指令（最后返回的指令）
        """
        if self._last_index == -1:
            raise IndexError(
                "No current instruction to remove (call next() first)")
        self.instructions[self._last_index] = instr

    def remove_current(self) -> IRInstruction:
        """
        删除当前迭代到的指令（最后返回的指令）
        返回被删除的指令
        """
        if self._last_index == -1:
            raise IndexError(
                "No current instruction to remove (call next() first)")

        # 删除指令
        removed = self.instructions.pop(self._last_index)

        # 调整索引位置
        if self._last_index < self.index:
            self.index -= 1

        self._last_index = -1  # 重置最后返回位置

        return removed

    def remove_at(self, index: int) -> IRInstruction:
        """删除指定位置的指令"""
        if index < 0 or index >= len(self.instructions):
            raise IndexError("Index out of range")

        removed = self.instructions.pop(index)

        # 调整索引位置
        if index < self.index:
            self.index -= 1
        if index == self._last_index:
            self._last_index = -1

        return removed

    def insert_here(self, instruction: IRInstruction) -> None:
        self.instructions.insert(self.index, instruction)

    def insert_after_current(self, instruction: IRInstruction) -> None:
        if self._last_index == -1:
            raise IndexError("No current instruction (call next() first)")

        insert_index = self._last_index + 1

        if insert_index > len(self.instructions):
            self.instructions.append(instruction)
        else:
            self.instructions.insert(insert_index, instruction)

    def insert_and_continue_with(self, instruction: IRInstruction) -> None:
        """插入指令并让迭代器继续从该指令开始"""
        self.insert_here(instruction)
        self.rollback()


class IRBuilderReversibleIterator:
    """反向迭代器类"""

    def __init__(self, instructions: list[IRInstruction], index: int = None):
        self.instructions = instructions
        if index is None:
            self.index = len(instructions) - 1  # 默认从末尾开始
        else:
            self.index = index
        self._last_index = -1

    def __iter__(self):
        return self

    def __next__(self):
        if self.index < 0:
            raise StopIteration

        self._last_index = self.index
        item = self.instructions[self.index]
        self.index -= 1
        return item

    def __reversed__(self):
        """转换为正向迭代器，保持当前位置"""
        # 计算正向迭代器的起始位置
        if self.index < len(self.instructions) - 1:
            forward_start_index = self.index + 1
        else:
            forward_start_index = len(self.instructions)
        return IRBuilderIterator(self.instructions, forward_start_index)
