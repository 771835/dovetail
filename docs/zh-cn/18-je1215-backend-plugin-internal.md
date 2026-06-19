# JE1215 后端插件内部机制

## 插件结构

```
plugins/je1215/
├── __init__.py
├── plugin.metadata            # 插件元数据
├── main.py                    # 插件入口
└── backend/
    ├── backend.py             # Backend 子类实现
    ├── initializer_function_writer.py   # load/tick 钩子写入
    ├── literal_pool_writer.py           # 字面量池写入
    ├── commands/              # 各类型命令生成器
    └── processors/            # IR opcode 处理器
```

## 插件元数据

```json
{
  "display_name": "JE1215 Backend",
  "plugin_main": "main",
  "plugin_version": "...",
  "plugin_type": "plugin",
  "main_class": "Plugin"
}
```

## 后端注册流程

插件加载时，`main.py` 中的 `Plugin.main_class` 被实例化，调用 `BackendFactory.register(JE1215Backend)` 完成注册。

## is_support 判断

```python
@staticmethod
def is_support(config: CompileConfig) -> bool:
    return (config.version.is_java_edition() and
            MinecraftVersion("1.21.5") <= config.version)
```

## 特殊写入器

### InitializerFunctionWriter

负责生成 Minecraft 的 `load.json` 和 `tick.json` 文件，将带有 `load_hook` / `tick_hook` flags 的函数注册到对应标签文件中。

### LiteralPoolWriter

管理字面量池，将字符串/数值字面量写入专用的 mcfunction 文件，避免重复生成相同内容。