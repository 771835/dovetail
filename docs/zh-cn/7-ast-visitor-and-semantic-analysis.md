# AST 访问器与语义分析

## 概述

`ASTVisitor`（[dovetail/core/parser/visitor.py](dovetail/core/parser/visitor.py)，1200+ 行）继承 Lark 的 `Interpreter`
类，是整个编译器前端的核心。它遍历 Lark 生成的 AST，执行语义分析并发射 IR 指令。

```python
visitor = ASTVisitor(config, source_path)
visitor.visit(ast_tree)
ir_builder = visitor.builder  # 获取生成的 IR
```

## 核心属性

```python
class ASTVisitor(Interpreter):
    config: CompileConfig  # 编译配置
    filepath: Path  # 当前编译的源文件路径
    builder: IRBuilder  # IR 构建器
    builtin_function: dict  # 内建函数处理器映射表
    include_manager: IncludeManager
```

## 六个辅助组件

`ASTVisitor` 将具体职责委托给 `parser/components/` 下的六个模块：

### 1. DeclarationHandler

处理所有**声明**语义：函数声明、类声明、变量声明、结构体/枚举声明。负责构建符号对象并注册到作用域。

### 2. ErrorReporter

结构化**错误报告**。封装 `report()` 调用，携带文件路径、行列信息、建议信息。注解处理器通过 `ctx.error_reporter` 使用它。

### 3. IncludeManager

处理 `include` 指令，维护**包含文件集合**，检测**循环包含**（`CircularIncludeException`）。

### 4. IREmitter

封装所有 **IR 指令发射**操作，是 `IRBuilder.insert()` 的上层封装，提供语义化的发射方法。

### 5. SymbolResolver

提供**跨作用域符号查找**，封装作用域链的 `resolve_symbol()` 调用，供注解处理器和类型检查器使用。

### 6. TypeChecker

执行**类型兼容性验证**：赋值兼容、函数参数类型、返回值类型、强制转换合法性。

## 注解处理时机

访问器在处理每个声明时，调用 `AnnotationRegistry` 的两阶段处理：

```
1. process_pre()   ← PRE_SYMBOL：条件编译，决定是否跳过该符号
       ↓ skip=False
2. 构建符号对象（Function / Class / ...）
       ↓
3. process_post()  ← POST_SYMBOL：标记、校验、附加 flags/metadata 到符号
```

## 作用域管理

访问器维护一棵作用域树，进入/退出代码块时压栈/弹栈：

```
GLOBAL
├── fn main (FUNCTION)
│   ├── if block (CONDITIONAL)
│   └── for body (LOOP_BODY)
└── class Player (CLASS)
```

每个作用域由 `Scope` 对象表示，通过 `SymbolResolutionMixin` 实现向上链式符号查找。

## 递归检测

访问器在函数调用时追踪调用链，检测到循环调用时报告错误（除非函数标注了 `@recursive` 且启用了 `--recursion`）。