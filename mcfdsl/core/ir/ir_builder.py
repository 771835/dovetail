# coding=utf-8
from typing import SupportsIndex

from mcfdsl.core.ir.instructions import IRInstruction


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


class IRBuilderIterator:
    def __init__(self, instructions: list[IRInstruction]):
        self.instructions = instructions
        self.index = 0
        self._last_index = -1  # 跟踪最后返回的指令索引

    def __iter__(self):
        return self

    def __next__(self):
        if self.index >= len(self.instructions):
            raise StopIteration

        self._last_index = self.index
        item = self.instructions[self.index]
        self.index += 1
        # print(f"返回指令: {item} | 位置: {self._last_index} | 下一索引: {self.index}")
        # # 调试
        return item

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
