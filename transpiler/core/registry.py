# coding=utf-8
from transpiler.core.generator_config import OptimizationLevel
from transpiler.core.specification import CodeGeneratorSpec, IROptimizationPass

backends: dict[str, type[CodeGeneratorSpec]] = {}
optimization_pass: dict[OptimizationLevel, list[type[IROptimizationPass]]] = {}
