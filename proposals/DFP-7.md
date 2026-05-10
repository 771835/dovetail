# DFP 7: 编译期错误恢复及报告机制

## 提案信息

**作者**: 771835 <2790834181@qq.com>  
**状态**: Accepted  
**创建日期**: 2026-02-03  
**最新更新**: 2026-05-10

## 设计目标

本提案旨在为 Dovetail 编译器规范错误恢复机制及报告机制，使编译器在遇到错误时能够继续分析代码，报告多个错误，提升开发体验。

## 动机

### 问题背景

当前编译器采用"遇到第一个错误即终止"的策略：

1. 开发效率低下  
   用户修复一个错误后重新编译，才能发现下一个错误。对于大型文件，这个循环极其低效。

2. 错误定位困难  
   单一错误可能引发连锁反应，后续的"假错误"混淆了真正的问题根源。

3. IDE 集成不友好  
   语言服务器无法提供实时的多错误诊断，影响编辑器体验。

### 需求分析

- 编译器需求：在错误状态下继续解析，生成尽可能完整的 AST 并报告错误
- 性能需求：错误恢复不应显著增加编译时间

## 技术规范

1. **错误分类**  
   将错误分为三类，采取不同的恢复策略：

   | 错误类型 | 恢复策略              | 示例          |
               |------|-------------------|-------------|
   | 语法错误 | 跳过到下一个有效语句        | 缺少分号、括号不匹配  |
   | 语义错误 | 插入占位符符号或跳过语句并继续分析 | 未定义变量、类型不匹配 |
   | 致命错误 | 立即终止编译            | 文件不存在、内存不足  |

2. **错误报告**  
   错误报告默认输出到`stderr`，当`stderr`不可用时写入`error.log`文件
   报告格式如下或(其他语言翻译应保持类似格式)
   ```log
   发生错误: (错误名)
   文件 "文件路径", 行 xxx, 纵 xxx
   相关代码:
   ...(错误行数及上下1-2行)
   (错误名): 错误详细内容 (错误解决建议)
   ```
3. **上下文**
   错误报告携带应上下文，以便于错误定位
   上下文位于错误报告后
   ```log
   [上下文: xxx -> xxx -> ...]
   ```

## 变更日志

- 2026-02-03: 始提案创建
- 2026-02-14: 规范了错误报告格式
- 2026-05-01: 增设了上下文规范
- 2026-05-10: 补充了完整错误一览表

# 附录一： 完整错误一览表(2026/5/10 版)

_此表仅供参考，实际以`dovetail.core.errors`为准_

### 语法错误 (0x1xxx)

| 编号     | 名称                          |
|--------|-----------------------------|
| 0x1001 | InvalidSyntax               |
| 0x1002 | MissingToken                |
| 0x1003 | InvalidOperator             |
| 0x1004 | DuplicateDefinition         |
| 0x1005 | InvalidAnnotation           |
| 0x1006 | AnnotationArgumentError     |
| 0x1007 | InvalidTypeDeclaration      |
| 0x1008 | InvalidArrayDimension       |
| 0x1009 | NullableTypeError           |
| 0x100A | IncludePathError            |
| 0x100B | CircularInclude             |
| 0x100C | EmptyStructDefinition       |
| 0x100D | InvalidEnumMember           |
| 0x100E | InvalidClassInheritance     |
| 0x100F | InvalidFunctionSignature    |
| 0x1010 | InvalidParameterDeclaration |
| 0x1011 | MissingTypeAnnotation       |
| 0x1012 | DefaultParameterPosition    |
| 0x1013 | TypedefRedefinition         |

### 语义错误 — 类型系统 (0x2xxx)

| 编号     | 名称                         |
|--------|----------------------------|
| 0x2001 | TypeMismatch               |
| 0x2002 | UndefinedType              |
| 0x2003 | ArgumentTypeMismatch       |
| 0x2004 | ArgumentNumberMismatch     |
| 0x2005 | NotCallable                |
| 0x2006 | PrimitiveTypeOperation     |
| 0x2007 | CompareTypeMismatch        |
| 0x2008 | TypeArgumentNumberMismatch |
| 0x2009 | MutabilityViolation        |
| 0x200A | InvalidMutUsage            |
| 0x200B | MutArgumentMismatch        |
| 0x200C | ArrayDimensionMismatch     |
| 0x200D | ArraySizeUndefined         |
| 0x200E | InvalidArrayLiteral        |
| 0x200F | NullableAccessError        |
| 0x2010 | NullAssignmentError        |
| 0x2011 | FStringExpressionError     |
| 0x2012 | InvalidMemberAccess        |
| 0x2013 | PrivateMemberAccess        |
| 0x2014 | NotIterable                |
| 0x2015 | InvalidArrayAccess         |

### 语义错误 — 符号解析 (0x3xxx)

| 编号     | 名称                |
|--------|-------------------|
| 0x3001 | SymbolResolution  |
| 0x3002 | UndefinedSymbol   |
| 0x3003 | UndefinedVariable |
| 0x3004 | UndefinedFunction |
| 0x3005 | SymbolCategory    |

### 语义错误 — 控制流 (0x4xxx)

| 编号     | 名称                     |
|--------|------------------------|
| 0x4001 | InvalidControlFlow     |
| 0x4002 | RecursionError         |
| 0x4003 | RecursionLimit         |
| 0x4004 | BreakOutsideLoop       |
| 0x4005 | ContinueOutsideLoop    |
| 0x4006 | ReturnTypeMismatch     |
| 0x4007 | MissingReturnStatement |

### 语义错误 — 接口/常量/注解 (0x5xxx)

| 编号     | 名称                             |
|--------|--------------------------------|
| 0x5001 | UnimplementedInterfaceMethods  |
| 0x5002 | MissingImplementation          |
| 0x5003 | FunctionNameConflict           |
| 0x5004 | ConstantReassignment           |
| 0x5005 | ConstantRequiresInitialization |
| 0x5006 | AnnotationNotApplicable        |
| 0x5007 | ConflictingAnnotations         |

### 内部错误 — 编译器 (0x6xxx)

| 编号     | 名称              |
|--------|-----------------|
| 0x6001 | UnexpectedError |
| 0x6002 | LibraryLoad     |
| 0x6003 | CompilerInclude |

### 内部错误 — IR (0x7xxx)

| 编号     | 名称                       |
|--------|--------------------------|
| 0x7001 | IRInvalidType            |
| 0x7002 | IRTypeCoercionFailed     |
| 0x7101 | IRInvalidBlock           |
| 0x7102 | IRInvalidInstruction     |
| 0x7201 | IROptimizationTooComplex |
| 0x7202 | IROptimizationTimeout    |

### 运行时错误 (0x8xxx)

| 编号     | 名称                           |
|--------|------------------------------|
| 0x8001 | FunctionTranslationFailed    |
| 0x8002 | VariableMappingFailed        |
| 0x8003 | InstructionTranslationFailed |
| 0x8004 | DataPackGenerationFailed     |
| 0x8005 | NamespaceConflict            |
| 0x8006 | ResourceExhaustion           |

### 系统错误 — 目标平台 (0x90xx)

| 编号     | 名称                        |
|--------|---------------------------|
| 0x9001 | UnsupportedTargetVersion  |
| 0x9002 | TargetFeatureNotSupported |

### 系统错误 — 输入输出 (0x91xx)

| 编号     | 名称                      |
|--------|-------------------------|
| 0x9101 | DirectoryCreationFailed |
| 0x9102 | FileWriteFailed         |
| 0x9103 | FileSizeTooLarge        |
| 0x9104 | DiskSpaceInsufficient   |

### 系统错误 — 其他 (0x92xx)

| 编号     | 名称                   |
|--------|----------------------|
| 0x9201 | VersionCompatibility |
| 0x9202 | MemoryLimit          |
| 0x9203 | ConfigurationError   |
| 0x9204 | FileNotFound         |
