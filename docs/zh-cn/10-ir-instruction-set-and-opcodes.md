# IR 指令集与操作码

## 设计原则

Dovetail IR 采用**统一指令类**设计：所有指令使用同一个 `IRInstruction` 类，通过 `IROpCode` 枚举区分类型。

```python
class IRInstruction:
    opcode: IROpCode  # 操作码
    operands: list[Any]  # 操作数列表
```

> 判断单条 IR 指令类型的**唯一金标准**是比较 `IROpCode` 的 ID 编号（`opcode.code`）是否相同。

## 操作码分类

### 控制流（0x00-0x1F）

| 操作码           | ID   | 说明     |
|---------------|------|--------|
| `JUMP`        | 0x00 | 无条件跳转  |
| `COND_JUMP`   | 0x01 | 条件跳转   |
| `FUNCTION`    | 0x02 | 函数定义开始 |
| `CALL`        | 0x03 | 函数调用   |
| `RETURN`      | 0x04 | 函数返回   |
| `SCOPE_BEGIN` | 0x05 | 作用域开始  |
| `SCOPE_END`   | 0x06 | 作用域结束  |
| `BREAK`       | 0x07 | 循环中断   |
| `CONTINUE`    | 0x08 | 循环继续   |

### 数据运算（0x20-0x3F）

| 操作码         | ID   | 说明                          |
|-------------|------|-----------------------------|
| `DECLARE`   | 0x20 | 变量声明                        |
| `ASSIGN`    | 0x21 | 赋值                          |
| `UNARY_OP`  | 0x22 | 一元运算（`-` `!` `~`）           |
| `BINARY_OP` | 0x23 | 二元运算（`+` `-` `*` `/` `%` 等） |
| `COMPARE`   | 0x24 | 比较运算（`==` `!=` `<` 等）       |
| `CAST`      | 0x25 | 类型转换                        |
| `FREE`      | 0x26 | 释放变量                        |

### 面向对象（0x40-0x5F）

| 操作码            | ID   | 说明     |
|----------------|------|--------|
| `CLASS`        | 0x40 | 类定义    |
| `NEW_OBJ`      | 0x41 | 新建对象实例 |
| `GET_PROPERTY` | 0x42 | 读取对象属性 |
| `SET_PROPERTY` | 0x43 | 设置对象属性 |
| `CALL_METHOD`  | 0x44 | 调用对象方法 |
| `FREE_OBJ`     | 0x55 | 释放对象   |

### 所有权（0x60-0x7F）

| 操作码      | ID   | 说明    |
|----------|------|-------|
| `MOVE`   | 0x60 | 所有权转移 |
| `BORROW` | 0x61 | 借用    |

## 指令分类（InstCategory）

| 分类             | 说明       |
|----------------|----------|
| `CONTROL_FLOW` | 控制流指令    |
| `DATA_OP`      | 数据运算指令   |
| `OOP`          | 面向对象指令   |
| `OWNERSHIP`    | 所有权指令    |
| `ARRAY`        | 数组操作（预留） |
| `SPECIAL`      | 特殊指令（预留） |

## 运算操作符

### 二元运算（BinaryOps）

算术：`+` `-` `*` `/` `%`
位运算：`&` `|` `^` `<<` `>>`
特殊：`min` `max`

### 一元运算（UnaryOps）

`-`（取负） `!`（逻辑非） `~`（按位取反）

### 比较运算（CompareOps）

`==` `!=` `<` `<=` `>` `>=`

## 工厂函数

`instructions.py` 提供类型安全的工厂函数（如 `IRDeclare`、`IRAssign`、`IRCall` 等），在 `FAST_MODE=False` 时启用运行时参数类型验证。

## 验证系统

```python
FAST_MODE = True  # 开启时跳过类型检查
ENABLE_INSTRUCTION_VALIDATION = True  # 启用 IR 指令类型验证（FAST_MODE 开启时无效）
```