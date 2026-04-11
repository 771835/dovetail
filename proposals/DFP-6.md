# DFP 6: 内置注解规范

## 提案信息

**作者**: 771835 <2790834181@qq.com>  
**状态**: Proposed  
**创建日期**: 2025-11-15  
**最新更新**: 2026-04-11

## 摘要/设计目标

规范化 Dovetail 语言的注解系统，定义所有内置注解的语法、语义和使用规则。建立统一的注解分类体系，明确注解的优先级、组合规则和冲突处理机制，为编译器优化和代码生成提供标准化指导。

## 动机

当前 Dovetail 编译器的注解系统存在以下问题：

1. 缺乏标准规范：注解的语法和语义散落在各个模块中，没有统一文档
2. 语义重叠混乱：执行时机注解与优化控制混合，职责边界不清
3. 扩展性不足：新增注解时缺乏设计指导，容易产生冲突
4. 优化器行为不一致：不同优化pass对注解的处理逻辑不统一

## 技术规范

### 注解语法

```lark
// 仅允许使用内置注解及插件注解
annotation : "@" ID | "@" ID "(" literal ("," literal)* ")"
```

### 注解分类体系

#### 1. 执行生命周期注解 (Lifecycle Annotations)

这些注解控制函数在 Minecraft 数据包生命周期中的执行时机。

##### `@init`

```dovetail
@init
fn setup() {
    // 数据包加载时执行，用于初始化
}
```

- **执行时机**：每次数据包加载（包括重载）
- **执行顺序**：按声明顺序
- **常用场景**：资源初始化、状态重置

##### `@tick(interval=1)`

```dovetail
@tick
fn gameLoop() {
    // 每游戏刻执行
}

@tick(20)  // 每20刻执行一次
fn slowUpdate() {
    // 降频执行的逻辑
}
```

- **执行时机**：游戏刻更新
- **可选参数**：`interval` - 执行间隔（刻数）
- **性能考虑**：避免过重逻辑

#### 2. 可见性控制注解 (Visibility Annotations)

控制函数的可见性和是否可被优化器删除。

##### `@internal`

```dovetail
@internal  
fn helperFunction() {
    // 内部函数，可激进优化
}
```

- **语义**：标记为内部实现，可积极优化
- **优化影响**：允许内联、删除未使用分支
- **默认行为**：未标注的函数默认为 @internal

##### `@noinline`

```dovetail
@noinline
fn complexFunction() {
    // 禁止内联此函数
}
```

- **影响优化**：阻止函数内联
- **使用场景**：调试、性能分析、代码大小控制

#### 3. 链接接口生成注解 (Linkage Annotations)

控制后端链接接口指令的生成

##### `@export`

```dovetail
    @export("dovetail:api/1")
    fn publicAPI() {
        // 导出函数，不会被优化删除
    }
```

- **语义**：标记为外部可访问，防止优化删除
- **用途**：API函数、调试接口、插件入口点
- **优化影响**：阻止死代码消除
- **参数**：
    1. `path` - 导出路径
    2. `abi` - 导出格式
- **特殊事宜**：有此注解的函数的函数名不会被归一化，故函数名不可使用大写字符或unicode字符

##### `@extern`

```dovetail
    @extern("dovetail:api/1")
    fn publicAPI(); // 导入函数，运行时寻找实际实现
```

- **语义**：标记为外部导入，不提供实现
- **用途**：API函数、调用其他数据包
- **优化影响**：阻止内联优化和函数调用删除
- **参数**：
    1. `path` - 导入路径
    2. `abi` - 参数传递格式
- **特殊事宜**：对于一些复杂数据类型参数不支持

#### 4. 条件编译注解注解 (Condition Annotations)

控制代码编译生成的注解。

##### `@target`

```dovetail
@target("je")  // Java Edition
fn javaSpecific() {
    // 仅在JE后端生成
}

@target("be")  // Bedrock Edition  
fn bedrockSpecific() {
    // 仅在BE后端生成
}

```

- **参数**：目标平台标识符
- **条件编译**：根据编译目标选择性生成
- **默认**：所有支持的目标平台
- **处理时机**：AST遍历阶段处理

##### `@version`

```dovetail
@version(min="1.19", max="1.20")
fn modernFeature() {
    // 版本限制的功能
}
```

- **参数**：`min`, `max` - 版本范围
- **验证**：编译时检查目标版本兼容性
- **格式**：语义版本号字符串
- **处理时机**：AST遍历阶段处理

##### `@if_not_exists`

```dovetail
@if_not_exists
fn setupScoreboard() {
    // 如果环境中已存在同名函数，跳过此声明
    // 用于提供默认实现
}
```

- **语义**
    - 编译时检查符号表是否已有同名函数
    - 如果存在则跳过当前声明（不覆盖）
    - 典型场景：库提供默认实现，允许用户覆盖
- **处理时机**：AST遍历阶段处理

##### `@if_symbol`

```dovetail
@if_symbol("AdvancedAPI")  // 仅当类 AdvancedAPI 存在时编译
fn useAdvancedFeature() {
    // 依赖特定符号的功能
}
```

- **参数**：
    1. `name` - 符号名称
    2. `type` - 符号类型(`class` | `function`| `variable` | `any`)
- **语义**
    - 编译时检查符号表存在指定符号
    - 如果存在则**进行**当前声明
- **处理时机**：AST遍历阶段处理

##### `@if_feature`

```dovetail
@if_feature("scoreboard_macros")
fn advancedScoreboard() {
    // 仅当编译配置启用该特性时生成
}
```

- **参数**：`feature` - 功能名称
- **语义**
    - 编译时检查编译器是否开启特定功能/配置
    - 如果存在则**进行**当前声明
- **处理时机**：AST遍历阶段处理

#### 5. 元数据注解 (Metadata Annotations)

提供额外信息的注解，不影响代码生成。

##### `@deprecated`

```dovetail
@deprecated("Use newFunction() instead")
fn oldFunction() {
    // 标记为已废弃
}
```

- **参数**：废弃消息
- **编译时警告**：使用时产生警告
- **文档生成**：影响API文档
- **特殊行为**：当开启 `--disable-deprecated-function` 时此类函数不会被声明和定义

##### `@doc`

```dovetail
@doc("Calculates player distance in blocks")
fn getDistance(player1: string, player2: string) -> float {
    // 文档注解
}
```

- **参数**：文档字符串
- **用途**：自动生成API文档
- **格式**：支持Markdown语法

##### `@author`

```dovetail
@author("PlayerName")
fn customLogic() {
    // 作者标记
}
```

- **参数**：作者名称
- **用途**：代码归属追踪
- **生成**：可选择包含在生成的注释中

##### `@since`

```dovetail
@since("1.1.0")
fn newFeature() {
    // 版本引入标记
}
```

- **参数**：引入版本号
- **文档**：API文档版本信息
- **兼容性**：向后兼容性追踪

#### 6. 后端处理提示注解 (Backend Hint)

这些注解**不影响 IR 生成**，仅作为后端优化提示传递到后端。

##### `@recursive`

```dovetail
@recursive
fn factorial(n: int) -> int {
    // 后端为此函数生成栈帧管理代码
    if (n <= 1) return 1;
    return n * factorial(n - 1);
}
```

- **语义**
  - **前端**：正常处理，将注解附加到函数符号
  - **后端**：检测到此注解时，为局部变量使用栈式存储而非全局计分板

## 变更日志

- 2025-11-15 提出提案
- 2025-12-28 修改了项目信息以适应最新格式
- 2026-04-11 增加了一些函数 