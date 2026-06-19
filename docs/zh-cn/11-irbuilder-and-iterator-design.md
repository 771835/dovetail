# IRBuilder 与迭代器设计

## IRBuilder

[dovetail/core/ir_builder.py](dovetail/core/ir_builder.py) 中的 `IRBuilder` 是 IR 指令序列的容器：

```python
class IRBuilder:
    def insert(instruction, index=None)  # 追加或插入指令

        def get_instructions() -> list  # 获取全部指令

        def __iter__()  # 返回 IRBuilderIterator

        def __reversed__()  # 返回 IRBuilderReversibleIterator

        def print()  # 缩进格式化打印 IR
```

`print()` 方法根据 `SCOPE_BEGIN`/`SCOPE_END` 自动调整缩进深度，用于 `--debug` 模式输出。

## IRBuilderIterator（正向迭代器）

正向遍历时支持**就地修改**操作：

```python
it = builder.__iter__()

it.peek()  # 查看下一条，不移动
it.current()  # 获取最后返回的指令
it.set_current(instr)  # 替换当前指令
it.remove_current()  # 删除当前指令，自动调整索引
it.remove_at(index)  # 删除指定位置指令
it.insert_here(instr)  # 在当前位置插入（当前指令之前）
it.insert_after_current(instr)  # 在当前指令之后插入
it.insert_and_continue_with(instr)  # 插入并回退，让下一次 next() 返回该指令
it.rollback(steps=1)  # 回退迭代位置
```

## IRBuilderReversibleIterator（反向迭代器）

从末尾向前遍历，同样支持修改操作。

## 双向转换协议

两个迭代器可以互相转换，且**不会跳过或重复处理任何指令**：

```python
# 正向 → 反向：从 index-1 开始
rev_iter = reversed(fwd_iter)

# 反向 → 正向：从 index+1 开始
fwd_iter = reversed(rev_iter)
```

这使得优化 Pass 可以在同一遍历中切换方向，例如先正向找到目标，再反向追溯依赖。

## 优化 Pass 使用模式

典型的 Pass 遍历模式：

```python
def execute(self) -> bool:
    changed = False
    iterator = self.builder.__iter__()
    for instr in iterator:
        if instr.opcode == IROpCode.ASSIGN:
            # 分析或修改
            iterator.set_current(new_instr)
            changed = True
    return changed
```

`execute()` 返回 `bool` 表示 IR 是否被修改，管道据此判断是否继续迭代。