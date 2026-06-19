# 后端抽象与工厂

## Backend 抽象基类

[dovetail/core/backend/base.py](dovetail/core/backend/base.py)：

```python
class Backend(ABC, metaclass=BackendMeta):
    processor_registry: ProcessorRegistry  # opcode → 处理器映射
    output_manager: OutputManager  # 输出文件管理

    def __init__(self, ir_builder, target: Path, config: CompileConfig)

    @staticmethod @ abstractmethod
    def is_support(config: CompileConfig) -> bool  # 是否支持该配置

    @staticmethod @ abstractmethod
    def get_name() -> str  # 后端唯一名称

    def generate(self):  # 代码生成主流程
```

`BackendMeta` 元类确保每个子类有**独立的** `processor_registry` 和 `output_manager` 实例，不共享。

## generate() 主流程

```python
def generate(self):
    context = GenerationContext(config, target, ir_builder)
    self._process_instructions(context)  # 遍历 IR，分发给处理器
    self._write_outputs(context)  # 写出所有文件
```

`_process_instructions()` 遍历每条 IR 指令，通过 `processor_registry.get_processor(opcode)` 查找处理器并调用
`processor.process(instruction, context)`。调试模式下在每条指令前插入注释。

## BackendFactory

[dovetail/core/backend/factory.py](dovetail/core/backend/factory.py)：

```python
BackendFactory.register(backend_class)  # 注册（由插件调用）
BackendFactory.auto_select(config, name="")  # 自动选择或按名指定
BackendFactory.get_available_backends()  # 获取所有已注册名称
BackendFactory.is_empty()  # 是否有已注册后端
```

`auto_select()` 逻辑：

- 若指定 `backend_name`，直接查找，不存在则抛出 `BackendNotFoundError`
- 若未指定，遍历所有后端调用 `is_support(config)`，返回第一个支持的

## 三个核心组件

### ProcessorRegistry

opcode → 处理器的映射注册表，后端子类通过装饰器注册每个 opcode 的处理逻辑。

### GenerationContext

代码生成过程中在各处理器间传递的上下文对象，携带：配置、目标路径、IR、当前生成的命令缓冲。

### OutputManager

管理多个输出文件（如 `.mcfunction` 文件、`pack.mcmeta` 等）的写入，最终统一落盘。

## 实现新后端

```python
from dovetail.core.backend.base import Backend


class MyBackend(Backend):
    @staticmethod
    def get_name() -> str:
        return "my_backend"

    @staticmethod
    def is_support(config) -> bool:
        return config.version.display_version == "1.21.5"

    # 注册 opcode 处理器（具体 API 见 processor.py）
```

然后在插件的 `main_class` 的初始化中调用 `BackendFactory.register(MyBackend)`。