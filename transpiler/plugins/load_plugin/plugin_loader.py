# coding=utf-8
import json
import os
from pathlib import Path

from jsonschema import ValidationError, validate

from transpiler.plugins.plugin_api_v1.plugin import Plugin

__all__ = [
    "plugin_loader",
]


class PluginLoader:
    """
    插件加载器
    """
    plugins_paths = [
        "transpiler/plugins",
        "plugins",
    ]
    plugin_meta_schema = {
        "type": "object",
        "properties": {
            "display_name": {
                "type": "string"
            },
            "plugin_main": {
                "type": "string"
            },
            "plugin_version": {
                "type": "string"
            },
            "plugin_type": {
                "type": "string",
                "enum": ["plugin", "library", "loader"]
            },
            "main_class_name": {
                "type": "string"
            },
            "plugin_author": {
                "type": "array",
                "items": {
                    "type": "string"
                }
            }
        },
        "required": [  # 必需的字段
            "display_name",
            "plugin_main",
            "plugin_version",
            "plugin_type",
            "main_class_name",
            "plugin_author"
        ],
        "additionalProperties": False  # 不允许额外属性
    }

    def __init__(self):
        self.plugins_locals: dict[str, dict] = {}
        self.plugins_main_class: dict[str, Plugin] = {}

    def load_plugin(self, plugin_name):
        # 根据插件目录名获取插件入口代码
        for plugins_path in PluginLoader.plugins_paths:
            plugin_path = Path(plugins_path) / plugin_name
            if plugin_path.exists() and plugin_path.is_dir():
                metadata_path = plugin_path / "plugin.metadata"
                if metadata_path.exists() and metadata_path.is_file():
                    try:
                        with open(metadata_path) as metadata_file:
                            metadata: dict = json.load(metadata_file)
                        # 效验插件配置文件是否正确
                        validate(instance=metadata, schema=self.plugin_meta_schema)
                    except (json.decoder.JSONDecodeError, ValidationError):
                        print(f"Plugin '{plugin_path}' is invalid")
                        if os.environ and os.environ.get("PLUGIN_DEBUG"):
                            raise
                        else:
                            continue
                    # 读取入口文件
                    plugin_main = Path(plugin_path) / metadata.get("plugin_main")
                    if plugin_main.exists() and plugin_main.is_file():
                        with open(plugin_main) as plugin_main_file:
                            code = plugin_main_file.read()
                    else:
                        print(f"Plugin '{plugin_path}' is invalid")
                        continue

                    print(f"Loading plugin '{plugin_name}' from '{plugin_path}'")
                    break
        else:
            print(f"No plugin '{plugin_name}' found")
            return
        # 获得插件的作用域
        plugin_locals = self.plugins_locals.get(plugin_name, {})
        try:
            global_env: dict = dict(globals())
            global_env.update(
                {
                    "__path__": str(plugin_path.resolve()),
                    "__package__": str(plugin_path.resolve().relative_to(Path.cwd())).replace("\\", "."),
                    "__name__": plugin_name,
                    "__file__": str(plugin_main.resolve())
                }
            )
            # 执行代码
            exec(code, global_env, plugin_locals)
            global_env.update(plugin_locals)
            self.plugins_locals[plugin_name] = plugin_locals
            # 搜索入口类
            if plugin_main_class := plugin_locals.get(metadata["main_class_name"], None):
                self.plugins_main_class[plugin_name] = plugin_main_class()
                if not self.plugins_main_class[plugin_name].validate():
                    raise RuntimeError(f"Plugin '{plugin_name}' has invalid configuration")
                self.plugins_main_class[plugin_name].load()
            else:
                raise ModuleNotFoundError(f"Plugin '{plugin_name}' is invalid")
        except Exception as e:
            print(f"加载插件{plugin_name}失败，原因：{e.__str__()}")
            if self.plugins_locals.get(plugin_name, None):
                del self.plugins_locals[plugin_name]
            if self.plugins_main_class.get(plugin_name, None):
                del self.plugins_main_class[plugin_name]
            if os.environ and os.environ.get("PLUGIN_DEBUG"):
                raise


plugin_loader = PluginLoader()
