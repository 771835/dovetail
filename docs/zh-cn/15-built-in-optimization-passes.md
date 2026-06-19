# 内置优化 Pass

Dovetail 共内置 8 个优化 Pass，分布在 `dovetail/core/optimize/passes/` 下。所有 Pass 继承 `IROptimizationPass`，通过
`@register_pass` 装饰器自动注册到全局 `PassRegistry`。

## Pass 总览

| Pass 名称                       | 类名                              | 阶段        | 最低级别 | 说明         |
|-------------------------------|---------------------------------|-----------|------|------------|
| `constant_folding`            | `ConstantFoldingPass`           | TRANSFORM | O1   | 编译时计算常量表达式 |
| `dead_code_elimination`       | `DeadCodeEliminationPass`       | CLEANUP   | O1   | 消除无用变量赋值   |
| `unreachable_code_removal`    | `UnreachableCodeRemovalPass`    | CLEANUP   | O1   | 消除不可达指令    |
| `unused_function_elimination` | `UnusedFunctionEliminationPass` | CLEANUP   | O1   | 删除未被调用的函数  |
| `chain_assign_elimination`    | `ChainAssignEliminationPass`    | TRANSFORM | O2   | 消除中间变量链式赋值 |
| `declare_cleanup`             | `DeclareCleanupPass`            | CLEANUP   | O1   | 清理多余变量声明   |
| `empty_scope`                 | `EmptyScopePass`                | CLEANUP   | O1   | 消除空作用域块    |
| `useless_scope`               | `UselessScopePass`              | CLEANUP   | O2   | 消除无意义作用域嵌套 |

---

## 1. 常量折叠（constant_folding）

**文件**：[passes/constant_folding.py](dovetail/core/optimize/passes/constant_folding.py)

最复杂的内置 Pass，采用**控制流敏感分析**。

### 执行流程

```
1. _prescan_branches()   预扫描：识别所有条件分支作用域结构
        ↓
2. _perform_folding()    主遍历：维护符号表，执行折叠替换
```

### 内部符号表（SymbolTable）

支持父子作用域结构，进入新作用域时继承父级状态，条件分支内使用独立临时符号表，遇到 `COND_JUMP` 时合并所有分支状态：

```python
class SymbolTable:
    name: str
    stype: StructureType
    table: dict[str, Reference | FoldingFlags]
    parent: SymbolTable | None

    def find(name)  # 向上链式查找

        def set(name, value)  # 在当前层设置

        def copy_state()  # 复制完整状态（含父级）
```

### 折叠标志（FoldingFlags）

```python
class FoldingFlags(Enum):
    UNKNOWN  # 无法静态追踪的变量（如函数返回值）
    UNDEFINED  # 未定义的变量
```

### 支持的运算

| 类型   | 运算符                                                    |
|------|--------------------------------------------------------|
| 二元运算 | `+` `-` `*` `/` `%` `min` `max` `&` `\|` `^` `<<` `>>` |
| 比较运算 | `==` `!=` `<` `<=` `>` `>=`                            |
| 一元运算 | `-`（取负）`!`（逻辑非）`~`（按位取反）                               |

---

## 2. 死代码消除（dead_code_elimination）

**文件**：[passes/dead_code_elimination.py](dovetail/core/optimize/passes/dead_code_elimination.py)

基于**定义-使用图**（def-use graph）分析，消除永远不会被使用的变量赋值和运算结果。

### 执行流程

```
1. _build_dependency_graph()   构建 def-use / use-def 双向图
        ↓
2. _propagate_liveness()       从根节点（参数、返回值、调用参数、条件变量）出发，BFS 传播活跃性
        ↓
3. _remove_dead_code()         删除不在活跃集合中的 ASSIGN / BINARY_OP / COMPARE / UNARY_OP / CAST 指令
```

### 活跃根节点

以下变量天然活跃，作为传播起点：

- `VariableType.PARAMETER`（函数参数）
- `VariableType.RETURN`（返回值变量）
- `CALL` 指令的所有参数
- `COND_JUMP` 的条件变量
- 有副作用指令（`CALL`、`SET_PROPERTY` 等）的操作数

### 注意

带有 `no_dce` flag 的**函数**不受此 Pass 影响（由 `unused_function_elimination` 单独处理）。

---

## 3. 不可达代码消除（unreachable_code_removal）

**文件**：[passes/unreachable_code.py](dovetail/core/optimize/passes/unreachable_code.py)

最简洁的 Pass（约 60 行），线性扫描实现。

### 逻辑

```
遍历 IR 指令：
  遇到 RETURN / BREAK / CONTINUE → 进入"不可达"状态
  不可达状态下：
    遇到 SCOPE_BEGIN → 嵌套深度 +1
    遇到 SCOPE_END   → 嵌套深度 -1；深度归零时退出不可达状态
    其他指令         → 直接删除
```

### 示例

```mcdl
fn foo() -> int {
    return 1
    print("永远不会执行")   // ← 被消除
    let x = 2              // ← 被消除
}
```

---

## 4. 未使用函数消除（unused_function_elimination）

**文件**：[passes/unused_function.py](dovetail/core/optimize/passes/unused_function.py)

### 执行流程

```
1. _analyze_functions()      扫描所有 FUNCTION 声明 + CALL / CALL_METHOD 调用，建立调用计数表
        ↓
2. _remove_unused_functions() 删除调用计数为 0 且无 no_dce flag 的函数及其全部指令
```

### 保留条件

函数满足以下任一条件时**不会被删除**：

- 存在至少一次 `CALL` / `CALL_METHOD` 调用
- 符号的 `all_flags()` 中包含 `"no_dce"`（由 `@init`、`@tick`、`@export` 等注解设置）

---

## 5. 链式赋值消除（chain_assign_elimination）

**文件**：[passes/chain_assign.py](dovetail/core/optimize/passes/chain_assign.py)

消除中间变量的无意义传递，例如：

```
a = 5
b = a       ← 可替换为 b = 5
c = b       ← 可替换为 c = 5
```

### 执行流程

```
1. _build_alias_maps()         构建作用域树 + 每个作用域的别名映射表
        ↓
2. _apply_alias_substitution() 将所有 ASSIGN 的 source 替换为别名最终值
```

### 分支处理策略（保守策略）

遇到 `COND_JUMP` 时，比较 true 分支和 false 分支的别名状态：若两分支对同一变量的别名**不一致**，则清除该变量的别名（回退到变量自身），避免引入错误。

### 别名解析

```python
def _resolve_alias(var_name, scope, alias_maps) -> Reference:
# 循环解析别名链，直到：
# - 找到字面量（直接返回）
# - 指向自身（终止）
# - 未找到别名（返回变量自身）
```

---

## 6-8. 作用域清理 Pass

### empty_scope — 空作用域消除（O1）

删除内部没有任何指令的 `SCOPE_BEGIN` / `SCOPE_END` 对：

```
SCOPE_BEGIN "x"     ← 若 x 内无任何指令
SCOPE_END   "x"     ← 两条一起删除
```

### useless_scope — 无意义作用域消除（O2）

删除不改变控制流语义的冗余嵌套作用域，减少后端生成时不必要的函数调用层级。

### declare_cleanup — 声明清理（O1）

清理在死代码消除或链式赋值消除后遗留的孤立 `DECLARE` 指令（变量被声明但对应的赋值已被消除）。

---

## Pass 特性依赖关系

```
constant_folding  ─provides→  simplified_arithmetic
dead_code_elimination  ─provides→  cleaned_dead_code
unreachable_code_removal  ─provides→  removed_unreachable
unused_function_elimination  ─provides→  removed_unused_functions
chain_assign_elimination  ─provides→  eliminated_chain_assigns
```

目前内置 Pass 之间无显式 `depends_on` 声明，依赖关系通过管道迭代收敛自然处理。
