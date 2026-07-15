# coding=utf-8
"""
IR 作用域结构验证工具。

用于检测 IR 中 SCOPE_BEGIN/SCOPE_END 配对是否正确、嵌套是否一致。
"""
from dovetail.core.instructions import IROpCode
from dovetail.core.ir_builder import IRBuilder


class IRScopeValidationError(Exception):
    """IR 作用域结构验证失败。"""


def validate_ir_scope_structure(builder: IRBuilder) -> list[str]:
    """
    验证 IR 中作用域结构是否有效。

    Args:
        builder: IRBuilder 实例

    Returns:
        错误消息列表，如果为空则说明验证通过。
    """
    errors: list[str] = []
    stack: list[tuple[str, object, int]] = []

    for idx, instr in enumerate(builder.get_instructions()):
        if instr.opcode == IROpCode.SCOPE_BEGIN:
            operands = instr.get_operands()
            if len(operands) < 2:
                errors.append(f"[{idx}] SCOPE_BEGIN 缺少操作数: {instr}")
                continue
            scope_name = operands[0]
            scope_type = operands[1]
            stack.append((scope_name, scope_type, idx))

        elif instr.opcode == IROpCode.SCOPE_END:
            operands = instr.get_operands()
            if len(operands) < 2:
                errors.append(f"[{idx}] SCOPE_END 缺少操作数: {instr}")
                continue
            scope_name = operands[0]
            scope_type = operands[1]

            if not stack:
                errors.append(
                    f"[{idx}] 未匹配的 SCOPE_END: {scope_name} ({getattr(scope_type, 'name', scope_type)})"
                )
                continue

            begin_name, begin_type, begin_idx = stack.pop()
            if begin_name != scope_name or begin_type != scope_type:
                errors.append(
                    f"[{idx}] SCOPE_END {scope_name} ({getattr(scope_type, 'name', scope_type)}) "
                    f"与之前的 SCOPE_BEGIN {begin_name} ({getattr(begin_type, 'name', begin_type)}) "
                    f"不匹配, 开始位置: {begin_idx}"
                )

    while stack:
        scope_name, scope_type, begin_idx = stack.pop()
        errors.append(
            f"[{begin_idx}] 未关闭的 SCOPE_BEGIN: {scope_name} ({getattr(scope_type, 'name', scope_type)})"
        )

    return errors


def assert_ir_scope_structure(builder: IRBuilder) -> None:
    """
    对 IR 作用域结构进行断言检查。

    若存在错误，则抛出 IRScopeValidationError。
    """
    errors = validate_ir_scope_structure(builder)
    if errors:
        raise IRScopeValidationError("IR 作用域结构验证失败:\n" + "\n".join(errors))
