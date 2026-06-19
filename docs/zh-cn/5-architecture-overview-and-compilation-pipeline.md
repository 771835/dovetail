# 架构概述与编译流水线

## 整体架构

Dovetail 采用**多阶段流水线架构**，每个阶段职责单一、输入输出明确：

```
源代码 (.mcdl)
  │
  ▼ [parser.py] Lark LALR 解析
AST (Lark Tree)
  │
  ▼ [visitor.py] ASTVisitor 语义分析 + IR 生成
     └── components/ 6个辅助模块
IR 指令序列 (IRBuilder)
  │
  ▼ [optimizer.py → pipeline.py] 多轮 Pass 迭代优化
优化后 IR
  │
  ▼ [Backend + ProcessorRegistry] 后端代码生成
数据包 (.mcfunction 等)
```

## 入口：Compiler 类

[main.py](../../main.py) 中的 `Compiler` 类是整个编译流程的入口：

```python
compiler = Compiler(config, backend_name, generate, output_temp_file)
compiler.compile(source_path, target_path)
```

`compile()` 会根据输入路径类型分发到：

- `_compile_file()` — 单文件编译
- `_compile_directory()` — 目录编译（读取 `pack.config`）

## 阶段一：词法/语法分析

**文件**：[dovetail/core/parser/parser.py](../../dovetail/core/parser/parser.py)

使用 Lark LALR 解析器，语法定义在 [lark/dovetail.lark](../../lark/dovetail.lark)：

```python
lark_parser = Lark(
    grammar,
    start=["program", "expr"],  # 两个起始符号
    parser='lalr',
    cache=".lark_cache",  # 缓存加速
    propagate_positions=True  # 保留位置信息用于错误报告
)
```

`parser_file()` 解析源文件，`parser_code()` 解析代码字符串，`parse_fstring_iter()` 处理 f-string 插值。

## 阶段二：语义分析与 IR 生成

**文件**：[dovetail/core/parser/visitor.py](../../dovetail/core/parser/visitor.py)（1200+ 行）

`ASTVisitor` 继承 Lark 的 `Interpreter`，是前端核心，职责包括：

| 职责    | 说明                                     |
|-------|----------------------------------------|
| 符号解析  | 构建符号表，解析变量、函数、类定义                      |
| 类型检查  | 验证类型兼容性与转换合法性                          |
| 作用域管理 | 维护嵌套作用域树                               |
| 注解处理  | 在 PRE_SYMBOL / POST_SYMBOL 两个时机调用注解处理器 |
| 递归检测  | 检测并报告不支持的递归调用                          |
| IR 生成 | 将 AST 节点转换为 `IRInstruction` 指令序列       |

**辅助组件**（`parser/components/`）：

| 模块                       | 职责          |
|--------------------------|-------------|
| `declaration_handler.py` | 类、函数、变量声明处理 |
| `error_reporter.py`      | 结构化编译错误报告   |
| `include_manager.py`     | 文件包含与循环包含检测 |
| `ir_emitter.py`          | IR 指令发射     |
| `symbol_resolver.py`     | 符号跨作用域查找    |
| `type_checker.py`        | 类型兼容性验证     |

## 阶段三：IR 优化

**文件
**：[dovetail/core/optimize/optimizer.py](../../dovetail/core/optimize/optimizer.py) → [pipeline.py](../../dovetail/core/optimize/pipeline.py)

`Optimizer` 委托 `OptimizationPipeline` 执行，管道构建流程：

1. 从 `PassRegistry` 收集满足当前优化级别的 Pass
2. 解析 Pass 间依赖关系，Kahn 算法拓扑排序
3. 按 `PassPhase`（ANALYZE → TRANSFORM → CLEANUP）组织执行顺序
4. 迭代执行直到收敛或达到最大轮数（O1/O2: 5轮，O3: 15轮）
5. O0 时直接跳过全部优化

## 阶段四：后端代码生成

**文件**：[dovetail/core/backend/base.py](../../dovetail/core/backend/base.py)

`Backend` 抽象类的代码生成主流程：

```python
def generate(self):
    context = GenerationContext(config, target, ir_builder)
    self._process_instructions(context)  # 遍历 IR，分发给处理器
    self._write_outputs(context)  # 写出文件
```

**核心组件**：

| 组件                  | 说明                 |
|---------------------|--------------------|
| `ProcessorRegistry` | opcode → 处理器函数的映射表 |
| `GenerationContext` | 携带配置、IR、输出缓冲的上下文对象 |
| `OutputManager`     | 管理多个输出文件的写入        |
| `BackendFactory`    | 注册/查找/自动选择后端       |

## 调试技巧

```bash
# 查看 AST 结构
python main.py input.mcdl --debug

# 输出中间 IR 文件
python main.py input.mcdl --output-temp-file

# 关闭优化隔离问题
python main.py input.mcdl -O 0
```

## 下一步

- [Lark 语法与解析器](6-lark-grammar-and-parser) — 深入了解语法定义
- [优化器与优化流水线](13-optimizer-and-optimization-pipeline) — 优化机制详解
- [后端抽象与工厂](16-backend-abstraction-and-factory.md) — 后端系统详解