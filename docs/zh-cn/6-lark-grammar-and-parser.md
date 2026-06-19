# Lark 语法与解析器

## 概述

Dovetail 使用 [Lark](https://github.com/lark-parser/lark) 库的 LALR
解析器，语法定义在 [lark/dovetail.lark](lark/dovetail.lark)，仅 170 行，覆盖完整语言语法。

## 解析器初始化

[dovetail/core/parser/parser.py](dovetail/core/parser/parser.py)：

```python
lark_parser = Lark(
    open(r".\lark\dovetail.lark", encoding='utf-8').read(),
    start=["program", "expr"],  # 两个起始符号
    parser='lalr',  # 确定性快速解析
    cache=".lark_cache",  # 缓存加速后续调用
    propagate_positions=True,  # 保留位置信息用于错误报告
    maybe_placeholders=True
)
```

两个起始符号的用途：

- `program`：解析完整 `.mcdl` 源文件
- `expr`：解析 f-string 中嵌入的表达式（由 `parse_fstring_iter` 驱动）

## 语法结构概览

### 程序结构

```lark
program: include* (enums|class|struct|function|let|const|typedef)*
```

顶层只允许五种元素：include、枚举、类、结构体、函数、变量声明、常量、类型别名。

### 函数与方法

```lark
function: annotation* ("function"|"fn"|"def") ID params [("->"|":") type] (block|pass_stmt)
method:   annotation* "method" ID params [("->"|":") type] (block|pass_stmt)
params:   "(" (param ("," param)*)? ")"
param:    [MUT] ID ":" type ("=" expr)?
        | [MUT] type ID ("=" expr)?
```

- `fn`、`function`、`def` 三个关键字完全等价
- 参数支持两种顺序：`name: type` 或 `type name`
- 返回类型用 `->` 或 `:` 标记均可
- 函数体可以是 `block`（`{...}`）或 `pass_stmt`（前向声明 `;`）

### 类型系统

```lark
type.2: ID ("<" type ("," type)* ">")? [QUESTION]
```

- 支持泛型语法 `list<int>`、`map<string, int>`
- 末尾 `?` 标记可空类型（仅对象类型有效）
- `.2` 是 Lark 优先级声明，确保类型规则在歧义时优先匹配

### 表达式优先级层次

从低到高：

```
or_expr        →  ||
and_expr       →  &&
cmp_expr       →  == != < <= > >=
add_expr       →  + -
mul_expr       →  * /
unary_expr     →  - ! （一元）
post_expr      →  方法调用 . 成员访问 [] 索引 () 调用
atom           →  字面量、标识符、括号表达式
```

### 注解语法

```lark
annotation: "@" ID | "@" ID "(" literal ("," literal)* ")"
```

注解参数只能是字面量（字符串/数字），不支持表达式。

### 控制流

```lark
for_loop: "for" "(" [let|expr] ";" [condition] ";" [expr] ")" block   // 传统 for
        | "for" "(" type ID ":" expr ")" block                         // 增强 for

while_loop: "while" "(" [condition] ")" block

if_stmt: "if" "(" [condition] ")" block ("else" (if_stmt|block))?
```

## f-string 解析

f-string 在两个层面处理：

1. **词法层面**：整个 `f"..."` 作为单个 `FSTRING` token 捕获
2. **访问者层面**：`parse_fstring_iter()` 逐段拆分，对 `{expr}` 部分用 `expr` 起始符号重新解析

```python
def parse_fstring_iter(fstring: str):
# 逐字符扫描，yield ('literal', content) 或 ('expr', content)
# 支持 {{ }} 转义
# 支持嵌套括号深度追踪
```

## 公开 API

| 函数                                             | 说明                      |
|------------------------------------------------|-------------------------|
| `parser_code(code, start)`                     | 解析代码字符串，返回 AST Tree     |
| `parser_file(filepath, start, error_reporter)` | 解析文件，返回 AST Tree 或 None |
| `parse_fstring_iter(fstring)`                  | 迭代 f-string 的字面量/表达式片段  |

`parser_file` 还处理文件不存在和文件过大（> 1GB）的错误情况。