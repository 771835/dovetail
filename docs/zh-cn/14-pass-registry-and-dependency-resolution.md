# Pass 注册与依赖解析

## PassRegistry

[dovetail/core/optimize/pass_registry.py](dovetail/core/optimize/pass_registry.py) 管理所有注册的优化 Pass：

```python
registry = get_registry()  # 全局单例

registry.get(name)  # 按名称查找
registry.get_all()  # 获取全部
registry.get_by_level(n)  # 获取指定级别及以下的 Pass
registry.get_by_phase(p)  # 获取指定阶段的 Pass
```

## 注册装饰器

```python
@register_pass(PassMetadata(
    name="my_pass",
    display_name="我的优化",
    level=OptimizationLevel.O1,
    phase=PassPhase.TRANSFORM,
    depends_on=("constant_folding",),  # 依赖常量折叠先执行
    provided_features=("my_feature",)
))
class MyPass(IROptimizationPass):
    def execute(self) -> bool:
        # 返回 True 表示 IR 被修改
        ...
```

## 依赖解析：Kahn 拓扑排序

`_resolve_dependencies()` 使用 Kahn 算法处理 Pass 间的 `depends_on` 关系：

```
构建有向图：dep → dependent（dep 必须先于 dependent 执行）
  ↓
计算每个 Pass 的入度
  ↓
将入度为 0 的 Pass 入队
  ↓
BFS 出队 → 记录顺序 → 更新邻居入度
  ↓
检测循环依赖（处理数量 < 总数量时抛出 ValueError）
```

不在候选列表中的依赖会被**静默忽略**（依赖的 Pass 因级别不足被过滤时不报错）。

## IROptimizationPass 基类

```python
class IROptimizationPass:
    def __init__(self, builder: IRBuilder, config: CompileConfig)

    @classmethod
    def get_metadata(cls) -> PassMetadata

    def execute(self) -> bool  # 执行优化，返回是否修改了 IR
```

## 编写自定义 Pass

```python
from dovetail.core.optimize.base import IROptimizationPass
from dovetail.core.optimize.pass_metadata import PassMetadata, PassPhase
from dovetail.core.optimize.pass_registry import register_pass
from dovetail.core.enums.optimization import OptimizationLevel


@register_pass(PassMetadata(
    name="my_custom_pass",
    display_name="自定义 Pass",
    level=OptimizationLevel.O2,
    phase=PassPhase.CLEANUP,
))
class MyCustomPass(IROptimizationPass):
    def execute(self) -> bool:
        changed = False
        for instr in self.builder:
            # 分析/修改 instr
            pass
        return changed
```

通过插件注册后，Pass 会在满足优化级别时自动加入管道。