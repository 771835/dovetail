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

STACK_TYPE = list[tuple[str, StructureType, int, set[str]]]  # {作用域名, 作用域类型, 作用域开始指令, 作用域内定义的变量}


class IRValidationError(Exception):
    """IR 结构验证失败。"""


def _validate_has_declared(var_name: str, stack: STACK_TYPE) -> tuple[bool, Optional[set[str]]]:
    for begin_name, begin_type, begin_idx, var_table in reversed(stack):
        if var_name in var_table:
            return True, var_table
    else:
        return False, None


def validate_ir(builder: IRBuilder) -> list[str]:
    """
    验证 IR 结构是否有效。

    不变量清单：
      1. scope BEGIN/END 完美配对且嵌套正确
      2. 无重复 DECLARE 同一变量
      3. 所有被读取的引用已声明
      4. 产生结果的指令，其 result 变量已声明
      5. 跳转目标 scope 名存在于 IR 中
      6. RETURN 仅出现在 FUNCTION scope 内
      7. BREAK/CONTINUE 仅出现在循环 scope 内

    Returns:
        错误消息列表，为空则验证通过。
    """
    errors: list[str] = []

    # ---- 第一遍：收集所有 scope 名 ----
    all_scope_names: set[str] = set()
    for idx, instr in enumerate(builder.get_instructions()):
        if instr.opcode == IROpCode.SCOPE_BEGIN:
            if len(instr.operands) >= 2:
                all_scope_names.add(instr.operands[0])

    # ---- 第二遍：逐条校验 ----
    stack: STACK_TYPE = [("global", StructureType.GLOBAL, -1, set())]
    current_var_table: Optional[set] = stack[0][3]

    for idx, instr in enumerate(builder.get_instructions()):
        if instr.opcode == IROpCode.SCOPE_BEGIN:
            operands = instr.operands
            if len(operands) < 2:
                errors.append(f"[{idx}] SCOPE_BEGIN 缺少操作数: {instr}")
                continue
            scope_name, scope_type = operands[0], operands[1]
            var_table = set()
            stack.append((scope_name, scope_type, idx, var_table))
            current_var_table = var_table

        elif instr.opcode == IROpCode.SCOPE_END:
            operands = instr.operands
            if len(operands) < 2:
                errors.append(f"[{idx}] SCOPE_END 缺少操作数: {instr}")
                continue
            scope_name, scope_type = operands[0], operands[1]
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

        elif instr.opcode == IROpCode.DECLARE:
            operands = instr.operands
            if len(operands) < 1:
                errors.append(f"[{idx}] DECLARE 缺少操作数: {instr}")
                continue
            var: Variable = operands[0]
            if current_var_table is not None:
                if var.name in current_var_table:
                    errors.append(f"[{idx}] 重复定义变量 '{var.name}'")
                else:
                    current_var_table.add(var.name)

        elif instr.opcode == IROpCode.RETURN:
            # 不变量 6: RETURN 必须在 FUNCTION scope 内
            in_function = any(s[1] == StructureType.FUNCTION for s in stack)
            if not in_function:
                errors.append(f"[{idx}] RETURN 出现在非函数作用域内")

        elif instr.opcode in (IROpCode.BREAK, IROpCode.CONTINUE):
            # 不变量 7: BREAK/CONTINUE 必须在循环 scope 内
            in_loop = any(
                s[1] in (StructureType.LOOP_CHECK, StructureType.LOOP_BODY)
                for s in stack
            )
            if not in_loop:
                errors.append(f"[{idx}] {instr.opcode.desc} 出现在非循环作用域内")

        # --- 跳转目标 scope 存在性 (不变量 5) ---
        if instr.opcode == IROpCode.JUMP:
            if len(instr.operands) >= 1 and instr.operands[0] not in all_scope_names:
                errors.append(f"[{idx}] JUMP 目标 scope '{instr.operands[0]}' 不存在")

        elif instr.opcode == IROpCode.COND_JUMP:
            for i, label in enumerate(("true_scope", "false_scope")):
                target = instr.operands[1 + i] if len(instr.operands) > 1 + i else None
                if target is not None and target not in all_scope_names:
                    errors.append(f"[{idx}] COND_JUMP {label} '{target}' 不存在")

        elif instr.opcode in (IROpCode.BREAK, IROpCode.CONTINUE):
            if len(instr.operands) >= 1 and instr.operands[0] not in all_scope_names:
                errors.append(f"[{idx}] {instr.opcode.desc} 目标 scope '{instr.operands[0]}' 不存在")

        # --- 被读取引用已声明 (不变量 3) ---
        if instr.opcode != IROpCode.SCOPE_BEGIN and instr.opcode != IROpCode.SCOPE_END:
            for operand in instr.opcode.get_used_refs(instr.operands):
                if isinstance(operand, Reference):
                    operand_val = operand.value
                    if isinstance(operand_val, Variable):
                        is_has, _ = _validate_has_declared(operand_val.name, stack)
                        if not is_has:
                            errors.append(
                                f"[{idx}] {instr.opcode.desc} '{operand_val.name}' 未被定义但被使用"
                            )

        # --- result 变量已声明 (不变量 4) ---
        if instr.opcode.produces_result:
            result_var = instr.opcode.get_result_var(instr.operands)
            if result_var is not None:
                is_has, _ = _validate_has_declared(result_var.name, stack)
                if not is_has:
                    errors.append(
                        f"[{idx}] {instr.opcode.desc} 的结果变量 '{result_var.name}' 未声明"
                    )

    # --- 未关闭 scope (不变量 1) ---
    while stack:
        scope_name, scope_type, begin_idx, var_table = stack.pop()
        if scope_type == StructureType.GLOBAL:
            continue
        errors.append(
            f"[{begin_idx}] 未关闭的 SCOPE_BEGIN: {scope_name} ({getattr(scope_type, 'name', scope_type)})"
        )

    return errors

def assert_ir(builder: IRBuilder) -> None:
    """
    对 IR 进行断言检查。

    若存在错误，则抛出 IRValidationError。
    """
    errors = validate_ir(builder)
    if errors:
        raise IRValidationError("IR 验证失败:\n" + "\n".join(errors))
