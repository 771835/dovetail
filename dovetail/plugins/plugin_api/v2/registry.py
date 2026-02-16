# coding=utf-8
from dovetail.core.backend import BackendFactory
from dovetail.core.lib.library_mapping import LibraryMapping
from dovetail.core.optimize.pass_registry import get_registry, register_pass

registry_backend = BackendFactory.register
registry_optimize_pass = get_registry().register
registry_optimize_pass_s = register_pass
registry_library = LibraryMapping.registry
