# coding=utf-8
"""
数值提供器提升 Pass

将连续的纯算术 BINARY_OP 链和多参数内建函数调用提取为表达式树，
坍缩为单条 COMPUTE 指令，供后端映射到 /compute 命令。

要求目标版本 >= 26.3（/compute 命令自 26.3 引入）。

优化能力：
  1. 同类运算聚合：  ADD(ADD(a,b),c) → sum(a, b, c)
  2. 跨类型嵌套：  MIN(sum(...), product(...))
  3. 函数调用提升：  CALL average(a,b,c) → average(a, b, c)
  4. 除法→平均识别：  (a+b+c)/3 → average(a, b, c)
  5. 减法包装：      a - b → sum(a, product(b, -1))

语义 dict 格式（人可读，后端负责转 MC JSON）：
  {"op": "sum", "args": [ref_a, ref_b, {"op": "product", "args": [ref_c, 3]}]}
  - Reference 叶节点：变量或常量
  - int/float 叶节点：仅由 -1 等内部常量产生
  - dict 叶节点：嵌套子表达式
"""
from __future__ import annotations

from collections import defaultdict
from typing import Optional

from dovetail.core.compile_config import CompileConfig
from dovetail.core.enums import (
    OptimizationLevel, BinaryOps
)
from dovetail.core.enums.minecraft import NewMinecraftVersion
from dovetail.core.enums.types import ValueType
from dovetail.core.ir_builder import IRBuilder
from dovetail.core.ir_code import IROpCode
from dovetail.core.instructions import IRInstruction, IRCompute, IRAssign
from dovetail.core.optimize.base import IROptimizationPass
from dovetail.core.optimize.pass_metadata import PassMetadata, PassPhase
from dovetail.core.optimize.pass_registry import register_pass
from dovetail.core.symbols import Literal, Reference, Function

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  映射表
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

_BINARY_OP_MAP: dict[str, str] = {
    BinaryOps.ADD.value: "sum",
    BinaryOps.SUB.value: "sum",
    BinaryOps.MUL.value: "product",
    BinaryOps.MIN.value: "minimum",
    BinaryOps.MAX.value: "maximum",
}

_BUILTIN_FUNC_MAP: dict[str, str] = {
    "sum": "sum",
    "product": "product",
    "minimum": "minimum",
    "maximum": "maximum",
    "average": "average",
    "min": "minimum",
    "max": "maximum",
    "avg": "average",
}

_LIFTABLE_BINARY_OPS = frozenset(_BINARY_OP_MAP.keys())

# /compute 最低版本：26.3
_COMPUTE_MIN_VERSION = NewMinecraftVersion.from_str("26.3")


@register_pass(PassMetadata(
    name="number_provider_lifting",
    display_name="数值提供器提升",
    description="将纯算术链提升为 COMPUTE 指令（映射到 /compute，需 26.3+）",
    level=OptimizationLevel.O2,
    phase=PassPhase.TRANSFORM,
    depends_on=("constant_folding",),
    provided_features=("compute_capable",),
))
class NumberProviderLiftingPass(IROptimizationPass):

    def __init__(self, builder: IRBuilder, config: CompileConfig):
        super().__init__(builder, config)
        self.changed = False

    def should_run(self, context) -> bool:
        """版本门控：目标 < 26.3 时不运行"""
        if not super().should_run(context):
            return False
        try:
            if self.config.version < _COMPUTE_MIN_VERSION:
                return False
        except Exception:
            return False
        return True

    # ━━━━━━━━━━━━━━ 主入口 ━━━━━━━━━━━━━━

    def execute(self) -> bool:
        self.changed = False

        def_map = self._build_def_map()
        use_map = self._build_use_map()
        fork_vars = self._build_fork_vars(use_map)  # ← 新增

        roots = self._collect_lift_roots(def_map, use_map)
        replaced: set[int] = set()

        for root_instr in roots:
            if id(root_instr) in replaced:
                continue

            tree, subtree, replace_target = self._extract_and_serialize(
                root_instr, def_map, fork_vars,  # ← 传入
            )
            if tree is None or replace_target is None:
                continue

            is_call = root_instr.opcode == IROpCode.CALL
            if not is_call and len(subtree) < 2:
                continue

            self._emit_compute(subtree, tree, replace_target)
            replaced.update(id(n) for n in subtree)
            self.changed = True
        return self.changed

    # ━━━━━━━━━━━━━━ def-use 构建 ━━━━━━━━━━━━━━

    def _build_def_map(self) -> dict[str, IRInstruction]:
        m: dict[str, IRInstruction] = {}
        for instr in self.builder:
            rv = instr.opcode.get_result_var(instr.operands)
            if rv is not None:
                m[rv.get_name()] = instr
        return m

    def _build_use_map(self) -> dict[str, list[IRInstruction]]:
        m: dict[str, list[IRInstruction]] = defaultdict(list)
        for instr in self.builder:
            for ref in instr.opcode.get_used_refs(instr.operands):
                if isinstance(ref, Reference):
                    m[ref.get_name()].append(instr)
        return m

    # ━━━━━━━━━━━━━━ 收集提升根 ━━━━━━━━━━━━━━

    def _collect_lift_roots(
            self,
            def_map: dict[str, IRInstruction],
            use_map: dict[str, list[IRInstruction]],
    ) -> list[IRInstruction]:
        """
        收集子图根候选：
          A) 可提升 BINARY_OP，且结果最终被不可提升指令消费（真·根）
          B) 可提升内建函数 CALL
        """
        roots = []
        seen: set[int] = set()

        for instr in self.builder:
            # 路径 A
            if instr.opcode == IROpCode.BINARY_OP:
                op_val = instr.operands[1].value
                if op_val in _LIFTABLE_BINARY_OPS and id(instr) not in seen:
                    true_root = self._find_chain_root(instr, def_map, use_map)
                    if true_root is not None and id(true_root) not in seen:
                        roots.append(true_root)
                        seen.add(id(true_root))
                    continue
            # 路径 B
            if instr.opcode == IROpCode.CALL:
                func: Function = instr.operands[1]
                if func.get_name() in _BUILTIN_FUNC_MAP and id(instr) not in seen:
                    roots.append(instr)
                    seen.add(id(instr))

        return roots

    def _find_chain_root(
            self,
            instr: IRInstruction,
            def_map: dict[str, IRInstruction],
            use_map: dict[str, list[IRInstruction]],
    ) -> Optional[IRInstruction]:
        """
        沿 use 链向上找到链条的真正根：结果被不可提升指令消费的那个节点。
        如果链中间分叉（一个结果被多条可提升指令使用），也停在分叉处。
        """
        current = instr
        while True:
            result_var = current.opcode.get_result_var(current.operands)
            if result_var is None:
                return current
            users = use_map.get(result_var.get_name(), [])
            liftable_users = []
            for u in users:
                if u.opcode == IROpCode.BINARY_OP and u.operands[1].value in _LIFTABLE_BINARY_OPS:
                    liftable_users.append(u)
                # DIV 也可能消费（average 模式），不视为截断
                elif u.opcode == IROpCode.BINARY_OP and u.operands[1].value == BinaryOps.DIV.value:
                    liftable_users.append(u)
                else:
                    # 被不可提升指令消费 → current 是真根
                    return current
            if len(liftable_users) != 1:
                # 0 个可提升用户或分叉 → current 是根
                return current
            current = liftable_users[0]

    # ━━━━━━━━━━━━━━ 提取 + 序列化 ━━━━━━━━━━━━━━

    def _extract_and_serialize(
            self,
            root: IRInstruction,
            def_map: dict[str, IRInstruction],
            fork_vars: frozenset[str]
    ) -> tuple[Optional[dict], list[IRInstruction], Optional[IRInstruction]]:
        """
        Returns:
            tree:           语义 dict，None 表示不可提升
            subtree:        被收入子图的指令列表
            replace_target: 应被 COMPUTE 替换的指令
        """
        subtree: list[IRInstruction] = []

        # ── 路径 B：多参数函数调用 ──
        if root.opcode == IROpCode.CALL:
            func: Function = root.operands[1]
            args_dict: dict = root.operands[2]
            np_op = _BUILTIN_FUNC_MAP[func.get_name()]
            serialized = []
            for arg_ref in args_dict.values():
                leaf = self._serialize_operand(arg_ref, def_map, subtree, fork_vars)
                if leaf is _FAIL:
                    return None, [], None
                serialized.append(leaf)
            return {"op": np_op, "args": serialized}, [root], root

        # ── 路径 C：DIV 根 → average 模式检测 ──
        if (root.opcode == IROpCode.BINARY_OP
                and root.operands[1].value == BinaryOps.DIV.value):
            left_ref = root.operands[2]
            right_ref = root.operands[3]
            subtree.append(root)

            left_tree = self._serialize_operand(left_ref, def_map, subtree, fork_vars)
            if left_tree is _FAIL:
                subtree.clear()
                return None, [], None

            divisor_val = self._try_get_literal_value(right_ref)

            if divisor_val is not None and divisor_val > 0:
                if (isinstance(left_tree, dict)
                        and left_tree.get("op") == "sum"):
                    var_count = sum(
                        1 for a in left_tree["args"]
                        if isinstance(a, (Reference, dict))
                    )
                    if divisor_val == var_count:
                        # average 匹配：替换 DIV
                        return {"op": "average", "args": list(left_tree["args"])}, subtree, root

            # 不匹配 average → 提升 ADD 链，DIV 留着
            subtree.remove(root)
            if isinstance(left_tree, dict):
                # 找到 ADD 链的顶：结果变量 == DIV 的左操作数
                add_chain_root = self._find_subtree_root_for_ref(
                    left_ref, subtree,
                )
                if add_chain_root is not None:
                    return left_tree, subtree, add_chain_root
            return None, [], None

        # ── 路径 A：二元运算链 ──
        tree = self._serialize_binary(root, def_map, subtree, fork_vars)
        if tree is _FAIL:
            return None, [], None

        return tree, subtree, root

    # ━━━━━━━━━━━━━━ 序列化：二元运算 ━━━━━━━━━━━━━━

    def _serialize_binary(
            self,
            instr: IRInstruction,
            def_map: dict[str, IRInstruction],
            subtree: list[IRInstruction],
            fork_vars: frozenset[str],  # ← 新增参数
    ) -> dict | object:
        if instr.opcode != IROpCode.BINARY_OP:
            return _FAIL
        op_val = instr.operands[1].value
        if op_val not in _LIFTABLE_BINARY_OPS:
            return _FAIL

        np_op = _BINARY_OP_MAP[op_val]
        left_ref = instr.operands[2]
        right_ref = instr.operands[3]
        subtree.append(instr)

        left = self._serialize_operand(left_ref, def_map, subtree, fork_vars)
        right = self._serialize_operand(right_ref, def_map, subtree, fork_vars)
        if left is _FAIL or right is _FAIL:
            return _FAIL

        if op_val == BinaryOps.SUB.value:
            neg_right = {"op": "product", "args": [right, -1]}
            return _flatten("sum", [left, neg_right])

        return _flatten(np_op, [left, right])

    def _serialize_operand(
            self,
            ref: Reference,
            def_map: dict[str, IRInstruction],
            subtree: list[IRInstruction],
            fork_vars: frozenset[str]
    ) -> Reference | dict | int | float | object:
        if isinstance(ref, Literal) or (
                isinstance(ref, Reference) and ref.value_type == ValueType.LITERAL
        ):
            return ref

        if isinstance(ref, Reference) and ref.value_type not in (
                ValueType.VARIABLE, ValueType.LITERAL,
        ):
            return _FAIL

        # 分叉保护：变量被多个可提升指令消费 → 不递归
        if isinstance(ref, Reference) and ref.get_name() in fork_vars:
            return ref

        def_instr = def_map.get(ref.get_name())
        if def_instr is None:
            return ref

        if def_instr.opcode == IROpCode.BINARY_OP:
            if def_instr.operands[1].value in _LIFTABLE_BINARY_OPS:
                return self._serialize_binary(def_instr, def_map, subtree, fork_vars)

        if def_instr.opcode == IROpCode.CALL:
            func = def_instr.operands[1]
            if func.get_name() in _BUILTIN_FUNC_MAP:
                tree, sub, _ = self._extract_and_serialize(def_instr, def_map, fork_vars)
                if tree is not None:
                    subtree.extend(sub)
                    return tree

        return ref

    def _build_fork_vars(
            self,
            use_map: dict[str, list[IRInstruction]],
    ) -> frozenset[str]:
        """
        收集分叉变量：被 ≥2 条可提升 BINARY_OP 消费的变量。

        这些变量不能被递归展开——否则多个提升会各自清零它，
        导致其他引用悬空。
        """
        fork: set[str] = set()
        for var_name, users in use_map.items():
            liftable = [
                u for u in users
                if u.opcode == IROpCode.BINARY_OP
                   and u.operands[1].value in _LIFTABLE_BINARY_OPS
            ]
            if len(liftable) >= 2:
                fork.add(var_name)
        return frozenset(fork)

    # ━━━━━━━━━━━━━━ average 模式 ━━━━━━━━━━━━━━

    @staticmethod
    def _try_get_literal_value(ref: Reference) -> Optional[int]:
        """尝试从 Reference 获取整数字面量值，失败返回 None"""
        if ref.is_literal():
            if isinstance(ref.value.value, (int, float)):
                return int(ref.value.value)
            return None
        if isinstance(ref, Reference) and ref.value_type == ValueType.LITERAL:
            try:
                return int(ref.get_name())
            except (ValueError, TypeError):
                return None
        return None

    @staticmethod
    def _find_subtree_root_for_ref(
            ref: Reference,
            subtree: list[IRInstruction],
    ) -> Optional[IRInstruction]:
        """在 subtree 中找到结果变量名 == ref 名的指令（即 ADD 链顶）"""
        target_name = ref.get_name()
        for instr in subtree:
            rv = instr.opcode.get_result_var(instr.operands)
            if rv is not None and rv.get_name() == target_name:
                return instr
        return None

    # ━━━━━━━━━━━━━━ 坍缩替换 ━━━━━━━━━━━━━━

    def _emit_compute(
            self,
            subtree_nodes: list[IRInstruction],
            tree: dict,
            replace_target: IRInstruction,
    ) -> None:
        # COMPUTE 的结果变量 = 被替换指令的结果变量
        result_var = replace_target.opcode.get_result_var(replace_target.operands)

        # TODO: 未来加浮点后，根据 result_var.dtype 决定 integer 值
        compute = IRCompute(result_var, tree, integer=True)

        # 替换目标指令
        it = self.builder.__iter__()
        for instr in it:
            if instr is replace_target:
                it.set_current(compute)
                break

        # 子图中其余指令 → 空 ASSIGN，DCE 会清理
        target_id = id(replace_target)
        for instr in self.builder:
            if id(instr) == target_id:
                continue
            if any(id(n) == id(instr) for n in subtree_nodes):
                rv = instr.opcode.get_result_var(instr.operands)
                if rv is not None:
                    nop = IRAssign(rv, Reference.literal(0))
                    it2 = self.builder.__iter__()
                    for i2 in it2:
                        if i2 is instr:
                            it2.set_current(nop)
                            break


# ━━━━━━━━━━━━━━ 工具函数 ━━━━━━━━━━━━━━

# 哨兵值：表示"不可提升"
_FAIL = object()


def _flatten(np_op: str, args: list) -> dict:
    """
    同类运算扁平化。

    sum(sum(a, b), sum(c, d)) → sum(a, b, c, d)
    product(x, product(y, z)) → product(x, y, z)
    """
    flat = []
    for a in args:
        if isinstance(a, dict) and a.get("op") == np_op:
            flat.extend(a["args"])
        else:
            flat.append(a)
    return {"op": np_op, "args": flat}
