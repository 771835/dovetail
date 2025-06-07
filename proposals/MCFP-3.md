# MCFP 3: McFuncDSL 到 Minecraft 命令的编译规范

## 状态
- [x] Draft  
- [ ] Proposed  
- [ ] Accepted  
- [ ] Rejected  
- [ ] Deferred  
- [ ] Implemented (版本: -)  

## 作者
- 771835 <2790834181@qq.com>  

## 创建日期
- 2025-06-06  

## 摘要
本提案规范 McFuncDSL 到 Minecraft 命令的编译策略，定义基于 Visitor 模式和 Scoreboard/NBT Storage 的编译实现方案，建立变量存储、控制流实现和函数调用的标准化编译流程。

## 动机
为实现 McFuncDSL 的高级语言特性在 Minecraft 原生命令系统上的运行，需解决以下核心问题：
1. 变量存储系统需要兼容 Scoreboard 和 NBT 的物理限制
2. 复杂控制流语句在函数文件体系中的实现
3. 类型系统到 Minecraft 原生数据结构的映射
4. 编译期优化与运行时效率的平衡

## 技术规范

### 1. 核心编译架构
#### 1.1 Visitor 模式实现
    // AST 遍历伪代码
    public class MCGenerator extends McFuncDSLBaseVisitor<Void> {
        @Override
        public Void visitVarDeclaration(McFuncDSLParser.VarDeclarationContext ctx) {
            // 1. 解析变量类型和初始值
            // 2. 在符号表中注册 Symbol 对象
            // 3. 生成初始化命令（scoreboard/data modify）
            return super.visitVarDeclaration(ctx);
        }
    }

#### 1.2 作用域树管理
    global_scope (root)
    ├── function_foo_scope
    │   └── for_loop_scope
    └── function_bar_scope
        ├── if_stmt_scope
        └── else_stmt_scope

### 2. 变量存储系统
#### 2.1 存储位置决策矩阵
| 操作类型   | Scoreboard 处理             | NBT 处理                         |
|--------|---------------------------|--------------------------------|
| 整数运算   | 直接使用 scoreboard operation | 需先执行 data get 转存到临时 Scoreboard |
| 字符串拼接  | 不支持                       | 通过 storage 的 append 操作实现       |
| 布尔条件判断 | 使用 execute if score       | 需转存为 0/1 的 Scoreboard 值        |

#### 2.2 变量生命周期示例
    var a:int = 10;  // 生成: scoreboard objectives add mcfdsl dummy
                   // scoreboard players set global.a mcfdsl 10
    
    var b:string = "text"; // 生成: data modify storage mcfdsl:global.data.b set value "text"

### 3. 表达式求值机制
#### 3.1 类型提升规则
    Operand1 | Operand2 | ResultType
    int      | int      | int
    int      | bool     | int
    string   | any      | string（自动调用 toString）

#### 3.2 临时变量生成策略
    // 处理 a = b + c 的伪代码
    1. 获取 b 的存储位置（假设为 NBT）
    2. 生成: execute store result score $temp1 run data get storage mcfdsl b
    3. 获取 c 的存储位置（假设为 Scoreboard）
    4. 生成: scoreboard players operation $temp2 = $temp1 + c.score
    5. 将 $temp2 赋值给 a

### 4. 控制流实现
#### 4.1 While 循环编译模式
    // 原始代码
    while (condition) {
        body
    }
    
    // 生成结构
    main.mcfunction:
        execute unless score $cond run function exit_loop
        function loop_body
        function loop_update
        function loop_check
    
    loop_check.mcfunction:
        execute store result score $cond run ... // 重新计算条件
        execute if score $cond run function loop_body

#### 4.2 If-Else 语句实现
    // 生成命令序列
    execute if score $condition matches 1 run function if_block
    execute unless score $condition matches 1 run function else_block

### 5. 函数调用规范
#### 5.1 参数传递机制
    // 调用 func(10, "test") 生成:
    scoreboard players set #arg0 mcfdsl 10
    data modify storage mcfdsl:args.0 set value "test"
    function namespace:func
    
    // 函数内参数读取:
    scoreboard players operation local.x = #arg0 mcfdsl
    data modify storage mcfdsl:local.data.x set from storage mcfdsl:args.0

## 兼容性影响
1. 要求 Minecraft 1.20+ 版本（依赖 execute store 语法）
2. 与纯命令块实现的模块存在 NBT 存储冲突风险
3. 需要预先生成 mcfdsl:storage 数据结构

## 参考实现
[mcfpp](https://github.com/rozukke/mcpp)


## 变更日志
- 2025-06-06 初版草案
- 2025-06-07 增加表达式求值和类型转换细节,修正了示例代码的语法错误
