# coding=utf-8
"""
优化管道模块

实现优化 Pass 的调度和执行管理，包括依赖解析、
拓扑排序和迭代优化。
"""
from __future__ import annotations

from collections import deque
from typing import TYPE_CHECKING

from transpiler.core.compile_config import CompileConfig
from transpiler.core.config import get_project_logger
from transpiler.core.enums.optimization import OptimizationLevel
from transpiler.core.ir_builder import IRBuilder
from transpiler.core.optimize.context import OptimizationContext
from transpiler.core.optimize.pass_metadata import PassPhase
from transpiler.core.optimize.pass_registry import get_registry

if TYPE_CHECKING:
    from transpiler.core.optimize.base import IROptimizationPass


class OptimizationPipeline:
    """
    优化管道

    负责构建和执行优化 Pass 序列，处理 Pass 之间的
    依赖关系和执行顺序。
    """

    def __init__(self, config: CompileConfig):
        """
        初始化优化管道

        Args:
            config: 编译配置
        """
        self.config = config
        self.registry = get_registry()
        self._pipeline: list[type[IROptimizationPass]] = []
        self._build_pipeline()

    def _build_pipeline(self) -> None:
        """构建优化管道"""
        # 收集所有符合条件的 Pass
        candidates = self._collect_candidates()

        # 解析依赖关系并拓扑排序
        sorted_passes = self._resolve_dependencies(candidates)

        # 按阶段组织执行顺序
        self._pipeline = self._organize_by_phase(sorted_passes)

        if self.config.debug:
            self._debug_pipeline()

    def _collect_candidates(self) -> list[type[IROptimizationPass]]:
        """
        收集所有符合条件的优化 Pass

        Returns:
            Pass 类列表
        """
        candidates = []

        for pass_class in self.registry.get_all().values():
            metadata = pass_class.get_metadata()

            # 检查优化级别
            if metadata.level > self.config.optimization_level:
                continue

            candidates.append(pass_class)

        return candidates

    def _resolve_dependencies(
            self,
            passes: list[type[IROptimizationPass]]
    ) -> list[type[IROptimizationPass]]:
        """
        解析 Pass 依赖关系并进行拓扑排序

        Args:
            passes: 待排序的 Pass 类列表

        Returns:
            拓扑排序后的 Pass 类列表

        Raises:
            ValueError: 当存在循环依赖时
        """
        # 构建依赖图
        pass_map = {p.get_metadata().name: p for p in passes}
        in_degree: dict[str, int] = {name: 0 for name in pass_map}
        adjacency: dict[str, list[str]] = {name: [] for name in pass_map}

        # 统计入度和邻接表
        for pass_class in passes:
            metadata = pass_class.get_metadata()
            pass_name = metadata.name

            for dep_name in metadata.depends_on:
                if dep_name in pass_map:
                    adjacency[dep_name].append(pass_name)
                    in_degree[pass_name] += 1
                # 忽略不在候选列表中的依赖

        # Kahn 算法进行拓扑排序
        queue = deque([name for name, degree in in_degree.items() if degree == 0])
        result: list[str] = []

        while queue:
            current = queue.popleft()
            result.append(current)

            for neighbor in adjacency[current]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        # 检查是否所有节点都已处理
        if len(result) != len(pass_map):
            remaining = [name for name, degree in in_degree.items() if degree > 0]
            raise ValueError(f"Circular dependency detected among passes: {remaining}")

        # 转换为 Pass 类列表
        return [pass_map[name] for name in result]

    def _organize_by_phase(
            self,
            passes: list[type[IROptimizationPass]]
    ) -> list[type[IROptimizationPass]]:
        """
        按阶段组织 Pass 执行顺序

        Args:
            passes: Pass 类列表

        Returns:
            按阶段组织后的 Pass 类列表
        """
        phase_order = PassPhase.get_phase_order()
        organized: list[type[IROptimizationPass]] = []

        for phase in phase_order:
            for pass_class in passes:
                if pass_class.get_metadata().phase == phase:
                    organized.append(pass_class)

        return organized

    def _debug_pipeline(self) -> None:
        """调试：打印管道信息"""
        get_project_logger().info(f"Optimization Pipeline for level {self.config.optimization_level}:")

        current_phase = None
        for pass_class in self._pipeline:
            metadata = pass_class.get_metadata()

            if metadata.phase != current_phase:
                current_phase = metadata.phase
                print(f"  Phase: {current_phase}")

            print(f"    - {metadata.display_name} ({metadata.name})")

    def run(self, builder: IRBuilder) -> IRBuilder:
        """
        执行优化管道

        Args:
            builder: IR 构建器

        Returns:
            优化后的 IR 构建器
        """
        # 无优化级别直接返回
        if self.config.optimization_level == OptimizationLevel.O0:
            return builder

        # 初始化上下文
        context = OptimizationContext(
            max_iterations=1 if self.config.optimization_level < OptimizationLevel.O3 else 10,
            debug=self.config.debug
        )

        # 迭代优化
        for iteration in range(context.max_iterations):
            context = context.with_updates(iteration=iteration)
            changed = False

            get_project_logger().debug(f"Optimization iteration {iteration}")

            for pass_class in self._pipeline:
                if self.config.debug:
                    get_project_logger().debug(f"Print builder")
                    builder.print()
                pass_instance = pass_class(builder, self.config)

                # 检查是否应该运行
                if not pass_instance.should_run(context):
                    if self.config.debug:
                        print(f"  Skipping: {pass_class.get_metadata().display_name}")
                    continue

                # 执行分析
                analysis = pass_instance.analyze()
                if analysis:
                    context = context.with_updates(
                        analysis_results={pass_class.get_metadata().name: analysis}
                    )

                # 执行优化
                if self.config.debug:
                    print(f"  Running: {pass_class.get_metadata().display_name}")

                if pass_instance.execute():
                    changed = True
                    context = context.with_updates(
                        executed_passes={pass_class.get_metadata().name}
                    )
                    context = context.with_updates(
                        ir_features=set(pass_class.get_metadata().provided_features)
                    )

            # 没有变化则提前结束
            if not changed:
                get_project_logger().debug("No changes detected, optimization complete")
                break

        return builder
