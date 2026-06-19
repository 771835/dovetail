# 代码示例解析

`example/` 目录包含 17 个 `.mcdl` 示例文件，覆盖了从基础语法到复杂特性的完整语言功能。

## example1.mcdl — 条件编译与前向声明

```mcdl
include "random"
include "mathlib.mcdl"
typedef int i32

fn foo() -> i32;          // 前向声明，仅声明签名

@init
fn bar() {
    if (foo() == 350234) {
        exec("say 𝔀𝓪𝔀")
        print("1")
    } else {
        exec("say 2")
    }
}

@target("edition" = "java")
fn foo() -> i32 {
    return 350234
}

@target("edition" = "be")
fn foo() -> i32 {
    return 0
}
```

**要点：**

- `typedef int i32` 创建类型别名
- `fn foo() -> i32;` 是前向声明（以分号结尾）
- `@target` 注解实现平台条件编译，两个 `foo` 实现只有一个会被编译进数据包
- `include` 不带后缀表示加载库，带 `.mcdl` 后缀表示包含源文件

## example2.mcdl — 数组与全局变量

```mcdl
let arr1: int[100]
let p = 0

fn foo(arr: int[]) -> int {
    arr1[p] = 1
}

@init
fn main() {
    let var = foo()
    print(str(var))
}
```

**要点：**

- 全局变量在函数外声明
- `int[100]` 固定大小数组，`int[]` 动态数组参数
- `str()` 将整数转为字符串以供 `print` 使用

## example3.mcdl — 类与对象

展示类定义、构造函数、字段访问与方法调用的完整流程：

```mcdl
class Player {
    string name
    int health

    method __init__(Player self, string playerName) {
        self.name = playerName
        self.health = 20
    }

    method heal(Player self, int amount) {
        self.health = self.health + amount
        if (self.health > 20) {
            self.health = 20
        }
        print(f"{self.name} 治疗了 {amount} 点")
    }
}

@init
fn main() {
    Player steve = Player("Steve")
    steve.heal(steve, 5)        // 调用方法时显式传入 self
}
```

**要点：**

- 构造函数固定名称为 `__init__`，不返回值
- 方法调用语法：`obj.method(obj, args...)` — self 必须显式传入
- f-string 插值可直接嵌入字段访问表达式

## example4-17.mcdl — 语言特性覆盖

| 示例        | 主要特性                      |
|-----------|---------------------------|
| example4  | while 循环、break/continue   |
| example5  | for 循环（传统与增强）             |
| example6  | 结构体（struct）               |
| example7  | 枚举（enum）                  |
| example8  | 多继承类                      |
| example9  | `@version` 版本条件编译         |
| example10 | `@deprecated` 弃用标注        |
| example11 | 常量折叠验证                    |
| example12 | 嵌套函数与作用域                  |
| example13 | 字符串操作                     |
| example14 | `@internal` / `@noinline` |
| example16 | 递归（需 `--recursion`）       |
| example17 | 复杂类层次结构                   |

## 通用语法规律总结

从所有示例中可以归纳出以下规律：

1. **无分号**：语句末尾不加分号，`;` 仅作空语句使用
2. **注解先行**：注解紧贴函数/类定义，不可用于变量
3. **显式 self**：方法定义和调用均需显式处理 self 参数
4. **类型前置**：变量声明中类型在名称之前，如 `Player steve = Player(...)`，或使用 `let` 自动推导
