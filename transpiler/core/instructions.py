# coding=utf-8

from transpiler.core.enums import StructureType, CompareOps, BinaryOps, UnaryOps, DataType
from transpiler.core.safe_enum import SafeEnum
from transpiler.core.symbols import Literal, Class, Constant, Function, Reference, Variable, Symbol


class IROpCode(SafeEnum):
    # ===== 控制流指令 (0x00-0x1F) =====
    JUMP = 0x00  # 无条件跳转
    COND_JUMP = 0x01  # 条件跳转
    FUNCTION = 0x02  # 函数定义
    CALL = 0x03  # 函数调用
    RETURN = 0x04  # 函数返回
    SCOPE_BEGIN = 0x05  # 作用域开始
    SCOPE_END = 0x06  # 作用域结束
    BREAK = 0x07  # 跳出循环
    CONTINUE = 0x08  # 继续循环
    # 预留 0x09-0x1F 用于控制流扩展

    # ===== 变量操作指令 (0x20-0x3F) =====
    DECLARE = 0x20  # 变量声明
    ASSIGN = 0x21  # 赋值操作
    UNARY_OP = 0x22  # 一元运算
    OP = 0x23  # 二元运算
    COMPARE = 0x24  # 比较运算
    CAST = 0x25  # 显式类型转换
    # 预留 0x26-0x3F 用于变量操作扩展

    # ===== 面向对象指令 (0x40-0x5F) =====
    CLASS = 0x40  # 类定义
    NEW_OBJ = 0x41  # 对象实例化
    GET_FIELD = 0x42  # 获取字段
    SET_FIELD = 0x43  # 设置字段
    CALL_METHOD = 0x44  # 方法调用

    # 预留 0x45-0x5F 用于OOP扩展

    # ===== 特殊指令 (0x60-0x7F) =====

    # 预留 0x60-0x7F 用于命令扩展

    # ==== 扩展指令集 (0x80-0xFF) ====
    # 预留 0x80-0xFF 用于未来补充

    # ==== 其他指令集 (0x100+) ====
    # 预留 0x100+ 用于用户自行使用

    def __hash__(self):
        return hash(self.value)


class IRInstruction:
    def __init__(
            self,
            opcode: IROpCode,
            operands: list[Reference | str | Symbol | SafeEnum],
            line: int = -1,
            column: int = -1,
            filename: str | None = None,
            flags: dict[str, int] = None
    ):
        self.opcode = opcode
        self.operands = operands
        self.filename = filename
        self.column = column
        self.line = line
        self.flags: dict[str, int] = flags or {}

    def __repr__(self):
        return f"{self.opcode}(operands={self.operands}, line={self.line}, column={self.column}, flags={self.flags})"

    def __hash__(self):
        # 处理操作数的哈希值计算
        operand_hashes = []

        for op in self.get_operands():
            if isinstance(op, (list, tuple)):
                # 递归处理嵌套列表/元组
                operand_hashes.append(tuple(self._flatten_nested(op)))
            elif isinstance(op, dict):
                # 字典转换为排序后的元组
                operand_hashes.append(tuple(sorted((k, self._flatten_nested(v)) for k, v in op.items())))
            elif hasattr(op, '__hash__') and callable(op.__hash__):
                # 可哈希对象直接使用
                operand_hashes.append(hash(op))
            else:
                # 最后手段：使用对象ID
                operand_hashes.append(id(op))

        return hash((self.opcode, tuple(operand_hashes)))

    def __eq__(self, other):
        return hash(self) == hash(other)

    def _flatten_nested(self, obj: list | tuple | dict | str):
        """递归处理嵌套结构"""
        if isinstance(obj, (list, tuple)):
            return tuple(self._flatten_nested(item) for item in obj)
        elif isinstance(obj, dict):
            return tuple(sorted((k, self._flatten_nested(v)) for k, v in obj.items()))
        elif hasattr(obj, '__hash__'):
            return hash(obj)
        elif hasattr(obj, 'unique_id') and callable(obj.unique_id):
            return obj.unique_id()
        return id(obj)

    def add_flag(self, flag: str, value: int):
        self.flags[flag] = value

    def get_operands(self):
        return self.operands

    def get_line(self):
        return self.line

    def get_column(self):
        return self.column

    def get_filename(self):
        return self.filename

    def get_opcode(self):
        return self.opcode

    def get_flags(self):
        return self.flags


# 具体指令实现
class IRJump(IRInstruction):
    def __init__(self, scope: str, line: int = -1,
                 column: int = -1, filename: str = None):
        operands = [
            scope
        ]
        super().__init__(IROpCode.JUMP, operands, line, column, filename)


class IRCondJump(IRInstruction):
    def __init__(self, cond: Variable, true_scope: str, false_scope: str = None, line: int = -1, column: int = -1,
                 filename: str = None):
        assert cond.dtype == DataType.BOOLEAN

        operands = [
            cond,
            true_scope,
            false_scope
        ]
        super().__init__(IROpCode.COND_JUMP, operands, line, column, filename)


class IRFunction(IRInstruction):
    def __init__(self, function: Function, line: int = -1, column: int = -1,
                 filename: str = None):
        operands = [
            function
        ]
        super().__init__(IROpCode.FUNCTION, operands, line, column, filename)


class IRReturn(IRInstruction):
    def __init__(self, value: Reference[Variable | Constant | Literal] | None = None, line: int = -1, column: int = -1,
                 filename: str = None):
        operands = [
            value,
        ]
        super().__init__(IROpCode.RETURN, operands, line, column, filename)


class IRCall(IRInstruction):
    def __init__(self, result: Variable | Constant | None, func: Function,
                 args: dict[str, Reference[Variable | Constant | Literal]] = None, line: int = -1, column: int = -1,
                 filename: str = None):
        if args is None:
            args = []
        operands = [
            result,
            func,
            args
        ]
        super().__init__(IROpCode.CALL, operands, line, column, filename)


class IRScopeBegin(IRInstruction):
    def __init__(self, name: str, stype: StructureType,
                 line: int = -1, column: int = -1, filename: str = None):
        operands = [
            name,
            stype
        ]
        super().__init__(IROpCode.SCOPE_BEGIN, operands, line, column, filename)


class IRScopeEnd(IRInstruction):
    def __init__(self, name: str, stype: StructureType, line: int = -1, column: int = -1, filename: str = None):
        operands = [
            name,
            stype
        ]
        super().__init__(IROpCode.SCOPE_END, operands, line, column, filename)


class IRBreak(IRInstruction):
    def __init__(self, scope_name: str, line: int = -1, column: int = -1, filename: str = None):
        operands = [
            scope_name
        ]
        super().__init__(IROpCode.BREAK, operands, line, column, filename)


class IRContinue(IRInstruction):
    def __init__(self, scope_name: str, line: int = -1, column: int = -1, filename: str = None):
        operands = [
            scope_name
        ]
        super().__init__(IROpCode.CONTINUE, operands, line, column, filename)


class IRDeclare(IRInstruction):
    def __init__(self, var: Variable | Constant, line: int = -1, column: int = -1,
                 filename: str = None):
        operands = [
            var
        ]
        super().__init__(IROpCode.DECLARE, operands, line, column, filename)


class IRAssign(IRInstruction):
    def __init__(self, target: Variable | Constant, source: Reference[Variable | Constant | Literal], line: int = -1,
                 column: int = -1, filename: str = None):
        operands = [
            target,
            source
        ]
        super().__init__(IROpCode.ASSIGN, operands, line, column, filename)


class IRUnaryOp(IRInstruction):
    def __init__(self, result: Variable | Constant, op: UnaryOps, operand: Reference[Variable | Constant | Literal],
                 line: int = -1,
                 column: int = -1,
                 filename: str = None):
        operands = [
            result,
            op,
            operand
        ]
        super().__init__(IROpCode.UNARY_OP, operands, line, column, filename)


class IROp(IRInstruction):
    def __init__(self, result: Variable | Constant, op: BinaryOps, left: Reference[Variable | Constant | Literal],
                 right: Reference[Variable | Constant | Literal], line: int = -1, column: int = -1,
                 filename: str = None):
        operands = [
            result,
            op,
            left,
            right
        ]
        super().__init__(IROpCode.OP, operands, line, column, filename)


class IRCompare(IRInstruction):
    def __init__(self, result: Variable | Constant, op: CompareOps, left: Reference[Variable | Constant | Literal],
                 right: Reference[Variable | Constant | Literal], line: int = -1, column: int = -1,
                 filename: str = None):
        operands = [
            result,
            op,
            left,
            right
        ]
        super().__init__(IROpCode.COMPARE, operands, line, column, filename)


class IRCast(IRInstruction):
    def __init__(self, result: Variable | Constant, dtype: DataType | Class,
                 value: Reference[Variable | Constant | Literal], line: int = -1,
                 column: int = -1, filename: str = None):
        operands = [
            result,
            dtype,
            value
        ]
        super().__init__(IROpCode.CAST, operands, line, column, filename)


class IRClass(IRInstruction):
    def __init__(self, class_: Class, line: int = -1,
                 column: int = -1, filename: str = None):
        operands = [
            class_
        ]
        super().__init__(IROpCode.CLASS, operands, line, column, filename)


class IRNewObj(IRInstruction):
    def __init__(self, result: Variable, class_: Class,
                 line: int = -1, column: int = -1,
                 filename: str = None):
        operands = [
            result,
            class_
        ]
        super().__init__(IROpCode.NEW_OBJ, operands, line, column, filename)


class IRGetField(IRInstruction):
    def __init__(self, result: Variable, obj: Reference[Variable | Constant], field: str, line: int = -1,
                 column: int = -1,
                 filename: str = None):
        operands = [
            result,
            obj,
            field
        ]
        super().__init__(IROpCode.GET_FIELD, operands, line, column, filename)


class IRSetField(IRInstruction):
    def __init__(self, obj: Variable, field: str, value: Reference[Variable | Constant | Literal], line: int = -1,
                 column: int = -1,
                 filename: str = None):
        operands = [
            obj,
            field,
            value
        ]
        super().__init__(IROpCode.SET_FIELD, operands, line, column, filename)


class IRCallMethod(IRInstruction):
    def __init__(self, result: Variable | None, class_: Class, method: Function,
                 args: dict[str, Reference] = None, line: int = -1,
                 column: int = -1, filename: str = None):
        operands = [
            result,
            class_,
            method,
            args
        ]
        super().__init__(IROpCode.CALL_METHOD, operands, line, column, filename)
