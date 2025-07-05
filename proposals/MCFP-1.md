# MCFP 1: 基础语法规范

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

本提案定义 McFuncDSL 的基础语法规范，包括程序结构、类型系统、控制流、类与接口定义等核心语言特性，为后续高级特性提供语法基础。

## 动机

Minecraft 命令系统缺乏结构化编程能力，现有解决方案存在以下问题：

1. 代码复用困难
2. 类型安全性缺失
3. 复杂逻辑表达能力有限
4. 缺乏面向对象特性

通过建立标准化的基础语法体系，可实现：

- 更好的代码组织能力
- 编译时类型检查
- 面向对象编程支持
- 与其他工具链的兼容性

## 技术规范

### 1. 程序结构

    import "minecraft_utils.mcdl";  // 模块导入
    
    class Entity extends BaseEntity implements Trackable {
        var health: int = 20;  // 字段声明
        
        constructor(name: string) {
            // 初始化逻辑
        }
        
        method takeDamage(amount: int): void {
            this.health = amount;
        }
    }
    
    func main():void {
        for (e : new Selector("@e[type=zombie]")) {
            // 命令执行块
        }
    }

### 2. 类型系统

#### 基础类型

| 类型       | 说明       | 示例值          |
|----------|----------|--------------|
| int      | 32位整数    | 42           |
| string   | UTF-8字符串 | "Hello"      |
| boolean  | 布尔值      | true/false   |
| Selector | 实体选择器    | @e[type=cow] |
| void     | 无返回值类型   | -            |

#### 复合类型

    class Player { /*...*/ }      // 类类型
    interface Damageable { /*...*/ } // 接口类型
    var arr: int[] = [1,2,3];     // 数组类型（需MCFP-5扩展）

### 3. 类与接口

    // 单继承+多接口实现
    class Zombie extends Mob implements Damageable, Trackable {
        const MAX_HEALTH: int = 20;  // 类常量
        
        method attack(target: Entity): void {
            cmd f"effect give ${target} minecraft:poison 30 1"!;
        }
    }

    // 接口定义
    interface Damageable {
        method takeDamage(amount: int): void;
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

1. () . [] (成员访问/方法调用)
2. \- (负号) ! (非)
3. \* /
4. \+ \-
5. \> < >= <=
6. == !=
7. && ||

#### 类型转换规则

    var num: int = (int) 3.14;  // 显式类型转换
    var str: string = "Count: " + (10).toString();

## 兼容性影响

1. 新增关键字（class/interface/extends等）可能导致现有标识符冲突
2. 强制类型标注要求现有无类型代码需添加类型声明
3. 选择器类型化需要重写原始字符串选择器

迁移方案：

- 提供自动类型推导工具
- 兼容模式允许省略类型标注（需@SuppressWarnings注解）
- 选择器字符串自动包装为Selector类型

## 参考实现

[语法解析器实现（ANTLR4）]

    // 节选自提案附带的语法规则
    expr
     : cmdExpr                            #CmdExpression
     | expr '.' ID argumentList          #MethodCall
     | expr '.' ID                       #MemberAccess
     | ID argumentList                   #DirectFuncCall
     | primary                           #PrimaryExpr
     | '-' expr                          #NegExpr
     | expr ('*'|'/') expr               #MulDivExpr
     | expr ('+'|'-') expr               #AddSubExpr
     | expr ('>'|'<'|'=='|'!='|'<='|'>=') expr #CompareExpr
     ;

    primary
     : 'new' 'Selector' '(' STRING ')'   #NewSelectorExpr
     | ID                                #VarExpr
     | literal                           #LiteralExpr
     | '(' expr ')'                      #ParenExpr
     | 'new' ID argumentList             #NewObjectExpr
     ;

## 变更日志

- 2025-06-06 初版草案