# 插件 API 与生命周期

## 插件目录结构

每个插件是 `plugins/` 下的一个子目录：

```
plugins/my_plugin/
├── plugin.metadata     # 必需：插件元数据
├── main.py             # 必需：包含插件主类
└── ...                 # 其他模块
```

## plugin.metadata 格式

```json
{
  "display_name": "My Plugin",
  "description": "插件描述",
  "plugin_main": "main",
  "plugin_version": "1.0.0",
  "plugin_type": "plugin",
  "main_class": "MyPlugin",
  "plugin_author": [
    "author"
  ]
}
```

`plugin_type` 取值：

- `plugin`：功能插件（如后端插件）
- `library`：库插件（提供函数库）
- `loader`：加载器插件（如 `plugin_loader` 本身）

## 插件主类

`main_class` 指定的类会在插件加载时被实例化。典型结构：

```python
class MyPlugin:
    def __init__(self):
        # 注册后端、注解处理器、优化 Pass 等
        BackendFactory.register(MyBackend)
        get_registry().register(MyAnnotationProcessor())
```

## v2 事件系统

`plugin_api/v2/` 提供事件驱动的插件交互机制：

```
plugin_api/v2/
├── event.py           # 事件基类
├── events/            # 具体事件定义
├── plugin_manager.py  # 插件管理器
└── registry.py        # 事件注册表
```

插件可以订阅编译生命周期事件，在特定阶段介入编译流程。

## 插件加载顺序

1. `plugin_loader.load_plugin("plugin_loader")` — 自举加载器
2. 加载器扫描 `plugins/` 目录
3. 读取并验证每个 `plugin.metadata`（通过 `PLUGIN_METADATA_VALIDATOR`）
4. 实例化 `main_class`，完成注册

禁用插件加载：`--disable-plugins`