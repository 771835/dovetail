# coding=utf-8
from abc import ABC, abstractmethod
from typing import TypeVar, Any

from dovetail.core.enums.operations import UnaryOps, BinaryOps, CompareOps
from dovetail.core.enums.types import DataType, StructureType
from dovetail.core.symbols import Literal, Class, Function, Reference, Variable, Symbol
from dovetail.utils.safe_enum import SafeEnum

T = TypeVar('T', bound="IRInstruction")


class InstCategory(SafeEnum):
    CONTROL_FLOW = "控制流"
    DATA_OP = "数据运算"
    OOP = "面向对象"
    OWNERSHIP = "所有权"
    ARRAY = "数组操作"
    SPECIAL = "特殊指令"


class IROpCode(SafeEnum):
    # CONTROL_FLOW (0x00-0x1F) - 控制流
    JUMP = (0x00, "跳转", InstCategory.CONTROL_FLOW)
    COND_JUMP = (0x01, "条件跳转", InstCategory.CONTROL_FLOW)
    FUNCTION = (0x02, "函数定义", InstCategory.CONTROL_FLOW)
    CALL = (0x03, "函数调用", InstCategory.CONTROL_FLOW)
    RETURN = (0x04, "返回", InstCategory.CONTROL_FLOW)
    SCOPE_BEGIN = (0x05, "作用域开始", InstCategory.CONTROL_FLOW)
    SCOPE_END = (0x06, "作用域结束", InstCategory.CONTROL_FLOW)
    BREAK = (0x07, "中断", InstCategory.CONTROL_FLOW)
    CONTINUE = (0x08, "继续", InstCategory.CONTROL_FLOW)

    # DATA_OP (0x20-0x3F) - 数据运算
    DECLARE = (0x20, "变量声明", InstCategory.DATA_OP)
    ASSIGN = (0x21, "赋值", InstCategory.DATA_OP)
    UNARY_OP = (0x22, "一元运算", InstCategory.DATA_OP)
    BINARY_OP = (0x23, "二元运算", InstCategory.DATA_OP)
    COMPARE = (0x24, "比较", InstCategory.DATA_OP)
    CAST = (0x25, "类型转换", InstCategory.DATA_OP)
    FREE = (0x26, "释放变量", InstCategory.DATA_OP)

    # OOP (0x40-0x5F) - 面对对象
    CLASS = (0x40, "类定义", InstCategory.OOP)
    NEW_OBJ = (0x41, "新建对象", InstCategory.OOP)
    GET_PROPERTY = (0x42, "获取属性", InstCategory.OOP)
    SET_PROPERTY = (0x43, "设置属性", InstCategory.OOP)
    CALL_METHOD = (0x44, "调用方法", InstCategory.OOP)
    FREE_OBJ = (0xA0, "释放对象", InstCategory.OOP)

    # OWNERSHIP (0x60-0x7F) - 所有权管理
    MOVE = (0x60, "所有权转移", InstCategory.OWNERSHIP)
    BORROW = (0x61, "借用", InstCategory.OWNERSHIP)

    # ARRAY_OPS (0x80-0x9F) - 数组操作
    ARRAY_NEW = (0x80, "数组创建", InstCategory.ARRAY)
    ARRAY_LOAD = (0x81, "数组读取", InstCategory.ARRAY)
    ARRAY_STORE = (0x82, "数组写入", InstCategory.ARRAY)
    ARRAY_FREE = (0x83, "", InstCategory.ARRAY)

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
    """

    def __init__(
            self,
            opcode: IROpCode,
            operands: list[Reference | str | Symbol | SafeEnum | Any]
    ):
        self.opcode = opcode
        self.operands = operands

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

    def get_opcode(self):
        return self.opcode


# 具体指令实现
class IRJump(IRInstruction):
    def __init__(
            self,
            scope: str
    ):
        operands = [
            scope
        ]
        super().__init__(IROpCode.JUMP, operands)

    def __repr__(self):
        return f"goto {self.operands[0]}"


class IRCondJump(IRInstruction):
    def __init__(
            self,
            condition: Variable | Literal,
            true_scope: str | None,
            false_scope: str | None = None
    ):
        assert DataType.BOOLEAN.is_subclass_of(condition.dtype),condition.dtype

        operands = [
            condition,
            true_scope,
            false_scope
        ]
        super().__init__(IROpCode.COND_JUMP, operands)

    def __repr__(self):
        cond = self.operands[0].value if isinstance(self.operands[0], Literal) else self.operands[0].get_name()
        true_label = self.operands[1]
        false_label = self.operands[2]
        return f"if {cond} goto {true_label} else goto {false_label}"


class IRFunction(IRInstruction):
    def __init__(self, function: Function):
        operands = [
            function
        ]
        super().__init__(IROpCode.FUNCTION, operands)

    def __repr__(self):
        function: Function = self.operands[0]
        annotations: list[str] = []
        for annotation, args in function.annotations.items():
            annotations.append(f"@{annotation.name}({','.join(f'{name}={val}' for name, val in args.items())})")

        return '\n'.join(annotations) + f"\nfunc {self.operands[0]}"


class IRReturn(IRInstruction):
    def __init__(
            self,
            value: Reference[Variable | Literal] | None = None
    ):
        operands = [
            value,
        ]
        super().__init__(IROpCode.RETURN, operands)

    def __repr__(self):
        return f"return {self.operands[0].get_display_value()}"


class IRCall(IRInstruction):
    def __init__(
            self,
            result: Variable | None,
            func: Function,
            args: dict[str, Reference[Variable | Literal]] = None
    ):
        if args is None:
            args = []
        operands = [
            result,
            func,
            args
        ]
        super().__init__(IROpCode.CALL, operands)

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
            stype: StructureType
    ):
        operands = [
            name,
            stype
        ]
        super().__init__(IROpCode.SCOPE_BEGIN, operands)

    def __repr__(self):
        return f'{self.operands[0]}:{self.operands[1].value}{{'


class IRScopeEnd(IRInstruction):
    def __init__(
            self,
            name: str,
            stype: StructureType
    ):
        operands = [
            name,
            stype
        ]
        super().__init__(IROpCode.SCOPE_END, operands)

    def __repr__(self):
        return '}'


class IRBreak(IRInstruction):
    def __init__(self, scope_name: str):
        operands = [
            scope_name
        ]
        super().__init__(IROpCode.BREAK, operands)

    def __repr__(self):
        return f'break {self.operands[0]}'


class IRContinue(IRInstruction):
    def __init__(self, scope_name: str):
        operands = [
            scope_name
        ]
        super().__init__(IROpCode.CONTINUE, operands)

    def __repr__(self):
        return f'continue {self.operands[0]}'


class IRDeclare(IRInstruction):
    def __init__(self, var: Variable):
        operands = [
            var
        ]
        super().__init__(IROpCode.DECLARE, operands)

    def __repr__(self):
        var = self.operands[0]
        return f'{var.dtype.value if isinstance(var.dtype, DataType) else var.dtype.get_name()} {var.get_name()}'


class IRAssign(IRInstruction):
    def __init__(self, target: Variable, source: Reference):
        operands = [
            target,
            source
        ]
        super().__init__(IROpCode.ASSIGN, operands)

    def __repr__(self):
        return f'{self.operands[0].get_name()} = {self.operands[1]}'


class IRUnaryOp(IRInstruction):
    def __init__(self, result: Variable, op: UnaryOps, operand: Reference[Variable | Literal]):
        operands = [
            result,
            op,
            operand
        ]
        super().__init__(IROpCode.UNARY_OP, operands)

    def __repr__(self):
        return f'{self.operands[0].get_name()}={self.operands[1].value}{self.operands[2]}'


class IRBinaryOp(IRInstruction):
    def __init__(self, result: Variable, op: BinaryOps, left: Reference[Variable | Literal],
                 right: Reference[Variable | Literal]):
        operands = [
            result,
            op,
            left,
            right
        ]
        super().__init__(IROpCode.BINARY_OP, operands)

    def __repr__(self):
        ops = self.operands
        return f'{ops[0].get_name()} = {ops[2]} {ops[1].value} {ops[3]}'


class IRCompare(IRInstruction):
    def __init__(self, result: Variable, op: CompareOps, left: Reference[Variable | Literal],
                 right: Reference[Variable | Literal]):
        operands = [
            result,
            op,
            left,
            right
        ]
        super().__init__(IROpCode.COMPARE, operands)

    def __repr__(self):
        ops = self.operands
        return f'{ops[0].get_name()} = {ops[2]} {ops[1].value} {ops[3]}'


class IRCast(IRInstruction):
    def __init__(self, result: Variable, dtype: DataType | Class,
                 value: Reference[Variable | Literal]):
        operands = [
            result,
            dtype,
            value
        ]
        super().__init__(IROpCode.CAST, operands)

    def __repr__(self):
        ops = self.operands
        return f'{ops[0].get_name()} = ({ops[1].get_name()}) {ops[2]}'


class IRClass(IRInstruction):
    def __init__(self, class_: Class):
        operands = [
            class_
        ]
        super().__init__(IROpCode.CLASS, operands)

    def __repr__(self):
        class_ = self.operands[0]
        return f'class {class_.get_name()}'


class IRNewObj(IRInstruction):
    def __init__(self, result: Variable, class_: Class):
        operands = [
            result,
            class_
        ]
        super().__init__(IROpCode.NEW_OBJ, operands)

    def __repr__(self):
        return f'{self.operands[0].get_name()}=new {self.operands[1].get_name()}()'


class IRGetProperty(IRInstruction):
    def __init__(self, result: Variable, obj: Variable, property_name: str):
        operands = [
            result,
            obj,
            property_name
        ]
        super().__init__(IROpCode.GET_PROPERTY, operands)

    def __repr__(self):
        return f'{self.operands[0].get_name()}={self.operands[1].get_name()}.{self.operands[2]}'


class IRSetProperty(IRInstruction):
    def __init__(
            self,
            obj: Variable,
            property_name: str,
            value: Reference[Variable | Literal]
    ):
        operands = [
            obj,
            property_name,
            value
        ]
        super().__init__(IROpCode.SET_PROPERTY, operands)

    def __repr__(self):
        return f'{self.operands[0]}.{self.operands[1]} = {self.operands[2]}'


class IRCallMethod(IRInstruction):
    def __init__(
            self,
            result: Variable | None,
            class_: Class,
            method: Function,
            args: dict[str, Reference] = None
    ):
        operands = [
            result,
            class_,
            method,
            args
        ]
        super().__init__(IROpCode.CALL_METHOD, operands)

    def __repr__(self):
        ops = self.operands
        args = (f"{name}={repr(value)}" for name, value in ops[3].items())
        if ops[0]:
            return f"{ops[0].get_name()} = {ops[1].get_name()}.{ops[2].get_name()}({','.join(args)})"
        return f"{ops[1].get_name()}.{ops[2].get_name()}({','.join(args)})"
