# DFP-6 附表 B：内置 flags 约定值

← [返回 DFP-6 主文档](DFP-6.md)

---

## 规则

flags 是附加在符号上的字符串集合。优化器和后端在做决策时，
必须且只能通过检查 flags 来判断行为，不应该通过注解名称或分类来判断。
这一规则确保注解系统与消费方之间的解耦：未来新增注解只需产生相应的 flags，
无需修改优化器或后端代码。

---

## 内置 flags 约定值

| flag              | 来源注解                                | 消费方 | 语义                      |
|-------------------|-------------------------------------|-----|-------------------------|
| `no_dce`          | `@init` `@tick` `@export` `@extern` | 优化器 | 禁止未使用函数消除 pass 删除此符号    |
| `no_inline`       | `@noinline` `@recursive` `@extern`  | 优化器 | 禁止内联 pass 对此符号执行内联      |
| `aggressive_opt`  | `@internal`                         | 优化器 | 允许对此符号执行激进优化策略          |
| `allow_recursion` | `@recursive`                        | 后端  | 允许递归调用，后端须为局部变量生成栈式存储   |
| `load_hook`       | `@init`                             | 后端  | 此函数须被注册到数据包 `#load` tag |
| `tick_hook`       | `@tick`                             | 后端  | 此函数须被注册到数据包 `#tick` tag |
| `preserve_name`   | `@export`                           | 前端  | 禁止对此函数名执行归一化处理          |
| `extern`          | `@extern`                           | 后端  | 生成对外部的访问指令              |
| `export`          | `@export`                           | 后端  | 生成供外部访问的接口              |

---

## 冲突处理

flags 之间无优先级，全部保留在集合中。当符号上同时存在语义冲突的 flags 时
（例如同时存在 `aggressive_opt` 和 `no_inline`），各消费方独立处理，
本规范不定义统一的冲突解决策略。

---

## 插件扩展

插件自定义的 flags 应使用命名空间前缀以避免与内置 flags 冲突，
推荐格式为 `plugin_name:flag_name`。
编译器核心不对插件 flags 的语义作任何假设。