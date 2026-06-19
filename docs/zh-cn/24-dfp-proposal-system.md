# DFP 提案系统

## 什么是 DFP？

DFP（Dovetail Feature Proposal）是 Dovetail 语言的功能提案机制，用于讨论、设计和记录语言特性与编译器架构决策。

## 提案编号规则

| 编号范围           | 领域              |
|----------------|-----------------|
| DFP-0          | 提案模板与规范         |
| DFP-1, DFP-2   | 基础/核心提案         |
| DFP-3xx        | 类型系统与内置函数       |
| DFP-4xx        | —               |
| DFP-6, DFP-6xx | 注解系统（含附录 A/B/C） |
| DFP-7, DFP-8   | —               |
| DFP-9xx        | —               |
| DFP-15xx       | 临时草案            |

## 当前提案列表

| 提案                                         | 状态   | 主题       |
|--------------------------------------------|------|----------|
| [DFP-0](proposals/DFP-0.md)                | 规范   | 提案模板     |
| [DFP-1](proposals/DFP-1.md)                | —    | 基础提案     |
| [DFP-2](proposals/DFP-2.md)                | —    | —        |
| [DFP-300](proposals/DFP-300.md)            | 已实现  | 内置函数系统   |
| [DFP-301](proposals/DFP-301.md)            | —    | 类型系统扩展   |
| [DFP-302](proposals/DFP-302.md)            | —    | —        |
| [DFP-305](proposals/DFP-305.md)            | —    | —        |
| [DFP-401](proposals/DFP-401.md)            | —    | —        |
| [DFP-6](proposals/DFP-6.md)                | 已实现  | 注解系统完整规范 |
| [DFP-6 附录A](proposals/DFP-6-appendix-a.md) | —    | 注解附录     |
| [DFP-6 附录B](proposals/DFP-6-appendix-b.md) | —    | 注解附录     |
| [DFP-6 附录C](proposals/DFP-6-appendix-c.md) | —    | 注解附录     |
| [DFP-601](proposals/DFP-601.md)            | —    | 注解系统扩展   |
| [DFP-602](proposals/DFP-602.md)            | —    | —        |
| [DFP-603](proposals/DFP-603.md)            | —    | —        |
| [DFP-7](proposals/DFP-7.md)                | —    | —        |
| [DFP-8](proposals/DFP-8.md)                | —    | —        |
| [DFP-901](proposals/DFP-901.md)            | —    | —        |
| [DFP-1501](proposals/DFP-1501.md)          | 临时草案 | —        |
| [DFP-1502](proposals/DFP-1502.md)          | 临时草案 | —        |

## 贡献复杂功能的流程

1. 在 `proposals/` 下创建或更新 DFP 文档（参考 DFP-0 模板）
2. 提交 issue，发起社区讨论
3. 讨论达成共识后，克隆新分支进行实现
4. 测试确保功能正确
5. 提交 PR，合并到主分支

## 临时草案（DFP-15xx）

编号 1500 以上的提案为临时草案，用于快速捕捉构想，仅限项目负责人和授权贡献者使用，不经过完整的社区治理流程。