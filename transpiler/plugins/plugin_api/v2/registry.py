# coding=utf-8
from transpiler.core.backend import BackendFactory
from transpiler.core.lib.library_mapping import LibraryMapping
from transpiler.core.optimize.pass_registry import get_registry, register_pass

registry_backend = BackendFactory.register
registry_optimize_pass = get_registry().register
registry_optimize_pass_s = register_pass
registry_library = LibraryMapping.registry
