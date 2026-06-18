# coding=utf-8
"""
注解声明规范（纯声明，不含逻辑）
仅供 visitor 的 annotation() 方法使用，
用于知道"有哪些注解"和"参数名是什么"。

根据DFP-6《内置注解规范》定义
"""
from typing import Final, Optional, Any

from attrs import define

from dovetail.core.annotations.base import AnnotationCategory


@define(slots=True, hash=False, repr=False)
class Annotation:
    name: str  # 注解名称
    params: Optional[dict[str, Any]]  # 参数字典
    category: AnnotationCategory  # 分类枚举

    def __repr__(self):
        return f"@{self.name}({','.join(self.params.keys())})"

    def __hash__(self):
        """
        哈希注解对象

        Returns:
            int: 哈希值
        """
        if self.params is None:
            return hash((self.name, self.category))
        return hash((self.name, frozenset(self.params.items()), self.category))


_specs: Final[dict[str, Annotation]] = {
    "init": Annotation("init", None, AnnotationCategory.LIFECYCLE),
    "tick": Annotation("tick", {"interval": 1}, AnnotationCategory.LIFECYCLE),
    "internal": Annotation("internal", None, AnnotationCategory.VISIBILITY),
    "noinline": Annotation("noinline", None, AnnotationCategory.VISIBILITY),
    "export": Annotation("export", {"path": "", "abi": "dovetail"}, AnnotationCategory.LINKAGE),
    "extern": Annotation("extern", {"path": "", "abi": "dovetail"}, AnnotationCategory.LINKAGE),
    "target": Annotation("target", {"edition": "java"}, AnnotationCategory.CONDITION),
    "version": Annotation("version", {"min": "1.20.4", "max": "1.21.4"}, AnnotationCategory.CONDITION),
    "if_not_exists": Annotation("if_not_exists", None, AnnotationCategory.CONDITION),
    "if_symbol": Annotation("if_symbol", {"name": "", "type": "any"}, AnnotationCategory.CONDITION),
    "if_feature": Annotation("if_feature", {"feature": ""}, AnnotationCategory.CONDITION),
    "recursive": Annotation("recursive", None, AnnotationCategory.BACKEND_HINT),
    "deprecated": Annotation("deprecated", {"msg": ""}, AnnotationCategory.METADATA),
    "doc": Annotation("doc", {"text": ""}, AnnotationCategory.METADATA),
    "author": Annotation("author", {"name": ""}, AnnotationCategory.METADATA),
    "since": Annotation("since", {"version": ""}, AnnotationCategory.METADATA),
}


def get_annotation_spec(name: str) -> Annotation | None:
    return _specs.get(name)


def inject_annotation_spec(annotation: Annotation):
    """插件注入自定义注解声明（仅声明，处理器仍需单独注册）"""
    _specs[annotation.name] = annotation
