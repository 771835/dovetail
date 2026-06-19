# 插件加载器与发现机制

## 加载器结构

```
plugins/plugin_loader/
├── __init__.py
├── loader.py          # 核心加载逻辑
├── main.py            # 加载器插件入口
└── plugin.metadata    # type: "loader"
```

## plugin_loader 全局实例

`loader.py` 中暴露全局 `plugin_loader` 对象，在 `main.py` 的参数解析后调用：

```python
from dovetail.plugins.plugin_loader.loader import plugin_loader

if not parsed_args.disable_plugins:
    plugin_loader.load_plugin("plugin_loader")
```

## 元数据验证

加载时使用 `PLUGIN_METADATA_VALIDATOR`（`fastjsonschema` 编译的验证器）严格检查 `plugin.metadata` 格式，必需字段：
`display_name`、`plugin_main`、`plugin_version`、`plugin_type`、`main_class`。不允许额外属性（`additionalProperties: false`）。