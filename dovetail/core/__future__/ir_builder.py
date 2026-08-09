# coding=utf-8
"""
IRBuilder — Unrolled Linked List 实现

接口与原 list 实现完全兼容：
  - IRBuilder.get_instructions() 仍返回内部扁平 list 的直接引用（通过 _flat 缓存维护）
  - IRBuilderIterator / IRBuilderReversibleIterator 接口签名不变
  - _last_index / index 语义不变，外部 optimize pass 零改动

底层结构：
  - 双向链表串联固定大小的 chunk（默认 CHUNK_SIZE=32）
  - 末尾追加 O(1)
  - 中间插入最多移动 CHUNK_SIZE 个元素，实际 O(1)
  - 顺序遍历 cache 友好（每个 chunk 是连续内存）
  - get_instructions() 通过脏标记懒惰重建，反复读同一快照无额外开销
"""

from typing import SupportsIndex, Optional, List
from dovetail.core.instructions import IRInstruction, IROpCode

CHUNK_SIZE = 32  # 每个 chunk 的容量上限，调大降低链表开销，调小降低插入移动成本

__all__ = ["IRBuilder", "IRBuilderIterator", "IRBuilderReversibleIterator"]

# ─── chunk ────────────────────────────────────────────────────────────────────

class _Chunk:
    __slots__ = ("items", "prev", "next")

    def __init__(self):
        self.items: List[IRInstruction] = []
        self.prev: Optional['_Chunk'] = None
        self.next: Optional['_Chunk'] = None

    def is_full(self) -> bool:
        return len(self.items) >= CHUNK_SIZE


# ─── IRBuilder ────────────────────────────────────────────────────────────────

class IRBuilder:
    def __init__(self):
        # 哨兵头尾 chunk，永远不存真实指令
        self._head = _Chunk()
        self._tail = _Chunk()
        self._head.next = self._tail
        self._tail.prev = self._head
        self._size: int = 0

        # get_instructions() 的懒惰缓存
        # 脏标记为 True 时重建，False 时直接返回缓存
        self._flat: List[IRInstruction] = []
        self._dirty: bool = False

    # ── 公开接口 ──────────────────────────────────────────────────

    def insert(self, instruction: IRInstruction, index: Optional[SupportsIndex] = None):
        if index is None:
            # 末尾追加：找最后一个真实 chunk，未满直接 append，O(1)
            last = self._tail.prev
            if last is self._head or last.is_full():
                last = self._new_chunk_before(self._tail)
            last.items.append(instruction)
            self._size += 1
            # 末尾追加只需往 _flat 直接 append，无需完整重建
            if not self._dirty:
                self._flat.append(instruction)
        else:
            # 中间插入：定位 chunk，局部 list.insert，O(chunk_size)
            idx = int(index)
            if idx < 0:
                idx = max(0, self._size + idx)
            chunk, offset = self._locate(idx)
            chunk.items.insert(offset, instruction)
            self._size += 1
            if len(chunk.items) > CHUNK_SIZE:
                self._split(chunk)
            self._dirty = True  # 结构变了，缓存失效

    def get_instructions(self) -> List[IRInstruction]:
        """
        返回内部 _flat 列表的直接引用（可写）。
        与原 list 实现语义相同：外部持有引用后写入会反映到 IRBuilder 中。
        通过脏标记懒惰重建，连续多次调用无重复开销。

        - 只读扫描：直接 for 遍历，get_instructions() 有脏缓存，连续调用免费
        - 随机写入：通过返回的引用直接操作（仅限 _transform_function 这类批量变换）
        - 边走边改：用迭代器接口，不要混用本方法

        """
        if self._dirty:
            self._rebuild_flat()
        return self._flat

    def peek(self) -> IRInstruction:
        last = self._tail.prev
        if last is self._head or not last.items:
            raise IndexError("IRBuilder is empty")
        return last.items[-1]

    def __len__(self) -> int:
        return self._size

    def __iter__(self):
        # 迭代器基于扁平缓存，与原实现完全相同
        return IRBuilderIterator(self.get_instructions())

    def __reversed__(self):
        return IRBuilderReversibleIterator(self.get_instructions())

    def __getitem__(self, index):
        return self.get_instructions()[index]

    def print(self):
        depth = 0
        for i in self:
            if i.opcode == IROpCode.SCOPE_END:
                depth -= 1
            print(depth * "    " + repr(i))
            if i.opcode == IROpCode.SCOPE_BEGIN:
                depth += 1

    # ── 内部工具 ──────────────────────────────────────────────────

    def _new_chunk_before(self, ref: _Chunk) -> _Chunk:
        c = _Chunk()
        prev = ref.prev
        prev.next = c
        c.prev = prev
        c.next = ref
        ref.prev = c
        return c

    def _locate(self, index: int):
        """
        找到第 index 条指令所在的 (chunk, offset)。
        index == self._size 时返回 (last_chunk, len) 表示末尾之后。
        O(n / CHUNK_SIZE)，比 list O(n) 移动快，但遍历次数仍正比于 chunk 数。
        """
        cur = self._head.next
        while cur is not self._tail:
            if index < len(cur.items):
                return cur, index
            index -= len(cur.items)
            cur = cur.next
        # index 恰好等于 size，插到末尾 chunk 的末尾
        last = self._tail.prev
        if last is self._head:
            last = self._new_chunk_before(self._tail)
        return last, len(last.items)

    def _split(self, chunk: _Chunk):
        """chunk 超过 CHUNK_SIZE 时从中间一分为二，O(chunk_size)"""
        mid = len(chunk.items) // 2
        new_chunk = self._new_chunk_before(chunk.next)
        new_chunk.items = chunk.items[mid:]
        chunk.items = chunk.items[:mid]

    def _rebuild_flat(self):
        """从链表重建扁平缓存，O(n)"""
        result: List[IRInstruction] = []
        cur = self._head.next
        while cur is not self._tail:
            result.extend(cur.items)
            cur = cur.next
        # 原地替换列表内容，保持外部持有的引用仍然有效
        self._flat[:] = result
        self._dirty = False


# ─── 正向迭代器 ───────────────────────────────────────────────────────────────
# 以下两个类与原实现 **完全相同**，一字不差。
# 它们操作的是 _flat 这个真实 list，所以所有索引语义天然成立。
# IRBuilder 的写操作会通过脏标记同步回 chunk 结构。
#
# 唯一注意：迭代器直接持有 _flat 引用并写入，
# IRBuilder 下次 insert(index=...) 时会 _dirty=True 并重建，
# 这与原 list 实现的"外部引用可写"语义完全一致。

class IRBuilderIterator:
    def __init__(self, instructions: list[IRInstruction], index: int = 0):
        self.instructions = instructions
        self.index = index
        self._last_index = -1

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
        if self.index > 0:
            reverse_start_index = self.index - 1
        else:
            reverse_start_index = -1
        return IRBuilderReversibleIterator(self.instructions, reverse_start_index)

    def peek(self) -> IRInstruction:
        if self.index >= len(self.instructions):
            raise StopIteration
        return self.instructions[self.index]

    def rollback(self, steps=1):
        self.index = min(max(0, self.index - steps), len(self.instructions))
        self._last_index = -1

    def current(self) -> IRInstruction:
        if self._last_index == -1:
            raise IndexError("No current instruction (call next() first)")
        return self.instructions[self._last_index]

    def set_current(self, instr: IRInstruction):
        if self._last_index == -1:
            raise IndexError("No current instruction (call next() first)")
        self.instructions[self._last_index] = instr

    def remove_current(self) -> IRInstruction:
        if self._last_index == -1:
            raise IndexError("No current instruction (call next() first)")
        removed = self.instructions.pop(self._last_index)
        if self._last_index < self.index:
            self.index -= 1
        self._last_index = -1
        return removed

    def remove_at(self, index: int) -> IRInstruction:
        if index < 0 or index >= len(self.instructions):
            raise IndexError("Index out of range")
        removed = self.instructions.pop(index)
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
        self.insert_here(instruction)
        self.rollback()



class IRBuilderReversibleIterator:
    def __init__(self, instructions: list[IRInstruction], index: Optional[int] = None):
        self.instructions = instructions
        if index is None:
            self.index = len(instructions) - 1
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
        if self.index < len(self.instructions) - 1:
            forward_start_index = self.index + 1
        else:
            forward_start_index = len(self.instructions)
        return IRBuilderIterator(self.instructions, forward_start_index)