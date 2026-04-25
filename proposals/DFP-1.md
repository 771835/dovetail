# DFP 1: 基础语法规范

## 提案信息

**作者**: 771835 <2790834181@qq.com>  
**状态**: Active  
**创建日期**: 2025-06-06  
**最新更新**: 2026-03-06

## 摘要

该提案定义了 `Dovetail` 的基础语法规范，涵盖了程序结构、类型系统、类与接口、控制流和表达式等内容。目标是为 `Dovetail`
提供一套结构化、安全且可扩展的基础语法体系，为后续模块提供语法与语义基础支持。

## 动机

当前 `Minecraft` 中的命令编写方式存在以下问题：

1. 代码复用性差：缺乏模块化与完整函数定义机制
2. 类型安全性不足：无法检查数据流动和使用上的错误
3. 表达能力有限：逻辑越复杂越难以维护
4. 缺乏面向对象能力：无法构建可复用的实体结构

通过结构化的语法设计，`Dovetail` 将实现如下改进：

- 代码结构更具模块性和可维护性
- 提供**编译时类型检查**
- 支持**类定义与多继承**，增强模块间交互
- 更易于与现代开发工具链集成

## 技术规范

### 程序结构

`Dovetail` 支持模块化开发，程序由顶层声明构成：

```dovetail
// 包含外部模块
include "mathlib.mcdl"
include "selector.mcdl"

// 顶层常量
const PI: float = 3.14159

// 顶层变量
let global_counter: int = 0

// 类定义
class Entity(BaseEntity) {
    let health: int
    let name: string
    
    method __init__(self: Entity, initial_health: int) {
        self.health = initial_health
    }
    
    method takeDamage(mut self: Entity, amount: int) {
        self.health -= amount
    }
}

// 函数定义
function main() {
    let player = Entity(100)
    player.takeDamage(20)
}
```

**语法要点**：

- 程序 = `include` 语句 + 顶层声明（类/函数/变量/常量）
- `include` 用于导入外部模块，接受字符串字面量
- 支持三种函数声明风格：`function`、`fn`、`def`

### 类型系统

#### 基础类型

| 类型      | 说明   | 示例值        |
|---------|------|------------|
| int     | 整数   | 42, -10    |
| float   | 浮点数  | 3.14, -0.5 |
| string  | 字符串  | "Hello"    |
| boolean | 布尔值  | true/false |
| null    | 空值句柄 | null       |

#### 类型标注

所有变量、参数、函数返回值**强制类型标注**（除非使用 `let` 自动推导）：

```dovetail
let x = 42                    // 自动推导为 int
let y: int = 42               // 显式标注
const MAX: int = 100          // 常量必须初始化

function add(a: int, b: int) -> int {
    return a + b
}

// 或使用前置类型风格
function int add(int a, int b) {
    return a + b
}
```

#### 复合类型

```dovetail
// 数组类型
let fixed_array: int[10]              // 固定大小数组
let dynamic_array: int[]              // 动态数组
let matrix: int[10][20]               // 多维数组

// 可空类型（仅对象）
let nullable_entity: Entity?          // 可为 null 的对象引用

// 类类型
class Player { /*...*/ }
```

**数组大小**可使用常量表达式或标识符：

```dovetail
const SIZE = 10
let arr: int[SIZE]
```

### 类与多继承

Dovetail 支持**多继承**：

```dovetail
class Zombie(Mob, Damageable, Aggressive) {
    let health: int
    
    method attack(target: Entity) {
        target.takeDamage(5)
    }
}

// 无继承
class SimpleEntity() {
    let id: int
}
```

**语法规则**：

- 类使用 `class` 关键字定义
- 支持多继承：`class Name(Parent1, Parent2, ...)`
- 成员变量使用 `let` 声明，必须标注类型
- 方法使用 `method` 关键字（可选，因为语法允许省略）

### 注解系统

支持内置注解和插件注解：

```dovetail
@inline
function fast_add(a: int, b: int) -> int {
    return a + b
}

@optimize("level", 3)
@deprecated
class OldSystem() {
    // ...
}
```

**语法规则**：

- `@ID` 或 `@ID(literal, literal, ...)`
- 可标注函数、类、方法

### 控制流语句

#### 条件分支

```dovetail
if (player.health <= 0) {
    respawnPlayer(player)
} else if (player.health < 20) {
    showWarning(player)
} else {
    showHealthBar(player)
}
```

#### 循环结构

```dovetail
// 传统 for 循环
for (let i: int = 0; i < 10; i += 1) {
    summonChicken()
}

// 增强 for 循环（迭代对象）
for (Entity entity: getEntities()) {
    entity.update()
}

// while 循环
while (gameRunning) {
    updateScoreboard()
}
```

**注意**：增强 for 循环中的表达式必须是可迭代类型（语义分析时检查）。

#### 其他控制语句

```dovetail
return value          // 返回值
return                // 无返回值
break                 // 跳出循环
continue              // 继续下一次循环
free resource         // 释放资源
pass                  // 空语句（或使用 ;）
```

### 表达式系统

#### 运算符优先级（从高到低）

| 优先级 | 运算符                          | 描述           |
|-----|------------------------------|--------------|
| 1   | `()` `.` `[]`                | 括号、成员访问、数组访问 |
| 2   | `-` `!` `not`                | 一元负号、逻辑非     |
| 3   | `*` `/` `%`                  | 乘除、模运算       |
| 4   | `+` `-`                      | 加减           |
| 5   | `==` `!=` `<` `>` `<=` `>=`  | 比较运算         |
| 6   | `&&` `and`                   | 逻辑与          |
| 7   | `\|\|` `or`                  | 逻辑或          |
| 8   | `=` `+=` `-=` `*=` `/=` `%=` | 赋值运算         |

#### 特殊表达式

```dovetail
// F-string（插值字符串）
let name = "Steve"
let msg = f"Hello, {name}!"

// 方法调用
entity.takeDamage(10)

// 成员访问
player.health

// 数组访问
arr[5]

// 函数调用
add(1, 2)

// 复合赋值
health += 10
arr[i] *= 2
player.score -= 5
```

#### 可变参数

使用 `mut` 关键字标记可变参数（目前仅对数组有效）：

```dovetail
function modify_array(mut arr: int[]) {
    arr[0] = 100  // 修改传入的数组
}
```

### 变量与常量

#### 变量声明

```dovetail
let x = 42                // 自动类型推导
let y: int = 42           // 显式类型
let z: int                // 延迟初始化（需要在使用前赋值，否则将出现未定义行为）
```

#### 常量声明

```dovetail
const PI: float = 3.14159
const int MAX = 100       // 前置类型风格
```

**注意**：常量必须在声明时初始化。

### 注释

支持多种注释风格：

```dovetail
// C++ 风格单行注释

/* C 风格
   多行注释 */

# Python 风格单行注释

[[ Lua 风格
   多行注释 ]]
```

## 变更日志

- 2025-06-06 初版草案
- 2025-08-26 更新了文档
- 2025-12-28 修改了项目信息以适应最新格式
- 2026-02-07 为语法更新做准备
- 2026-02-12 语法更新，采用 Lark 解析器代替旧有 ANTLR 解析器
- 2026-03-06 新增多继承、F-string、可空类型等特性
