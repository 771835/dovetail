# 作用域管理

## 设计模式：混入组合

Dovetail 的作用域系统采用 **Mixin 组合模式**，将作用域功能拆分为独立混入类，通过多重继承组合使用，而非单一庞大的作用域类。

核心文件：[dovetail/core/scope/mixins/base.py](dovetail/core/scope/mixins/base.py)

## 五个混入类

### CoreMixin

提供作用域的核心属性：

```python
class CoreMixin(ScopeCore):
    name: str  # 作用域名称
    parent: Self | None  # 父作用域引用
    stype: StructureType  # 作用域类型
```

### SymbolStorageMixin

单层符号存储与查找：

```python
def add_symbol(symbol, force=False) -> bool  # 添加符号

    def has_symbol(name) -> bool  # 检查存在

    def set_symbol(symbol, force=False) -> bool  # 修改符号

    def remove_symbol(name) -> bool  # 删除符号

    def find_symbol(name) -> Symbol | None  # 单层查找（不向上）

    def get_symbols() -> dict  # 获取当前层所有符号
```

### SymbolResolutionMixin

**跨作用域**符号解析（向上链式查找）：

```python
def resolve_symbol(name) -> Symbol | None


# 从当前作用域向上遍历父链，直到找到符号或到达根

def resolve_symbol_in_chain(name, chain: list[StructureType]) -> Symbol | None


# 限定只在指定类型的作用域中查找

def get_all_symbols() -> dict
# 获取从当前到根的完整符号表（子级覆盖父级）
```

### HierarchyMixin

作用域树的子节点管理：

```python
def create_child(name, stype) -> Self  # 创建子作用域
```

### AuxiliaryMixin

（`mixins/auxiliary.py`）提供辅助查询功能，如查找最近的函数作用域、循环作用域等。

## Scope 类

`parser/scope.py` 中的 `Scope` 类通过组合上述混入构成完整的作用域对象：

```python
class Scope(CoreMixin, SymbolStorageMixin, SymbolResolutionMixin, HierarchyMixin):
    pass
```

## 作用域协议

`scope/protocols.py` 定义了三个协议（Protocol）作为接口契约：

| 协议                | 说明                                |
|-------------------|-----------------------------------|
| `ScopeCore`       | 要求实现 `name`、`parent`、`stype`      |
| `SymbolContainer` | 要求实现 `find_symbol`、`add_symbol` 等 |
| `SymbolResolver`  | 要求实现 `resolve_symbol`             |

注解处理器通过 `ctx.symbol_resolver` 接收 `SymbolResolver` 协议对象，实现与具体 Scope 实现的解耦。

## 作用域生命周期

在 IR 层面，作用域通过 `SCOPE_BEGIN` / `SCOPE_END` 指令表示：

```
SCOPE_BEGIN("main_loop", StructureType.LOOP_BODY)
  DECLARE ...
  ASSIGN  ...
SCOPE_END("main_loop")
```

优化器的多个 Pass（如 `empty_scope`、`useless_scope`）会分析这些指令并清除不必要的作用域嵌套。
