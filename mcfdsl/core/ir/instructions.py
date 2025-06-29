# coding=utf-8
from dataclasses import dataclass
from typing import List, Any

from mcfdsl.core._interfaces import ISymbol
from mcfdsl.core.language_class import Class
from mcfdsl.core.language_types import StructureType, DataType
from mcfdsl.core.safe_enum import SafeEnum


class IROpCode(SafeEnum):
    # ===== 控制流指令 (0x00-0x1F) =====
    JUMP = 0x00  # 无条件跳转
    COND_JUMP = 0x01  # 条件跳转
    FUNCTION = 0x02  # 函数定义
    CALL = 0x03  # 函数调用
    CALL_INLINE = 0x04  # 内联函数调用
    RETURN = 0x05  # 函数返回
    SCOPE_BEGIN = 0x06  # 作用域开始
    SCOPE_END = 0x07  # 作用域结束
    LOOP_BEGIN = 0x08  # 循环开始
    LOOP_END = 0x09  # 循环结束
    BREAK = 0x0A  # 跳出循环
    CONTINUE = 0x0B  # 继续循环
    # 预留 0x0C-0x1F 用于控制流扩展

    # ===== 变量操作指令 (0x20-0x3F) =====
    DECLARE = 0x20  # 变量声明
    DECLARE_TEMP = 0x21  # 临时变量声明
    VAR_RELEASE = 0x22  # 变量释放
    ASSIGN = 0x23  # 赋值操作
    UNARY_OP = 0x24  # 一元运算
    OP = 0x25  # 二元运算
    COMPARE = 0x26  # 比较运算
    # 预留 0x27-0x3F 用于变量操作扩展

    # ===== 面向对象指令 (0x40-0x5F) =====
    CLASS = 0x40  # 类定义
    NEW_OBJ = 0x41  # 对象实例化
    GET_FIELD = 0x42  # 获取字段
    SET_FIELD = 0x43  # 设置字段
    CALL_METHOD = 0x44  # 方法调用
    # 预留 0x45-0x5F 用于OOP扩展

    # ===== 命令生成指令 (0x60-0x7F) =====
    RAW_CMD = 0x60  # 原始命令输出
    FSTRING = 0x61  # 格式化字符串
    # 预留 0x62-0x7F 用于命令扩展

    # ==== 扩展指令集 (0x80-0xFF) ====
    # 预留 0x80-0xFF 用于未来补充

    # ==== 其他指令集 (0x100+) ====
    # 预留 0x100+ 用于插件使用


@dataclass
class IRInstruction:
    opcode: IROpCode
    operands: List[Any]
    line: int = -1
    column: int = -1
    filename: str = None

    def __repr__(self):
        ops = ", ".join(f"{op = }" for op in self.operands)
        return f"{self.opcode}({ops})"


# 具体指令实现
@dataclass
class IRJump(IRInstruction):
    def __init__(self, scope: str, line: int = -1, column: int = -1, filename: str = None):
        operands = [
            scope
        ]
        super().__init__(IROpCode.JUMP, operands, line, column, filename)


@dataclass
class IRCondJump(IRInstruction):
    def __init__(self, cond_var: str, true_scope: str, false_scope: str = None, line: int = -1, column: int = -1,
                 filename: str = None):
        operands = [
            cond_var,
            true_scope,
            false_scope
        ]
        super().__init__(IROpCode.COND_JUMP, operands, line, column, filename)


@dataclass
class IRFunction(IRInstruction):
    def __init__(self, func_name: str, params: List[ISymbol] = None, line: int = -1, column: int = -1,
                 filename: str = None):
        if params is None:
            params = []
        operands = [
            func_name,
            params
        ]
        super().__init__(IROpCode.FUNCTION, operands, line, column, filename)


@dataclass
class IRReturn(IRInstruction):
    def __init__(self, value: ISymbol = None, line: int = -1, column: int = -1, filename: str = None):
        operands = [
            value
        ]
        super().__init__(IROpCode.RETURN, operands, line, column, filename)


@dataclass
class IRCall(IRInstruction):
    def __init__(self, func: str, args: List[ISymbol] = None, line: int = -1, column: int = -1, filename: str = None):
        if args is None:
            args = []
        operands = [
            func,
            args
        ]
        super().__init__(IROpCode.CALL, operands, line, column, filename)


@dataclass
class IRCallInline(IRInstruction):
    def __init__(self, func: str, args: List[ISymbol] = None, line: int = -1, column: int = -1, filename: str = None):
        if args is None:
            args = []
        operands = [
            func,
            args
        ]
        super().__init__(IROpCode.CALL_INLINE, operands, line, column, filename)


@dataclass
class IRScopeBegin(IRInstruction):
    def __init__(self, name: str, stype: StructureType, line: int = -1, column: int = -1, filename: str = None):
        operands = [
            name,
            stype
        ]
        super().__init__(IROpCode.SCOPE_BEGIN, operands, line, column, filename)


@dataclass
class IRScopeEnd(IRInstruction):
    def __init__(self, name: str, line: int = -1, column: int = -1, filename: str = None):
        operands = [
            name
        ]
        super().__init__(IROpCode.SCOPE_END, operands, line, column, filename)


@dataclass
class IRLoopBegin(IRInstruction):
    def __init__(self, loop_id: str, init: List[IRInstruction], cond: List[IRInstruction], line: int = -1,
                 column: int = -1, filename: str = None):
        operands = [
            loop_id,
            init,
            cond
        ]
        super().__init__(IROpCode.LOOP_BEGIN, operands, line, column, filename)


@dataclass
class IRLoopEnd(IRInstruction):
    def __init__(self, loop_id: str, line: int = -1, column: int = -1, filename: str = None):
        operands = [
            loop_id
        ]
        super().__init__(IROpCode.LOOP_END, operands, line, column, filename)


@dataclass
class IRBreak(IRInstruction):
    def __init__(self, loop_id: str, line: int = -1, column: int = -1, filename: str = None):
        operands = [
            loop_id
        ]
        super().__init__(IROpCode.BREAK, operands, line, column, filename)


@dataclass
class IRContinue(IRInstruction):
    def __init__(self, loop_id: str, line: int = -1, column: int = -1, filename: str = None):
        operands = [
            loop_id
        ]
        super().__init__(IROpCode.CONTINUE, operands, line, column, filename)


@dataclass
class IRDeclare(IRInstruction):
    def __init__(self, name: str, dtype: DataType, value: ISymbol = None, line: int = -1, column: int = -1,
                 filename: str = None):
        operands = [
            name,
            dtype,
            value
        ]
        super().__init__(IROpCode.DECLARE, operands, line, column, filename)


@dataclass
class IRDeclareTemp(IRInstruction):
    def __init__(self, name: str, dtype: DataType, value: ISymbol = None, line: int = -1, column: int = -1,
                 filename: str = None):
        operands = [
            name,
            dtype,
            value
        ]
        super().__init__(IROpCode.DECLARE_TEMP, operands, line, column, filename)


@dataclass
class IRVarRelease(IRInstruction):
    def __init__(self, name: str, line: int = -1, column: int = -1, filename: str = None):
        operands = [
            name
        ]
        super().__init__(IROpCode.VAR_RELEASE, operands, line, column, filename)


@dataclass
class IRAssign(IRInstruction):
    def __init__(self, target: ISymbol, source: ISymbol, line: int = -1, column: int = -1, filename: str = None):
        operands = [
            target,
            source
        ]
        super().__init__(IROpCode.ASSIGN, operands, line, column, filename)


@dataclass
class IRUnaryOp(IRInstruction):
    def __init__(self, result: ISymbol, op, operand: ISymbol, line: int = -1, column: int = -1, filename: str = None):
        operands = [
            result,
            op,
            operand
        ]
        super().__init__(IROpCode.UNARY_OP, operands, line, column, filename)


@dataclass
class IROp(IRInstruction):
    def __init__(self, result: ISymbol, op, left: ISymbol, right: ISymbol, line: int = -1, column: int = -1,
                 filename: str = None):
        operands = [
            result,
            op,
            left,
            right
        ]
        super().__init__(IROpCode.OP, operands, line, column, filename)


@dataclass
class IRCompare(IRInstruction):
    def __init__(self, result: ISymbol, op, left: ISymbol, right: ISymbol, line: int = -1, column: int = -1,
                 filename: str = None):
        operands = [
            result,
            op,
            left,
            right
        ]
        super().__init__(IROpCode.COMPARE, operands, line, column, filename)


@dataclass
class IRClass(IRInstruction):
    def __init__(self, class_: Class, line: int = -1, column: int = -1, filename: str = None):
        operands = [
            class_
        ]
        super().__init__(IROpCode.CLASS, operands, line, column, filename)


@dataclass
class IRNewObj(IRInstruction):
    def __init__(self, result: ISymbol, class_: str, args: List[ISymbol], line: int = -1, column: int = -1,
                 filename: str = None):
        operands = [
            result,
            class_,
            args
        ]
        super().__init__(IROpCode.NEW_OBJ, operands, line, column, filename)


@dataclass
class IRGetField(IRInstruction):
    def __init__(self, result: ISymbol, obj: ISymbol, field: str, line: int = -1, column: int = -1,
                 filename: str = None):
        operands = [
            result,
            obj,
            field
        ]
        super().__init__(IROpCode.GET_FIELD, operands, line, column, filename)


@dataclass
class IRSetField(IRInstruction):
    def __init__(self, obj: ISymbol, field: str, value: ISymbol, line: int = -1, column: int = -1,
                 filename: str = None):
        operands = [
            obj,
            field,
            value
        ]
        super().__init__(IROpCode.SET_FIELD, operands, line, column, filename)


@dataclass
class IRCallMethod(IRInstruction):
    def __init__(self, result: ISymbol, obj: ISymbol, method: str, args: List[ISymbol] = None, line: int = -1,
                 column: int = -1, filename: str = None):
        operands = [
            result,
            obj,
            method,
            args
        ]
        super().__init__(IROpCode.CALL_METHOD, operands, line, column, filename)


@dataclass
class IRRawCmd(IRInstruction):
    def __init__(self, command_string: List[str] | str, line: int = -1, column: int = -1, filename: str = None):
        if isinstance(command_string, str):
            command_string = [command_string]
        operands = [
            command_string
        ]
        super().__init__(IROpCode.RAW_CMD, operands, line, column, filename)
