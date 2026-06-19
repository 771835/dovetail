# 编译配置参考

## 配置系统结构

Dovetail 配置分为三层：

| 层级               | 来源                | 作用域    |
|------------------|-------------------|--------|
| `CompileConfig`  | CLI 参数构造，传递给各编译阶段 | 单次编译任务 |
| `config.py` 全局常量 | 源码硬编码             | 整个项目   |
| `pack.config` 文件 | 目录编译时读取           | 该目录项目  |

## CompileConfig 字段参考

定义在 [dovetail/core/compile_config.py](../../dovetail/core/compile_config.py)：

| 字段                            | 类型                  | CLI 参数                          | 默认值           | 说明                           |
|-------------------------------|---------------------|---------------------------------|---------------|------------------------------|
| `namespace`                   | `str`               | `-n`                            | `"namespace"` | 数据包命名空间                      |
| `optimization_level`          | `OptimizationLevel` | `-O`                            | `O2`          | 优化级别 (O0-O3)                 |
| `version`                     | `MinecraftVersion`  | `-mcv`                          | `1.21.5 Java` | 目标 MC 版本                     |
| `debug`                       | `bool`              | `--debug`                       | `False`       | 调试模式                         |
| `recursion`                   | `bool`              | `--recursion`                   | `False`       | 启用递归                         |
| `same_name_function_nesting`  | `bool`              | `--same-name-function-nesting`  | `False`       | 同名函数嵌套                       |
| `first_class_functions`       | `bool`              | —                               | `False`       | 函数一等公民（未实现）                  |
| `disable_deprecated_function` | `bool`              | `--disable-deprecated-function` | `False`       | 禁用弃用函数                       |
| `experimental`                | `bool`              | `--experimental`                | `False`       | 实验性功能（如 `@extern`/`@export`） |
| `lib_path`                    | `Path`              | `-l`                            | `lib/`        | 标准库路径                        |
| `description`                 | `str`               | `pack.config`                   | `""`          | 数据包描述                        |

## 优化级别说明

| 级别   | 启用的 Pass          | 适用场景       |
|------|-------------------|------------|
| `O0` | 无                 | 调试，排查优化器问题 |
| `O1` | 基础 Pass（如常量折叠）    | 快速编译       |
| `O2` | 标准 Pass（默认）       | 日常开发       |
| `O3` | 全部 Pass，最多 15 轮迭代 | 生产构建       |

## Minecraft 版本系统

版本通过 `MinecraftVersion.instance(version_str)` 工厂方法解析：

- 以 `"1."` 开头 → `OldMinecraftVersion`（如 `1.21.5`，格式 `major.minor[.patch]`）
- 其他格式 → `NewMinecraftVersion`（年份格式，未来版本）

版本对象携带平台信息（`MinecraftEdition.JAVA_EDITION` / `BEDROCK_EDITION`），用于 `@target` 注解和后端兼容性判断。

`MinecraftEdition.from_str()` 识别规则：包含 `be`、`bedrock`、`pe` 的字符串识别为基岩版，其余为 Java 版。

## 全局常量参考

定义在 [dovetail/core/config.py](../../dovetail/core/config.py)：

| 常量                              | 值              | 说明                         |
|---------------------------------|----------------|----------------------------|
| `PROJECT_NAME`                  | `"Dovetail"`   | 项目名称                       |
| `PROJECT_VERSION`               | `"1.0.2-rc.6"` | 当前版本                       |
| `PROJECT_LICENSE`               | `"Apache 2.0"` | 许可证                        |
| `FILE_PREFIX`                   | `".mcdl"`      | 源文件扩展名                     |
| `CACHE_FILE_PREFIX`             | `".mcdc"`      | 中间文件扩展名                    |
| `MAX_FILE_SIZE`                 | 1 GB           | 单文件最大体积限制                  |
| `FAST_MODE`                     | `True`         | 跳过部分编译器内部类型检查以加速           |
| `ENABLE_INSTRUCTION_VALIDATION` | `True`         | IR 指令类型验证（FAST_MODE 开启时无效） |

## pack.config 格式

目录编译时，目录根路径下需包含 `pack.config`：

```json
{
  "main": "main.mcdl",
  "description": "我的数据包描述"
}
```

| 字段            | 必需 | 说明                                    |
|---------------|----|---------------------------------------|
| `main`        | ✅  | 入口文件相对路径                              |
| `description` | ❌  | 数据包描述，会覆盖 `CompileConfig.description` |

## 插件元数据格式

每个插件目录需包含 `plugin.metadata` 文件：

```json
{
  "display_name": "JE 1.21.5 Backend",
  "plugin_main": "main",
  "plugin_version": "1.0.0",
  "plugin_type": "plugin",
  "main_class": "Plugin",
  "description": "Java Edition 1.21.5 后端",
  "plugin_author": [
    "author"
  ]
}
```

| 字段               | 必需 | 可选值                                   |
|------------------|----|---------------------------------------|
| `display_name`   | ✅  | 显示名称                                  |
| `plugin_main`    | ✅  | 入口模块名                                 |
| `plugin_version` | ✅  | 版本字符串                                 |
| `plugin_type`    | ✅  | `"plugin"` / `"library"` / `"loader"` |
| `main_class`     | ✅  | 插件主类名                                 |
| `description`    | ❌  | 描述                                    |
| `plugin_author`  | ❌  | 作者列表                                  |

## 下一步

- [快速开始](2-quick-start) — 命令行参数的实际使用
- [注解系统与自定义注解](21-annotation-system-and-custom-annotations) — 与配置交互的注解行为