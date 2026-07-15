# coding=utf-8
"""
链式赋值消除 Pass

消除中间变量的无意义链式赋值。
支持复杂作用域和控制流分析。
"""
from __future__ import annotations

from typing import Optional

from dovetail.core.compile_config import CompileConfig
from dovetail.core.enums import OptimizationLevel
from dovetail.core.enums.types import ValueType, StructureType
from dovetail.core.instructions import (
    IRAssign, IRBinaryOp, IRCompare, IRUnaryOp, IRCall,
    IRCondJump,
    IRCallMethod, IROpCode, IRInstruction, PrimitiveDataType, IRCast
)
from dovetail.core.ir_builder import IRBuilder
from dovetail.core.optimize.base import IROptimizationPass
from dovetail.core.optimize.pass_metadata import PassMetadata, PassPhase
from dovetail.core.optimize.pass_registry import register_pass
from dovetail.core.symbols import Variable, Reference

# ---- 类型别名 ----
_AliasMap = dict[str, Reference]  # {var_name: canonical_ref}
_ScopeTree = dict[str, str | None]  # {scope_name: parent_scope_name}
_Snapshot = dict[int, _AliasMap]  # {指令索引: 执行该指令前的别名快照}


@register_pass(PassMetadata(
    name="chain_assign_elimination",
    display_name="链式赋值消除",
    description="消除中间变量的无意义链式赋值",
    level=OptimizationLevel.O2,
    phase=PassPhase.TRANSFORM,
    provided_features=("eliminated_chain_assigns",)
))
class ChainAssignEliminationPass(IROptimizationPass):
    """
    链式赋值消除优化 Pass

    功能：
    1. 识别链式赋值: a = b, c = a → c = b
    2. 支持作用域嵌套与继承
    3. 支持控制流分支（保守合并策略）
    4. 条件分支两侧别名不一致时，清除对应别名

    算法：两遍扫描
      第一遍: 构建每个作用域的别名映射表，同时为每条指令记录执行前的别名快照
      第二遍: 用每条指令自己的快照做替换，避免"未来状态污染过去指令"的问题
    """

    def __init__(self, builder: IRBuilder, config: CompileConfig):
        super().__init__(builder, config)
        self._assigned_vars: Optional[dict[str, set[str]]] = None
        self._changed = False

    # ------------------------------------------------------------------ #
    #  公开接口                                                            #
    # ------------------------------------------------------------------ #

    def execute(self) -> bool:
        """执行链式赋值消除优化"""
        self._changed = False

        self._scope_tree, self._scope_types = self._prescan_scope_tree()
        self._assigned_vars = self._collect_assigned_vars()  # 预扫描

        # 第一遍：构建别名映射 + 逐指令快照
        scope_tree, alias_maps, snapshots = self._build_alias_maps()

        # 第二遍：用快照精确替换，而非最终状态
        self._apply_alias_substitution(snapshots)

        return self._changed

    # ------------------------------------------------------------------ #
    #  第一遍：构建别名映射 + 快照                                           #
    # ------------------------------------------------------------------ #

    def _build_alias_maps(self) -> tuple[_ScopeTree, dict[str, _AliasMap], _Snapshot]:
        """
        遍历 IR，为每个作用域建立变量别名映射。
        同时在处理每条指令「之前」拍下当前作用域的别名快照。

        Returns:
            (scope_tree, alias_maps, snapshots)
        """
        scope_tree: _ScopeTree = {}
        alias_maps: dict[str, _AliasMap] = {"global": {}}
        scope_stack: list[str] = ["global"]
        snapshots: _Snapshot = {}

        # 需要按索引记录快照，先转成列表
        instructions = list(self.builder.get_instructions())

        for idx, instr in enumerate(instructions):
            current_scope = scope_stack[-1]

            # 在处理本条指令之前，先拍快照
            snapshots[idx] = dict(alias_maps[current_scope])

            if instr.opcode == IROpCode.SCOPE_BEGIN:
                scope_name = instr.get_operands()[0]
                scope_type = instr.get_operands()[1]
                parent = scope_stack[-1]

                scope_stack.append(scope_name)
                inherited = dict(alias_maps[parent])

                if scope_type in (StructureType.LOOP_CHECK, StructureType.LOOP_BODY):
                    # 循环内部写过的变量
                    dirty_inner = self._collect_all_written_in_scope(
                        scope_name, self._assigned_vars, self._scope_tree
                    )
                    # 祖先作用域中赋值过、可能跨迭代存活的变量
                    dirty_carried = self._collect_loop_carried_vars(scope_name)

                    dirty_vars = dirty_inner | dirty_carried

                    for var_name in dirty_vars:
                        if var_name in inherited:
                            # 不直接 pop，而是降级为恒等引用，保留类型信息
                            old_ref = inherited[var_name]
                            inherited[var_name] = Reference(
                                Variable(var_name, old_ref.value.dtype)
                            )

                alias_maps[scope_name] = inherited


            elif instr.opcode == IROpCode.SCOPE_END:
                if len(scope_stack) > 1:
                    leaving_scope = scope_stack[-1]  # 先记住要离开的作用域
                    leaving_type = self._scope_types.get(leaving_scope)
                    scope_stack.pop()  # 再弹栈
                    parent = scope_stack[-1]  # 弹完才能拿到父作用域
                    # 如果离开的是循环作用域，把它写过的变量从父作用域别名表里清掉
                    if leaving_type in (StructureType.LOOP_CHECK, StructureType.LOOP_BODY):
                        dirty = self._collect_all_written_in_scope(
                            leaving_scope, self._assigned_vars, self._scope_tree
                        )
                        for var_name in dirty:
                            if var_name in alias_maps[parent]:
                                old_ref = alias_maps[parent][var_name]
                                alias_maps[parent][var_name] = Reference(
                                    Variable(var_name, old_ref.value.dtype)
                                )

            elif instr.opcode == IROpCode.DECLARE:
                var = instr.get_operands()[0]
                alias_maps[current_scope][var.get_name()] = Reference(var)

            elif instr.opcode == IROpCode.ASSIGN:
                self._process_assign(instr, current_scope, alias_maps)

            elif instr.opcode == IROpCode.COND_JUMP:
                self._merge_branch_aliases(instr, current_scope, alias_maps)

            elif instr.opcode in (
                    IROpCode.BINARY_OP, IROpCode.COMPARE,
                    IROpCode.UNARY_OP, IROpCode.CALL, IROpCode.CALL_METHOD
            ):
                # 这些指令产生新值，结果变量不是别名，指向自身
                result = instr.get_operands()[0]
                if isinstance(result, Variable):
                    alias_maps[current_scope][result.get_name()] = Reference(result)

        return scope_tree, alias_maps, snapshots

    def _process_assign(
            self,
            instr: IRInstruction,
            current_scope: str,
            alias_maps: dict[str, _AliasMap]
    ) -> None:
        """处理赋值指令，更新当前作用域的别名映射。"""
        target, source = instr.get_operands()
        target_name = target.get_name()
        current_aliases = alias_maps[current_scope]

        # target 被重新赋值，所有以 target 为别名源的条目失效
        stale = [
            k for k, v in current_aliases.items()
            if v.value_type == ValueType.VARIABLE and v.get_name() == target_name
        ]
        for k in stale:
            current_aliases[k] = Reference(Variable(k, current_aliases[k].value.dtype))

        if isinstance(source, Reference):
            if source.value_type == ValueType.VARIABLE:
                final = self._resolve_alias(source.get_name(), current_scope, alias_maps)
                current_aliases[target_name] = final

            elif source.value_type == ValueType.LITERAL:
                current_aliases[target_name] = source

            else:
                current_aliases[target_name] = Reference(target)
        else:
            current_aliases[target_name] = Reference(target)

    def _merge_branch_aliases(
            self,
            instr: IRInstruction,
            current_scope: str,
            alias_maps: dict[str, _AliasMap]
    ) -> None:
        """
        IRCondJump 出现后，将两个分支的别名保守合并回当前作用域。

        策略：两侧别名一致则保留，否则清除（回退到指向自身）。
        """
        _, true_scope, false_scope = instr.get_operands()

        true_aliases = alias_maps.get(true_scope, {})
        false_aliases = alias_maps.get(false_scope, {})
        current_aliases = alias_maps[current_scope]

        all_vars = set(true_aliases) | set(false_aliases)

        for var_name in all_vars:
            true_ref = true_aliases.get(var_name)
            false_ref = false_aliases.get(var_name)

            if self._refs_equal(true_ref, false_ref):
                if true_ref is not None:
                    current_aliases[var_name] = true_ref
            else:
                if var_name in current_aliases:
                    original_ref = current_aliases[var_name]
                    if original_ref.value_type != ValueType.VARIABLE:
                        var = Variable(var_name, original_ref.value.dtype)
                        current_aliases[var_name] = Reference(var)

    # ------------------------------------------------------------------ #
    #  预扫描，收集变量名                                                    #
    # ------------------------------------------------------------------ #

    def _collect_assigned_vars(self) -> dict[str, set[str]]:
        """
        预扫描，收集每个作用域内直接被赋值的变量名。
        key: scope_name, value: 该作用域内被写入的变量名集合
        """
        assigned: dict[str, set[str]] = {}
        scope_stack = ["global"]

        for instr in self.builder.get_instructions():
            current = scope_stack[-1]

            if instr.opcode == IROpCode.SCOPE_BEGIN:
                scope_name = instr.get_operands()[0]
                scope_stack.append(scope_name)
                assigned.setdefault(scope_name, set())

            elif instr.opcode == IROpCode.SCOPE_END:
                if len(scope_stack) > 1:
                    scope_stack.pop()

            elif instr.opcode == IROpCode.ASSIGN:
                target = instr.get_operands()[0]
                assigned.setdefault(current, set()).add(target.get_name())

            elif instr.opcode in (IROpCode.BINARY_OP, IROpCode.COMPARE, IROpCode.UNARY_OP):
                result = instr.get_operands()[0]
                assigned.setdefault(current, set()).add(result.get_name())

        return assigned

    def _collect_all_written_in_scope(
            self,
            scope_name: str,
            assigned: dict[str, set[str]],
            scope_tree: _ScopeTree
    ) -> set[str]:
        """
        递归收集一个作用域及其所有子作用域内被写入的变量名。
        用于判断循环体内哪些变量是"不稳定"的。
        """
        result = set(assigned.get(scope_name, set()))
        for child, parent in scope_tree.items():
            if parent == scope_name:
                result |= self._collect_all_written_in_scope(child, assigned, scope_tree)
        return result

    def _collect_loop_carried_vars(self, loop_scope: str) -> set[str]:
        """
        收集所有在循环祖先作用域中被赋值过的变量名。
        这些变量可能跨迭代存活（loop-carried），不能在循环内做常量传播。
        """
        result = set()
        parent = self._scope_tree.get(loop_scope)
        while parent and parent != "global":
            result |= self._assigned_vars.get(parent, set())
            parent = self._scope_tree.get(parent)
        return result

    def _prescan_scope_tree(self) -> tuple[_ScopeTree, dict[str, StructureType]]:
        """
        预扫描完整的作用域树和每个作用域的类型。
        必须在 _build_alias_maps 之前完成。
        """
        scope_tree: _ScopeTree = {}
        scope_types: dict[str, StructureType] = {}
        scope_stack = ["global"]

        for instr in self.builder.get_instructions():
            if instr.opcode == IROpCode.SCOPE_BEGIN:
                scope_name = instr.get_operands()[0]
                scope_type = instr.get_operands()[1]
                parent = scope_stack[-1]
                scope_tree[scope_name] = parent
                scope_types[scope_name] = scope_type
                scope_stack.append(scope_name)

            elif instr.opcode == IROpCode.SCOPE_END:
                if len(scope_stack) > 1:
                    scope_stack.pop()

        return scope_tree, scope_types

    # ------------------------------------------------------------------ #
    #  别名解析                                                             #
    # ------------------------------------------------------------------ #

    def _resolve_alias(
            self,
            var_name: str,
            scope: str,
            alias_maps: dict[str, _AliasMap]
    ) -> Reference:
        """沿别名链追踪，返回变量的最终规范引用。"""
        seen: set[str] = set()
        current_name = var_name
        current_aliases = alias_maps.get(scope, {})

        while current_name not in seen:
            seen.add(current_name)

            ref = current_aliases.get(current_name)
            if ref is None:
                break

            if ref.value_type == ValueType.LITERAL:
                return ref

            if ref.value_type == ValueType.VARIABLE:
                next_name = ref.get_name()
                if next_name == current_name:
                    return ref
                current_name = next_name
            else:
                return ref

        ref = current_aliases.get(current_name)
        if ref is not None:
            return ref

        original = current_aliases.get(var_name)
        return original if original is not None else Reference(Variable(var_name, _UNKNOWN_DTYPE))

    # ------------------------------------------------------------------ #
    #  别名比较                                                             #
    # ------------------------------------------------------------------ #

    @staticmethod
    def _refs_equal(r1: Reference | None, r2: Reference | None) -> bool:
        """判断两个引用是否语义等价（同时比较名称和 dtype）。"""
        if r1 is None and r2 is None:
            return True
        if r1 is None or r2 is None:
            return False
        if r1.value_type != r2.value_type:
            return False
        if r1.value_type == ValueType.LITERAL:
            return r1.value.value == r2.value.value and r1.value.dtype == r2.value.dtype
        if r1.value_type == ValueType.VARIABLE:
            return r1.get_name() == r2.get_name() and r1.value.dtype == r2.value.dtype
        return False

    # ------------------------------------------------------------------ #
    #  第二遍：替换操作数                                                    #
    # ------------------------------------------------------------------ #

    def _apply_alias_substitution(self, snapshots: _Snapshot) -> None:
        """
        遍历 IR，用每条指令执行前的快照做精确替换。

        不再使用最终 alias_maps，而是用 snapshots[idx]，
        确保每条指令只能"看到"它执行前已确立的别名，
        不会被后续赋值语句的结果反向污染。
        """
        iterator = self.builder.__iter__()
        idx = 0

        for instr in iterator:
            # 作用域边界不需要替换，直接跳过
            if instr.opcode in (IROpCode.SCOPE_BEGIN, IROpCode.SCOPE_END):
                idx += 1
                continue

            # 拿这条指令执行前的快照
            aliases = snapshots.get(idx, {})
            new_instr = self._substitute(instr, aliases)

            if new_instr is not instr:
                iterator.set_current(new_instr)
                self._changed = True

            idx += 1

    def _substitute(self, instr: IRInstruction, aliases: _AliasMap) -> IRInstruction:
        """
        对单条指令应用别名替换，返回新指令（无变化则返回原指令）。
        """
        if instr.opcode == IROpCode.ASSIGN:
            target, source = instr.get_operands()
            new_source = self._resolve_ref(source, aliases)
            if new_source is not source:
                return IRAssign(target, new_source)

        elif instr.opcode == IROpCode.BINARY_OP:
            result, op, left, right = instr.get_operands()
            new_left = self._resolve_ref(left, aliases)
            new_right = self._resolve_ref(right, aliases)
            if new_left is not left or new_right is not right:
                return IRBinaryOp(result, op, new_left, new_right)

        elif instr.opcode == IROpCode.COMPARE:
            result, op, left, right = instr.get_operands()
            new_left = self._resolve_ref(left, aliases)
            new_right = self._resolve_ref(right, aliases)
            if new_left is not left or new_right is not right:
                return IRCompare(result, op, new_left, new_right)

        elif instr.opcode == IROpCode.UNARY_OP:
            result, op, operand = instr.get_operands()
            new_operand = self._resolve_ref(operand, aliases)
            if new_operand is not operand:
                return IRUnaryOp(result, op, new_operand)

        elif instr.opcode == IROpCode.COND_JUMP:
            cond, true_scope, false_scope = instr.get_operands()
            new_cond = self._resolve_ref(cond, aliases)
            if new_cond is not cond:
                return IRCondJump(new_cond, true_scope, false_scope)

        elif instr.opcode == IROpCode.CALL:
            result, func, args = instr.get_operands()
            new_args, changed = self._resolve_args(args, aliases)
            if changed:
                return IRCall(result, func, new_args)

        elif instr.opcode == IROpCode.CALL_METHOD:
            result, obj, func, args = instr.get_operands()
            new_args, changed = self._resolve_args(args, aliases)
            if changed:
                return IRCallMethod(result, obj, func, new_args)

        elif instr.opcode == IROpCode.CAST:
            result, target_type, source = instr.get_operands()
            new_source = self._resolve_ref(source, aliases)
            if source is not new_source:
                return IRCast(result, target_type, new_source)

        return instr

    def _resolve_ref(self, ref: Reference, aliases: _AliasMap) -> Reference:
        """若 ref 是变量且别名表中有更优目标，返回替换后的引用；否则返回原引用。"""
        if not isinstance(ref, Reference):
            return ref
        if ref.value_type != ValueType.VARIABLE:
            return ref

        alias = aliases.get(ref.get_name())
        if alias is None or self._refs_equal(alias, ref):
            return ref

        return alias

    @staticmethod
    def _resolve_args(
            args: dict[str, Reference],
            aliases: _AliasMap
    ) -> tuple[dict[str, Reference], bool]:
        """替换参数字典中所有可替换的引用，返回新字典和是否发生变化。"""
        new_args: dict[str, Reference] = {}
        changed = False

        for param_name, arg_ref in args.items():
            if isinstance(arg_ref, Reference) and arg_ref.value_type == ValueType.VARIABLE:
                alias = aliases.get(arg_ref.get_name())
                if alias is not None and alias is not arg_ref:
                    new_args[param_name] = alias  # noqa
                    changed = True
                    continue
            new_args[param_name] = arg_ref

        return new_args, changed


# 兜底占位类型，仅在别名表完全无信息时使用
_UNKNOWN_DTYPE = PrimitiveDataType.INT
