# Dovetail 文档目录

## 入门指南

> 文档为ai整理和生成，部分由人工审查，请以实际代码为准

| # | 文章标题                                               | Slug                                | 说明                             |
|---|----------------------------------------------------|-------------------------------------|--------------------------------|
| 1 | [概述](1-overview)                                   | `1-overview`                        | 项目简介、核心特性、整体架构、编译流程概览          |
| 2 | [快速开始](2-quick-start)                              | `2-quick-start`                     | 安装方式、第一个程序、完整命令行参数参考、目录编译      |
| 3 | [语言语法与 MCDL 基础](3-language-syntax-and-mcdl-basics) | `3-language-syntax-and-mcdl-basics` | 函数、变量、类型、运算符、控制流、类、结构体、枚举、注解速览 |
| 4 | [代码示例解析](4-code-examples-walkthrough)              | `4-code-examples-walkthrough`       | 逐一解析 `example/` 目录下 17 个示例文件   |

## 深入探索

| # | 文章标题                                                           | Slug                                               | 说明                          |
|---|----------------------------------------------------------------|----------------------------------------------------|-----------------------------|
| 5 | [架构概述与编译流水线](5-architecture-overview-and-compilation-pipeline) | `5-architecture-overview-and-compilation-pipeline` | 五阶段流水线、Compiler 入口类、各阶段职责概述 |

### 前端与解析

| # | 文章标题                                                | Slug                                  | 说明                                                  |
|---|-----------------------------------------------------|---------------------------------------|-----------------------------------------------------|
| 6 | [Lark 语法与解析器](6-lark-grammar-and-parser)            | `6-lark-grammar-and-parser`           | Lark LALR 解析器配置、语法结构、表达式优先级、f-string 解析             |
| 7 | [AST 访问器与语义分析](7-ast-visitor-and-semantic-analysis) | `7-ast-visitor-and-semantic-analysis` | ASTVisitor 核心、六个辅助组件、注解处理两阶段、作用域管理、递归检测             |
| 8 | [符号表与类型系统](8-symbol-table-and-type-system)          | `8-symbol-table-and-type-system`      | Symbol 基类、各符号类型、PrimitiveDataType、复合类型、FunctionType |
| 9 | [作用域管理](9-scope-management)                         | `9-scope-management`                  | Mixin 组合模式、五个混入类、Scope 类、协议接口、IR 层作用域指令             |

### 中间表示

| #  | 文章标题                                                 | Slug                                | 说明                                                                   |
|----|------------------------------------------------------|-------------------------------------|----------------------------------------------------------------------|
| 10 | [IR 指令集与操作码](10-ir-instruction-set-and-opcodes)      | `10-ir-instruction-set-and-opcodes` | IRInstruction 统一设计、四大操作码分类、所有操作码完整列表、工厂函数                            |
| 11 | [IRBuilder 与迭代器设计](11-irbuilder-and-iterator-design) | `11-irbuilder-and-iterator-design`  | IRBuilder 容器、正向/反向迭代器、就地修改 API、双向转换协议                                |
| 12 | [符号模型与注解](12-symbol-model-and-annotations)           | `12-symbol-model-and-annotations`   | AnnotationMixin、AnnotationAttachment、AnnotationResult 字段、常见 flags 含义 |

### 优化流水线

| #  | 文章标题                                                       | Slug                                         | 说明                                                        |
|----|------------------------------------------------------------|----------------------------------------------|-----------------------------------------------------------|
| 13 | [优化器与优化流水线](13-optimizer-and-optimization-pipeline)        | `13-optimizer-and-optimization-pipeline`     | Optimizer → Pipeline 委托、管道构建流程、迭代收敛机制、PassPhase 执行顺序      |
| 14 | [Pass 注册与依赖解析](14-pass-registry-and-dependency-resolution) | `14-pass-registry-and-dependency-resolution` | PassRegistry 全局单例、@register_pass 装饰器、Kahn 拓扑排序、编写自定义 Pass |
| 15 | [内置优化 Pass](15-built-in-optimization-passes)               | `15-built-in-optimization-passes`            | 8 个内置 Pass 完整说明：常量折叠、死代码消除、不可达代码、未使用函数、链式赋值等              |

### 后端与代码生成

| #  | 文章标题                                                   | Slug                                    | 说明                                                                         |
|----|--------------------------------------------------------|-----------------------------------------|----------------------------------------------------------------------------|
| 16 | [后端抽象与工厂](16-backend-abstraction-and-factory)          | `16-backend-abstraction-and-factory`    | Backend 基类、BackendMeta 元类、BackendFactory 注册与自动选择、实现新后端                     |
| 17 | [处理器注册表与 IR 分发](17-processor-registry-and-ir-dispatch) | `17-processor-registry-and-ir-dispatch` | IRProcessor 基类、ProcessorRegistry、@ir_processor 装饰器、GenerationContext、分发主流程 |
| 18 | [JE1215 后端插件内部机制](18-je1215-backend-plugin-internals)  | `18-je1215-backend-plugin-internals`    | je1215 插件结构、InitializerFunctionWriter、LiteralPoolWriter、processors/ 目录     |

### 插件与扩展系统

| #  | 文章标题                                                      | Slug                                          | 说明                                       |
|----|-----------------------------------------------------------|-----------------------------------------------|------------------------------------------|
| 19 | [插件 API 与生命周期](19-plugin-api-and-lifecycle)               | `19-plugin-api-and-lifecycle`                 | plugin.metadata 格式、插件主类、v2 事件系统、插件加载顺序   |
| 20 | [插件加载器与发现机制](20-plugin-loader-and-discovery)              | `20-plugin-loader-and-discovery`              | plugin_loader 结构、全局实例、元数据验证、加载流程         |
| 21 | [注解系统与自定义注解](21-annotation-system-and-custom-annotations) | `21-annotation-system-and-custom-annotations` | 六大注解分类、全部内置注解详解、AnnotationResult、自定义注解编写 |

### 配置与实用工具

| #  | 文章标题                                         | Slug                                 | 说明                                                                         |
|----|----------------------------------------------|--------------------------------------|----------------------------------------------------------------------------|
| 22 | [编译配置参考](22-compile-configuration-reference) | `22-compile-configuration-reference` | CompileConfig 字段、优化级别说明、Minecraft 版本系统、全局常量、pack.config 格式                 |
| 23 | [实用模块与辅助工具](23-utility-modules-and-helpers)  | `23-utility-modules-and-helpers`     | logger、NameNormalizer、@timed、IRSymbolSerializer、SafeEnum、datapack_format 等 |
| 24 | [DFP 提案系统](24-dfp-proposal-system)           | `24-dfp-proposal-system`             | DFP 机制说明、编号规则、当前提案列表、贡献复杂功能的完整流程                                           |
