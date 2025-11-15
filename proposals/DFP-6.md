# DFP 6: 内置注解规范

## 状态

- [ ] Draft
- [x] Proposed
- [ ] Accepted
- [ ] Rejected
- [ ] Deferred
- [ ] Implemented (版本: )
- [ ] Active
- [ ] Abandoned (版本: )

## 作者

- 771835 <2790834181@qq.com>

## 创建日期

- 2025-11-15

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

```antlrv4
annotation // 仅允许使用内置注解及插件注解
    : '@' ID
    | '@' ID LPAREN literal (COMMA literal)* RPAREN
    ;
```

### 注解分类体系

#### 1. 执行生命周期注解 (Lifecycle Annotations)

这些注解控制函数在 Minecraft 数据包生命周期中的执行时机。

##### `@init`

```dovetail
@init
func setup() {
    // 数据包加载时执行，用于初始化
}
```

- **执行时机**：每次数据包加载（包括重载）
- **执行顺序**：按声明顺序
- **常用场景**：资源初始化、状态重置

##### `@tick(interval=1)`

```dovetail
@tick
func gameLoop() {
    // 每游戏刻执行
}

@tick(20)  // 每20刻执行一次
func slowUpdate() {
    // 降频执行的逻辑
}
```

- **执行时机**：游戏刻更新
- **可选参数**：`interval` - 执行间隔（刻数）
- **性能考虑**：避免过重逻辑

#### 2. 可见性控制注解 (Visibility Annotations)

控制函数的可见性和是否可被优化器删除。

##### `@export`

```dovetail
    @export
    func publicAPI() {
        // 导出函数，不会被优化删除
    }
```

- **语义**：标记为外部可访问，防止优化删除
- **用途**：API函数、调试接口、插件入口点
- **优化影响**：阻止死代码消除

##### `@internal`

```dovetail
@internal  
func helperFunction() {
    // 内部函数，可激进优化
}
```

- **语义**：标记为内部实现，可积极优化
- **优化影响**：允许内联、删除未使用分支
- **默认行为**：未标注的函数默认为 @internal

##### `@public`

```dovetail
@public
func libraryFunction() {
    // 库函数，对其他模块可见
}
```

- **语义**：跨模块可见性
- **作用域**：模块级别的可见性控制
- **与 @export 区别**：@public 是模块间可见，@export 是优化保护

##### `@noinline`

```dovetail
@noinline
func complexFunction() {
    // 禁止内联此函数
}
```

- **影响优化**：阻止函数内联
- **使用场景**：调试、性能分析、代码大小控制

#### 3. 代码生成控制注解 (Codegen Annotations)

控制目标代码生成的注解。

##### `@target`

```dovetail
@target("je")  // Java Edition
func javaSpecific() {
    // 仅在JE后端生成
}

@target("be")  // Bedrock Edition  
func bedrockSpecific() {
    // 仅在BE后端生成
}

@target(["je", "be"])  // 多目标
func crossPlatform() {
    // 在指定平台生成
}
```

- **参数**：目标平台标识符
- **条件编译**：根据编译目标选择性生成
- **默认**：所有支持的目标平台
- **处理时机**：AST遍历阶段处理

##### `@version`

```dovetail
@version(min="1.19", max="1.20")
func modernFeature() {
    // 版本限制的功能
}
```

- **参数**：`min`, `max` - 版本范围
- **验证**：编译时检查目标版本兼容性
- **格式**：语义版本号字符串
- **处理时机**：AST遍历阶段处理

#### 4. 元数据注解 (Metadata Annotations)

提供额外信息的注解，不影响代码生成。

##### `@deprecated`

```dovetail
@deprecated("Use newFunction() instead")
func oldFunction() {
    // 标记为已废弃
}

@deprecated(since="1.2.0", removal="2.0.0")  
func legacyAPI() {
    // 详细废弃信息
}
```

- **参数**：废弃消息、版本信息
- **编译时警告**：使用时产生警告
- **文档生成**：影响API文档

##### `@doc`

```dovetail
@doc("Calculates player distance in blocks")
func getDistance(player1: string, player2: string): float {
    // 文档注解
}
```

- **参数**：文档字符串
- **用途**：自动生成API文档
- **格式**：支持Markdown语法

##### `@author`

```dovetail
@author("PlayerName")
func customLogic() {
    // 作者标记
}
```

- **参数**：作者名称
- **用途**：代码归属追踪
- **生成**：可选择包含在生成的注释中

##### `@since`

```dovetail
@since("1.1.0")
func newFeature() {
    // 版本引入标记
}
```

- **参数**：引入版本号
- **文档**：API文档版本信息
- **兼容性**：向后兼容性追踪

## 变更日志

- 2025-11-15 提出提案