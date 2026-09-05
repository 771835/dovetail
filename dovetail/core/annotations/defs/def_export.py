# coding=utf-8
from dovetail.core.annotations.base import (
    AnnotationProcessor, AnnotationContext, AnnotationResult, AnnotationTarget
)
from dovetail.core.annotations.category import AnnotationCategory
from dovetail.core.annotations.decorator import annotation_processor
from dovetail.core.enums import PrimitiveDataType
from dovetail.core.errors import Errors
from dovetail.core.symbols.function import Function

_KNOWN_ABIS = {"dovetail", "clang-mc"}
_DEFAULT_OBJECTIVE = {
    "dovetail": "dovetail",
    "clang-mc": "vm_regs",
}

_FFI_SAFE = {
    PrimitiveDataType.INT,
    PrimitiveDataType.BOOLEAN,
    PrimitiveDataType.VOID,
    PrimitiveDataType.STRING,
}


def _check_abi(abi: str, ctx: AnnotationContext) -> bool:
    if abi not in _KNOWN_ABIS:
        ctx.error_reporter.report(
            Errors.AnnotationArgumentError,
            "export",
            f"未知 ABI '{abi}'，支持的值: {', '.join(_KNOWN_ABIS)}",
            meta=ctx.meta,
        )
        return False
    return True


def _check_ffi_types(func: Function, abi: str, ctx: AnnotationContext) -> bool:
    if abi == "dovetail":
        return True
    if abi == "clang-mc":
        if func.return_type not in _FFI_SAFE:
            ctx.error_reporter.report(
                Errors.NotFFISafeType,
                f"({', '.join(t.get_name() for t in _FFI_SAFE)})",
                func.return_type.get_name(),
                meta=ctx.meta,
                suggestion=f"clang-mc ABI 不支持返回类型 {func.return_type.get_name()}"
            )
            return False
        for param in func.params:
            if param.get_dtype() not in _FFI_SAFE:
                ctx.error_reporter.report(
                    Errors.NotFFISafeType,
                    param.get_dtype().get_name(),
                    meta=ctx.meta,
                    suggestion=f"参数 '{param.get_name()}' 的类型不是 clang-mc ABI 安全类型"
                )
                return False
        return True
    ctx.error_reporter.report(
        Errors.AnnotationArgumentError,
        "export",
        f"未知的 ABI 标识符 '{abi}'，支持的值: dovetail, clang-mc",
        meta=ctx.meta
    )
    return False


@annotation_processor(
    name="export",
    category=AnnotationCategory.LINKAGE,
    params={"path": "", "abi": "dovetail", "objective": ""},
)
class ExportProcessor(AnnotationProcessor):
    experimental = True
    applicable_targets = [AnnotationTarget.FUNCTION]

    def validate(self, args, context):
        abi = args.get("abi", "dovetail")
        if isinstance(context.symbol, Function) and not _check_ffi_types(context.symbol, abi, context):
            return False
        return _check_abi(abi, context)

    def process(self, args, context):
        abi = args.get("abi", "dovetail")
        default_objective = args.get("objective", None) or _DEFAULT_OBJECTIVE.get(abi) or "dovetail"
        return AnnotationResult(
            flags={"no_dce", "preserve_name", "export"},
            metadata={"abi": abi, "path": args.get("path", ""), "objective": default_objective}
        )