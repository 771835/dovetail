# coding=utf-8
from dovetail.core import builtin_annotation
from dovetail.core.backend import BackendFactory
from dovetail.core.lib.library_mapping import LibraryMapping
from dovetail.core.optimize.pass_registry import get_registry, register_pass
from dovetail.core.symbols.annotation import Annotation
from dovetail.utils.mixin_manager import Mixin, Inject, At, CallbackInfoReturnable


@Mixin(builtin_annotation, force=True)
class AnnotationRegistry:
    ANNOTATIONS: dict[str, Annotation] = {}

    @staticmethod
    def register_annotation(name: str, annotation: Annotation) -> bool:
        """
        注册内建注解的注解对象

        Args:
            name: 注解名
            annotation: 注解对象

        Returns:
            bool: 当失败时返回False
        """
        annotations = getattr(AnnotationRegistry, "ANNOTATIONS")
        if isinstance(annotations, dict):
            annotations[name] = annotation
            return True
        return False

    @staticmethod
    @Inject("get_annotation", At(At.TAIL), cancellable=True)
    def get_annotation(ci: CallbackInfoReturnable, name: str):
        """
        获取内建注解的注解对象

        Args:
            name: 内建函数的函数名

        Returns:
            注解对象，当不存在时返回None
        """

        annotations = getattr(AnnotationRegistry, "ANNOTATIONS", {})
        if name in annotations:
            ci.set_return_value(annotations[name])


registry_backend = BackendFactory.register
registry_optimize_pass = get_registry().register
registry_optimize_pass_s = register_pass
registry_library = LibraryMapping.registry
registry_annotation = getattr(AnnotationRegistry, "register_annotation", lambda name, annotation: False)
