# Dovetail 概述

## 什么是 Dovetail？

Dovetail 是一个专为 Minecraft 数据包开发设计的编程语言与编译器工具链。它将传统的过程导向命令开发方式，转变为具备面向对象特征的高级语言开发方式，生成合法的
Minecraft 数据包。

> **项目现状**
> - 语法基本可用，能编译简单程序
> - 缺乏大量标准库，错误信息不够友好
> - 优化器可能在边缘情况下引入错误
> - OOP 特性与数组借用机制尚未完整实现
> - 语法迭代较快，**不保证向后兼容**
>
> 如需生产环境使用，建议考虑 [MCFPP](https://github.com/MinecraftFunctionPlusPlus/MCFPP) 等成熟项目。

## 核心特性

| 特性       | 说明                         |
|----------|----------------------------|
| **面向对象** | 支持类、结构体、枚举、多继承             |
| **类型安全** | 编译时类型检查，减少运行时错误            |
| **模块化**  | `include` 包含系统与库管理         |
| **多后端**  | 插件架构支持不同 Minecraft 版本      |
| **注解系统** | 6 大类注解控制编译行为               |
| **优化编译** | O0-O3 四级优化，基于 Pass 管道的多轮迭代 |

## 项目架构

```
root/
├── dovetail/              # 核心编译器
│   ├── core/              # 编译器核心
│   │   ├── annotations/   # 注解系统（6大类处理器）
│   │   ├── backend/       # 后端抽象层
│   │   ├── enums/         # 枚举定义
│   │   ├── optimize/      # 优化流水线
│   │   ├── parser/        # 前端解析
│   │   ├── scope/         # 作用域管理
│   │   └── symbols/       # 符号模型
│   ├── plugins/           # 后端插件
│   │   ├── je1215/        # JE 1.21.5 官方后端
│   │   ├── plugin_api/    # 插件 API
│   │   └── plugin_loader/ # 插件加载器
│   └── utils/             # 工具函数
├── lark/                  # Lark 语法定义
├── example/               # 示例代码（17 个 .mcdl 文件）
├── docs/                  # 文档
└── proposals/             # DFP 语言提案
```

## 编译流程

```
源代码(.mcdl)
  ↓ Lark LALR 解析器
AST（抽象语法树）
  ↓ ASTVisitor 语义分析
IR 指令序列（IRInstruction）
  ↓ OptimizationPipeline 多轮 Pass
优化后 IR
  ↓ Backend + ProcessorRegistry
数据包（.mcfunction 等）
```

## 已知永久限制

- **不支持递归**：在 Minecraft 中维护运行时栈帧开销极大，建议改写为迭代实现
- **泄漏式内存管理**：当前内存管理策略较为激进

## 下一步

- [快速开始](2-quick-start) — 安装、配置并编译你的第一个程序
- [语言语法与 MCDL 基础](3-language-syntax-and-mcdl-basics) — 完整语法参考
