# coding=utf-8
class PeekableCounter:
    def __init__(self, start=0, step=1):
        self.current = start
        self.step = step

    def __iter__(self):
        return self

    def __next__(self):
        val = self.current
        self.current += self.step
        return val

    def peek(self):
        """查看当前值，但不改变状态"""
        return self.current