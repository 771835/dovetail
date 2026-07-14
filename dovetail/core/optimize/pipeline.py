# coding=utf-8
"""
优化管道模块

调度策略：
  依赖绝对优先——拓扑排序决定执行顺序。
  阶段作 tie-breaker——同入度为 0 的节点间按 ANALYZE < TRANSFORM < CLEANUP 排列。
  禁止跨阶段逆序依赖——TRANSFORM Pass 不能依赖 CLEANUP Pass，违者在构建时抛出 ValueError。
"""
from __future__ import annotations

from typing import TYPE_CHECKING

from dovetail.core.compile_config import CompileConfig
from dovetail.core.enums.optimization import OptimizationLevel
from dovetail.core.ir_builder import IRBuilder
from dovetail.core.optimize.context import OptimizationContext
from dovetail.core.optimize.pass_metadata import PassPhase
from dovetail.core.optimize.pass_registry import get_registry
from dovetail.utils.logger import get_logger

if TYPE_CHECKING:
    from dovetail.core.optimize.base import IROptimizationPass

logger = get_logger(__name__)

# 阶段优先级：值越小越先执行
_PHASE_PRIORITY: dict[PassPhase, int] = {
    PassPhase.ANALYZE: 0,
    PassPhase.TRANSFORM: 1,
    PassPhase.CLEANUP: 2,
}


def _phase_priority(pass_class: type[IROptimizationPass]) -> int:
    """获取 Pass 的阶段优先级数值"""
    phase = pass_class.get_metadata().phase
    return _PHASE_PRIORITY.get(phase, 1)


def _level_value(level) -> int:
    """将 OptimizationLevel 统一转换为可比较的整数"""
    val = level.value if isinstance(level, OptimizationLevel) else int(level)
    if isinstance(val, tuple):
        return val[0]
    return val


class OptimizationPipeline:
    """
    优化管道

    构建阶段：筛选 → 校验跨阶段依赖 → 拓扑排序（含阶段 tie-breaker）
    执行阶段：不动点迭代，每轮通过 next_iteration() 重置单轮状态
    """

    def __init__(self, config: CompileConfig):
        self.config = config
        self.registry = get_registry()
        self._pipeline: list[type[IROptimizationPass]] = []
        self._build_pipeline()

    # ── 构建 ──────────────────────────────────────────────────

    def _build_pipeline(self) -> None:
        """构建优化管道的完整流程"""
        candidates = self._collect_candidates()
        self._validate_cross_phase_dependencies(candidates)
        self._pipeline = self._resolve_dependencies(candidates)

        if self.config.debug:
            self._log_pipeline()

    def _collect_candidates(self) -> list[type[IROptimizationPass]]:
        """
        收集所有满足优化级别要求的 Pass。

        Pass 的 level 不超过当前配置的 optimization_level 时才纳入候选。
        """
        config_val = _level_value(self.config.optimization_level)
        candidates = []
        for pass_class in self.registry.get_all().values():
            if _level_value(pass_class.get_metadata().level) <= config_val:
                candidates.append(pass_class)
        return candidates

    def _validate_cross_phase_dependencies(
            self,
            candidates: list[type[IROptimizationPass]],
    ) -> None:
        """
        校验不存在跨阶段逆序依赖。

        若 Pass A（早阶段）声明依赖 Pass B（晚阶段），
        则 A 必须在 B 之后运行，但阶段约束要求 A 在 B 之前——矛盾，报错。

        例：TRANSFORM Pass 依赖 CLEANUP Pass → 违规。

        Raises:
            ValueError: 存在跨阶段逆序依赖
        """
        name_to_class = {p.get_metadata().name: p for p in candidates}

        for pass_class in candidates:
            meta = pass_class.get_metadata()
            my_priority = _PHASE_PRIORITY.get(meta.phase, 1)

            for dep_name in meta.depends_on:
                if dep_name not in name_to_class:
                    continue  # 不在候选列表中的依赖静默忽略
                dep_priority = _PHASE_PRIORITY.get(
                    name_to_class[dep_name].get_metadata().phase, 1
                )
                if my_priority < dep_priority:
                    raise ValueError(
                        f"跨阶段逆序依赖：'{meta.name}'（阶段 {meta.phase}）"
                        f"依赖 '{dep_name}'（阶段 {name_to_class[dep_name].get_metadata().phase}）。"
                        f"早期阶段的 Pass 不能依赖晚期阶段的 Pass。"
                    )

    def _resolve_dependencies(
            self,
            candidates: list[type[IROptimizationPass]],
    ) -> list[type[IROptimizationPass]]:
        """
        Kahn 拓扑排序，阶段优先级作为 tie-breaker。

        算法：
          1. 构建入度表和邻接表
          2. 将所有入度为 0 的节点按阶段优先级排序加入 ready 队列
          3. 每次从 ready 队头取节点（入度最小且阶段最早）
          4. 将其所有后继节点入度 -1，若降为 0 则按优先级插入 ready
          5. 处理完所有节点；若有剩余则存在循环依赖

        Raises:
            ValueError: 存在循环依赖
        """
        pass_map: dict[str, type[IROptimizationPass]] = {
            p.get_metadata().name: p for p in candidates
        }
        in_degree: dict[str, int] = {name: 0 for name in pass_map}
        adjacency: dict[str, list[str]] = {name: [] for name in pass_map}

        for pass_class in candidates:
            meta = pass_class.get_metadata()
            for dep_name in meta.depends_on:
                if dep_name in pass_map:
                    # dep 必须在当前 pass 之前执行
                    adjacency[dep_name].append(meta.name)
                    in_degree[meta.name] += 1

        # 初始 ready 队列：入度为 0，按阶段优先级升序
        ready: list[str] = sorted(
            [name for name, deg in in_degree.items() if deg == 0],
            key=lambda n: _phase_priority(pass_map[n]),
        )
        result: list[str] = []

        while ready:
            current = ready.pop(0)
            result.append(current)

            newly_ready: list[str] = []
            for neighbor in adjacency[current]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    newly_ready.append(neighbor)

            if newly_ready:
                newly_ready.sort(key=lambda n: _phase_priority(pass_map[n]))
                # 归并插入 ready，保持阶段优先级有序
                merged: list[str] = []
                i = j = 0
                while i < len(ready) and j < len(newly_ready):
                    if _phase_priority(pass_map[ready[i]]) <= _phase_priority(pass_map[newly_ready[j]]):
                        merged.append(ready[i])
                        i += 1
                    else:
                        merged.append(newly_ready[j])
                        j += 1
                merged.extend(ready[i:])
                merged.extend(newly_ready[j:])
                ready = merged

        if len(result) != len(pass_map):
            cycle = [n for n, d in in_degree.items() if d > 0]
            raise ValueError(f"Pass 间存在循环依赖：{cycle}")

        return [pass_map[name] for name in result]

    def _log_pipeline(self) -> None:
        """调试模式下打印管道顺序"""
        logger.info(f"优化管道（级别 {self.config.optimization_level}）：")
        for pass_class in self._pipeline:
            meta = pass_class.get_metadata()
            logger.info(f"  [{meta.phase}] {meta.display_name} ({meta.name})")

    # ── 执行 ──────────────────────────────────────────────────

    def run(self, builder: IRBuilder) -> IRBuilder:
        """
        执行优化管道（不动点迭代）。

        O0 时直接返回原始 builder，不做任何优化。
        O1/O2 最多迭代 5 轮，O3 最多 15 轮。
        每轮结束若无 Pass 产生变化，提前退出（不动点收敛）。

        每轮开始时调用 context.next_iteration()：
          - 保留 executed_passes（跨迭代互斥判断）
          - 清空 ir_features 和 analysis_results（重新收集本轮状态）

        Args:
            builder: IR 构建器

        Returns:
            优化后的 IR 构建器（原地修改，同一对象）
        """
        if self.config.optimization_level == OptimizationLevel.O0:
            return builder

        max_iter = 5 * _level_value(self.config.optimization_level)

        context = OptimizationContext(
            max_iterations=max_iter,
            debug=self.config.debug,
        )

        for iteration in range(max_iter):
            # 第 0 轮不调用 next_iteration，避免 iteration 从 1 开始
            if iteration > 0:
                context = context.next_iteration()

            changed = False
            logger.debug(f"优化迭代 {iteration}/{max_iter}")

            for pass_class in self._pipeline:
                pass_instance = pass_class(builder, self.config)

                if not pass_instance.should_run(context):
                    if self.config.debug:
                        logger.debug(f"  跳过：{pass_class.get_metadata().display_name}")
                    continue

                # 执行分析（不修改 IR）
                analysis = pass_instance.analyze()
                if analysis:
                    context = context.with_updates(
                        analysis_results={pass_class.get_metadata().name: analysis}
                    )

                if self.config.debug:
                    builder.print()
                    logger.info(f"  执行：{pass_class.get_metadata().display_name}")


                # 执行优化（修改 IR）
                if pass_instance.execute():
                    changed = True
                    context = context.with_updates(
                        executed_passes={pass_class.get_metadata().name},
                        ir_features=set(pass_class.get_metadata().provided_features),
                    )

            if not changed:
                logger.debug(f"  第 {iteration} 轮无变化，提前退出")
                break

        return builder
