# coding=utf-8
"""
IR 指令系统

核心原则：
1. 所有指令使用统一的 IRInstruction 类
2. 通过 opcode 区分指令类型
3. 使用工厂函数提供类型提示和自动补全
4. 可选的运行时验证（通过装饰器控制）
"""
import functools
from typing import Any, Optional, Union, get_type_hints, Callable

from dovetail.core.config import ENABLE_FUTURE_INSTRUCTION_VALIDATION, FAST_MODE
from dovetail.core.enums import DataType, StructureType, BinaryOps, CompareOps, UnaryOps
from dovetail.core.enums.types import Array
from dovetail.core.symbols import Variable, Literal, Reference, Function, Class
from dovetail.core.symbols.enumeration import Enumeration
from dovetail.core.symbols.structure import Structure
from dovetail.utils.safe_enum import SafeEnum

_DefinableDataTypes = Union[
    DataType,
    Structure,
    Class,
    Array,
    Enumeration
]

_CastableDataTypes = Union[
    DataType,
    Class,
]


# ==================== 操作码定义 ====================

class InstCategory(SafeEnum):
    CONTROL_FLOW = "控制流"
    DATA_OP = "数据运算"
    OOP = "面向对象"
    OWNERSHIP = "所有权"
    ARRAY = "数组操作"
    SPECIAL = "特殊指令"


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

    # DATA_OP (0x20-0x3F)
    DECLARE = (0x20, "变量声明", InstCategory.DATA_OP)
    ASSIGN = (0x21, "赋值", InstCategory.DATA_OP)
    UNARY_OP = (0x22, "一元运算", InstCategory.DATA_OP)
    BINARY_OP = (0x23, "二元运算", InstCategory.DATA_OP)
    COMPARE = (0x24, "比较", InstCategory.DATA_OP)
    CAST = (0x25, "类型转换", InstCategory.DATA_OP)
    FREE = (0x26, "释放变量", InstCategory.DATA_OP)

    # OOP (0x40-0x5F)
    CLASS = (0x40, "类定义", InstCategory.OOP)
    NEW_OBJ = (0x41, "新建对象", InstCategory.OOP)
    GET_PROPERTY = (0x42, "获取属性", InstCategory.OOP)
    SET_PROPERTY = (0x43, "设置属性", InstCategory.OOP)
    CALL_METHOD = (0x44, "调用方法", InstCategory.OOP)
    FREE_OBJ = (0xA0, "释放对象", InstCategory.OOP)

    # OWNERSHIP (0x60-0x7F)
    MOVE = (0x60, "所有权转移", InstCategory.OWNERSHIP)
    BORROW = (0x61, "借用", InstCategory.OWNERSHIP)

    # ARRAY_OPS (0x80-0x9F)
    ARRAY_NEW = (0x80, "数组创建", InstCategory.ARRAY)
    ARRAY_LOAD = (0x81, "数组读取", InstCategory.ARRAY)
    ARRAY_STORE = (0x82, "数组写入", InstCategory.ARRAY)
    ARRAY_FREE = (0x83, "数组释放", InstCategory.ARRAY)

    def __init__(self, code: int, desc: str, category: InstCategory):
        self.code = code
        self.desc = desc
        self.category = category

    @classmethod
    def find(cls, code: int):
        return next(cls(val) for name, val in zip(cls.names(), cls.values()) if val[0] == code)

    def __hash__(self):
        return hash(self.value)


# ==================== 验证系统 ====================


class ValidationError(Exception):
    """IR 指令验证错误"""
    pass


def validate_instruction(func):
    """
    指令验证装饰器

    根据函数签名的类型注解自动验证参数
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if FAST_MODE or not ENABLE_FUTURE_INSTRUCTION_VALIDATION:
            return func(*args, **kwargs)

        # 获取函数签名的类型注解
        type_hints = get_type_hints(func)
        sig = func.__annotations__

        # 验证参数
        for i, (param_name, arg) in enumerate(zip(sig.keys(), args)):
            expected_type = type_hints.get(param_name)

            # 检查参数类型
            if expected_type is None:
                continue  # 如果没有类型注解，跳过

            # 处理 Optional 类型
            if getattr(expected_type, '__origin__', None) is Union:
                if arg is None:
                    continue  # 允许 None 值
                expected_types = expected_type.__args__
                if not any(isinstance(arg, t) for t in expected_types):
                    raise ValidationError(
                        f"{func.__name__}: 参数 '{param_name}' 期望类型 {expected_type}，"
                        f"实际得到 {type(arg)}"
                    )
            elif hasattr(expected_type, '__origin__'):
                # 处理其他泛型类型（如 List, Dict 等）
                if not isinstance(arg, expected_type.__origin__):
                    raise ValidationError(
                        f"{func.__name__}: 参数 '{param_name}' 期望类型 {expected_type}，"
                        f"实际得到 {type(arg)}"
                    )
            else:
                # 普通类型检查
                if not isinstance(arg, expected_type):  # NOQA
                    raise ValidationError(
                        f"{func.__name__}: 参数 '{param_name}' 期望类型 {expected_type}，"
                        f"实际得到 {type(arg)}"
                    )

        return func(*args, **kwargs)

    return wrapper


# ==================== 统一指令类 ====================

class IRInstruction:
    """
    统一的 IR 指令类

    所有指令都使用这个类，通过 opcode 区分类型
    """

    __slots__ = ('opcode', 'operands', '_hash_cache')

    def __init__(
            self,
            opcode: IROpCode,
            *operands: Any,
            **named_operands: Any
    ):
        """
        创建 IR 指令

        Args:
            opcode: 操作码
            operands: 位置操作数
            named_operands: 命名操作数（可选，用于复杂指令）
        """
        self.opcode = opcode

        # 合并位置参数和命名参数
        if named_operands:
            self.operands = list(operands) + [named_operands]
        else:
            self.operands = list(operands)

        self._hash_cache = None

    def __repr__(self) -> str:
        """
        默认的字符串表示

        可以通过注册自定义 repr 函数来覆盖
        """
        # 查找是否有注册的自定义 repr
        if self.opcode in _repr_registry:
            return _repr_registry[self.opcode](self)

        # 默认格式
        operands_str = ", ".join(str(op) for op in self.operands)
        return f"{self.opcode.name}({operands_str})"

    def __hash__(self):
        if self._hash_cache is None:
            operand_hashes = []
            for op in self.operands:
                if isinstance(op, (list, tuple)):
                    operand_hashes.append(tuple(self._flatten_nested(op)))
                elif isinstance(op, dict):
                    operand_hashes.append(
                        tuple(sorted((k, self._flatten_nested(v)) for k, v in op.items()))
                    )
                elif hasattr(op, '__hash__') and callable(op.__hash__):
                    try:
                        operand_hashes.append(hash(op))
                    except TypeError:
                        operand_hashes.append(id(op))
                else:
                    operand_hashes.append(id(op))

            self._hash_cache = hash((self.opcode, tuple(operand_hashes)))

        return self._hash_cache

    def __eq__(self, other):
        if not isinstance(other, IRInstruction):
            return False
        return hash(self) == hash(other)

    def _flatten_nested(self, obj) -> tuple | int:
        """递归处理嵌套结构"""
        if isinstance(obj, (list, tuple)):
            return tuple(self._flatten_nested(item) for item in obj)
        elif isinstance(obj, dict):
            return tuple(sorted((k, self._flatten_nested(v)) for k, v in obj.items()))
        elif hasattr(obj, '__hash__') and callable(obj.__hash__):
            try:
                return hash(obj)
            except TypeError:
                return id(obj)
        return id(obj)

    def get_operands(self) -> list:
        """获取操作数列表"""
        return self.operands

    def get_opcode(self) -> IROpCode:
        """获取操作码"""
        return self.opcode


# ==================== Repr 注册系统 ====================

_repr_registry: dict[IROpCode, Callable] = {}


def register_repr(opcode: IROpCode):
    """
    注册自定义 repr 函数的装饰器

    Args:
        opcode: 要注册的操作码

    Returns:
        装饰器函数
    """

    def decorator(func):
        _repr_registry[opcode] = func
        return func

    return decorator


# ==================== 控制流指令 ====================

@validate_instruction
def IRJump(scope: str) -> IRInstruction:
    """
    跳转指令

    Args:
        scope: 目标作用域名称

    Returns:
        跳转指令
    """
    return IRInstruction(IROpCode.JUMP, scope)


@register_repr(IROpCode.JUMP)
def _jump_repr(instr: IRInstruction) -> str:
    return f"goto {instr.operands[0]}"


@validate_instruction
def IRCondJump(
        condition: Variable | Literal,
        true_scope: Optional[str] = None,
        false_scope: Optional[str] = None
) -> IRInstruction:
    """
    条件跳转指令

    Args:
        condition: 条件变量或字面量（必须是布尔类型）
        true_scope: 条件为真时的目标作用域
        false_scope: 条件为假时的目标作用域

    Returns:
        条件跳转指令

    Raises:
        ValidationError: 如果条件不是布尔类型
    """
    # 类型验证
    if not FAST_MODE and ENABLE_FUTURE_INSTRUCTION_VALIDATION:
        if not DataType.BOOLEAN.is_subclass_of(condition.dtype):
            raise ValidationError(
                f"条件跳转要求布尔类型，实际得到 {condition.dtype}"
            )

    return IRInstruction(IROpCode.COND_JUMP, condition, true_scope, false_scope)


@register_repr(IROpCode.COND_JUMP)
def _cond_jump_repr(instr: IRInstruction) -> str:
    cond = (instr.operands[0].value
            if isinstance(instr.operands[0], Literal)
            else instr.operands[0].get_name())
    true_label = instr.operands[1]
    false_label = instr.operands[2]

    if false_label:
        return f"if {cond} goto {true_label} else goto {false_label}"
    else:
        return f"if {cond} goto {true_label}"


@validate_instruction
def IRFunction(function: Function) -> IRInstruction:
    """
    函数定义指令

    Args:
        function: 函数符号对象

    Returns:
        函数定义指令
    """
    return IRInstruction(IROpCode.FUNCTION, function)


@register_repr(IROpCode.FUNCTION)
def _function_repr(instr: IRInstruction) -> str:
    func: Function = instr.operands[0]
    params_str = ", ".join(
        f"{p.var.dtype.get_name()} {p.var.get_name()}"
        for p in func.params
    )
    return f"function {func.return_type.get_name()} {func.get_name()}({params_str})"


@validate_instruction
def IRCall(
        result: Optional[Variable],
        function: Function,
        arguments: dict[str, Reference]
) -> IRInstruction:
    """
    函数调用指令

    Args:
        result: 返回值存储变量（如果函数返回 void 则为 None）
        function: 被调用的函数对象
        arguments: 参数字典，键为参数名，值为 Reference 对象

    Returns:
        函数调用指令
    """
    return IRInstruction(IROpCode.CALL, result, function, arguments)


@register_repr(IROpCode.CALL)
def _call_repr(instr: IRInstruction) -> str:
    result = instr.operands[0]
    func: Function = instr.operands[1]
    args: dict[str, Reference] = instr.operands[2]

    args_str = ", ".join(f"{name}={val}" for name, val in args.items())

    if result:
        return f"{result.get_name()} = {func.get_name()}({args_str})"
    else:
        return f"{func.get_name()}({args_str})"


@validate_instruction
def IRReturn(value: Optional[Reference] = None) -> IRInstruction:
    """
    返回指令

    Args:
        value: 返回值（可选，void 函数为 None）

    Returns:
        返回指令
    """
    return IRInstruction(IROpCode.RETURN, value)


@register_repr(IROpCode.RETURN)
def _return_repr(instr: IRInstruction) -> str:
    if instr.operands[0] is None:
        return "return"

    value = instr.operands[0]

    return f"return {value}"


@validate_instruction
def IRScopeBegin(name: str, scope_type: StructureType) -> IRInstruction:
    """
    作用域开始指令

    Args:
        name: 作用域名称
        scope_type: 作用域类型（来自 StructureType 枚举）

    Returns:
        作用域开始指令
    """
    return IRInstruction(IROpCode.SCOPE_BEGIN, name, scope_type)


@register_repr(IROpCode.SCOPE_BEGIN)
def _scope_begin_repr(instr: IRInstruction) -> str:
    return f"scope {instr.operands[0]} ({instr.operands[1].name}) {{"


@validate_instruction
def IRScopeEnd(name: str, scope_type: StructureType) -> IRInstruction:
    """
    作用域结束指令

    Args:
        name: 作用域名称
        scope_type: 作用域类型（来自 StructureType 枚举）

    Returns:
        作用域结束指令
    """
    return IRInstruction(IROpCode.SCOPE_END, name, scope_type)


@register_repr(IROpCode.SCOPE_END)
def _scope_end_repr(instr: IRInstruction) -> str:
    return f"}} // end scope {instr.operands[0]}"


@validate_instruction
def IRBreak(scope: str) -> IRInstruction:
    """
    中断指令（跳出循环）

    Args:
        scope: 目标循环作用域名称

    Returns:
        中断指令
    """
    return IRInstruction(IROpCode.BREAK, scope)


@register_repr(IROpCode.BREAK)
def _break_repr(instr: IRInstruction) -> str:
    return f"break to {instr.operands[0]}"


@validate_instruction
def IRContinue(scope: str) -> IRInstruction:
    """
    继续指令（跳到循环开始）

    Args:
        scope: 目标循环作用域名称

    Returns:
        继续指令
    """
    return IRInstruction(IROpCode.CONTINUE, scope)


@register_repr(IROpCode.CONTINUE)
def _continue_repr(instr: IRInstruction) -> str:
    return f"continue to {instr.operands[0]}"


# ==================== 数据操作指令 ====================

@validate_instruction
def IRDeclare(variable: Variable) -> IRInstruction:
    """
    变量声明指令

    Args:
        variable: 要声明的变量对象

    Returns:
        声明指令
    """
    return IRInstruction(IROpCode.DECLARE, variable)


@register_repr(IROpCode.DECLARE)
def _declare_repr(instr: IRInstruction) -> str:
    var: Variable = instr.operands[0]
    return f"declare {var.dtype.get_name()} {var.get_name()}"


@validate_instruction
def IRAssign(
        target: Variable,
        source: Union[Reference, Variable, Literal]
) -> IRInstruction:
    """
    赋值指令

    Args:
        target: 目标变量
        source: 赋值来源（可以是 Reference、Variable 或 Literal）

    Returns:
        赋值指令
    """
    return IRInstruction(IROpCode.ASSIGN, target, source)


@register_repr(IROpCode.ASSIGN)
def _assign_repr(instr: IRInstruction) -> str:
    target: Variable = instr.operands[0]
    source = instr.operands[1]

    return f"{target.get_name()} = {source}"


@validate_instruction
def IRUnaryOp(
        result: Variable,
        op: UnaryOps,
        operand: Reference
) -> IRInstruction:
    """
    一元运算指令

    Args:
        result: 结果变量
        op: 一元运算符（来自 UnaryOps 枚举，如 NOT、NEG）
        operand: 操作数

    Returns:
        一元运算指令
    """
    return IRInstruction(IROpCode.UNARY_OP, result, op, operand)


@register_repr(IROpCode.UNARY_OP)
def _unary_op_repr(instr: IRInstruction) -> str:
    result: Variable = instr.operands[0]
    op: UnaryOps = instr.operands[1]
    operand: Reference = instr.operands[2]

    return f"{result.get_name()} = {op.value}{operand}"


@validate_instruction
def IRBinaryOp(
        result: Variable,
        op: BinaryOps,
        left: Reference,
        right: Reference
) -> IRInstruction:
    """
    二元运算指令

    Args:
        result: 结果变量
        op: 二元运算符（来自 BinaryOps 枚举，如 ADD、SUB、MUL、DIV、MOD）
        left: 左操作数
        right: 右操作数

    Returns:
        二元运算指令
    """
    return IRInstruction(IROpCode.BINARY_OP, result, op, left, right)


@register_repr(IROpCode.BINARY_OP)
def _binary_op_repr(instr: IRInstruction) -> str:
    result: Variable = instr.operands[0]
    op: BinaryOps = instr.operands[1]
    left: Reference = instr.operands[2]
    right: Reference = instr.operands[3]

    return f"{result.get_name()} = {left} {op.value} {right}"


@validate_instruction
def IRCompare(
        result: Variable,
        op: CompareOps,
        left: Reference,
        right: Reference
) -> IRInstruction:
    """
    比较指令

    Args:
        result: 结果变量（必须是布尔类型）
        op: 比较运算符（来自 CompareOps 枚举，如 EQ、NE、LT、GT、LE、GE）
        left: 左操作数
        right: 右操作数

    Returns:
        比较指令

    Raises:
        ValidationError: 如果结果变量不是布尔类型
    """
    if not FAST_MODE and ENABLE_FUTURE_INSTRUCTION_VALIDATION and result.dtype != DataType.BOOLEAN:
        raise ValidationError(f"比较结果必须是布尔类型，实际得到 {result.dtype}")

    return IRInstruction(IROpCode.COMPARE, result, op, left, right)


@register_repr(IROpCode.COMPARE)
def _compare_repr(instr: IRInstruction) -> str:
    result: Variable = instr.operands[0]
    op: CompareOps = instr.operands[1]
    left: Reference = instr.operands[2]
    right: Reference = instr.operands[3]

    return f"{result.get_name()} = {left} {op.value} {right}"


@validate_instruction
def IRCast(
        result: Variable,
        target_type: _CastableDataTypes,
        source: Reference
) -> IRInstruction:
    """
    类型转换指令

    Args:
        result: 结果变量
        source: 源值
        target_type: 目标类型（DataType 或其他类型对象）

    Returns:
        类型转换指令
    """
    return IRInstruction(IROpCode.CAST, result, target_type, source)


@register_repr(IROpCode.CAST)
def _cast_repr(instr: IRInstruction) -> str:
    result: Variable = instr.operands[0]
    target_type = instr.operands[1]
    source: Reference = instr.operands[2]

    return f"{result.get_name()} = cast<{target_type}>({source})"


@validate_instruction
def IRFree(variable: Variable) -> IRInstruction:
    """
    释放变量指令

    Args:
        variable: 要释放的变量

    Returns:
        释放指令
    """
    return IRInstruction(IROpCode.FREE, variable)


@register_repr(IROpCode.FREE)
def _free_repr(instr: IRInstruction) -> str:
    var: Variable = instr.operands[0]
    return f"free {var.get_name()}"


# ==================== 面向对象指令 ====================

@validate_instruction
def IRClass(class_symbol: Class) -> IRInstruction:
    """
    类定义指令

    Args:
        class_symbol: 类符号对象

    Returns:
        类定义指令
    """
    return IRInstruction(IROpCode.CLASS, class_symbol)


@register_repr(IROpCode.CLASS)
def _class_repr(instr: IRInstruction) -> str:
    cls: Class = instr.operands[0]
    return f"class {cls.get_name()}"


@validate_instruction
def IRNewObj(
        result: Variable,
        class_type: Class,
        arguments: dict[str, Reference]
) -> IRInstruction:
    """
    新建对象指令

    Args:
        result: 结果变量（存储对象引用）
        class_type: 类类型对象
        arguments: 构造函数参数字典，键为参数名，值为 Reference 对象

    Returns:
        新建对象指令
    """
    return IRInstruction(IROpCode.NEW_OBJ, result, class_type, arguments)


@register_repr(IROpCode.NEW_OBJ)
def _new_obj_repr(instr: IRInstruction) -> str:
    result: Variable = instr.operands[0]
    class_type: Class = instr.operands[1]
    args: dict = instr.operands[2]

    args_str = ", ".join(f"{name}={val}" for name, val in args.items())

    return f"{result.get_name()} = new {class_type.get_name()}({args_str})"


@validate_instruction
def IRGetProperty(
        result: Variable,
        object_ref: Reference,
        property_name: str
) -> IRInstruction:
    """
    获取属性指令

    Args:
        result: 结果变量（存储属性值）
        object_ref: 对象引用
        property_name: 属性名称

    Returns:
        获取属性指令
    """
    return IRInstruction(IROpCode.GET_PROPERTY, result, object_ref, property_name)


@register_repr(IROpCode.GET_PROPERTY)
def _get_property_repr(instr: IRInstruction) -> str:
    result: Variable = instr.operands[0]
    obj_ref: Reference = instr.operands[1]
    prop_name: str = instr.operands[2]

    return f"{result.get_name()} = {obj_ref}.{prop_name}"


@validate_instruction
def IRSetProperty(
        object_ref: Reference,
        property_name: str,
        value: Reference
) -> IRInstruction:
    """
    设置属性指令

    Args:
        object_ref: 对象引用
        property_name: 属性名称
        value: 新值

    Returns:
        设置属性指令
    """
    return IRInstruction(IROpCode.SET_PROPERTY, object_ref, property_name, value)


@register_repr(IROpCode.SET_PROPERTY)
def _set_property_repr(instr: IRInstruction) -> str:
    obj_ref: Reference = instr.operands[0]
    prop_name: str = instr.operands[1]
    value: Reference = instr.operands[2]

    return f"{obj_ref}.{prop_name} = {value}"


@validate_instruction
def IRCallMethod(
        result: Optional[Variable],
        object_ref: Reference,
        method_name: str,
        arguments: dict[str, Reference]
) -> IRInstruction:
    """
    调用方法指令

    Args:
        result: 返回值存储变量（void 方法为 None）
        object_ref: 对象引用
        method_name: 方法名称
        arguments: 方法参数字典，键为参数名，值为 Reference 对象

    Returns:
        调用方法指令
    """
    return IRInstruction(IROpCode.CALL_METHOD, result, object_ref, method_name, arguments)


@register_repr(IROpCode.CALL_METHOD)
def _call_method_repr(instr: IRInstruction) -> str:
    result: Optional[Variable] = instr.operands[0]
    obj_ref: Reference = instr.operands[1]
    method_name: str = instr.operands[2]
    args: dict = instr.operands[3]

    args_str = ", ".join(f"{name}={val}" for name, val in args.items())

    call_str = f"{obj_ref}.{method_name}({args_str})"

    if result:
        return f"{result} = {call_str}"
    else:
        return call_str


@validate_instruction
def IRFreeObj(object_ref: Reference) -> IRInstruction:
    """
    释放对象指令

    Args:
        object_ref: 要释放的对象引用

    Returns:
        释放对象指令
    """
    return IRInstruction(IROpCode.FREE_OBJ, object_ref)


@register_repr(IROpCode.FREE_OBJ)
def _free_obj_repr(instr: IRInstruction) -> str:
    obj_ref: Reference = instr.operands[0]
    return f"free {obj_ref}"


# ==================== 所有权管理指令 ====================

@validate_instruction
def IRMove(
        target: Variable,
        source: Reference
) -> IRInstruction:
    """
    所有权转移指令

    Args:
        target: 目标变量（接收所有权）
        source: 源引用（转移所有权）

    Returns:
        所有权转移指令
    """
    return IRInstruction(IROpCode.MOVE, target, source)


@register_repr(IROpCode.MOVE)
def _move_repr(instr: IRInstruction) -> str:
    target: Variable = instr.operands[0]
    source: Reference = instr.operands[1]

    return f"{target} = move({source})"


@validate_instruction
def IRBorrow(
        target: Variable,
        source: Reference,
        mutable: bool = False
) -> IRInstruction:
    """
    借用指令

    Args:
        target: 目标变量（借用引用）
        source: 源引用（被借用对象）
        mutable: 是否可变借用

    Returns:
        借用指令
    """
    return IRInstruction(IROpCode.BORROW, target, source, mutable)


@register_repr(IROpCode.BORROW)
def _borrow_repr(instr: IRInstruction) -> str:
    target: Variable = instr.operands[0]
    source: Reference = instr.operands[1]
    mutable: bool = instr.operands[2]

    borrow_type = "borrow_mut" if mutable else "borrow"

    return f"{target.get_name()} = {borrow_type}({source})"


# ==================== 数组操作指令 ====================

@validate_instruction
def IRArrayNew(
        result: Variable,
        element_type: Any,
        size: Union[Reference, int]
) -> IRInstruction:
    """
    数组创建指令

    Args:
        result: 结果变量（存储数组引用）
        element_type: 元素类型（DataType 或其他类型对象）
        size: 数组大小（可以是整数常量或 Reference 对象）

    Returns:
        数组创建指令
    """
    return IRInstruction(IROpCode.ARRAY_NEW, result, element_type, size)


@register_repr(IROpCode.ARRAY_NEW)
def _array_new_repr(instr: IRInstruction) -> str:
    result: Variable = instr.operands[0]
    elem_type = instr.operands[1]
    size = instr.operands[2]

    return f"{result.get_name()} = new {elem_type}[{size}]"


@validate_instruction
def IRArrayLoad(
        result: Variable,
        array_ref: Reference,
        index: Union[Reference, int]
) -> IRInstruction:
    """
    数组读取指令

    Args:
        result: 结果变量（存储读取的值）
        array_ref: 数组引用
        index: 索引（可以是整数常量或 Reference 对象）

    Returns:
        数组读取指令
    """
    return IRInstruction(IROpCode.ARRAY_LOAD, result, array_ref, index)


@register_repr(IROpCode.ARRAY_LOAD)
def _array_load_repr(instr: IRInstruction) -> str:
    result: Variable = instr.operands[0]
    array_ref: Reference = instr.operands[1]
    index = instr.operands[2]

    return f"{result.get_name()} = {array_ref}[{index}]"


@validate_instruction
def IRArrayStore(
        array_ref: Reference,
        index: Union[Reference, int],
        value: Reference
) -> IRInstruction:
    """
    数组写入指令

    Args:
        array_ref: 数组引用
        index: 索引（可以是整数常量或 Reference 对象）
        value: 要写入的值

    Returns:
        数组写入指令
    """
    return IRInstruction(IROpCode.ARRAY_STORE, array_ref, index, value)


@register_repr(IROpCode.ARRAY_STORE)
def _array_store_repr(instr: IRInstruction) -> str:
    array_ref: Reference = instr.operands[0]
    index = instr.operands[1]
    value: Reference = instr.operands[2]

    return f"{array_ref}[{index}] = {value}"


@validate_instruction
def IRArrayFree(array_ref: Reference) -> IRInstruction:
    """
    数组释放指令

    Args:
        array_ref: 要释放的数组引用

    Returns:
        数组释放指令
    """
    return IRInstruction(IROpCode.ARRAY_FREE, array_ref)


@register_repr(IROpCode.ARRAY_FREE)
def _array_free_repr(instr: IRInstruction) -> str:
    array_ref: Reference = instr.operands[0]
    return f"free {array_ref}"
