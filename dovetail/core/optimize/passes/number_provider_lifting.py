# dovetail/core/optimize/passes/number_provider_lifting.py
# coding=utf-8
"""
数值提供器提升 Pass

将连续的纯算术 BINARY_OP 链和可提升内建函数调用提取为表达式树，
坍缩为单条 COMPUTE 指令，供后端映射到 /compute 命令。

要求目标版本 >= 26.3（/compute 命令自 26.3 引入）。

26.3 格式：输出语义 dict 使用 MC 官方字段名
  multi:   {"type": "minecraft:add", "inputs": [ref_a, ref_b, ...]}
  binary:  {"type": "minecraft:sub", "left": ..., "right": ...}
  unary:   {"type": "minecraft:abs", "input": ...}

优化能力：
  1. 同类运算聚合：  ADD(ADD(a,b),c) → add(a, b, c)
  2. 独立减法：      SUB(a, b) → sub(left=a, right=b)
  3. 跨类型嵌套：    MIN(add(...), mul(...))
  4. 函数调用提升：  CALL avg(a,b,c) → avg(a, b, c)
  5. average 反向推导： div(add(a,b,c), 3) → avg(a, b, c)
  6. 整数/浮点分流：根据操作数类型推断 compute_kind
"""
from __future__ import annotations

from collections import defaultdict
from typing import Optional

from dovetail.core.compile_config import CompileConfig
from dovetail.core.enums import (
    OptimizationLevel, BinaryOps, PrimitiveDataType, FunctionType,
)
from dovetail.core.enums.minecraft import NewMinecraftVersion
from dovetail.core.enums.types import ValueType
from dovetail.core.ir_builder import IRBuilder
from dovetail.core.ir_code import IROpCode
from dovetail.core.instructions import IRInstruction, IRCompute, IRAssign
from dovetail.core.optimize.base import IROptimizationPass
from dovetail.core.optimize.pass_metadata import PassMetadata, PassPhase
from dovetail.core.optimize.pass_registry import register_pass
from dovetail.utils.provider_format import (
    lookup_op, lookup_by_func_name,
    emit_provider, flatten_multi, is_same_multi_type,
)
from dovetail.core.symbols import Literal, Reference, Function

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  可提升运算集合
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# IR BinaryOps 值中，可以提升为 number provider 的运算
_LIFTABLE_BINARY_OPS: frozenset[str] = frozenset({
    BinaryOps.ADD.value,
    BinaryOps.SUB.value,
    BinaryOps.MUL.value,
    BinaryOps.DIV.value,
    BinaryOps.MOD.value,
    BinaryOps.MIN.value,
    BinaryOps.MAX.value,
})

# 可提升的内建函数名集合
_LIFTABLE_FUNC_NAMES: frozenset[str] = frozenset({
    "sum", "add", "product", "mul",
    "minimum", "min", "maximum", "max",
    "average", "avg",
})

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

    def execute(self, context=None) -> bool:
        self.changed = False

        def_map = self._build_def_map()
        use_map = self._build_use_map()
        fork_vars = self._build_fork_vars(use_map)

        roots = self._collect_lift_roots(def_map, use_map)
        replaced: set[int] = set()

        for root_instr in roots:
            if id(root_instr) in replaced:
                continue

            tree, subtree, replace_target, compute_kind = (
                self._extract_and_serialize(root_instr, def_map, fork_vars)
            )
            if tree is None or replace_target is None:
                continue

            is_call = root_instr.opcode == IROpCode.CALL
            if not is_call and len(subtree) < 2:
                continue

            self._emit_compute(subtree, tree, replace_target, compute_kind)
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

    def _build_fork_vars(
            self,
            use_map: dict[str, list[IRInstruction]],
    ) -> frozenset[str]:
        """
        收集分叉变量：被 ≥2 条可提升指令消费的变量。
        这些变量不能被递归展开——否则多个提升会各自清零它，导致悬空引用。
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

    # ━━━━━━━━━━━━━━ 收集提升根 ━━━━━━━━━━━━━━

    def _collect_lift_roots(
            self,
            def_map: dict[str, IRInstruction],
            use_map: dict[str, list[IRInstruction]],
    ) -> list[IRInstruction]:
        """
        收集子图根候选：
          A) 可提升 BINARY_OP，结果最终被不可提升指令消费（真·根）
          B) 可提升内建函数 CALL
        """
        roots: list[IRInstruction] = []
        seen: set[int] = set()

        for instr in self.builder:
            # 路径 A: 二元运算
            if instr.opcode == IROpCode.BINARY_OP:
                op_val = instr.operands[1].value
                if op_val in _LIFTABLE_BINARY_OPS and id(instr) not in seen:
                    true_root = self._find_chain_root(instr, def_map, use_map)
                    if true_root is not None and id(true_root) not in seen:
                        roots.append(true_root)
                        seen.add(id(true_root))
                    continue

            # 路径 B: 内建函数调用
            if instr.opcode == IROpCode.CALL:
                func: Function = instr.operands[1]
                if func.get_name() in _LIFTABLE_FUNC_NAMES and id(instr) not in seen:
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
        分叉时也停在分叉处。
        """
        current = instr
        while True:
            result_var = current.opcode.get_result_var(current.operands)
            if result_var is None:
                return current
            users = use_map.get(result_var.get_name(), [])
            liftable_users: list[IRInstruction] = []
            for u in users:
                if (u.opcode == IROpCode.BINARY_OP
                        and u.operands[1].value in _LIFTABLE_BINARY_OPS):
                    liftable_users.append(u)
                else:
                    # 被不可提升指令消费 → current 是真根
                    return current
            if len(liftable_users) != 1:
                # 0 个可提升用户或分叉 → current 是根
                return current
            current = liftable_users[0]

    # ━━━━━━━━━━━━━━ 类型推断 ━━━━━━━━━━━━━━

    def _infer_compute_kind(
            self,
            result_var,
            tree: dict,
    ) -> str:
        """
        推断 COMPUTE 应使用 integer 还是 float。

        策略：
        1. 如果结果变量是 FLOAT → float
        2. 如果树中有浮点专用类型（from_int, sqrt, sin, cos, length, ...）→ float
        3. 否则 → integer
        """
        # 检查结果变量类型
        if result_var is not None:
            try:
                if result_var.dtype == PrimitiveDataType.FLOAT:
                    return "float"
            except Exception:  # 显然易见的，float目前没有，所以会报错
                pass

        # 递归检查树中是否有浮点专用类型
        if self._tree_has_float_type(tree):
            return "float"

        return "integer"

    def _tree_has_float_type(self, tree) -> bool:
        """递归检查语义树是否包含浮点专用 provider 类型"""
        if not isinstance(tree, dict):
            return False
        type_str = tree.get("type", "")
        # 浮点专用类型集合
        float_only_types = {
            "minecraft:from_int", "minecraft:from_float",
            "minecraft:sqrt", "minecraft:sin", "minecraft:cos",
            "minecraft:length", "minecraft:floor", "minecraft:ceil",
            "minecraft:round", "minecraft:truncate",
        }
        if type_str in float_only_types:
            return True
        # 递归检查子节点
        for key in ("inputs", "input", "left", "right", "base", "exponent"):
            child = tree.get(key)
            if child is None:
                continue
            if isinstance(child, dict) and self._tree_has_float_type(child):
                return True
            if isinstance(child, list):
                for item in child:
                    if isinstance(item, dict) and self._tree_has_float_type(item):
                        return True
        return False

    # ━━━━━━━━━━━━━━ 提取 + 序列化 ━━━━━━━━━━━━━━

    def _extract_and_serialize(
            self,
            root: IRInstruction,
            def_map: dict[str, IRInstruction],
            fork_vars: frozenset[str],
    ) -> tuple[Optional[dict], list[IRInstruction], Optional[IRInstruction], str]:
        """
        Returns:
            tree:           语义 dict，None 表示不可提升
            subtree:        被收入子图的指令列表
            replace_target: 应被 COMPUTE 替换的指令
            compute_kind:   "integer" 或 "float"
        """
        subtree: list[IRInstruction] = []

        # ── 路径 B：多参数函数调用 ──
        if root.opcode == IROpCode.CALL:
            func: Function = root.operands[1]
            args_dict: dict = root.operands[2]
            provider_op = lookup_by_func_name(func.get_name())
            if provider_op is None:
                return None, [], None, "integer"

            serialized = []
            for arg_ref in args_dict.values():
                leaf = self._serialize_operand(arg_ref, def_map, subtree, fork_vars)
                if leaf is _FAIL:
                    return None, [], None, "integer"
                serialized.append(leaf)

            tree = emit_provider(provider_op, serialized)
            kind = self._infer_compute_kind(
                root.opcode.get_result_var(root.operands), tree
            )
            return tree, [root], root, kind

        # ── 路径 C：DIV 根 → average 反向推导 ──
        if (root.opcode == IROpCode.BINARY_OP
                and root.operands[1].value == BinaryOps.DIV.value):
            return self._try_average_or_div(root, def_map, subtree, fork_vars)

        # ── 路径 A：二元运算链 ──
        tree = self._serialize_binary(root, def_map, subtree, fork_vars)
        if tree is _FAIL:
            return None, [], None, "integer"
        tree: dict

        kind = self._infer_compute_kind(
            root.opcode.get_result_var(root.operands), tree
        )
        return tree, subtree, root, kind

    # ━━━━━━━━━━━━━━ average 反向推导 ━━━━━━━━━━━━━━

    def _try_average_or_div(
            self,
            div_instr: IRInstruction,
            def_map: dict[str, IRInstruction],
            subtree: list[IRInstruction],
            fork_vars: frozenset[str],
    ) -> tuple[Optional[dict], list[IRInstruction], Optional[IRInstruction], str]:
        """
        DIV 根的特殊处理：尝试 average 反向推导。

        div(add(a,b,c), 3) → avg(a, b, c)    ← 除数 == 操作数数量
        div(add(a,b,c), n) → div(left=add(...), right=n)  ← 除数不匹配，DIV 独立提升
        """
        left_ref = div_instr.operands[2]
        right_ref = div_instr.operands[3]
        subtree.append(div_instr)

        left_tree = self._serialize_operand(left_ref, def_map, subtree, fork_vars)
        if left_tree is _FAIL:
            subtree.clear()
            return None, [], None, "integer"

        divisor_val = self._try_get_literal_value(right_ref)

        # ── 尝试 average 匹配 ──
        if divisor_val is not None and divisor_val > 0:
            if isinstance(left_tree, dict) and is_same_multi_type(
                    left_tree, lookup_op("+") or lookup_op("add")):
                var_count = sum(
                    1 for a in left_tree.get("inputs", [])
                    if isinstance(a, (Reference, dict))
                )
                if divisor_val == var_count:
                    # average 匹配成功！
                    avg_op = lookup_op("avg")
                    avg_tree = emit_provider(avg_op, list(left_tree["inputs"]))
                    kind = self._infer_compute_kind(
                        div_instr.opcode.get_result_var(div_instr.operands), avg_tree
                    )
                    return avg_tree, subtree, div_instr, kind

        # ── average 不匹配 → DIV 作为独立二元运算提升 ──
        # 左侧可能是 multi-arg 链，需要保留其 COMPUTE
        # 整体变成 div(left=<left_tree>, right=<right_ref>)
        div_op = lookup_op(BinaryOps.DIV.value)
        if div_op is None:
            # DIV 不在可提升集合中 → 只提升左侧链
            subtree.remove(div_instr)
            if isinstance(left_tree, dict):
                add_root = self._find_subtree_root_for_ref(left_ref, subtree)
                if add_root is not None:
                    kind = self._infer_compute_kind(
                        div_instr.opcode.get_result_var(div_instr.operands), left_tree
                    )
                    return left_tree, subtree, add_root, kind
            return None, [], None, "integer"

        # DIV 独立提升：div(left=left_tree, right=right_ref)
        right_leaf = self._serialize_operand(right_ref, def_map, subtree, fork_vars)
        if right_leaf is _FAIL:
            subtree.remove(div_instr)
            return None, [], None, "integer"

        div_tree = emit_provider(div_op, [left_tree, right_leaf])
        kind = self._infer_compute_kind(
            div_instr.opcode.get_result_var(div_instr.operands), div_tree
        )
        return div_tree, subtree, div_instr, kind

    # ━━━━━━━━━━━━━━ 序列化：二元运算 ━━━━━━━━━━━━━━

    def _serialize_binary(
            self,
            instr: IRInstruction,
            def_map: dict[str, IRInstruction],
            subtree: list[IRInstruction],
            fork_vars: frozenset[str],
    ) -> dict | object:
        if instr.opcode != IROpCode.BINARY_OP:
            return _FAIL
        op_val = instr.operands[1].value
        if op_val not in _LIFTABLE_BINARY_OPS:
            return _FAIL

        provider_op = lookup_op(op_val)
        if provider_op is None:
            return _FAIL

        left_ref = instr.operands[2]
        right_ref = instr.operands[3]
        subtree.append(instr)

        left = self._serialize_operand(left_ref, def_map, subtree, fork_vars)
        right = self._serialize_operand(right_ref, def_map, subtree, fork_vars)
        if left is _FAIL or right is _FAIL:
            return _FAIL

        # multi-arg 运算（ADD, MUL, MIN, MAX）→ 尝试扁平化
        if provider_op.is_multi():
            return flatten_multi(provider_op, [left, right])

        # binary 运算（SUB, DIV, MOD）→ 独立二元，不扁平化
        return emit_provider(provider_op, [left, right])

    # ━━━━━━━━━━━━━━ 序列化：操作数 ━━━━━━━━━━━━━━

    def _serialize_operand(
            self,
            ref: Reference,
            def_map: dict[str, IRInstruction],
            subtree: list[IRInstruction],
            fork_vars: frozenset[str],
    ) -> Reference | dict | int | float | object:
        # 字面量 → 直接作为叶节点
        if isinstance(ref, Literal) or (
                isinstance(ref, Reference) and ref.value_type == ValueType.LITERAL
        ):
            return ref

        # 非变量非字面量 → 不可提升
        if isinstance(ref, Reference) and ref.value_type not in (
                ValueType.VARIABLE, ValueType.LITERAL,
        ):
            return _FAIL

        # 分叉保护：变量被多个可提升指令消费 → 不递归，保留为叶节点
        if isinstance(ref, Reference) and ref.get_name() in fork_vars:
            return ref

        def_instr = def_map.get(ref.get_name())
        if def_instr is None:
            return ref  # 外部变量 → 保留为叶节点

        # 定义指令是可提升的二元运算 → 递归序列化
        if def_instr.opcode == IROpCode.BINARY_OP:
            if def_instr.operands[1].value in _LIFTABLE_BINARY_OPS:
                return self._serialize_binary(def_instr, def_map, subtree, fork_vars)

        # 定义指令是可提升的内建函数调用 → 递归序列化
        if def_instr.opcode == IROpCode.CALL:
            func = def_instr.operands[1]
            if func.get_name() in _LIFTABLE_FUNC_NAMES and func.func_type == FunctionType.BUILTIN:
                tree, sub, _, kind = self._extract_and_serialize(
                    def_instr, def_map, fork_vars
                )
                if tree is not None:
                    subtree.extend(sub)
                    return tree

        return ref  # 其他情况 → 保留为叶节点

    # ━━━━━━━━━━━━━━ 辅助方法 ━━━━━━━━━━━━━━

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
        """在 subtree 中找到结果变量名 == ref 名的指令"""
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
            compute_kind: str,
    ) -> None:
        """用 COMPUTE 指令替换子图"""
        result_var = replace_target.opcode.get_result_var(replace_target.operands)

        compute = IRCompute(result_var, tree, compute_kind=compute_kind)

        # 替换目标指令为 COMPUTE
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


# ━━━━━━━━━━━━━━ 哨兵值 ━━━━━━━━━━━━━━

_FAIL = object()
