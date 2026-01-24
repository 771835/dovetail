# coding=utf-8
from abc import ABC, abstractmethod
from typing import TypeVar, Any

from transpiler.core.enums.operations import UnaryOps, BinaryOps, CompareOps
from transpiler.core.enums.types import DataType, StructureType
from transpiler.core.symbols import Literal, Class, Constant, Function, Reference, Variable, Symbol
from transpiler.utils.safe_enum import SafeEnum

IRInstructionType = TypeVar('IRInstructionType', bound="IRInstruction")


class InstCategory(SafeEnum):
    CONTROL_FLOW = "控制流"
    DATA_OP = "数据运算"
    OOP = "面向对象"
    SPECIAL = "特殊"


class IROpCode(SafeEnum):
    # CONTROL_FLOW (0x00-0x1F)
    JUMP = (0x00, "跳转", InstCategory.CONTROL_FLOW)
    COND_JUMP = (0x01, "条件跳转", InstCategory.CONTROL_FLOW)
    FUNCTION = (0x02, "函数定义", InstCategory.CONTROL_FLOW)
    CALL = (0x03, "函数调用", InstCategory.CONTROL_FLOW)
    RETURN = (0x04, "返回", InstCategory.CONTROL_FLOW)
    SCOPE_BEGIN = (0x05, "作用域开始", InstCategory.CONTROL_FLOW)
    SCOPE_END = (0x06, "作用域结束", InstCategory.CONTROL_FLOW)
    BREAK = (0x07, "中断", InstCategory.CONTROL_FLOW)
    CONTINUE = (0x08, "继续", InstCategory.CONTROL_FLOW)

    # DATA_OP (0x40-0x5F)
    DECLARE = (0x20, "变量声明", InstCategory.DATA_OP)
    ASSIGN = (0x21, "赋值", InstCategory.DATA_OP)
    UNARY_OP = (0x22, "一元运算", InstCategory.DATA_OP)
    BINARY_OP = (0x23, "二元运算", InstCategory.DATA_OP)
    COMPARE = (0x24, "比较", InstCategory.DATA_OP)
    CAST = (0x25, "类型转换", InstCategory.DATA_OP)

    # OOP (0x40-0x5F)
    CLASS = (0x40, "类定义", InstCategory.OOP)
    NEW_OBJ = (0x41, "新建对象", InstCategory.OOP)
    GET_PROPERTY = (0x42, "获取属性", InstCategory.OOP)
    SET_PROPERTY = (0x43, "设置属性", InstCategory.OOP)
    CALL_METHOD = (0x44, "调用方法", InstCategory.OOP)

    def __init__(self, code: int, desc: str, category: InstCategory):
        self.code = code
        self.desc = desc
        self.category = category

    def __hash__(self):
        return hash(self.value)


class IRInstruction(ABC):
    """
    中间表示指令基类

    Args:
        opcode: 指令操作码
        operands: 操作数列表
        line: 源代码行号
        column: 源代码列号
        filename: 源文件名
    """

    def __init__(
            self,
            opcode: IROpCode,
            operands: list[Reference | str | Symbol | SafeEnum | Any],
            line: int = -1,
            column: int = -1,
            filename: str | None = None,
    ):
        self.opcode = opcode
        self.operands = operands
        self.filename = filename
        self.column = column
        self.line = line

    @abstractmethod
    def __repr__(self):
        return f"{self.opcode.name}(operands={self.operands})"

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
        elif hasattr(obj, '__hash__') and callable(obj.__hash__):
            return hash(obj)
        elif hasattr(obj, 'unique_id') and callable(obj.unique_id):
            return obj.unique_id()
        return id(obj)

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


# 具体指令实现
class IRJump(IRInstruction):
    def __init__(
            self,
            scope: str,
            line: int = -1,
            column: int = -1,
            filename: str = None
    ):
        operands = [
            scope
        ]
        super().__init__(IROpCode.JUMP, operands, line, column, filename)

    def __repr__(self):
        return f"goto {self.operands[0]}"


class IRCondJump(IRInstruction):
    def __init__(
            self,
            condition: Variable | Literal,
            true_scope: str | None,
            false_scope: str | None = None,
            line: int = -1,
            column: int = -1,
            filename: str = None
    ):
        assert condition.dtype == DataType.BOOLEAN

        operands = [
            condition,
            true_scope,
            false_scope
        ]
        super().__init__(IROpCode.COND_JUMP, operands, line, column, filename)

    def __repr__(self):
        cond = self.operands[0].value if isinstance(self.operands[0], Literal) else self.operands[0].get_name()
        true_label = self.operands[1]
        false_label = self.operands[2]
        return f"if {cond} goto {true_label} else goto {false_label}"


class IRFunction(IRInstruction):
    def __init__(
            self,
            function: Function,
            line: int = -1,
            column: int = -1,
            filename: str = None
    ):
        operands = [
            function
        ]
        super().__init__(IROpCode.FUNCTION, operands, line, column, filename)

    def __repr__(self):
        return 'function ' \
            + self.operands[0].get_name() \
            + '(' \
            + ','.join(
                f"{param.get_data_type().get_name()} {param.get_name()}"
                for param in self.operands[0].params
            ) \
            + ')'


class IRReturn(IRInstruction):
    def __init__(
            self,
            value: Reference[Variable | Constant | Literal] | None = None,
            line: int = -1,
            column: int = -1,
            filename: str = None
    ):
        operands = [
            value,
        ]
        super().__init__(IROpCode.RETURN, operands, line, column, filename)

    def __repr__(self):
        return f"return {self.operands[0].get_display_value()}"


class IRCall(IRInstruction):
    def __init__(
            self,
            result: Variable | Constant | None,
            func: Function,
            args: dict[str, Reference[Variable | Constant | Literal]] = None,
            line: int = -1, column: int = -1,
            filename: str = None
    ):
        if args is None:
            args = []
        operands = [
            result,
            func,
            args
        ]
        super().__init__(IROpCode.CALL, operands, line, column, filename)

    def __repr__(self):
        ops = self.operands
        args = (f"{name}={repr(value)}" for name, value in ops[2].items())
        if ops[0]:
            return f"{ops[0].get_name()} = {ops[1].get_name()}({','.join(args)})"
        return f"{ops[1].get_name()}({','.join(args)})"


class IRScopeBegin(IRInstruction):
    def __init__(
            self,
            name: str,
            stype: StructureType,
            line: int = -1,
            column: int = -1,
            filename: str = None
    ):
        operands = [
            name,
            stype
        ]
        super().__init__(IROpCode.SCOPE_BEGIN, operands, line, column, filename)

    def __repr__(self):
        return f'{self.operands[0]}:{self.operands[1].value}{{'


class IRScopeEnd(IRInstruction):
    def __init__(
            self,
            name: str,
            stype: StructureType,
            line: int = -1,
            column: int = -1,
            filename: str = None
    ):
        operands = [
            name,
            stype
        ]
        super().__init__(IROpCode.SCOPE_END, operands, line, column, filename)

    def __repr__(self):
        return '}'


class IRBreak(IRInstruction):
    def __init__(self, scope_name: str, line: int = -1, column: int = -1, filename: str = None):
        operands = [
            scope_name
        ]
        super().__init__(IROpCode.BREAK, operands, line, column, filename)

    def __repr__(self):
        return f'break {self.operands[0]}'


class IRContinue(IRInstruction):
    def __init__(self, scope_name: str, line: int = -1, column: int = -1, filename: str = None):
        operands = [
            scope_name
        ]
        super().__init__(IROpCode.CONTINUE, operands, line, column, filename)

    def __repr__(self):
        return f'continue {self.operands[0]}'


class IRDeclare(IRInstruction):
    def __init__(self, var: Variable | Constant, line: int = -1, column: int = -1,
                 filename: str = None):
        operands = [
            var
        ]
        super().__init__(IROpCode.DECLARE, operands, line, column, filename)

    def __repr__(self):
        var = self.operands[0]
        return f'{var.dtype.value if isinstance(var.dtype, DataType) else var.dtype.get_name()} {var.get_name()}'


class IRAssign(IRInstruction):
    def __init__(self, target: Variable | Constant, source: Reference[Variable | Constant | Literal], line: int = -1,
                 column: int = -1, filename: str = None):
        operands = [
            target,
            source
        ]
        super().__init__(IROpCode.ASSIGN, operands, line, column, filename)

    def __repr__(self):
        return f'{self.operands[0].get_name()} = {self.operands[1]}'


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

    def __repr__(self):
        return f'{self.operands[0].get_name()}={self.operands[1].value}{self.operands[2]}'


class IRBinaryOp(IRInstruction):
    def __init__(self, result: Variable | Constant, op: BinaryOps, left: Reference[Variable | Constant | Literal],
                 right: Reference[Variable | Constant | Literal], line: int = -1, column: int = -1,
                 filename: str = None):
        operands = [
            result,
            op,
            left,
            right
        ]
        super().__init__(IROpCode.BINARY_OP, operands, line, column, filename)

    def __repr__(self):
        ops = self.operands
        return f'{ops[0].get_name()} = {ops[2]} {ops[1].value} {ops[2]}'


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

    def __repr__(self):
        ops = self.operands
        return f'{ops[0].get_name()} = {ops[2]} {ops[1].value} {ops[3]}'


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

    def __repr__(self):
        ops = self.operands
        return f'{ops[0].get_name()} = ({ops[1].get_name()}) {ops[2]}'


class IRClass(IRInstruction):
    def __init__(self, class_: Class, line: int = -1,
                 column: int = -1, filename: str = None):
        operands = [
            class_
        ]
        super().__init__(IROpCode.CLASS, operands, line, column, filename)

    def __repr__(self):
        class_ = self.operands[0]
        return f'class {class_.get_name()}'


class IRNewObj(IRInstruction):
    def __init__(self, result: Variable, class_: Class,
                 line: int = -1, column: int = -1,
                 filename: str = None):
        operands = [
            result,
            class_
        ]
        super().__init__(IROpCode.NEW_OBJ, operands, line, column, filename)

    def __repr__(self):
        return f'{self.operands[0].get_name()}=new {self.operands[1].get_name()}()'


class IRGetProperty(IRInstruction):
    def __init__(self, result: Variable, obj: Variable | Constant, property_name: str, line: int = -1,
                 column: int = -1,
                 filename: str = None):
        operands = [
            result,
            obj,
            property_name
        ]
        super().__init__(IROpCode.GET_PROPERTY, operands, line, column, filename)

    def __repr__(self):
        return f'{self.operands[0].get_name()}={self.operands[1].get_name()}.{self.operands[2]}'


class IRSetProperty(IRInstruction):
    def __init__(
            self,
            obj: Variable | Constant,
            property_name: str,
            value: Reference[Variable | Constant | Literal],
            line: int = -1,
            column: int = -1,
            filename: str = None
    ):
        operands = [
            obj,
            property_name,
            value
        ]
        super().__init__(IROpCode.SET_PROPERTY, operands, line, column, filename)

    def __repr__(self):
        return f'{self.operands[0]}.{self.operands[1]} = {self.operands[2]}'


class IRCallMethod(IRInstruction):
    def __init__(
            self,
            result: Variable | None,
            class_: Class,
            method: Function,
            args: dict[str, Reference] = None,
            line: int = -1,
            column: int = -1,
            filename: str = None
    ):
        operands = [
            result,
            class_,
            method,
            args
        ]
        super().__init__(IROpCode.CALL_METHOD, operands, line, column, filename)

    def __repr__(self):
        ops = self.operands
        args = (f"{name}={repr(value)}" for name, value in ops[3].items())
        if ops[0]:
            return f"{ops[0].get_name()} = {ops[1].get_name()}.{ops[2].get_name()}({','.join(args)})"
        return f"{ops[1].get_name()}.{ops[2].get_name()}({','.join(args)})"
