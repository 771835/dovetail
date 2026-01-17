# coding=utf-8
"""
链式赋值消除 Pass

消除中间变量的无意义链式赋值。
支持复杂作用域和控制流分析。
"""
from __future__ import annotations

from transpiler.core.compile_config import CompileConfig
from transpiler.core.enums import OptimizationLevel
from transpiler.core.enums.types import ValueType, StructureType, DataType
from transpiler.core.instructions import *
from transpiler.core.ir_builder import IRBuilder
from transpiler.core.optimize.base import IROptimizationPass
from transpiler.core.optimize.pass_metadata import PassMetadata, PassPhase
from transpiler.core.optimize.pass_registry import register_pass
from transpiler.core.symbols import Variable, Reference


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
    2. 支持作用域嵌套
    3. 支持控制流分支
    4. 保守策略：条件分支后清除不确定的别名
    """

    def __init__(self, builder: IRBuilder, config: CompileConfig):
        super().__init__(builder, config)
        self._changed = False

    def execute(self) -> bool:
        """执行链式赋值消除优化"""
        self._changed = False

        # 构建别名映射和作用域树
        scope_tree, alias_maps = self._build_alias_maps()

        # 应用别名替换
        self._apply_alias_substitution(alias_maps, scope_tree)

        return self._changed

    def _build_alias_maps(self) -> tuple[dict, dict]:
        """
        构建作用域树和别名映射

        Returns:
            (scope_tree, alias_maps)
            - scope_tree: {scope_name: parent_scope_name}
            - alias_maps: {scope_name: {var_name: alias_ref}}
        """
        scope_tree = {}
        alias_maps = {"global": {}}

        scope_stack = ["global"]
        current_scope = "global"

        # 跟踪条件分支
        conditional_scopes = set()
        pending_conditionals = {}  # {parent: [child_scopes]}

        for instr in self.builder.get_instructions():
            if isinstance(instr, IRScopeBegin):
                scope_name = instr.get_operands()[0]
                scope_type = instr.get_operands()[1]
                parent_scope = current_scope

                scope_tree[scope_name] = parent_scope
                scope_stack.append(scope_name)
                current_scope = scope_name

                # 继承父作用域的别名（深拷贝）
                alias_maps[current_scope] = alias_maps[parent_scope].copy()

                # 标记条件分支
                if scope_type == StructureType.CONDITIONAL:
                    conditional_scopes.add(scope_name)
                    if parent_scope not in pending_conditionals:
                        pending_conditionals[parent_scope] = []
                    pending_conditionals[parent_scope].append(scope_name)

            elif isinstance(instr, IRScopeEnd):
                if scope_stack:
                    scope_stack.pop()
                    current_scope = scope_stack[-1] if scope_stack else "global"

            elif isinstance(instr, IRDeclare):
                var = instr.get_operands()[0]
                var_name = var.get_name()
                # 变量声明时指向自己
                alias_maps[current_scope][var_name] = Reference(ValueType.VARIABLE, var)

            elif isinstance(instr, IRAssign):
                target, source = instr.get_operands()
                target_name = target.get_name()

                if isinstance(source, Reference):
                    if source.value_type == ValueType.VARIABLE:
                        source_name = source.get_name()
                        # 查找源变量的最终别名
                        final_alias = self._resolve_alias(source_name, current_scope, alias_maps)
                        alias_maps[current_scope][target_name] = final_alias
                    elif source.value_type == ValueType.LITERAL:
                        # 字面量直接作为别名
                        alias_maps[current_scope][target_name] = source
                    else:
                        # 其他类型（函数调用结果等）清除别名
                        alias_maps[current_scope][target_name] = Reference(ValueType.VARIABLE, target)

            elif isinstance(instr, IRCondJump):
                # 条件跳转后，合并分支的别名状态
                true_scope = instr.get_operands()[1]
                false_scope = instr.get_operands()[2]

                # 获取两个分支的别名映射
                true_aliases = alias_maps.get(true_scope, {})
                false_aliases = alias_maps.get(false_scope, {})

                # 找出所有被修改的变量
                all_vars = set(true_aliases.keys()) | set(false_aliases.keys())

                for var_name in all_vars:
                    true_val = true_aliases.get(var_name)
                    false_val = false_aliases.get(var_name)

                    # 如果两个分支的别名不同，清除该变量的别名
                    if not self._aliases_equal(true_val, false_val):
                        # 回退到变量自身
                        if var_name in alias_maps[current_scope]:
                            # 创建一个指向自身的引用
                            var = Variable(var_name, DataType.INT)  # 类型不重要，后续会被覆盖
                            alias_maps[current_scope][var_name] = Reference(ValueType.VARIABLE, var)

            elif isinstance(instr, (IRBinaryOp, IRCompare, IRUnaryOp, IRCall)):
                # 这些指令产生新值，结果变量不是别名
                result = instr.get_operands()[0]
                if isinstance(result, Variable):
                    alias_maps[current_scope][result.name] = Reference(ValueType.VARIABLE, result)

        return scope_tree, alias_maps

    def _resolve_alias(self, var_name: str, scope: str, alias_maps: dict) -> Reference:
        """
        解析变量的最终别名

        Args:
            var_name: 变量名
            scope: 当前作用域
            alias_maps: 别名映射表

        Returns:
            最终的别名引用
        """
        seen = set()
        current_name = var_name
        current_scope = scope

        while current_name not in seen:
            seen.add(current_name)

            if current_scope in alias_maps and current_name in alias_maps[current_scope]:
                alias = alias_maps[current_scope][current_name]

                # 如果别名是字面量，直接返回
                if alias.value_type == ValueType.LITERAL:
                    return alias

                # 如果别名是变量，继续解析
                if alias.value_type == ValueType.VARIABLE:
                    next_name = alias.get_name()
                    if next_name == current_name:
                        # 指向自己，终止
                        return alias
                    current_name = next_name
                else:
                    return alias
            else:
                # 没有别名，返回变量自身
                break

        # 循环或未找到，返回原始变量
        return Reference(ValueType.VARIABLE, Variable(var_name, DataType.INT))

    def _aliases_equal(self, alias1: Reference | None, alias2: Reference | None) -> bool:
        """判断两个别名是否相等"""
        if alias1 is None or alias2 is None:
            return alias1 == alias2

        if alias1.value_type != alias2.value_type:
            return False

        if alias1.value_type == ValueType.LITERAL:
            return alias1.value.value == alias2.value.value

        if alias1.value_type == ValueType.VARIABLE:
            return alias1.get_name() == alias2.get_name()

        return False

    def _apply_alias_substitution(self, alias_maps: dict, scope_tree: dict) -> None:
        """应用别名替换"""
        iterator = self.builder.__iter__()
        scope_stack = ["global"]
        current_scope = "global"

        while True:
            try:
                instr = next(iterator)
            except StopIteration:
                break

            if isinstance(instr, IRScopeBegin):
                scope_name = instr.get_operands()[0]
                scope_stack.append(scope_name)
                current_scope = scope_name

            elif isinstance(instr, IRScopeEnd):
                if scope_stack:
                    scope_stack.pop()
                    current_scope = scope_stack[-1] if scope_stack else "global"

            else:
                # 获取当前作用域的别名映射
                aliases = alias_maps.get(current_scope, {})

                # 根据指令类型进行替换
                if isinstance(instr, IRAssign):
                    if self._replace_assign(iterator, instr, aliases):
                        self._changed = True

                elif isinstance(instr, IRBinaryOp):
                    if self._replace_binary_op(iterator, instr, aliases):
                        self._changed = True

                elif isinstance(instr, IRCompare):
                    if self._replace_compare(iterator, instr, aliases):
                        self._changed = True

                elif isinstance(instr, IRUnaryOp):
                    if self._replace_unary_op(iterator, instr, aliases):
                        self._changed = True

                elif isinstance(instr, IRCall):
                    if self._replace_call(iterator, instr, aliases):
                        self._changed = True

                elif isinstance(instr, IRCondJump):
                    if self._replace_cond_jump(iterator, instr, aliases):
                        self._changed = True

    def _replace_assign(self, iterator, instr: IRAssign, aliases: dict) -> bool:
        """替换赋值指令中的别名"""
        target, source = instr.get_operands()

        if isinstance(source, Reference) and source.value_type == ValueType.VARIABLE:
            source_name = source.get_name()
            if source_name in aliases:
                alias = aliases[source_name]
                # 避免自赋值
                if alias.value_type != ValueType.VARIABLE or alias.get_name() != source_name:
                    iterator.set_current(IRAssign(target, alias))
                    return True

        return False

    def _replace_binary_op(self, iterator, instr: IRBinaryOp, aliases: dict) -> bool:
        """替换二元运算中的别名"""
        result, op, left, right = instr.get_operands()
        changed = False
        new_left = left
        new_right = right

        if isinstance(left, Reference) and left.value_type == ValueType.VARIABLE:
            left_name = left.get_name()
            if left_name in aliases:
                alias = aliases[left_name]
                if alias.value_type != ValueType.VARIABLE or alias.get_name() != left_name:
                    new_left = alias
                    changed = True

        if isinstance(right, Reference) and right.value_type == ValueType.VARIABLE:
            right_name = right.get_name()
            if right_name in aliases:
                alias = aliases[right_name]
                if alias.value_type != ValueType.VARIABLE or alias.get_name() != right_name:
                    new_right = alias
                    changed = True

        if changed:
            iterator.set_current(IRBinaryOp(result, op, new_left, new_right))

        return changed

    def _replace_compare(self, iterator, instr: IRCompare, aliases: dict) -> bool:
        """替换比较运算中的别名"""
        result, op, left, right = instr.get_operands()
        changed = False
        new_left = left
        new_right = right

        if isinstance(left, Reference) and left.value_type == ValueType.VARIABLE:
            left_name = left.get_name()
            if left_name in aliases:
                alias = aliases[left_name]
                if alias.value_type != ValueType.VARIABLE or alias.get_name() != left_name:
                    new_left = alias
                    changed = True

        if isinstance(right, Reference) and right.value_type == ValueType.VARIABLE:
            right_name = right.get_name()
            if right_name in aliases:
                alias = aliases[right_name]
                if alias.value_type != ValueType.VARIABLE or alias.get_name() != right_name:
                    new_right = alias
                    changed = True

        if changed:
            iterator.set_current(IRCompare(result, op, new_left, new_right))

        return changed

    def _replace_unary_op(self, iterator, instr: IRUnaryOp, aliases: dict) -> bool:
        """替换一元运算中的别名"""
        result, op, operand = instr.get_operands()

        if isinstance(operand, Reference) and operand.value_type == ValueType.VARIABLE:
            operand_name = operand.get_name()
            if operand_name in aliases:
                alias = aliases[operand_name]
                if alias.value_type != ValueType.VARIABLE or alias.get_name() != operand_name:
                    iterator.set_current(IRUnaryOp(result, op, alias))
                    return True

        return False

    def _replace_call(self, iterator, instr: IRCall, aliases: dict) -> bool:
        """替换函数调用参数中的别名"""
        result, func, args = instr.get_operands()
        new_args = {}
        changed = False

        for param_name, arg_ref in args.items():
            if isinstance(arg_ref, Reference) and arg_ref.value_type == ValueType.VARIABLE:
                arg_name = arg_ref.get_name()
                if arg_name in aliases:
                    alias = aliases[arg_name]
                    if alias.value_type != ValueType.VARIABLE or alias.get_name() != arg_name:
                        new_args[param_name] = alias
                        changed = True
                    else:
                        new_args[param_name] = arg_ref
                else:
                    new_args[param_name] = arg_ref
            else:
                new_args[param_name] = arg_ref

        if changed:
            iterator.set_current(IRCall(result, func, new_args))

        return changed

    def _replace_cond_jump(self, iterator, instr: IRCondJump, aliases: dict) -> bool:
        """替换条件跳转中的别名"""
        cond_var, true_scope, false_scope = instr.get_operands()

        if isinstance(cond_var, Variable):
            cond_name = cond_var.name
            if cond_name in aliases:
                alias = aliases[cond_name]
                if alias.value_type == ValueType.VARIABLE:
                    alias_var = alias.value
                    if alias_var.name != cond_name:
                        iterator.set_current(IRCondJump(alias_var, true_scope, false_scope))
                        return True

        return False
