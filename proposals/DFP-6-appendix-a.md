# DFP-6 附表 A：AnnotationResult 字段与合并语义

← [返回 DFP-6 主文档](DFP-6.md)

---

## 字段定义

注解处理器的处理结果以 `AnnotationResult` 结构体表示，包含以下字段：

| 字段              | 类型                   | 默认值   | 有效时机        | 说明                         |
|-----------------|----------------------|-------|-------------|----------------------------|
| `skip`          | bool                 | False | PRE_SYMBOL  | 为 True 时跳过当前声明的全部编译流程      |
| `flags`         | set[str]             | 空集合   | POST_SYMBOL | 附加到符号的行为标记，优化器与后端据此做决策     |
| `metadata`      | dict[str, Any]       | 空字典   | POST_SYMBOL | 结构化附加信息，供后端与工具链按需读取        |
| `type_override` | FunctionType \| None | None  | POST_SYMBOL | 覆盖函数的类型标记，目前仅 `@extern` 使用 |

**时机约束**：PRE_SYMBOL 处理器填写 `flags`、`metadata`、`type_override`
的内容不会被写入符号。POST_SYMBOL 处理器填写 `skip` 为 True 的行为未定义。
编译器实现不得在时机不匹配时报错，而应静默忽略无效字段。

---

## 合并语义

同一声明上携带多个注解时，各注解的 `AnnotationResult` 在各自时机内依次合并。
合并规则如下：

| 字段              | 合并规则                            |
|-----------------|---------------------------------|
| `skip`          | 逻辑或，任一为 True 则结果为 True          |
| `flags`         | 集合并集                            |
| `metadata`      | 字典合并，后处理的注解覆盖先处理的同名键            |
| `type_override` | 取最后一个非 None 值，全为 None 则结果为 None |

注解的处理顺序与其在源码中的声明顺序一致。