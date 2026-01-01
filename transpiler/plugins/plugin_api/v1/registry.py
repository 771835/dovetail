# coding=utf-8


from transpiler.core.lib.library import Library
from transpiler.core.lib.library_mapping import LibraryMapping




def registry_library(library_name, library: type[Library]):
    LibraryMapping.registry(library_name, library)


registry_backend = lambda backend: print("The function 'registry_backend' is deprecated.")
registry_optimization_pass = lambda optimization_pass, level: print(
    "The function 'registry_optimization_pass' is deprecated.")
