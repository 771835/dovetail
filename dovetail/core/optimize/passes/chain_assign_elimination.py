# coding=utf-8
"""
链式赋值消除 Pass

消除中间变量的无意义链式赋值。
支持复杂作用域和控制流分析。
"""
from __future__ import annotations

from copy import copy
from typing import Optional

from dovetail.core.compile_config import CompileConfig
from dovetail.core.enums import OptimizationLevel
from dovetail.core.enums.types import ValueType, StructureType
from dovetail.core.instructions import (IRCall,
    IRCondJump, IRCallMethod, IROpCode, IRInstruction,
    PrimitiveDataType
)
from dovetail.core.ir_builder import IRBuilder
from dovetail.core.optimize.base import IROptimizationPass
from dovetail.core.optimize.pass_metadata import PassMetadata, PassPhase
from dovetail.core.optimize.pass_registry import register_pass
from dovetail.core.symbols import Variable, Reference
from dovetail.utils.logger import get_logger

logger = get_logger(__name__)

# ---- 类型别名 ----
_AliasMap = dict[str, Reference]  # {var_name: canonical_ref}
_ScopeTree = dict[str, str | None]  # {scope_name: parent_scope_name}

# 兜底占位类型，仅在别名表完全无信息时使用
_UNKNOWN_DTYPE = PrimitiveDataType.INT


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
      第一遍（_prescan_all）：
        同时收集 scope_tree、scope_types、assigned_vars，单次遍历完成。

      第二遍（_build_and_apply）：
        边构建 alias_map 边原地替换。
        关键不变量：处理指令 i 前，alias_map 的值 ≡ 原实现 snapshot[i]。
        因此无需快照字典，内存从 O(n×m) 降至 O(depth×m)。

    边建边替换的正确性：
      - snapshot[i] 定义为"处理完第 i-1 条指令后 alias_map 的状态"
      - 本实现在处理指令 i 时，alias_map 恰好处于"已处理完 i-1"的状态
      - 只要保证：① 先用当前 alias_map 替换，② 再更新 alias_map，
        不变量在每一步都成立，因此两种实现结果完全一致
    """

    def __init__(self, builder: IRBuilder, config: CompileConfig):
        super().__init__(builder, config)
        self._scope_tree: _ScopeTree = {}
        self._scope_types: dict[str, StructureType] = {}
        self._assigned_vars: dict[str, set[str]] = {}
        self._written_cache: dict[str, set[str]] = {}
        self._changed = False

    # ------------------------------------------------------------------ #
    #  公开接口                                                            #
    # ------------------------------------------------------------------ #

    def execute(self) -> bool:
        """执行链式赋值消除优化"""
        self._changed = False
        self._written_cache = {}  # 每次 execute 清空缓存，保证跨迭代正确

        # 第一遍：收集 scope_tree + scope_types + assigned_vars
        self._prescan_all()

        # 第二遍：边构建别名映射，边原地替换
        self._build_and_apply()

        return self._changed

    # ------------------------------------------------------------------ #
    #  第一遍：单次预扫描                                                   #
    # ------------------------------------------------------------------ #

    def _prescan_all(self) -> None:
        """
        单次遍历 IR，同时收集：
          - scope_tree:    作用域父子关系
          - scope_types:   每个作用域的 StructureType
          - assigned_vars: 每个作用域内直接被写入的变量名集合

        原实现用两次独立的全量遍历（_prescan_scope_tree + _collect_assigned_vars），
        此处合并为一次，结果完全等价。
        """
        scope_tree: _ScopeTree = {}
        scope_types: dict[str, StructureType] = {}
        assigned_vars: dict[str, set[str]] = {}
        scope_stack: list[str] = ["global"]

        for instr in self.builder:
            current = scope_stack[-1]

            if instr.opcode == IROpCode.SCOPE_BEGIN:
                scope_name, scope_type = instr.get_operands()
                scope_tree[scope_name] = scope_stack[-1]
                scope_types[scope_name] = scope_type
                assigned_vars.setdefault(scope_name, set())
                scope_stack.append(scope_name)

            elif instr.opcode == IROpCode.SCOPE_END:
                if len(scope_stack) > 1:
                    scope_stack.pop()

            elif instr.opcode == IROpCode.ASSIGN:
                target = instr.get_operands()[0]
                assigned_vars.setdefault(current, set()).add(target.get_name())

            elif instr.opcode in (
                    IROpCode.BINARY_OP, IROpCode.COMPARE, IROpCode.UNARY_OP
            ):
                result = instr.get_operands()[0]
                assigned_vars.setdefault(current, set()).add(result.get_name())

        self._scope_tree = scope_tree
        self._scope_types = scope_types
        self._assigned_vars = assigned_vars

    # ------------------------------------------------------------------ #
    #  第二遍：边建别名映射边替换                                            #
    # ------------------------------------------------------------------ #

    def _build_and_apply(self) -> None:
        """
        单次遍历 IR：
          1. 遇到作用域边界：维护 alias_maps 和 scope_stack
          2. 遇到普通指令：
             a. 先用当前 alias_map 替换操作数（此时 alias_map = snapshot[i]）
             b. 再根据指令语义更新 alias_map

        这样每条指令"看到"的都是它执行前确立的别名状态，
        与原实现的快照方案数学等价。
        """
        alias_maps: dict[str, _AliasMap] = {"global": {}}
        scope_stack: list[str] = ["global"]
        iterator = self.builder.__iter__()

        for instr in iterator:
            current_scope = scope_stack[-1]

            # ── 作用域开始 ───────────────────────────────────────────── #
            if instr.opcode == IROpCode.SCOPE_BEGIN:
                scope_name, scope_type = instr.get_operands()
                inherited = dict(alias_maps[scope_stack[-1]])

                # 循环作用域：清除可能跨迭代存活的变量别名
                if scope_type in (StructureType.LOOP_CHECK, StructureType.LOOP_BODY):
                    dirty = (
                            self._collect_all_written_in_scope(scope_name)
                            | self._collect_loop_carried_vars(scope_name)
                    )
                    for var_name in dirty:
                        if var_name in inherited:
                            old_ref = inherited[var_name]
                            inherited[var_name] = Reference(
                                Variable(var_name, old_ref.value.dtype)
                            )

                alias_maps[scope_name] = inherited
                scope_stack.append(scope_name)
                continue

            # ── 作用域结束 ───────────────────────────────────────────── #
            elif instr.opcode == IROpCode.SCOPE_END:
                if len(scope_stack) > 1:
                    leaving = scope_stack[-1]
                    leaving_type = self._scope_types.get(leaving)
                    scope_stack.pop()
                    parent = scope_stack[-1]

                    # 离开循环作用域：清除父作用域中被循环写过的变量别名
                    if leaving_type in (StructureType.LOOP_CHECK, StructureType.LOOP_BODY):
                        dirty = self._collect_all_written_in_scope(leaving)
                        for var_name in dirty:
                            if var_name in alias_maps[parent]:
                                old_ref = alias_maps[parent][var_name]
                                alias_maps[parent][var_name] = Reference(
                                    Variable(var_name, old_ref.value.dtype)
                                )
                continue

            # ── 普通指令：先替换，再更新 alias_map ──────────────── #
            aliases = alias_maps[current_scope]

            # 替换：使用当前（指令执行前）的 alias_map 状态
            new_instr = self._substitute(instr, aliases)
            if new_instr is not instr:
                iterator.set_current(new_instr)
                self._changed = True
                # 注意：更新 alias_map 仍用原始 instr，语义更清晰
                # （new_instr 与 instr 的操作数可能已被替换为字面量，
                #   但 _process_assign 内部会自行 resolve，传原始 instr 不影响结果）

            # 更新 alias_map
            if instr.opcode == IROpCode.DECLARE:
                var = instr.get_operands()[0]
                aliases[var.get_name()] = Reference(var)

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
                    aliases[result.get_name()] = Reference(result)

    # ------------------------------------------------------------------ #
    #  alias_map 更新逻辑                                                  #
    # ------------------------------------------------------------------ #

    def _process_assign(
            self,
            instr: IRInstruction,
            current_scope: str,
            alias_maps: dict[str, _AliasMap],
    ) -> None:
        """
        处理赋值指令，更新当前作用域的别名映射。

        步骤：
          1. 令 target 被重新赋值，所有以 target 为别名源的条目失效（降级为自身引用）
          2. 根据 source 的类型更新 target 的别名
        """
        target, source = instr.get_operands()
        target_name = target.get_name()
        current_aliases = alias_maps[current_scope]

        # 失效处理：凡是别名指向 target 的变量，降级为指向自身
        stale = [
            k for k, v in current_aliases.items()
            if v.value_type == ValueType.VARIABLE
               and v.get_name() == target_name
        ]
        for k in stale:
            current_aliases[k] = Reference(
                Variable(k, current_aliases[k].value.dtype)
            )

        if isinstance(source, Reference):
            if source.value_type == ValueType.VARIABLE:
                # 追踪别名链，得到最终规范引用
                final = self._resolve_alias(
                    source.get_name(), current_scope, alias_maps
                )
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
            alias_maps: dict[str, _AliasMap],
    ) -> None:
        """
        IRCondJump 出现后，将两个分支的别名保守合并回当前作用域。

        策略：两侧别名完全一致则保留，否则降级为指向自身。
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
                        current_aliases[var_name] = Reference(
                            Variable(var_name, original_ref.value.dtype)
                        )

    # ------------------------------------------------------------------ #
    #  脏变量收集                                                           #
    # ------------------------------------------------------------------ #

    def _collect_all_written_in_scope(self, scope_name: str) -> set[str]:
        """
        递归收集一个作用域及其所有子作用域内被写入的变量名。

        结果缓存在 self._written_cache，避免同一 scope 被重复递归。
        缓存在每次 execute() 开始时清空，保证跨迭代正确性。
        """
        if scope_name in self._written_cache:
            return self._written_cache[scope_name]

        result = set(self._assigned_vars.get(scope_name, set()))
        for child, parent in self._scope_tree.items():
            if parent == scope_name:
                result |= self._collect_all_written_in_scope(child)

        self._written_cache[scope_name] = result
        return result

    def _collect_loop_carried_vars(self, loop_scope: str) -> set[str]:
        """
        收集所有在循环祖先作用域中被赋值过的变量名。
        这些变量可能跨迭代存活（loop-carried），不能在循环内做常量传播。
        """
        result: set[str] = set()
        parent = self._scope_tree.get(loop_scope)
        while parent and parent != "global":
            result |= self._assigned_vars.get(parent, set())
            parent = self._scope_tree.get(parent)
        return result

    # ------------------------------------------------------------------ #
    #  别名解析                                                             #
    # ------------------------------------------------------------------ #

    def _resolve_alias(
            self,
            var_name: str,
            scope: str,
            alias_maps: dict[str, _AliasMap],
    ) -> Reference:
        """
        沿别名链追踪，返回变量的最终规范引用。
        遇到环（理论上不应出现）或找不到条目时安全返回。
        """
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
        return original if original is not None else Reference(
            Variable(var_name, _UNKNOWN_DTYPE)
        )

    # ------------------------------------------------------------------ #
    #  引用比较                                                             #
    # ------------------------------------------------------------------ #

    @staticmethod
    def _refs_equal(r1: Optional[Reference], r2: Optional[Reference]) -> bool:
        """判断两个引用是否语义等价（同时比较名称和 dtype）。"""
        if r1 is None and r2 is None:
            return True
        if r1 is None or r2 is None:
            return False
        if r1.value_type != r2.value_type:
            return False
        if r1.value_type == ValueType.LITERAL:
            return (
                    r1.value.value == r2.value.value
                    and r1.value.dtype == r2.value.dtype
            )
        if r1.value_type == ValueType.VARIABLE:
            return (
                    r1.get_name() == r2.get_name()
                    and r1.value.dtype == r2.value.dtype
            )
        return False

    # ------------------------------------------------------------------ #
    #  替换操作数                                                           #
    # ------------------------------------------------------------------ #

    def _substitute(
            self, instr: IRInstruction, aliases: _AliasMap
    ) -> IRInstruction:
        """
        对单条指令应用别名替换，返回新指令（无变化则返回原指令）。
        """
        opcode = instr.opcode
        if opcode.use_indices and not opcode.use_extractor:
            new_operands = copy(instr.operands)
            changed = False
            for i in opcode.use_indices:
                operand = instr.operands[i]
                if isinstance(operand, Reference):
                    new_operand = self._resolve_ref(operand, aliases)
                    if operand is not new_operand:
                        changed = True
                        new_operands[i] = new_operand

            if changed:
                return IRInstruction(opcode, *new_operands)
            return instr

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

        logger.debug(f"指令 {opcode.desc}({opcode.code}) 缺少对应的别名替换，已返回原始指令。")
        return instr

    def _resolve_ref(self, ref: Reference, aliases: _AliasMap) -> Reference:
        """
        若 ref 是变量且别名表中有更优目标，返回替换后的引用；否则返回原引用。
        """
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
            aliases: _AliasMap,
    ) -> tuple[dict[str, Reference], bool]:
        """
        替换参数字典中所有可替换的引用，返回新字典和是否发生变化。
        """
        new_args: dict[str, Reference] = {}
        changed = False

        for param_name, arg_ref in args.items():
            if (
                    isinstance(arg_ref, Reference)
                    and arg_ref.value_type == ValueType.VARIABLE
            ):
                alias = aliases.get(arg_ref.get_name())
                # 因为包装数据的类不同，而其中的数据相同，因此比较数据而非引用
                if alias is not None and alias.value is not arg_ref.value:
                    new_args[param_name] = alias  # noqa
                    changed = True
                    continue
            new_args[param_name] = arg_ref

        return new_args, changed
