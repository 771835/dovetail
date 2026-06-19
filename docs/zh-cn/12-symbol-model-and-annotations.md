# 符号模型与注解

## 符号与注解的关系

每个携带注解的符号（Function、Class、Structure、Enumeration）通过 `AnnotationMixin` 持有一个注解附件字典：

```python
annotations: dict[str, AnnotationAttachment]
#                  注解名 →  处理后的完整注解信息
```

## AnnotationAttachment

```python
@define(slots=True)
class AnnotationAttachment:
    name: str  # 注解名称
    args: dict[str, Any]  # 注解参数
    result: AnnotationResult  # 处理结果

    @property
    def flags(self) -> set[str]  # 直接访问 flags

        @property
        def metadata(self) -> dict  # 直接访问 metadata
```

## AnnotationResult

注解处理器返回的结构化结果，三类消费方各取所需：

| 字段              | 类型                   | 消费方        | 说明                     |
|-----------------|----------------------|------------|------------------------|
| `skip`          | `bool`               | ASTVisitor | 跳过该符号（仅 PRE_SYMBOL 有效） |
| `type_override` | `FunctionType\|None` | ASTVisitor | 覆盖函数类型                 |
| `flags`         | `set[str]`           | 优化器、后端     | 行为标记集合                 |
| `metadata`      | `dict[str,Any]`      | 后端、工具链     | 任意附加信息                 |

多个注解的结果通过 `merge()` 合并：

```python
def merge(self, other: AnnotationResult) -> AnnotationResult:
    return AnnotationResult(
        skip=self.skip or other.skip,
        type_override=other.type_override or self.type_override,
        flags=self.flags | other.flags,
        metadata={**self.metadata, **other.metadata},
    )
```

## 常见 flags 及含义

| Flag              | 设置者                                 | 含义          |
|-------------------|-------------------------------------|-------------|
| `load_hook`       | `@init`                             | 注册为数据包加载钩子  |
| `tick_hook`       | `@tick`                             | 注册为 tick 钩子 |
| `no_dce`          | `@init`/`@tick`/`@extern`/`@export` | 禁止死代码消除     |
| `no_inline`       | `@noinline`/`@recursive`/`@extern`  | 禁止内联        |
| `aggressive_opt`  | `@internal`                         | 允许激进优化      |
| `allow_recursion` | `@recursive`                        | 允许递归调用      |
| `extern`          | `@extern`                           | 标记为外部函数     |
| `export`          | `@export`                           | 标记为导出函数     |
| `preserve_name`   | `@export`                           | 保持原始名称不被规范化 |

## AnnotationSpec

`annotations/spec.py` 中的 `Annotation` 对象是注解的**解析时表示**（解析阶段），与 `AnnotationAttachment`（处理后）相对：

```python
@define(slots=True)
class Annotation:
    name: str  # 注解名称
    args: list[Any]  # 位置参数（字面量列表）
```