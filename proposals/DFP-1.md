# DFP 1: 基础语法规范

## 状态

- [ ] Draft
- [ ] Proposed
- [ ] Accepted
- [ ] Rejected
- [ ] Deferred
- [ ] Implemented (版本: 1.0.0)
- [x] Active
- [ ] Abandoned (版本: )

## 作者

- 771835 <2790834181@qq.com>

## 创建日期

- 2025-06-06

## 摘要

该提案定义了 Dovetail 的基础语法规范，涵盖了程序结构、类型系统、类与接口、控制流和表达式等内容。目标是为 Dovetail
提供一套结构化、安全且可扩展的基础语法体系，为后续模块提供语法与语义基础支持。

## 动机

当前 Minecraft 中的命令编写方式存在以下问题：

1. 代码复用性差：缺乏模块化与完整函数定义机制
2. 类型安全性不足：无法检查数据流动和使用上的错误
3. 表达能力有限：逻辑越复杂越难以维护
4. 缺乏面向对象能力：无法构建可复用的实体结构。

通过引入面向对象与结构化的语法设计，Dovetail 将实现如下改进：

- 代码结构更具模块性和可维护性
- 提供**编译时类型检查**
- 支持**类与接口定义**，增强模块间交互
- 更易于与现代开发工具链集成

## 技术规范

### 1. 程序结构

Dovetail 支持模块化开发，允许导入与模块组织：

```dovetail
include "math";  // 模块导入

class Entity extends BaseEntity implements Trackable {
    var health: int = 20;  // 字段声明

    method __init__(self: Entity, name: string) {
        // 初始化逻辑
    }

    method takeDamage(self: Entity, amount: int) {
        this.health = this.health - amount;
    }
}

func main(): void {
    for (entity : Selector("@e[type=zombie]")) {
        entity.takeDamage(5);
    }
}

```

### 2. 类型系统

#### 基础类型

| 类型      | 说明     | 示例值        |
|---------|--------|------------|
| int     | 32位整数  | 42         |
| string  | 字符串    | "Hello"    |
| boolean | 布尔值    | true/false |
| null    | 无返回值/空 | -          |

#### 复合类型

    class Player { /*...*/ }      // 类类型
    interface Damageable { /*...*/ } // 接口类型
    var arr: int[] = [1,2,3];     // 数组类型（需DFP-5扩展）

### 3. 类与接口

    // 单继承+多接口实现
    class Zombie extends Mob implements Damageable, Trackable {
        const MAX_HEALTH: int = 20;  // 类常量
        
        method attack(target: Entity) {
            exec(f"effect give ${target} minecraft:poison 30 1"!);
        }
    }

    // 接口定义
    interface Damageable {
        method takeDamage(amount: int);
    }

### 4. 控制流语句

#### 条件分支

    if (player.health <= 0) {
        respawnPlayer(player);
    } else {
        showHealthBar(player);
    }

#### 循环结构

    // 传统for循环
    for (var i: int = 0; i < 10; i = i + 1) {
        summonChicken();
    }

    // 增强for循环（选择器迭代）
    for (entity: "@e[type=sheep]") { // "@e[type=sheep]"可以替换成new Selector("@e[type=sheep]")
        dyeSheep(entity, COLORS.RED);
    }

    // while循环
    while (gameRunning) {
        updateScoreboard();
    }

### 5. 表达式系统

#### 运算符优先级（从高到低）

| 运算符             | 描述        |
|-----------------|-----------|
| `() . []`       | 成员访问/方法调用 |
| `-, !`          | 一元负号、逻辑非  |
| `*, /, %`       | 乘除、模运算    |
| `+, -`          | 加减        |
| `> , <, >=, <=` | 大小比较      |
| `==, !=`        | 等值判断      |
| `&&`            | 逻辑与       |
| `\|\|`          | 逻辑或       |
| `?:, if/else`   | 三元表达式     |

## 参考实现

[语法解析器实现（ANTLR4）](../antlr/transpiler.g4)

    // 节选自提案附带的语法规则
    expr
    : primary                              # PrimaryExpr
    | expr '.' ID argumentList             # MethodCall
    | expr '.' ID                          # MemberAccess
    | expr '[' expr ']'                    # ArrayAccess
    | expr argumentList                    # FunctionCall
    | '-' expr                             # NegExpr
    | '!' expr                             # LogicalNotExpr
    | expr ('*' | '/' | '%') expr          # FactorExpr
    | expr ('+' | '-') expr                # TermExpr
    | expr ('>' | '<' | '==' | '!=' | '<=' | '>=') expr  # CompareExpr
    | expr '&&' expr                       # LogicalAndExpr
    | expr '||' expr                       # LogicalOrExpr
    | <assoc=right> expr '?' expr ':' expr # TernaryTraditionalExpr
    | <assoc=right> expr IF expr ELSE expr # TernaryPythonicExpr
    | expr '[' expr ']' '=' expr           # ArrayAssignmentExpr
    | expr '.' ID '=' expr                 # MemberAssignmentExpr
    | ID '=' expr                          # LocalAssignmentExpr
    ;

## 变更日志

- 2025-06-06 初版草案
- 2025-08-26 更新了文档