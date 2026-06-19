# 实用模块与辅助工具

`dovetail/utils/` 提供一系列横切关注点的工具模块。

## 模块速览

| 模块                     | 说明                                                     |
|------------------------|--------------------------------------------------------|
| `logger.py`            | `ThreadSafeLogger` 线程安全日志器                             |
| `naming.py`            | `NameNormalizer` 命名规范化（`--disable-names-normalize` 控制） |
| `annotations.py`       | `@timed` 等工具装饰器                                        |
| `ir_serializer.py`     | `IRSymbolSerializer` IR 序列化（`.mcdc` 文件）                |
| `binary_serializer.py` | 二进制序列化基础设施                                             |
| `escape_processor.py`  | 字符串转义处理                                                |
| `safe_enum.py`         | `SafeEnum` 枚举基类                                        |
| `mixin_manager.py`     | Mixin 管理工具                                             |
| `string_similarity.py` | 字符串相似度（用于错误提示"你是否想输入...")                              |
| `datapack_format.py`   | 数据包格式版本映射（对应 wiki 数据）                                  |
| `download_tool.py`     | 下载工具                                                   |

## ThreadSafeLogger

项目全局日志器，线程安全。通过 `config.py` 中的 `set_project_logger()` / `get_project_logger()` 全局访问。

```python
set_project_logger(get_logger(PROJECT_NAME, logging.INFO))
get_project_logger().info("...")
get_project_logger().debug("...")
get_project_logger().error("...")
get_project_logger().critical("...")
```

## NameNormalizer

控制符号名称的规范化处理（将 MCDL 中的名称转换为 Minecraft 合法的命令名称）。

```python
NameNormalizer.enable = not parsed_args.disable_names_normalize

_n = NameNormalizer.normalize  # 规范化
_dn = NameNormalizer.denormalize  # 反规范化
```

## @timed 装饰器

```python
from dovetail.utils.annotations import timed


@timed("写入临时文件用时{:.3f}s")
def _write_temp_file(self, ...):
    ...
```

在函数执行后自动记录耗时并输出到日志。

## IRSymbolSerializer

将 `IRBuilder` 序列化为二进制 `.mcdc` 文件：

```python
data = IRSymbolSerializer.dump(builder)  # bytes
builder = IRSymbolSerializer.load(data)  # IRBuilder
```

配合 `--output-temp-file` 参数使用。

## SafeEnum

项目内所有枚举的基类，扩展了标准 `Enum` 的功能（更安全的查找、更友好的错误信息）。

## datapack_format

动态维护 Minecraft 版本与数据包格式版本号之间的映射关系，数据来源参考中文 wiki。