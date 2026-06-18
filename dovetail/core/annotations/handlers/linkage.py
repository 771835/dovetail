# coding=utf-8
import re
from typing import TYPE_CHECKING

from dovetail.core.annotations.base import (
    AnnotationProcessor, AnnotationContext, AnnotationResult, AnnotationTarget, AnnotationTiming
)
from dovetail.core.annotations.decorator import annotation_processor
from dovetail.core.enums import PrimitiveDataType
from dovetail.core.enums.types import FunctionType
from dovetail.core.errors import Errors

if TYPE_CHECKING:
    from dovetail.core.symbols import Function


_KNOWN_ABIS = {"dovetail", "clang-mc"}
_FFI_SAFE = {
    PrimitiveDataType.INT,
    PrimitiveDataType.BOOLEAN,
    PrimitiveDataType.VOID,
    PrimitiveDataType.STRING,
}
_NAMESPACE_PATTERN = re.compile(r'^[0-9a-z_.-]+$')
_NAME_PATTERN = re.compile(r'^[0-9a-z_./-]+$')


def _check_abi(abi: str, ctx: AnnotationContext) -> bool:
    if abi not in _KNOWN_ABIS:
        ctx.error_reporter.report(
            Errors.AnnotationArgumentError,
            "extern/export",
            f"未知 ABI '{abi}'，支持的值: {', '.join(_KNOWN_ABIS)}",
            meta=ctx.meta,
        )
        return False
    return True


def _check_ffi_types(func: "Function", abi: str, ctx: AnnotationContext) -> bool:
    """
    校验 extern/export 函数的签名是否满足 ABI 约束

    Args:
        func: 函数符号
        abi: ABI 标识符（如 "clang-mc", "dovetail"）
        ctx: 注解上下文

    Returns:
        True 表示签名合法
    """
    if abi == "dovetail":
        return True  # 原生 ABI 无限制

    if abi == "clang-mc":
        # 检查返回值类型
        if func.return_type not in _FFI_SAFE:
            ctx.error_reporter.report(
                Errors.NotFFISafeType,
                f"({', '.join(t.get_name() for t in _FFI_SAFE)})",
                func.return_type.get_name(),
                meta=ctx.meta,
                suggestion=f"clang-mc ABI 不支持返回类型 {func.return_type.get_name()}"
            )
            return False

        # 检查参数类型
        for param in func.params:
            if param.get_dtype() not in _FFI_SAFE:
                ctx.error_reporter.report(
                    Errors.NotFFISafeType,
                    param.get_dtype().get_name(),
                    meta=ctx.meta,
                    suggestion=f"参数 '{param.get_name()}' 的类型 {param.get_dtype().get_name()} 不是 clang-mc ABI 安全类型"
                )
                return False
        return True

    # 未知 ABI
    ctx.error_reporter.report(
        Errors.AnnotationArgumentError,
        "extern/export",
        f"未知的 ABI 标识符 '{abi}'，支持的值: dovetail, clang-mc",
        meta=ctx.meta
    )
    return False

def _check_path(s: str, ctx: AnnotationContext) -> bool:
    if ":" not in s:
        ctx.error_reporter.report(
            Errors.AnnotationArgumentError,

            abi,
            meta=ctx.meta,
            suggestion=f"未知的 ABI 标识符 '{abi}'，支持的值: dovetail, clang-mc"
        )
        return False
    namespace,path = s.split(":", maxsplit=1)

    if ".." in namespace: return False
    if not bool(_NAMESPACE_PATTERN.match(namespace)):return  False
    if not bool(_NAME_PATTERN.match(path)):return  False
    return True


@annotation_processor
class ExternProcessor(AnnotationProcessor):
    annotation_name = "extern"
    experimental = True
    applicable_targets = [AnnotationTarget.FUNCTION]
    timing = AnnotationTiming.POST_SYMBOL

    def validate(self, args, ctx):
        abi = args.get("abi", "dovetail")
        path = args.get("path", "")
        return _check_abi(abi, ctx) and _check_ffi_types(ctx.symbol, abi, ctx) and _check_path(path)

    def process(self, args, ctx):
        return AnnotationResult(
            flags={"no_inline", "no_dce", "extern"},
            type_override=FunctionType.EXTERN,
            metadata={"abi": args.get("abi", "dovetail"), "path": args.get("path", "")},
        )


@annotation_processor
class ExportProcessor(AnnotationProcessor):
    annotation_name = "export"
    experimental = True
    applicable_targets = [AnnotationTarget.FUNCTION]
    timing = AnnotationTiming.POST_SYMBOL

    def validate(self, args, ctx):
        abi = args.get("abi", "dovetail")
        return _check_abi(abi, ctx) and _check_ffi_types(ctx.symbol, abi, ctx)

    def process(self, args, ctx):
        return AnnotationResult(
            flags={"no_dce", "preserve_name", "export"},
            metadata={"abi": args.get("abi", "dovetail"), "path": args.get("path", "")},
        )
