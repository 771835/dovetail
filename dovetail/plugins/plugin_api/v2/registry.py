# coding=utf-8
"""
注册函数集合库
供插件使用，用于注册后端、优化管道、内建库、注解等

See Also:
     _d 后缀为装饰器函数

根据DFP-602《插件系统规范》定义
"""
import dovetail.core.annotations.registry as annotation_registry
import dovetail.core.optimize.pass_registry as pass_registry
from dovetail.core.annotations.decorator import annotation_processor
from dovetail.core.annotations.spec import inject_annotation_spec
from dovetail.core.backend import BackendFactory
from dovetail.core.lib.library_mapping import LibraryMapping

__all__ = [
    "registry_backend",
    "registry_optimize_pass",
    "registry_optimize_pass_d",
    "registry_library",
    "registry_annotation",
    "registry_annotation_spec",
    "registry_annotation_processor",
    "registry_annotation_processor_d"
]

registry_backend = BackendFactory.register
registry_optimize_pass = pass_registry.get_registry().register
registry_optimize_pass_d = pass_registry.register_pass
registry_library = LibraryMapping.registry
registry_annotation = inject_annotation_spec  # 仅用于兼容
registry_annotation_spec = inject_annotation_spec
registry_annotation_processor = annotation_registry.get_registry().register
registry_annotation_processor_d = annotation_processor
