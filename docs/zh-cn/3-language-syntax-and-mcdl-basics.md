# 语言语法与 MCDL 基础

## 1. 基本程序结构

```mcdl
@init
fn main() {
    print("Hello World!")
}
```

- 语句末尾**不需要分号**（`;` 等价于 `pass`，即空语句）
- `fn`、`function`、`def` 三个关键字等价，均可定义函数
- `@init` 注解标记此函数在数据包加载时执行

## 2. 函数

### 2.1 定义函数

```mcdl
// 无参数函数
fn sayHello() {
    print("你好！")
}

// 有参数函数（参数格式：名称: 类型）
fn greet(name: string) {
    print("你好，" + name)
}

// 选填参数（必须放在最后）
fn greet(name: string = "世界") {
    print("你好，" + name)
}

// 有返回值的函数
fn add(a: int, b: int) -> int {
    return a + b
}
```

> ⚠️ 不写 `return` 是**未定义行为**，可能造成任何未知问题。

### 2.2 前向声明

```mcdl
fn foo() -> int;       // 声明但不实现（以分号结尾）

@init
fn bar() {
    print(str(foo()))
}

fn foo() -> int {      // 后续提供实现
    return 42
}
```

### 2.3 调用函数

```mcdl
sayHello()
greet("小明")
let result = add(5, 3)
```

## 3. 变量与常量

```mcdl
let name = "小明"              // 自动推导类型
let age: int = 25             // 明确指定类型
let flag: boolean = true
let foo: int                  // 仅声明，需标明类型（使用前必须赋值，否则为未定义行为）

const MAX: int = 100          // 常量
```

## 4. 数据类型

### 4.1 基本类型

| 类型        | 说明            | 示例              |
|-----------|---------------|-----------------|
| `int`     | 整数            | `42`, `-5`      |
| `string`  | 字符串           | `"你好"`          |
| `boolean` | 布尔值           | `true`, `false` |
| `void`    | 空返回类型（不可用于变量） | —               |
| `null`    | 空值（不可初始化为此类型） | `null`          |

> `boolean` 是 `int` 的子类型，可以强制转换。

### 4.2 复合类型

```mcdl
let arr: int[100]     // 固定大小数组
let items: int[]      // 动态数组
```

内部类型系统还支持泛型形式：`list<T>`、`array<T>`、`map<K, V>`。

### 4.3 可空类型

```mcdl
let obj: MyClass?     // 可空（仅对象类型允许 ? 标记）
```

### 4.4 类型别名

```mcdl
typedef int i32       // i32 是 int 的别名
```

## 5. 字符串操作

```mcdl
let a = "你好"
let b = "世界"
let c = a + "，" + b + "！"      // 字符串拼接
let d = f"你好，{b}！"            // f-string 插值
let e = f"结果是 {1 + 2}"         // 插值表达式
```

## 6. 运算符

### 6.1 算术运算符

`+` `-` `*` `/` `%`

### 6.2 比较运算符

`==` `!=` `<` `<=` `>` `>=`

### 6.3 逻辑运算符

`&&`（逻辑与） `||`（逻辑或） `!`（逻辑非）
`and` / `or` 为对应关键字形式，语义相同。

### 6.4 位运算符

`&` `|` `^` `<<` `>>` `~`

> ⚠️ 位运算部分后端可能不实现，使用前确认后端支持。

## 7. 条件语句

```mcdl
if (age >= 18) {
    print("成年")
} else if (age >= 12) {
    print("青少年")
} else {
    print("儿童")
}
```

## 8. 循环语句

```mcdl
// 传统 for 循环
for (let i = 0; i < 5; i++) {
    print(str(i))
}

// 增强 for 循环（expr 需为可迭代 class）
for (int item : collection) {
    print(str(item))
}

// while 循环
let count = 0
while (count < 3) {
    print(str(count))
    count = count + 1
}
```

流程控制关键字：`break`、`continue`、`return`、`pass`（`;` 等价）

## 9. 类与对象

### 9.1 定义类

```mcdl
class Student {
    string name
    int age

    method __init__(Student self, string name, int age) {
        self.name = name
        self.age = age
    }

    method greet(Student self) {
        print(f"你好，我是 {self.name}")
    }
}
```

### 9.2 创建与使用对象

```mcdl
@init
fn main() {
    Student s = Student("Alice", 18)
    s.greet(s)               // 调用方法时需显式传入 self
    s.age = 20               // 直接修改字段
    print(str(s.age))
}
```

### 9.3 多继承

```mcdl
class C : A, B {
    // ...
}
```

### 9.4 类的约束

- **显式 self**：所有方法第一个参数必须是对象自身引用
- **不支持方法重载**：同一类中方法名必须唯一
- **引用语义**：`a = b` 使两者指向同一实例
- **不支持递归**：类间循环调用会造成严重问题
- **未初始化字段**：使用未赋值字段是未定义行为

## 10. 结构体

```mcdl
struct Point {
    x: int
    y: int
}
```

## 11. 枚举

```mcdl
enum Direction {
    NORTH = 0,
    SOUTH = 1,
    EAST  = 2,
    WEST  = 3,
}
```

## 12. include

```mcdl
include "random"           // 包含库（无后缀，从库路径加载）
include "mathlib.mcdl"     // 包含源文件（带后缀）
```

## 13. 内置函数

| 函数              | 说明                      |
|-----------------|-------------------------|
| `print(expr)`   | 输出到聊天框（生成 `tellraw` 指令） |
| `str(expr)`     | 将值转为字符串                 |
| `exec(command)` | 执行原始 Minecraft 指令       |

更多内置函数见 [DFP-300](../../proposals/DFP-300.md)。

## 14. 注解速览

```mcdl
@init                                  // 数据包加载时执行
@tick                                  // 每 tick 执行
@tick("interval" = 5)                  // 每 5 tick 执行
@target("edition" = "java")            // 仅 Java 版编译
@version("min" = "1.20.4", "max" = "1.21.5")
@deprecated("msg" = "请用新函数")
@internal                              // 允许激进优化
@noinline                              // 禁止内联
@recursive                             // 声明递归函数（需 --recursion）
```

完整注解文档见 [注解系统与自定义注解](21-annotation-system-and-custom-annotations)。

## 下一步

- [代码示例解析](4-code-examples-walkthrough) — 通过实际示例加深理解
- [注解系统与自定义注解](21-annotation-system-and-custom-annotations) — 注解完整参考