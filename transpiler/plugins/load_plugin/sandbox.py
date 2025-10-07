# coding=utf-8
import importlib.util
import json
import traceback
from pathlib import Path
from jsonschema import ValidationError, validate

__all__ = [
    "plugin_loader",
]

from transpiler.plugins.plugin_api_v1.plugin import Plugin


class SandboxSecurityException(Exception):
    """沙盒安全异常"""
    pass


class RestrictedImporter:
    def __init__(self, whitelist_paths: list[str | Path], blacklist_paths: list[str | Path] = None):
        """
        初始化受限导入器。

        Args:
            whitelist_paths: 允许导入的模块所在目录路径
            blacklist_paths: 禁止导入的模块所在目录路径
        """
        self.whitelist_paths = [Path(p).resolve() for p in whitelist_paths]
        self.blacklist_paths = [Path(p).resolve() for p in (blacklist_paths or [])]
        self._original_import = __import__

    def _is_path_under_any(self, test_path, path_list):
        """检查 test_path 是否在 path_list 中任一路径下"""
        for base_path in path_list:
            try:
                if test_path.is_relative_to(base_path):
                    return True
            except AttributeError:
                try:
                    test_path.relative_to(base_path)
                    return True
                except ValueError:
                    continue
        return False

    def _find_module_path(self, name):
        """查找模块对应的文件路径"""
        # 尝试通过 importlib 查找模块规范
        spec = importlib.util.find_spec(name)
        if spec is None or spec.origin is None or spec.origin == 'built-in':
            return None

        # 对于包，origin 可能是 __init__.py，我们需要包目录
        if spec.submodule_search_locations:
            # 这是一个包，返回包目录
            return Path(spec.submodule_search_locations[0]).resolve()
        else:
            # 这是一个单文件模块，返回文件路径
            return Path(spec.origin).resolve().parent

    def __call__(self, name, globals=None, locals=None, fromlist=(), level=0):
        """
        当代码执行 `import ...` 时调用的方法。
        """
        # 1. 查找要导入的模块的路径
        target_module_path = self._find_module_path(name)

        if target_module_path is None:
            # 如果是内置模块或无法找到的模块，默认拒绝（或者你可以选择允许）
            raise ImportError(f"Import of '{name}' is not allowed (cannot locate module or built-in module)")

        # 2. 黑名单优先检查：目标模块路径是否在任何黑名单路径下
        if self.blacklist_paths and self._is_path_under_any(target_module_path, self.blacklist_paths):
            raise ImportError(
                f"Import of '{name}' is forbidden (module is in a blacklisted path: '{target_module_path}')")

        # 3. 白名单检查：目标模块路径是否在任何白名单路径下
        if self._is_path_under_any(target_module_path, self.whitelist_paths):
            # 允许导入
            return self._original_import(name, globals, locals, fromlist, level)

        # 4. 默认拒绝
        raise ImportError(
            f"Import of '{name}' is not allowed (module '{target_module_path}' is not in a whitelisted path)")


def safe_build_class(func, name, *bases, metaclass=None, **kwargs):
    """
    安全的 __build_class__ 替代实现
    遵循「默认拒绝」原则，只允许最必要的功能

    Args:
        func: 由类体编译而成的函数，用于填充命名空间。
        name: 类的名称（字符串）。
        *bases: 基类元组。
        metaclass: 显式指定的元类（可选）。
        **kwargs: 传递给元类的额外关键字参数。

    Returns:
        创建的新类

    Raises:
        SandboxSecurityException: 当检测到任何安全违规时
    """

    # === 1. 元类审查 ===
    # 只允许使用默认的 type 元类，明确拒绝任何自定义元类
    if metaclass is not None and metaclass is not type:
        raise SandboxSecurityException(
            f"安全违规: 禁止使用自定义元类 '{metaclass.__name__}'"
        )

    # 拒绝任何其他关键字参数
    if kwargs:
        raise SandboxSecurityException(
            f"安全违规: 不支持的关键字参数: {list(kwargs.keys())}"
        )

    # === 2. 基类审查 ===
    # 严格的白名单：只允许继承自指定类
    PERMITTED_BASES = (object, Plugin)

    if not bases:
        bases = (object,)  # 如果没有指定基类，默认使用 object

    for base in bases:
        # 检查是否为类型且在白名单中
        if not isinstance(base, type):
            raise SandboxSecurityException(
                f"安全违规: 基类 '{base}' 不是有效的类型"
            )
        if base not in PERMITTED_BASES:
            raise SandboxSecurityException(
                f"安全违规: 禁止继承自基类 '{base.__name__}'。只允许继承自: {[b.__name__ for b in PERMITTED_BASES]}"
            )

    # === 3. 类名审查 ===
    # 防止使用可能冲突或可疑的类名
    if not name.isidentifier():
        raise SandboxSecurityException(
            f"安全违规: 类名 '{name}' 不是有效的标识符"
        )

    RESERVED_NAMES = {'sys', 'os', 'builtins', 'import', 'eval', 'exec', 'open'}
    if name.lower() in RESERVED_NAMES:
        raise SandboxSecurityException(
            f"安全违规: 类名 '{name}' 是保留名称"
        )

    try:
        # 使用 type 创建类
        namespace = {}
        try:
            exec(func.__code__, plugin_loader.global_env, namespace)
        except Exception as e:
            raise SandboxSecurityException(
                f"执行类体代码时发生错误: {e}"
            ) from e
        new_class = type(name, bases, {**kwargs, **namespace})
    except Exception as e:
        raise SandboxSecurityException(
            f"创建类时发生错误: {e}"
        ) from e
    # 严格的魔法方法审查
    allowed_dunders = {
        # 相对安全的魔法方法或属性
        '__repr__', '__str__', '__len__', '__iter__', '__next__',
        '__getitem__', '__setitem__', '__delitem__', '__contains__',
        '__hash__', '__bool__', '__int__', '__float__', '__str__',
        '__init__', '__doc__', '__module__'
    }

    forbidden_dunders = {
        # 明确禁止的危险方法或属性
        '__getattribute__', '__setattr__', '__delattr__', '__new__',
        '__del__', '__call__', '__prepare__'
    }

    # 检查所有下划线开头的方法
    for attr_name in new_class.__dict__.keys():
        if attr_name.startswith('__') and attr_name.endswith('__'):
            if attr_name in forbidden_dunders:
                raise SandboxSecurityException(
                    f"安全违规: 禁止定义魔法方法 '{attr_name}'"
                )
            elif attr_name not in allowed_dunders:
                # 对于未明确允许的魔法方法，要求特殊审批或记录
                print(f"警告: 插件定义了未常见魔法方法 '{attr_name}'")
                # 可以选择删除或保留，这里选择保留但记录
    return new_class


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
            "plugin_name": {
                "type": "string"
            },
            "plugin_main": {
                "type": "string"
            },
            "plugin_version": {
                "type": "string"
            },
            "plugin_backend": {
                "type": "array",
                "items": {
                    "type": "string"
                }
            },
            "plugin_optimize_pass": {
                "type": "array",
                "items": {
                    "type": "string"
                }
            },
            "min_permission_level": {
                "type": "integer",
                "minimum": 1,
                "maximum": 4
            },
            "plugin_type": {
                "type": "string",
                "enum": ["plugin", "library", "loader", "api"]
            },
            "plugin_main_class": {
                "type": "string"
            },
            "plugin_author": {
                "type": "array",
                "items": {
                    "type": "string"
                }
            }
        },
        "required": [  # 所有字段都是必需的
            "plugin_name",
            "plugin_main",
            "plugin_version",
            "plugin_backend",
            "plugin_optimize_pass",
            "min_permission_level",
            "plugin_type",
            "plugin_main_class",
            "plugin_author"
        ],
        "additionalProperties": False  # 不允许额外属性
    }

    def __init__(self):
        # 创建受限的内置函数
        safe_builtins = {
            'print': print,
            'len': len,
            'str': str,
            'int': int,
            'float': float,
            'list': list,
            'dict': dict,
            'tuple': tuple,
            'range': range,
            'enumerate': enumerate,
            'zip': zip,
            'min': min,
            'max': max,
            'sum': sum,
            'abs': abs,
            'round': round,
            'bool': bool,
            # 'type': type, 可用来动态创建类
            'isinstance': isinstance,
            'hasattr': hasattr,
            'getattr': getattr,
            'setattr': setattr,
            'BaseException': BaseException,
            'super': super,
            '__import__': RestrictedImporter(PluginLoader.plugins_paths, ["transpiler/plugins/load_plugin"]),
            '__build_class__': safe_build_class

        }
        # 创建全局环境
        self.global_env = {
            '__builtins__': safe_builtins,
            '__name__': '__plugin__',
        }
        self.plugins_locals: dict[str, dict] = {}
        self.plugins_main_class: dict[str, type[Plugin]] = {}

    def load_plugin(self, plugin_name, permission_level=1):
        # 根据插件名获取插件入口代码
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
                        continue
                    # 读取入口文件
                    plugin_main = Path(plugin_path) / metadata["plugin_main"]
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
            # 执行代码
            if metadata["min_permission_level"] >= 3 and permission_level >= 3:
                # 当权限等级大于等于3时直接执行，不使用沙盒环境
                exec(code, None, plugin_locals)
            else:
                exec(code, self.global_env, plugin_locals)
            self.plugins_locals[plugin_name] = plugin_locals
            # 搜索入口类
            if plugin_main_class := plugin_locals.get(metadata["plugin_main_class"], None):
                self.plugins_main_class[plugin_name] = plugin_main_class
            else:
                raise ModuleNotFoundError(f"Plugin '{plugin_name}' is invalid")
        except Exception as e:
            print(f"加载插件{plugin_name}失败，原因：{e.__str__()}")
            if self.plugins_locals.get(plugin_name, None):
                del self.plugins_locals[plugin_name]
            if self.plugins_main_class.get(plugin_name, None):
                del self.plugins_main_class[plugin_name]
            raise


plugin_loader = PluginLoader()
