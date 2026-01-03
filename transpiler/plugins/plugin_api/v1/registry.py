# coding=utf-8

from transpiler.plugins.plugin_api.v2.registry import registry_library as registry_library_v2

registry_library = registry_library_v2

registry_backend = lambda backend: print("The function 'registry_backend' is deprecated.")
registry_optimization_pass = lambda optimization_pass, level: print(
    "The function 'registry_optimization_pass' is deprecated.")
