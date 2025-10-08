# coding=utf-8
from transpiler.core import registry
from transpiler.core.generator_config import OptimizationLevel

from transpiler.core.lib.library import Library
from transpiler.core.lib.library_mapping import LibraryMapping
from transpiler.core.specification import IROptimizationPass, CodeGeneratorSpec


def registry_optimization_pass(optimization_pass: type[IROptimizationPass], level: OptimizationLevel):
    try:
        registry.optimization_pass[level].append(optimization_pass)
    except KeyError:
        raise ValueError(f"Invalid optimization pass level {level}")


def registry_library(library_name, library: type[Library]):
    LibraryMapping.registry(library_name, library)


def registry_backend(backend: type[CodeGeneratorSpec]):
    registry.backends[backend.get_name()] = backend
