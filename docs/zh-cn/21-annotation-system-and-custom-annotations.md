# 注解系统与自定义注解

## 概述

注解（Annotation）是附着在函数、类、结构体、枚举等定义上的编译指令，用于修改编译器对该符号的处理方式。

语法：

```mcdl
@annotation_name
@annotation_name("key1" = "value1", "key2" = "value2")
```

注解由 `AnnotationRegistry` 统一管理，在 AST 遍历阶段的两个时机处理：

- **PRE_SYMBOL**：符号对象创建之前（用于条件编译，决定是否跳过）
- **POST_SYMBOL**：符号对象创建之后（用于标记、校验、元数据附加）

## 注解六大分类

| 类别常量           | 说明             | 包含注解                                                                 |
|----------------|----------------|----------------------------------------------------------------------|
| `LIFECYCLE`    | 控制函数执行时机       | `@init`, `@tick`                                                     |
| `VISIBILITY`   | 控制可见性与优化策略     | `@internal`, `@noinline`, `@recursive`                               |
| `LINKAGE`      | 控制后端链接与跨语言 FFI | `@extern`, `@export`                                                 |
| `BACKEND_HINT` | 提示后端代码生成方式     | （预留扩展）                                                               |
| `CONDITION`    | 条件编译，决定是否生成代码  | `@version`, `@target`, `@if_not_exists`, `@if_symbol`, `@if_feature` |
| `METADATA`     | 元数据，不影响编译逻辑    | `@deprecated`, `@doc`, `@author`, `@since`                           |

## 生命周期注解（LIFECYCLE）

### `@init`

将函数注册为数据包**加载时**执行的函数（Minecraft 的 `load` 标签）。

```mcdl
@init
fn main() {
    print("数据包已加载")
}
```

效果：设置 flags `{"load_hook", "no_dce"}`（禁止死代码消除）。

### `@tick`

将函数注册为**每 tick** 执行的函数（Minecraft 的 `tick` 标签）。

```mcdl
@tick
fn gameLoop() {
    exec("scoreboard players add timer global 1")
}

@tick("interval" = 5)      // 每 5 tick 执行，interval 必须为正整数
fn slowLoop() { ... }
```

效果：设置 flags `{"tick_hook", "no_dce"}`。

## 可见性注解（VISIBILITY）

### `@internal`

允许优化器对该函数使用**激进优化策略**。

```mcdl
@internal
fn helperFunc() { ... }
```

效果：设置 flag `{"aggressive_opt"}`。

### `@noinline`

**禁止**编译器将此函数内联到调用处。

```mcdl
@noinline
fn dontInline() { ... }
```

效果：设置 flags `{"no_inline"}`。

### `@recursive`

声明此函数**支持递归调用**（需配合 `--recursion` 启用）。

```mcdl
@recursive
fn factorial(n: int) -> int {
    if (n <= 1) { return 1 }
    return n * factorial(n - 1)
}
```

效果：设置 flags `{"allow_recursion", "no_inline"}`。

## 条件编译注解（CONDITION）

这类注解在 `PRE_SYMBOL` 时机执行，决定是否生成对应符号。`skip = true` 时该定义整体被跳过。

### `@version`

根据目标 Minecraft **版本范围**条件编译。

```mcdl
@version("min" = "1.20.4", "max" = "1.21.5")
fn newFeature() { ... }
```

### `@target`

根据目标 Minecraft **平台版本**（Java / 基岩版）条件编译。

```mcdl
@target("edition" = "java")
fn javaOnly() -> int {
    return 350234
}

@target("edition" = "be")
fn beOnly() -> int {
    return 0
}
```

`edition` 支持值：`"java"`、`"bedrock"`、`"be"`、`"pe"`

### `@if_not_exists`

当作用域中**不存在**同名符号时才编译（常用于库的默认实现）。

```mcdl
@if_not_exists
fn fallback() { ... }
```

### `@if_symbol`

当指定符号**存在**时才编译。

```mcdl
@if_symbol("name" = "MyClass", "type" = "class")
fn useMyClass() { ... }
```

`type` 支持值：`"class"`、`"function"`、`"variable"`、`"any"`

### `@if_feature`

当 `CompileConfig` 上指定特性标志为真时才编译。

```mcdl
@if_feature("feature" = "experimental")
fn expFunc() { ... }
```

## 链接注解（LINKAGE）

> ⚠️ 链接注解为**实验性功能**，需使用 `--experimental` 参数启用。

### `@extern`

声明从**外部数据包**导入的函数（类似 C 的 `extern`）。

```mcdl
@extern("abi" = "clang-mc", "path" = "myns:my_func")
fn external_func() -> int;
```

效果：设置 flags `{"no_inline", "no_dce", "extern"}`，`type_override = FunctionType.EXTERN`。

### `@export`

将函数**导出**供外部数据包调用。

```mcdl
@export("abi" = "dovetail")
fn my_export() -> int { ... }
```

效果：设置 flags `{"no_dce", "preserve_name", "export"}`。

**支持的 ABI：**

| ABI        | 说明           | 类型限制                              |
|------------|--------------|-----------------------------------|
| `dovetail` | 原生 ABI       | 无限制                               |
| `clang-mc` | clang-mc 互操作 | 仅 `int`/`boolean`/`void`/`string` |

## 元数据注解（METADATA）

这类注解不影响编译逻辑，仅附加信息到符号上。

### `@deprecated`

标记符号为**已弃用**。配合 `--disable-deprecated-function` 可在编译时完全跳过。

```mcdl
@deprecated("msg" = "请使用 newFunc 代替")
fn oldFunc() { ... }
```

### `@doc`

为符号附加**文档字符串**。

```mcdl
@doc("text" = "此函数计算两数之和")
fn add(a: int, b: int) -> int { ... }
```

### `@author` / `@since`

```mcdl
@author("name" = "developer")
@since("version" = "1.0.0")
fn myFunc() { ... }
```

## 自定义注解（插件扩展）

通过插件 API 可注册自定义注解处理器，继承 `AnnotationProcessor` 基类：

```python
from dovetail.core.annotations.base import (
    AnnotationProcessor, AnnotationResult,
    AnnotationTarget, AnnotationTiming
)


class MyProcessor(AnnotationProcessor):
    annotation_name = "my_annotation"
    applicable_targets = [AnnotationTarget.FUNCTION]
    timing = AnnotationTiming.POST_SYMBOL

    def process(self, args, ctx) -> AnnotationResult:
        return AnnotationResult(
            flags={"my_flag"},
            metadata={"key": args.get("key", "")}
        )
```

然后通过 `get_registry().register(MyProcessor())` 注册。

## AnnotationResult 字段说明

| 字段                | 消费方        | 说明                          |
|-------------------|------------|-----------------------------|
| `skip: bool`      | ASTVisitor | 是否跳过该符号的编译（仅 PRE_SYMBOL 有效） |
| `type_override`   | ASTVisitor | 覆盖函数类型                      |
| `flags: set[str]` | 优化器、后端     | 标记集合，影响优化和代码生成行为            |
| `metadata: dict`  | 后端、工具链     | 任意元数据键值对                    |

## 下一步

- [架构概述与编译流水线](5-architecture-overview-and-compilation-pipeline) — 了解注解在编译流程中的处理时机
- [编译配置参考](22-compile-configuration-reference) — 与注解行为相关的编译配置项