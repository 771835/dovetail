# coding=utf-8
"""
Number Provider 格式抽象层

将抽象的操作描述转成 Minecraft 数据包 JSON 格式。
所有 MC 格式细节（键名、前缀、字段结构）只在本文件中出现。
Mojang 改格式 → 只改这里。

26.3 格式规范：
  multi-arg: {"type": "minecraft:add", "inputs": [...]}
  binary:    {"type": "minecraft:sub", "left": ..., "right": ...}
  unary:     {"type": "minecraft:abs", "input": ...}
  leaf:      Reference / Literal / int / float（直接嵌入）
"""
from __future__ import annotations

from enum import Enum
from typing import Optional, Union


class ProviderArity(Enum):
    MULTI = "multi"  # 可变参数: add, mul, min, max, avg
    BINARY = "binary"  # 固定两参数: sub, div, mod, pow, ...
    UNARY = "unary"  # 单参数: abs, negate, from_int, ...


class ProviderOp:
    """
    一个 provider 操作的元数据描述。

    Attributes:
        mc_type:       MC 类型名（不含 minecraft: 前缀），如 "add", "sub"
        arity:         参数元数类别
        left_key:      二元运算的左字段名（默认 "left"，pow 用 "base"）
        right_key:     二元运算的右字段名（默认 "right"，pow 用 "exponent"）
        input_key:     一元运算的字段名（默认 "input"）
        registries:    该操作存在于哪些注册表: "int", "float", 或两者
    """
    __slots__ = ('mc_type', 'arity', 'left_key', 'right_key',
                 'input_key', 'registries')

    def __init__(
            self,
            mc_type: str,
            arity: ProviderArity,
            left_key: str = "left",
            right_key: str = "right",
            input_key: str = "input",
            registries: tuple[str, ...] = ("int",),
    ):
        self.mc_type = mc_type
        self.arity = arity
        self.left_key = left_key
        self.right_key = right_key
        self.input_key = input_key
        self.registries = registries

    @property
    def full_type(self) -> str:
        """完整 MC 类型 ID，如 'minecraft:add'"""
        return f"minecraft:{self.mc_type}"

    def is_multi(self) -> bool:
        return self.arity == ProviderArity.MULTI

    def is_binary(self) -> bool:
        return self.arity == ProviderArity.BINARY

    def is_unary(self) -> bool:
        return self.arity == ProviderArity.UNARY

    def supports_registry(self, registry: str) -> bool:
        return registry in self.registries


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  操作注册表
#  ── IR BinaryOps / UnaryOps / 内建函数 → MC provider ──
#  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PROVIDER_OPS: dict[str, ProviderOp] = {
    # ── 算术运算（IR BinaryOps 值 → MC provider）──
    "+": ProviderOp("add", ProviderArity.MULTI, registries=("int", "float")),
    "-": ProviderOp("sub", ProviderArity.BINARY, registries=("int", "float")),
    "*": ProviderOp("mul", ProviderArity.MULTI, registries=("int", "float")),
    "/": ProviderOp("div", ProviderArity.BINARY, registries=("int", "float")),
    "%": ProviderOp("mod", ProviderArity.BINARY, registries=("int", "float")),
    "min": ProviderOp("min", ProviderArity.MULTI, registries=("int", "float")),
    "max": ProviderOp("max", ProviderArity.MULTI, registries=("int", "float")),

    # ── 26.3 新增二元运算（需在 BinaryOps 枚举中先注册）──
    # 取消注释即可启用，无需改其他文件：
    # "floor_div":  ProviderOp("floor_div",  ProviderArity.BINARY, registries=("int",)),
    # "floor_mod":  ProviderOp("floor_mod",  ProviderArity.BINARY, registries=("int",)),
    # "**":         ProviderOp("pow",        ProviderArity.BINARY,
    #                       left_key="base", right_key="exponent",
    #                       registries=("int", "float")),

    # ── 一元运算（IR UnaryOps 值 → MC provider）──
    # "-":  (NEG) 由 sub 处理，不单独映射
    "abs": ProviderOp("abs", ProviderArity.UNARY, registries=("int", "float")),
    "negate": ProviderOp("negate", ProviderArity.UNARY, registries=("int", "float")),

    # ── 聚合函数（从 IR CALL 提升）──
    "avg": ProviderOp("avg", ProviderArity.MULTI, registries=("int", "float")),

    # ── 浮点专用（仅浮点注册表）──
    "from_int": ProviderOp("from_int", ProviderArity.UNARY, registries=("float",)),
    "from_float": ProviderOp("from_float", ProviderArity.UNARY, registries=("int",)),
    "sqrt": ProviderOp("sqrt", ProviderArity.UNARY, registries=("float",)),
    "sin": ProviderOp("sin", ProviderArity.UNARY, registries=("float",)),
    "cos": ProviderOp("cos", ProviderArity.UNARY, registries=("float",)),
    "length": ProviderOp("length", ProviderArity.MULTI, registries=("float",)),
    "floor": ProviderOp("floor", ProviderArity.UNARY, registries=("float",)),
    "ceil": ProviderOp("ceil", ProviderArity.UNARY, registries=("float",)),
    "round": ProviderOp("round", ProviderArity.UNARY, registries=("float",)),
    "truncate": ProviderOp("truncate", ProviderArity.UNARY, registries=("float",)),
}

# 内建函数名 → 操作查找键（兼容旧名称别名）
_FUNC_NAME_ALIASES: dict[str, str] = {
    "sum": "+", "add": "+",
    "product": "*", "mul": "*",
    "minimum": "min", "maximum": "max",
    "average": "avg", "avg": "avg",
}


def lookup_op(key: str) -> Optional[ProviderOp]:
    """通过 IR 枚举值或函数名查找 ProviderOp"""
    return PROVIDER_OPS.get(key) or PROVIDER_OPS.get(_FUNC_NAME_ALIASES.get(key, ""))


def lookup_by_func_name(name: str) -> Optional[ProviderOp]:
    """通过内建函数名查找（含别名）"""
    key = _FUNC_NAME_ALIASES.get(name, name)
    return PROVIDER_OPS.get(key)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  格式发射
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# 叶节点类型：Reference / Literal / int / float / dict
Leaf = Union[dict, int, float]


def emit_provider(op: ProviderOp, children: list) -> dict:
    """
    把抽象操作 + 子节点列表 → MC 格式的 dict。

    multi:   {"type": "minecraft:add", "inputs": [a, b, c]}
    binary:  {"type": "minecraft:sub", "left": a, "right": b}
    unary:   {"type": "minecraft:abs", "input": a}
    """
    if op.is_multi():
        return {"type": op.full_type, "inputs": children}
    elif op.is_binary():
        if len(children) != 2:
            raise ValueError(
                f"Binary op '{op.mc_type}' expects 2 children, got {len(children)}"
            )
        return {
            "type": op.full_type,
            op.left_key: children[0],
            op.right_key: children[1],
        }
    elif op.is_unary():
        if len(children) != 1:
            raise ValueError(
                f"Unary op '{op.mc_type}' expects 1 child, got {len(children)}"
            )
        return {"type": op.full_type, op.input_key: children[0]}
    else:
        raise ValueError(f"Unknown arity: {op.arity}")


def flatten_multi(op: ProviderOp, children: list) -> dict:
    """
    同类 multi-arg 运算扁平化。

    add(add(a, b), add(c, d)) → add(a, b, c, d)
    mul(x, mul(y, z)) → mul(x, y, z)

    仅对 MULTI 元数有意义，对 BINARY / UNARY 直接 emit。
    """
    if not op.is_multi():
        # 非聚合运算不做扁平化，直接发射
        return emit_provider(op, children)

    target_type = op.full_type
    flat: list = []
    for child in children:
        if isinstance(child, dict) and child.get("type") == target_type:
            # 同类型子节点 → 展开其 inputs
            flat.extend(child.get("inputs", []))
        else:
            flat.append(child)
    return emit_provider(op, flat)


def is_same_multi_type(tree: dict, op: ProviderOp) -> bool:
    """判断一个 dict 是否为同类型的 multi-arg provider"""
    return (
            isinstance(tree, dict)
            and tree.get("type") == op.full_type
            and "inputs" in tree
    )