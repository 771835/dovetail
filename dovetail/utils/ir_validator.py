# coding=utf-8
"""
IR 结构验证工具。

用于检测 IR 结构是否有效。
"""
from typing import Optional

from dovetail.core.enums import StructureType
from dovetail.core.instructions import IROpCode
from dovetail.core.ir_builder import IRBuilder
from dovetail.core.symbols import Variable, Reference

STACK_TYPE = list[tuple[str, StructureType, int, set[str]]] # {作用域名, 作用域类型, 作用域开始指令, 作用域内定义的变量}

class IRValidationError(Exception):
    """IR 结构验证失败。"""

def _validate_has_declared(var_name:str, stack: STACK_TYPE) -> tuple[bool, Optional[set[str]]]:
    for begin_name, begin_type, begin_idx, var_table in reversed(stack):
        if var_name in var_table:
            return True, var_table
    else:
        return False, None

def validate_ir(builder: IRBuilder) -> list[str]:
    """
    验证 IR 结构是否有效。

    Args:
        builder: IRBuilder 实例

    Returns:
        错误消息列表，如果为空则说明验证通过。

    Notes:
        定义清理后意外的提示是正常的，死代码清理会修正所有未被定义但被使用的操作
    """
    errors: list[str] = []
    stack: STACK_TYPE = []
    current_var_table: Optional[set] = None

    for idx, instr in enumerate(builder.get_instructions()):
        if instr.opcode == IROpCode.SCOPE_BEGIN:
            operands = instr.operands
            if len(operands) < 2:
                errors.append(f"[{idx}] SCOPE_BEGIN 缺少操作数: {instr}")
                continue
            scope_name = operands[0]
            scope_type = operands[1]
            var_table = set()
            stack.append((scope_name, scope_type, idx, var_table))
            current_var_table = var_table

        elif instr.opcode == IROpCode.DECLARE:
            operands = instr.operands
            if len(operands) < 1:
                errors.append(f"[{idx}] DECLARE 缺少操作数: {instr}")
                continue
            var:Variable = operands[0]
            if current_var_table is None:
                continue
            if var.name in current_var_table:
                errors.append(f"[{idx}] 重复定义变量 '{var.name}'")
                continue
            current_var_table.add(var.name)

        elif instr.opcode == IROpCode.FREE:
            operands = instr.operands
            if len(operands) < 1:
                errors.append(f"[{idx}] FREE 缺少操作数: {instr}")
                continue
            var: Variable = operands[0]

            _is_has, _table = _validate_has_declared(var.name, stack)
            if _is_has:
                assert _table is not None
                _table.remove(var.name)
                break
            else:
                errors.append(f"[{idx}] FREE 试图释放未被定义的变量 '{var.name}'")

        elif instr.opcode == IROpCode.SCOPE_END:
            operands = instr.operands
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

            begin_name, begin_type, begin_idx, var_table = stack.pop()
            current_var_table = stack[-1][3] if stack else None
            if begin_name != scope_name or begin_type != scope_type:
                errors.append(
                    f"[{idx}] SCOPE_END {scope_name} ({getattr(scope_type, 'name', scope_type)}) "
                    f"与之前的 SCOPE_BEGIN {begin_name} ({getattr(begin_type, 'name', begin_type)}) "
                    f"不匹配, 开始位置: {begin_idx}"
                )

        else:
            operands = instr.operands
            for operand in operands:
                if isinstance(operand, Reference):
                    operand_val = operand.value
                    if isinstance(operand_val, Variable):
                        _is_has, _table = _validate_has_declared(operand_val.name, stack)
                        if not _is_has:
                            errors.append(f"[{idx}] {instr.opcode.name} '{operand_val.name}' 未被定义但被使用")
                elif isinstance(operand, Variable):
                    _is_has, _table = _validate_has_declared(operand.name, stack)
                    if not _is_has:
                        errors.append(f"[{idx}] {instr.opcode.name} '{operand.name}' 未被定义但被使用")

    while stack:
        scope_name, scope_type, begin_idx, var_table = stack.pop()
        errors.append(
            f"[{begin_idx}] 未关闭的 SCOPE_BEGIN: {scope_name} ({getattr(scope_type, 'name', scope_type)})"
        )

    return errors


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


def assert_ir(builder: IRBuilder) -> None:
    """
    对 IR 进行断言检查。

    若存在错误，则抛出 IRValidationError。
    """
    errors = validate_ir_scope_structure(builder)
    if errors:
        raise IRValidationError("IR 作用域结构验证失败:\n" + "\n".join(errors))
