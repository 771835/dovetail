# coding=utf-8
"""
链式赋值消除 Pass

消除中间变量的无意义链式赋值。
支持复杂作用域和控制流分析。
"""
from __future__ import annotations

from dovetail.core.compile_config import CompileConfig
from dovetail.core.enums import OptimizationLevel, StructureType
from dovetail.core.enums.types import ValueType
from dovetail.core.instructions import (
    IRAssign, IRBinaryOp, IRCompare, IRUnaryOp, IRCall,
    IRCondJump,
    IRCallMethod, IROpCode, IRInstruction, PrimitiveDataType
)
from dovetail.core.ir_builder import IRBuilder
from dovetail.core.optimize.base import IROptimizationPass
from dovetail.core.optimize.pass_metadata import PassMetadata, PassPhase
from dovetail.core.optimize.pass_registry import register_pass
from dovetail.core.symbols import Variable, Reference

# ---- 类型别名 ----
_AliasMap = dict[str, Reference]  # {var_name: canonical_ref}
_ScopeTree = dict[str, str | None]  # {scope_name: parent_scope_name}


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
      第一遍: 构建每个作用域的别名映射表
      第二遍: 替换所有指令中的可替换操作数
    """

    def __init__(self, builder: IRBuilder, config: CompileConfig):
        super().__init__(builder, config)
        self._changed = False

    # ------------------------------------------------------------------ #
    #  公开接口                                                            #
    # ------------------------------------------------------------------ #

    def execute(self) -> bool:
        """执行链式赋值消除优化"""
        self._changed = False

        # 构建别名映射和作用域树
        scope_tree, alias_maps = self._build_alias_maps()

        # 应用别名替换
        self._apply_alias_substitution(alias_maps)
        return self._changed

    # ------------------------------------------------------------------ #
    #  第一遍：构建别名映射                                                  #
    # ------------------------------------------------------------------ #

    def _build_alias_maps(self) -> tuple[_ScopeTree, dict[str, _AliasMap]]:
        """
        遍历 IR，为每个作用域建立变量别名映射。

        Returns:
            (scope_tree, alias_maps)
        """
        scope_tree: _ScopeTree = {}
        alias_maps: dict[str, _AliasMap] = {"global": {}}
        scope_stack: list[str] = ["global"]

        for instr in self.builder.get_instructions():

            if instr.opcode == IROpCode.SCOPE_BEGIN:
                scope_name, scope_type = instr.get_operands()[0], instr.get_operands()[1]
                parent = scope_stack[-1]

                scope_tree[scope_name] = parent
                scope_stack.append(scope_name)

                # 子作用域继承父作用域别名（独立拷贝，互不污染）
                alias_maps[scope_name] = dict(alias_maps[parent])

                if scope_type == StructureType.CONDITIONAL:
                    pass  # branch_children 此版本不需要，保留注释备查

            elif instr.opcode == IROpCode.SCOPE_END:
                if len(scope_stack) > 1:
                    scope_stack.pop()

            elif instr.opcode == IROpCode.DECLARE:
                var = instr.get_operands()[0]
                current = scope_stack[-1]
                alias_maps[current][var.get_name()] = Reference(var)

            elif instr.opcode == IROpCode.ASSIGN:
                self._process_assign(instr, scope_stack[-1], alias_maps)

            elif instr.opcode == IROpCode.COND_JUMP:
                self._merge_branch_aliases(instr, scope_stack[-1], alias_maps)

            elif instr.opcode in (
                    IROpCode.BINARY_OP, IROpCode.COMPARE,
                    IROpCode.UNARY_OP, IROpCode.CALL, IROpCode.CALL_METHOD
            ):
                # 这些指令产生新值，结果变量不是别名，指向自身
                result = instr.get_operands()[0]
                if isinstance(result, Variable):
                    alias_maps[scope_stack[-1]][result.get_name()] = Reference(result)

        return scope_tree, alias_maps

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

    def _apply_alias_substitution(self, alias_maps: dict[str, _AliasMap]) -> None:
        """遍历 IR，将所有可替换的操作数替换为其规范形式。"""
        iterator = self.builder.__iter__()
        scope_stack: list[str] = ["global"]

        for instr in iterator:
            if instr.opcode == IROpCode.SCOPE_BEGIN:
                scope_stack.append(instr.get_operands()[0])
                continue

            if instr.opcode == IROpCode.SCOPE_END:
                if len(scope_stack) > 1:
                    scope_stack.pop()
                continue

            aliases = alias_maps.get(scope_stack[-1], {})
            new_instr = self._substitute(instr, aliases)

            if new_instr is not instr:
                iterator.set_current(new_instr)
                self._changed = True

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
                return IRCondJump(new_cond.value, true_scope, false_scope)

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
                    assert alias is not None
                    new_args[param_name] = alias
                    changed = True
                    continue
            new_args[param_name] = arg_ref

        return new_args, changed


# 兜底占位类型，仅在别名表完全无信息时使用
_UNKNOWN_DTYPE = PrimitiveDataType.INT
