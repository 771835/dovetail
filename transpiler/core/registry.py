# coding=utf-8
from transpiler.core.enums.optimization import OptimizationLevel
from transpiler.core.specification import IROptimizationPass

optimization_pass: dict[OptimizationLevel, list[type[IROptimizationPass]]] = {}
