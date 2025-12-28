# coding=utf-8

from transpiler.core import registry
from transpiler.core.enums.optimization import OptimizationLevel

from transpiler.core.lib.library import Library
from transpiler.core.lib.library_mapping import LibraryMapping
from transpiler.core.specification import IROptimizationPass


def registry_optimization_pass(optimization_pass: type[IROptimizationPass], level: OptimizationLevel):
    try:
        registry.optimization_pass[level].append(optimization_pass)
    except KeyError:
        raise ValueError(f"Invalid optimization pass level {level}")


def registry_library(library_name, library: type[Library]):
    LibraryMapping.registry(library_name, library)


registry_backend = lambda backend: print("The function 'registry_backend' is deprecated.")
