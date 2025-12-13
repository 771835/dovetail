# coding=utf-8
from transpiler.core.backend import Backend, BackendFactory


def registry_backend(backend: type[Backend]):
    BackendFactory.register(backend)
