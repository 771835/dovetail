# coding=utf-8
from enum import Flag, auto
from typing import Callable, Any

from attrs import define, field

from dovetail.core.symbols import Reference, Variable
from dovetail.utils.constant_operator_handlers import BINARY_OP_HANDLERS, COMPARE_OP_HANDLERS, UNARY_OP_HANDLERS
from dovetail.utils.safe_enum import SafeEnum


class InstructionCategory(SafeEnum):
    CONTROL_FLOW = "控制流"
    DATA_OP = "数据运算"
    OOP = "面向对象"
    STRUCT = "结构体"
    OWNERSHIP = "所有权"
    SPECIAL = "特殊指令"


class InstructionFlag(Flag):
    """
    指令标识 用于标记某一种指令拥有的特性
    """
    NONE = 0 # 无任何属性
    SIDE_EFFECT = auto()  # 有副作用，不可消除/重排
    PURE_COMPUTE = auto()  # 纯计算，结果仅依赖操作数
    PRODUCES_RESULT = auto()  # 产生结果变量（operands[0]）
    TERMINATOR = auto()  # 终止控制流（return/break/continue）
    JUMP = auto()  # 跳转到其他作用域
    CALL = auto()  # 函数/方法调用

@define(frozen=True, eq=False)
class IROpDescriptor:
    """
    指令操作码描述符。

    比较和哈希的唯一依据是 code（0xXX）——金标准。
    其余字段均为语义属性，供 Pass 查询。
    """
    code: int  # 金标准
    desc: str  # 人类可读描述
    category: InstructionCategory  # 保留粗粒度分类（向后兼容）
    flags: InstructionFlag = InstructionFlag.NONE  # 语义标志位
    result_index: int = -1  # 结果变量在 operands 中的位置，-1 = 无
    use_indices: tuple[int, ...] = ()  # 被读取的操作数位置（常规指令）
    # 不规则指令的自定义提取器（CALL 的 args 是 dict，COND_JUMP 的目标是 scope 名）
    use_extractor: Callable | None = field(default=None, eq=False, hash=False)
    # 常量折叠专用 handler
    fold_handler: dict[Any, Callable] | None = field(default=None, eq=False, hash=False)

    # ---- 比较与哈希：仅看 code ----
    def __eq__(self, other: Any) -> bool:
        if isinstance(other, IROpDescriptor):
            return self.code == other.code
        if isinstance(other, int):
            return self.code == other
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self.code)

    # ---- 便捷属性 ----
    @property
    def has_side_effect(self) -> bool:
        return bool(self.flags & InstructionFlag.SIDE_EFFECT)

    @property
    def is_pure(self) -> bool:
        return bool(self.flags & InstructionFlag.PURE_COMPUTE)

    @property
    def produces_result(self) -> bool:
        return bool(self.flags & InstructionFlag.PRODUCES_RESULT)

    @property
    def is_terminator(self) -> bool:
        return bool(self.flags & InstructionFlag.TERMINATOR)

    @property
    def is_jump(self) -> bool:
        return bool(self.flags & InstructionFlag.JUMP)

    @property
    def is_call(self) -> bool:
        return bool(self.flags & InstructionFlag.CALL)

    def get_used_refs(self, operands: list) -> list[Reference]:
        """从 operands 中提取所有被读取的 Reference"""
        if self.use_extractor is not None:
            return self.use_extractor(operands)
        return [operands[i] for i in self.use_indices if i < len(operands)]

    def get_result_var(self, operands: list) -> Variable | None:
        """从 operands 中提取结果变量"""
        if self.result_index < 0 or self.result_index >= len(operands):
            return None
        return operands[self.result_index]


def _call_uses(operands) -> list:
    """CALL: (result, func, args_dict) → 提取 args 中所有 Reference"""
    _, _, args = operands
    return list(args.values()) if isinstance(args, dict) else []


def _call_method_uses(operands) -> list:
    """CALL_METHOD: (result, obj_ref, method, args_dict)"""
    _, obj_ref, _, args = operands
    refs = [obj_ref]
    if isinstance(args, dict):
        refs.extend(args.values())
    return refs


def _new_obj_uses(operands) -> list:
    """NEW_OBJ: (result, class_type, args_dict)"""
    _, _, args = operands
    return list(args.values()) if isinstance(args, dict) else []


def _struct_new_uses(operands) -> list:
    """STRUCT_NEW: (result, struct_type, args_dict)"""
    _, _, args = operands
    return list(args.values()) if isinstance(args, dict) else []


def _struct_call_uses(operands) -> list:
    """STRUCT_CALL: (result, struct_ref, method, args_dict)"""
    _, struct_ref, _, args = operands
    refs = [struct_ref]
    if isinstance(args, dict):
        refs.extend(args.values())
    return refs


class IROpCode:
    """指令操作码。每个成员是自描述的 IROpDescriptor，比较/哈希的金标准是 code属性。"""

    # ==================== CONTROL_FLOW (0x00-0x1F) ====================

    JUMP = IROpDescriptor(
        0x00, "跳转", InstructionCategory.CONTROL_FLOW,
        flags=InstructionFlag.JUMP,
    )

    COND_JUMP = IROpDescriptor(
        0x01, "条件跳转", InstructionCategory.CONTROL_FLOW,
        flags=InstructionFlag.JUMP,
        use_indices=(0,),  # operands[0] = condition: Reference
    )

    FUNCTION = IROpDescriptor(
        0x02, "函数定义", InstructionCategory.CONTROL_FLOW,
        flags=InstructionFlag.SIDE_EFFECT,
    )

    CALL = IROpDescriptor(
        0x03, "函数调用", InstructionCategory.CONTROL_FLOW,
        flags=InstructionFlag.SIDE_EFFECT | InstructionFlag.CALL | InstructionFlag.PRODUCES_RESULT,
        result_index=0,
        use_extractor=_call_uses,
    )

    RETURN = IROpDescriptor(
        0x04, "返回", InstructionCategory.CONTROL_FLOW,
        flags=InstructionFlag.SIDE_EFFECT | InstructionFlag.TERMINATOR,
        use_indices=(0,),  # operands[0] = return value: Reference | None
    )

    SCOPE_BEGIN = IROpDescriptor(
        0x05, "作用域开始", InstructionCategory.CONTROL_FLOW,
    )

    SCOPE_END = IROpDescriptor(
        0x06, "作用域结束", InstructionCategory.CONTROL_FLOW,
    )

    BREAK = IROpDescriptor(
        0x07, "中断", InstructionCategory.CONTROL_FLOW,
        flags=InstructionFlag.TERMINATOR,
    )

    CONTINUE = IROpDescriptor(
        0x08, "继续", InstructionCategory.CONTROL_FLOW,
        flags=InstructionFlag.TERMINATOR,
    )

    # ==================== DATA_OP (0x20-0x3F) ====================

    DECLARE = IROpDescriptor(
        0x20, "变量声明", InstructionCategory.DATA_OP,
    )

    ASSIGN = IROpDescriptor(
        0x21, "赋值", InstructionCategory.DATA_OP,
        flags=InstructionFlag.PRODUCES_RESULT,
        result_index=0,  # target: Variable
        use_indices=(1,),  # source: Reference
    )

    UNARY_OP = IROpDescriptor(
        0x22, "一元运算", InstructionCategory.DATA_OP,
        flags=InstructionFlag.PURE_COMPUTE | InstructionFlag.PRODUCES_RESULT,
        result_index=0,  # result: Variable
        use_indices=(2,),  # operand: Reference
        fold_handler=UNARY_OP_HANDLERS,
    )

    BINARY_OP = IROpDescriptor(
        0x23, "二元运算", InstructionCategory.DATA_OP,
        flags=InstructionFlag.PURE_COMPUTE | InstructionFlag.PRODUCES_RESULT,
        result_index=0,  # result: Variable
        use_indices=(2, 3),  # left, right: Reference
        fold_handler=BINARY_OP_HANDLERS,
    )

    COMPARE = IROpDescriptor(
        0x24, "比较", InstructionCategory.DATA_OP,
        flags=InstructionFlag.PURE_COMPUTE | InstructionFlag.PRODUCES_RESULT,
        result_index=0,  # result: Variable
        use_indices=(2, 3),  # left, right: Reference
        fold_handler=COMPARE_OP_HANDLERS,
    )

    CAST = IROpDescriptor(
        0x25, "类型转换", InstructionCategory.DATA_OP,
        flags=InstructionFlag.PURE_COMPUTE | InstructionFlag.PRODUCES_RESULT,
        result_index=0,  # result: Variable
        use_indices=(2,),  # source: Reference
    )

    FREE = IROpDescriptor(
        0x26, "释放变量", InstructionCategory.DATA_OP,
        flags=InstructionFlag.SIDE_EFFECT,
        use_indices=(0,),  # variable: Variable
    )

    # ==================== OOP (0x40-0x5F) ====================

    CLASS = IROpDescriptor(
        0x40, "类定义", InstructionCategory.OOP,
        flags=InstructionFlag.SIDE_EFFECT,
    )

    NEW_OBJ = IROpDescriptor(
        0x41, "新建对象", InstructionCategory.OOP,
        flags=InstructionFlag.SIDE_EFFECT | InstructionFlag.PRODUCES_RESULT,
        result_index=0,
        use_extractor=_new_obj_uses,
    )

    GET_PROPERTY = IROpDescriptor(
        0x42, "获取属性", InstructionCategory.OOP,
        flags=InstructionFlag.PURE_COMPUTE | InstructionFlag.PRODUCES_RESULT,
        result_index=0,  # result: Variable
        use_indices=(1,),  # object_ref: Reference
    )

    SET_PROPERTY = IROpDescriptor(
        0x43, "设置属性", InstructionCategory.OOP,
        flags=InstructionFlag.SIDE_EFFECT,
        use_indices=(0, 2),  # object_ref: Reference, value: Reference
    )

    CALL_METHOD = IROpDescriptor(
        0x44, "调用方法", InstructionCategory.OOP,
        flags=InstructionFlag.SIDE_EFFECT | InstructionFlag.CALL | InstructionFlag.PRODUCES_RESULT,
        result_index=0,
        use_extractor=_call_method_uses,
    )

    FREE_OBJ = IROpDescriptor(
        0x45, "释放对象", InstructionCategory.OOP,
        flags=InstructionFlag.SIDE_EFFECT,
        use_indices=(0,),  # object_ref: Reference
    )

    # ==================== CONTAINER (0x80-0x9F) ====================

    INDEX_GET = IROpDescriptor(
        0x80, "索引读取", InstructionCategory.DATA_OP,
        flags=InstructionFlag.PURE_COMPUTE | InstructionFlag.PRODUCES_RESULT,
        result_index=0,  # result: Variable
        use_indices=(1, 2),  # container: Reference, key: Reference
    )

    INDEX_SET = IROpDescriptor(
        0x81, "索引写入", InstructionCategory.DATA_OP,
        flags=InstructionFlag.SIDE_EFFECT,
        use_indices=(0, 1, 2),  # container, key, value: Reference
    )

    CONTAINER_LEN = IROpDescriptor(
        0x82, "获取长度", InstructionCategory.DATA_OP,
        flags=InstructionFlag.PURE_COMPUTE | InstructionFlag.PRODUCES_RESULT,
        result_index=0,  # result: Variable
        use_indices=(1,),  # container: Reference
    )

    LIST_APPEND = IROpDescriptor(
        0x83, "追加元素", InstructionCategory.DATA_OP,
        flags=InstructionFlag.SIDE_EFFECT,
        use_indices=(0, 1),  # container: Reference, value: Reference
    )

    DICT_HAS = IROpDescriptor(
        0x84, "检查键", InstructionCategory.DATA_OP,
        flags=InstructionFlag.PURE_COMPUTE | InstructionFlag.PRODUCES_RESULT,
        result_index=0,  # result: Variable
        use_indices=(1, 2),  # container: Reference, key: Reference
    )

    DICT_REMOVE = IROpDescriptor(
        0x85, "删除键", InstructionCategory.DATA_OP,
        flags=InstructionFlag.SIDE_EFFECT,
        use_indices=(0, 1),  # container: Reference, key: Reference
    )

    # ==================== STRUCT (0xA0-0xBF) ====================

    STRUCT_DEF = IROpDescriptor(
        0xA0, "结构体定义", InstructionCategory.STRUCT,
        flags=InstructionFlag.SIDE_EFFECT,
    )

    STRUCT_NEW = IROpDescriptor(
        0xA1, "结构体实例化", InstructionCategory.STRUCT,
        flags=InstructionFlag.SIDE_EFFECT | InstructionFlag.PRODUCES_RESULT,
        result_index=0,
        use_extractor=_struct_new_uses,
    )

    STRUCT_GET = IROpDescriptor(
        0xA2, "字段读取", InstructionCategory.STRUCT,
        flags=InstructionFlag.PURE_COMPUTE | InstructionFlag.PRODUCES_RESULT,
        result_index=0,  # result: Variable
        use_indices=(1,),  # struct_ref: Reference
    )

    STRUCT_SET = IROpDescriptor(
        0xA3, "字段写入", InstructionCategory.STRUCT,
        flags=InstructionFlag.SIDE_EFFECT,
        use_indices=(0, 2),  # struct_ref: Reference, value: Reference
    )

    STRUCT_CALL = IROpDescriptor(
        0xA4, "结构体方法调用", InstructionCategory.STRUCT,
        flags=InstructionFlag.SIDE_EFFECT | InstructionFlag.CALL | InstructionFlag.PRODUCES_RESULT,
        result_index=0,
        use_extractor=_struct_call_uses,
    )

    STRUCT_FREE = IROpDescriptor(
        0xA5, "结构体释放", InstructionCategory.STRUCT,
        flags=InstructionFlag.SIDE_EFFECT,
        use_indices=(0,),  # struct_ref: Reference
    )

    UNKNOWN = IROpDescriptor(-0x01, "未知指令", InstructionCategory.SPECIAL, )

    @classmethod
    def find(cls, code: int):
        for attr in dir(cls):
            if isinstance(attr, IROpDescriptor) and attr.code == code:
                return attr

        return cls.UNKNOWN