# 处理器注册表与 IR 分发

## 概述

后端代码生成的核心机制是**分发**：遍历每条 `IRInstruction`，根据其 `opcode` 查找对应的 `IRProcessor`，调用 `process()` 生成
Minecraft 命令。

相关文件：

- [dovetail/core/backend/processor.py](dovetail/core/backend/processor.py) — 处理器基类与注册表
- [dovetail/core/backend/context.py](dovetail/core/backend/context.py) — 生成上下文

---

## IRProcessor 基类

```python
class IRProcessor(ABC):
    opcode: IROpCode = None  # 子类必须指定，对应要处理的操作码

    @abstractmethod
    def process(self, instruction: IRInstruction, context: GenerationContext):
        """处理单条 IR 指令，向 context 写入生成的命令"""
        ...

    def can_handle(self, instruction) -> bool:
        return instruction.opcode == self.opcode
```

---

## ProcessorRegistry

每个 `Backend` 子类通过 `BackendMeta` 元类拥有**独立的** `ProcessorRegistry` 实例：

```python
class ProcessorRegistry:
    def register(processor: IRProcessor)

        def register_class(processor_class: type[IRProcessor])  # 自动实例化

        def register_batch(processors: list[IRProcessor])  # 批量注册

        def get_processor(opcode: IROpCode) -> IRProcessor  # 查找，未找到返回 DefaultProcessor

        def has_processor(opcode: IROpCode) -> bool

        def get_all_opcodes() -> list[IROpCode]

        def clear()
```

### DefaultProcessor

当某个 opcode 没有注册处理器时，`DefaultProcessor` 会向输出写入一条警告注释，并通过日志记录：

```
# WARNING: No processor for ASSIGN(赋值)
```

这使得后端不会因为未实现的 opcode 而崩溃，但会在输出中留下可见的警告。

---

## @ir_processor 注册装饰器

```python
from dovetail.core.backend.processor import ir_processor, IRProcessor
from dovetail.core.backend.base import Backend
from dovetail.core.instructions import IROpCode


@ir_processor(MyBackend, IROpCode.ASSIGN)
class AssignProcessor(IRProcessor):
    def process(self, instruction, context):
        target, source = instruction.get_operands()
        context.add_command(
            f"scoreboard players operation {target.get_name()} dovetail = {source.get_name()} dovetail"
        )
```

装饰器同时完成两件事：

1. 将 `cls.opcode` 设为指定操作码
2. 调用 `target.processor_registry.register_class(cls)` 注册到目标后端

也可以直接传入 `ProcessorRegistry` 实例而非 `Backend` 类。

---

## GenerationContext

[dovetail/core/backend/context.py](dovetail/core/backend/context.py) 中的 `GenerationContext` 是处理器之间共享的状态容器，贯穿整个代码生成过程：

```python
@define
class GenerationContext:
    config: CompileConfig
    target: Path  # 输出目录
    ir_builder: IRBuilder
    # ... 当前作用域、命令缓冲、符号信息等
```

### Scope（后端上下文中的作用域）

后端有自己的 `Scope` 数据结构（与前端的 `Scope` 不同），用于追踪代码生成时的层级结构：

```python
@define
class Scope:
    name: str
    scope_type: StructureType
    parent: Scope | None
    children: list[Scope]
    commands: list[str]  # 该作用域生成的命令列表
    symbols: dict[str, Symbol]
    flags: dict[str, Any]

    def add_command(command: str)

        def has_commands() -> bool

        def get_absolute_path(separator='.') -> str  # 用于生成 mcfunction 文件路径

        def get_file_path() -> Path
```

`get_absolute_path()` 处理了同名子作用域的消歧（追加 `-N` 后缀），确保生成的 `.mcfunction` 文件路径唯一。

### PackMcmeta

`context.py` 还包含 `PackMcmeta` 类，负责生成和序列化 `pack.mcmeta` 文件，并根据目标 Minecraft 版本选择不同的格式：

| 版本范围            | 格式字段                                    |
|-----------------|-----------------------------------------|
| < 1.20.2        | `pack_format`（单值）                       |
| 1.20.2 - 1.21.8 | `pack_format` + `supported_formats`（范围） |
| ≥ 1.21.9        | `min_format` + `max_format`（新格式）        |

### DependencyFile

表示后端需要下载的前置数据包依赖：

```python
@define
class DependencyFile:
    url: str
    sha256: str = None  # 校验哈希
    min_version: int | float = 0  # 适用版本范围
    max_version: int | float = 127
    hook: Callable | None = None  # 下载后执行的修改钩子
```

---

## 分发主流程

回顾 [backend/base.py](dovetail/core/backend/base.py) 中的分发逻辑：

```python
def _process_instructions(self, context: GenerationContext):
    for instruction in self.ir_builder:
        # 调试模式：在每条指令前插入注释
        if context.config.debug and instruction.opcode:
            context.add_command(f"# {instruction.opcode.value[1]}:{repr(instruction)}")

        processor = self.processor_registry.get_processor(instruction.opcode)
        try:
            processor.process(instruction, context)
        except Exception as e:
            get_project_logger().error(f"Failed to process {instruction.opcode.name}: {e!r}")
            if self.config.debug:
                raise  # 调试模式下重新抛出，暴露完整堆栈
```

处理器执行异常时**不会中止整个编译**（除非开启 `--debug`），而是记录错误并继续处理下一条指令。