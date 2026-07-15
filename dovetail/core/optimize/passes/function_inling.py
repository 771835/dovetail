# coding=utf-8
"""
函数内联 Pass

将短小的函数调用展开到调用点，减少函数调用开销。
"""
from __future__ import annotations

from copy import deepcopy

from dovetail.core.compile_config import CompileConfig
from dovetail.core.enums import OptimizationLevel
from dovetail.core.enums.types import ValueType, VariableType
from dovetail.core.instructions import *
from dovetail.core.ir_builder import IRBuilder, IRBuilderIterator
from dovetail.core.optimize.base import IROptimizationPass
from dovetail.core.optimize.pass_metadata import PassMetadata, PassPhase
from dovetail.core.optimize.pass_registry import register_pass
from dovetail.core.symbols import Reference, Variable, Function

# 内联阈值：函数体指令数超过此值不内联
INLINE_THRESHOLD = 15


@register_pass(PassMetadata(
    name="function_inlining",
    display_name="函数内联",
    description="将短小的非递归函数调用展开到调用点",
    level=OptimizationLevel.O3,# O2即可，但是由于这个优化属于实验性的，故暂时设为O3
    phase=PassPhase.TRANSFORM,
    provided_features=("inlined_functions",)
))
class FunctionInliningPass(IROptimizationPass):
    """函数内联优化 Pass

    Attributes:
        _inline_candidates (dict[str, list[IRInstruction]]): 可内联的函数体指令列表，key 为函数名
        _recursive_funcs (set[str]): 递归函数名集合，不可内联
        _inline_counter (int): 全局内联计数器，用于生成不冲突的变量名
        _changed (bool): 是否发生了变化
    """

    def __init__(self, builder: IRBuilder, config: CompileConfig):
        super().__init__(builder, config)
        self._inline_candidates: dict[str, list[IRInstruction]] = {}
        self._recursive_funcs: set[str] = set()
        self._inline_counter: int = 0
        self._changed: bool = False

    def execute(self) -> bool:
        self._changed = False
        self._collect_candidates()
        self._perform_inlining()
        return self._changed

    # ------------------------------------------------------------------ #
    #  第一步：收集可内联的函数体                                           #
    # ------------------------------------------------------------------ #

    def _collect_candidates(self) -> None:
        """
        遍历整个 IR，收集每个函数的指令体，
        同时检测递归调用，标记不可内联的函数。
        """
        instructions = list(self.builder.get_instructions())

        # 先收集所有函数体
        # 结构：FUNCTION -> SCOPE_BEGIN(FUNCTION) -> ... -> SCOPE_END
        i = 0
        while i < len(instructions):
            instr = instructions[i]

            if instr.opcode == IROpCode.FUNCTION:
                func: Function = instr.get_operands()[0]
                func_name = func.name

                # 找到紧随其后的 SCOPE_BEGIN
                j = i + 1
                if j >= len(instructions) or instructions[j].opcode != IROpCode.SCOPE_BEGIN:
                    i += 1
                    continue

                # 收集 SCOPE 内的所有指令（不含 SCOPE_BEGIN/SCOPE_END 本身）
                body, end_idx = self._extract_scope_body(instructions, j)
                self._inline_candidates[func_name] = deepcopy(body)
                # 指令数超过阈值，不内联
                if len(body) > INLINE_THRESHOLD:
                    i = end_idx + 1
                    continue

                self._inline_candidates[func_name] = body
                i = end_idx + 1
            else:
                i += 1

        # 第二步：检测递归，从候选里剔除
        for func_name, body in self._inline_candidates.items():
            for instr in body:
                if instr.opcode == IROpCode.CALL:
                    callee: Function = instr.get_operands()[1]
                    if callee.name == func_name:
                        self._recursive_funcs.add(func_name)
                        break

        for name in self._recursive_funcs:
            self._inline_candidates.pop(name, None)

    def _extract_scope_body(
            self,
            instructions: list[IRInstruction],
            scope_begin_idx: int
    ) -> tuple[list[IRInstruction], int]:
        """
        从 SCOPE_BEGIN 开始，提取对应 SCOPE 内的所有指令（不含首尾的 SCOPE_BEGIN/SCOPE_END）。
        正确处理嵌套作用域。

        Returns:
            (body指令列表, SCOPE_END 的索引)
        """
        body = []
        depth = 0
        i = scope_begin_idx

        while i < len(instructions):
            instr = instructions[i]

            if instr.opcode == IROpCode.SCOPE_BEGIN:
                if depth == 0:
                    # 最外层的 SCOPE_BEGIN 本身不放入 body
                    depth += 1
                else:
                    depth += 1
                    body.append(instr)

            elif instr.opcode == IROpCode.SCOPE_END:
                depth -= 1
                if depth == 0:
                    # 最外层的 SCOPE_END，收集结束
                    return body, i
                else:
                    body.append(instr)
            else:
                body.append(instr)

            i += 1

        return body, i

    # ------------------------------------------------------------------ #
    #  第二步：执行内联                                                     #
    # ------------------------------------------------------------------ #

    def _perform_inlining(self) -> None:
        """遍历 IR，遇到可内联的 CALL 指令就展开"""
        iterator = self.builder.__iter__()

        while True:
            try:
                instr = next(iterator)
            except StopIteration:
                break

            if instr.opcode != IROpCode.CALL:
                continue

            result_var: Optional[Variable] = instr.get_operands()[0]
            callee: Function = instr.get_operands()[1]
            arguments: dict[str, Reference] = instr.get_operands()[2]

            if callee.name not in self._inline_candidates:
                continue

            body = self._inline_candidates[callee.name]
            self._inline_call(iterator, body, callee, result_var, arguments)
            self._changed = True

    def _inline_call(
            self,
            iterator: IRBuilderIterator,
            body: list[IRInstruction],
            callee: Function,
            result_var: Optional[Variable],
            arguments: dict[str, Reference]
    ) -> None:
        """
        在当前 CALL 指令位置展开函数体。

        步骤：
        1. 生成变量重命名表（函数体内所有变量 → 带 inline 前缀的新变量）
        2. 插入参数绑定指令（形参 = 实参）
        3. 逐条插入函数体指令（变量名替换）
        4. 把 RETURN 替换为对 result_var 的赋值
        5. 删除原 CALL 指令
        """
        suffix = self._next_suffix()

        # 1. 构建变量重命名表
        rename_map = self._build_rename_map(body, callee, suffix)
        scope_rename = self._build_scope_rename_map(body, suffix)

        # 2. 收集要插入的指令序列和信息
        inlined_instrs: list[IRInstruction] = []
        param_names = {param.get_name() for param in callee.params}

        # 2a. 形参绑定：为每个参数插入 DECLARE + ASSIGN
        for param in callee.params:
            new_var = rename_map[param.get_name()]
            inlined_instrs.append(IRInstruction(IROpCode.DECLARE, new_var))
            arg_ref = arguments.get(param.get_name())
            if arg_ref is not None:
                inlined_instrs.append(IRAssign(new_var, arg_ref))

        # 2b. 函数体指令（跳过原始的 DECLARE，因为 rename_map 会重建；RETURN 特殊处理）
        for orig_instr in body:
            if orig_instr.opcode == IROpCode.DECLARE:
                var: Variable = orig_instr.get_operands()[0]
                if var.name in param_names:
                    # 参数已经在形参绑定时 DECLARE 过了，跳过并修改变量的var_type
                    var.var_type = VariableType.COMMON
                    continue
                new_var = rename_map.get(var.name)
                if new_var is not None:
                    inlined_instrs.append(IRInstruction(IROpCode.DECLARE, new_var))

            elif orig_instr.opcode == IROpCode.RETURN:
                # RETURN value → result_var = value（替换后不再需要 RETURN）
                if result_var is not None:
                    ret_operands: list[Optional[Reference]] = orig_instr.get_operands()
                    ret_val = ret_operands[0] if ret_operands else None
                    if ret_val is not None:
                        new_ref = self._remap_ref(ret_val, rename_map)
                        inlined_instrs.append(IRAssign(result_var, new_ref))

            else:
                # 普通指令：重建，所有操作数里的变量引用替换为重命名版本
                new_instr = self._remap_instruction(orig_instr, rename_map, scope_rename)
                inlined_instrs.append(new_instr)

        # 3. 把所有内联指令插入到当前位置（CALL 指令之前），然后删除 CALL
        #    insert_here 在当前 index 插入，所以倒序插入保证顺序正确
        for new_instr in reversed(inlined_instrs):
            iterator.insert_here(new_instr)

        # 删除原始 CALL 指令
        iterator.remove_current()

    # ------------------------------------------------------------------ #
    #  工具方法                                                             #
    # ------------------------------------------------------------------ #

    def _next_suffix(self) -> str:
        """生成全局唯一的内联后缀，避免变量名冲突"""
        self._inline_counter += 1
        return f"__inline_{self._inline_counter}"

    def _build_rename_map(
            self,
            body: list[IRInstruction],
            callee: Function,
            suffix: str
    ) -> dict[str, Variable]:
        """
        扫描函数体，为所有出现的变量生成重命名映射。

        Args:
            body: 函数体指令列表
            callee: 被内联的函数对象
            suffix: 本次内联的唯一后缀

        Returns:
            {原始变量名: 新 Variable 对象}
        """
        rename_map: dict[str, Variable] = {}

        def _ensure(var: Variable) -> None:
            if var.name not in rename_map:
                new_name = f"{var.name}{suffix}"
                rename_map[var.name] = Variable(
                    name=new_name,
                    dtype=var.dtype,
                    var_type=VariableType.COMMON
                )

        # 参数也要重命名
        for param in callee.params:
            param_var = Variable(
                name=param.get_name(),
                dtype=param.get_dtype(),
                var_type=VariableType.PARAMETER
            )
            _ensure(param_var)

        # 扫描函数体里所有指令里出现的变量
        for instr in body:
            for operand in instr.get_operands():
                if isinstance(operand, Variable):
                    _ensure(operand)
                elif isinstance(operand, Reference) and operand.value_type == ValueType.VARIABLE:
                    _ensure(operand.value)

        return rename_map

    def _remap_ref(
            self,
            ref: Reference,
            rename_map: dict[str, Variable]
    ) -> Reference:
        """将一个 Reference 里的变量替换为重命名版本"""
        if isinstance(ref, Reference) and ref.value_type == ValueType.VARIABLE:
            new_var = rename_map.get(ref.get_name())
            if new_var is not None:
                return Reference(new_var)
        return ref

    def _build_scope_rename_map(
            self,
            body: list[IRInstruction],
            suffix: str
    ) -> dict[str, str]:
        """为函数体内所有作用域名生成重命名映射"""
        scope_rename: dict[str, str] = {}
        for instr in body:
            if instr.opcode == IROpCode.SCOPE_BEGIN:
                scope_name = instr.get_operands()[0]
                if scope_name not in scope_rename:
                    scope_rename[scope_name] = f"{scope_name}{suffix}"
        return scope_rename

    def _remap_instruction(
            self,
            instr: IRInstruction,
            rename_map: dict[str, Variable],
            scope_rename: dict[str, str]
    ) -> IRInstruction:
        """
        重建一条指令，把所有操作数里的变量替换为重命名版本。
        直接按 opcode 分发处理，保证指令结构正确。
        """
        op = instr.opcode

        if op == IROpCode.ASSIGN:
            target, source = instr.get_operands()
            new_target = rename_map.get(target.name, target)
            new_source = self._remap_ref(source, rename_map)
            assert isinstance(new_target, Variable)
            return IRAssign(new_target, new_source)

        elif op in (IROpCode.BINARY_OP, IROpCode.COMPARE):
            result, operator, left, right = instr.get_operands()
            new_result = rename_map.get(result.name, result)
            new_left = self._remap_ref(left, rename_map)
            new_right = self._remap_ref(right, rename_map)
            return IRInstruction(op, new_result, operator, new_left, new_right)

        elif op == IROpCode.UNARY_OP:
            result, operator, operand = instr.get_operands()
            new_result = rename_map.get(result.name, result)
            new_operand = self._remap_ref(operand, rename_map)
            assert isinstance(new_result, Variable)
            return IRUnaryOp(new_result, operator, new_operand)

        elif op == IROpCode.CAST:
            result, dtype, value_ref = instr.get_operands()
            new_result = rename_map.get(result.name, result)
            new_value_ref = self._remap_ref(value_ref, rename_map)
            assert isinstance(new_result, Variable)
            return IRCast(new_result, dtype, new_value_ref)

        elif op == IROpCode.CALL:
            result, func, args = instr.get_operands()
            new_result = rename_map.get(result.name, result) if result else None
            new_args = {k: self._remap_ref(v, rename_map) for k, v in args.items()}
            return IRCall(new_result, func, new_args)

        elif op in (IROpCode.SCOPE_BEGIN, IROpCode.SCOPE_END):
            scope_name, scope_type = instr.get_operands()
            return IRInstruction(op, scope_rename.get(scope_name, scope_name), scope_type)

        elif op == IROpCode.COND_JUMP:
            cond_var, true_scope, false_scope = instr.get_operands()
            new_cond = rename_map.get(cond_var.name, cond_var)
            return IRInstruction(
                op,
                new_cond,
                scope_rename.get(true_scope, true_scope),
                scope_rename.get(false_scope, false_scope)
            )

        elif op == IROpCode.JUMP:  # IRJump 对应的 opcode
            target_scope = instr.get_operands()[0]
            return IRInstruction(op, scope_rename.get(target_scope, target_scope))
        else:
            # 其他指令原样返回，保守处理
            return instr
