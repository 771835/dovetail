# 优化器与优化流水线

## 整体结构

```
Optimizer
  └── OptimizationPipeline
        ├── _collect_candidates()     收集满足优化级别的 Pass
        ├── _resolve_dependencies()   Kahn 算法拓扑排序
        ├── _organize_by_phase()      按阶段排序
        └── run()                     迭代执行
```

## OptimizationPipeline.run()

```python
def run(self, builder: IRBuilder) -> IRBuilder:
    if optimization_level == O0:
        return builder  # 跳过全部优化

    context = OptimizationContext(
        max_iterations=5  # O1/O2
    = 15  # O3
    )

    for iteration in range(max_iterations):
        changed = False
        for pass_class in self._pipeline:
            pass_instance = pass_class(builder, config)
            if pass_instance.execute():
                changed = True
        if not changed:
            break  # 提前收敛
    return builder
```

## Pass 执行阶段

按 `PassPhase` 顺序执行：

```
ANALYZE  → 收集 IR 信息，不修改
TRANSFORM → 修改 IR 结构
CLEANUP  → 清理冗余代码
```

## 八个内置优化 Pass

| Pass 名称                 | 阶段        | 最低级别 | 说明                            |
|-------------------------|-----------|------|-------------------------------|
| `constant_folding`      | TRANSFORM | O1   | 编译时计算常量表达式，支持控制流敏感分析          |
| `dead_code_elimination` | CLEANUP   | O1   | 消除无 `no_dce` 标志的未引用函数         |
| `unreachable_code`      | CLEANUP   | O1   | 消除 `return`/`break` 后的不可达指令   |
| `unused_function`       | CLEANUP   | O1   | 删除从未被调用的函数                    |
| `chain_assign`          | TRANSFORM | O2   | 优化链式赋值（`a = b; b = c` → 直接传播） |
| `declare_cleanup`       | CLEANUP   | O1   | 清理多余的变量声明                     |
| `empty_scope`           | CLEANUP   | O1   | 消除空作用域块                       |
| `useless_scope`         | CLEANUP   | O2   | 消除无实际意义的作用域嵌套                 |

## 常量折叠详解

`ConstantFoldingPass` 是最复杂的内置 Pass，采用**控制流敏感**分析：

1. **预扫描**：识别所有条件分支作用域结构
2. **符号表**：维护支持父子结构的 `SymbolTable`，在分支内使用临时符号表
3. **分支合并**：遇到 `COND_JUMP` 时合并所有分支的状态
4. **折叠操作**：将所有运算符（`BinaryOps`、`CompareOps`、`UnaryOps`）的常量结果直接替换对应的 `ASSIGN` 指令

## Pass 元数据（PassMetadata）

```python
@define(frozen=True, slots=True)
class PassMetadata:
    name: str  # 唯一标识符
    display_name: str  # 显示名称
    description: str
    level: OptimizationLevel  # 启用所需的最低优化级别
    phase: PassPhase  # 执行阶段
    depends_on: tuple[str, ...]  # 依赖的其他 Pass 名称
    incompatible_with: tuple[str, ...]
    repeatable: bool
    required_features: tuple[str, ...]
    provided_features: tuple[str, ...]
```