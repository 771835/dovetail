# coding=utf-8
from dataclasses import dataclass
from typing import List, Any

from mcfdsl.core._interfaces import IScope, ISymbol
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
    def __init__(self, scope: IScope, line: int = -1, column: int = -1, filename: str = None):
        operands = [
            scope
        ]
        super().__init__(IROpCode.JUMP, operands, line, column, filename)


@dataclass
class IRCondJump(IRInstruction):
    def __init__(self, cond_var: ISymbol, true_scope: IScope, false_scope: IScope = None, line: int = -1, column: int = -1,
                 filename: str = None):
        operands = [
            cond_var,
            true_scope,
            false_scope
        ]
        super().__init__(IROpCode.COND_JUMP, operands, line, column, filename)


@dataclass
class IRFunction(IRInstruction):
    def __init__(self,function: ISymbol, params: List[ISymbol] = None, line: int = -1, column: int = -1, filename: str = None):
        operands = [

        ]
        super().__init__(IROpCode, operands, line, column, filename)


@dataclass
class IR(IRInstruction):
    def __init__(self, line: int = -1, column: int = -1, filename: str = None):
        operands = [

        ]
        super().__init__(IROpCode, operands, line, column, filename)
