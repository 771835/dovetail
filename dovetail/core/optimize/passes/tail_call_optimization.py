# coding=utf-8
"""
尾递归优化 Pass

将函数内的直接尾递归调用转换为循环跳转。
仅处理直接尾递归（函数尾部调用自身），不处理互递归。
"""
from __future__ import annotations

from dovetail.core.compile_config import CompileConfig
from dovetail.core.enums import OptimizationLevel
from dovetail.core.instructions import (
    IRInstruction, IROpCode,
    IRAssign, IRJump, IRScopeBegin, IRScopeEnd,
)
from dovetail.core.enums.types import StructureType
from dovetail.core.ir_builder import IRBuilder
from dovetail.core.optimize.base import IROptimizationPass
from dovetail.core.optimize.context import OptimizationContext
from dovetail.core.optimize.pass_metadata import PassMetadata, PassPhase
from dovetail.core.optimize.pass_registry import register_pass
from dovetail.core.symbols import Function, Reference

# ─── 常量 ────────────────────────────────────────────────────────────────────

_TCO_SCOPE_SUFFIX = "__tco_loop"


# ─── Pass 注册 ────────────────────────────────────────────────────────────────

@register_pass(PassMetadata(
    name="tail_call_optimization",
    display_name="尾递归优化",
    description="将直接尾递归调用转换为循环跳转，消除栈帧增长",
    level=OptimizationLevel.O3,
    phase=PassPhase.TRANSFORM,
    depends_on=("constant_folding",),
    provided_features=("tail_call_optimized",),
))
class TailCallOptimizationPass(IROptimizationPass):
    """
    尾递归优化 Pass

    识别模式：在函数体内，`IRCall(result, func_self, args)` 之后
    紧跟 `IRReturn(result)`（中间允许存在 SCOPE_END），且被调用函数
    与当前函数一致，则为直接尾递归候选。

    变换策略：
        1. 在函数体入口的 SCOPE_BEGIN 之后，插入一个具名循环作用域
           SCOPE_BEGIN(func_name + __tco_loop, FUNCTION)
        2. 将 IRCall 替换为对函数参数的逐一 IRAssign
        3. 将对应的 IRReturn 替换为 IRJump(loop_scope_name)
        4. 在函数体 SCOPE_END 之前插入循环作用域的 SCOPE_END
    """

    def __init__(self, builder: IRBuilder, config: CompileConfig):
        super().__init__(builder, config)
        self._changed = False

    def should_run(self, context: OptimizationContext) -> bool:
        if self.config.recursion:
            return super().should_run(context)
        else:  # 当不支持递归时直接拒绝运行
            return False

    # ── 分析阶段 ──────────────────────────────────────────────────────────────

    def analyze(self) -> dict:
        """
        扫描 IR，找出所有直接尾递归候选。

        Returns:
            {
                "candidates": {
                    func_name: [
                        {"call_index": int, "return_index": int,
                         "function": Function, "call_instr": IRInstruction}
                    ]
                }
            }
        """
        instructions = self.builder.get_instructions()
        candidates: dict[str, list[dict]] = {}

        current_func: Function | None = None
        func_scope_depth = 0  # 追踪当前函数体的作用域嵌套深度

        i = 0
        while i < len(instructions):
            instr = instructions[i]

            # 进入新函数定义
            if instr.opcode is IROpCode.FUNCTION:
                current_func = instr.operands[0]
                func_scope_depth = 0
                i += 1
                continue

            # 离开函数（depth 回到 0 之后的 SCOPE_END 意味着函数体结束）
            if instr.opcode is IROpCode.SCOPE_BEGIN:
                func_scope_depth += 1
                i += 1
                continue

            if instr.opcode is IROpCode.SCOPE_END:
                func_scope_depth -= 1
                if func_scope_depth < 0:
                    # 函数体已结束
                    current_func = None
                    func_scope_depth = 0
                i += 1
                continue

            # 查找 IRCall
            if instr.opcode is IROpCode.CALL and current_func is not None:
                called_func: Function = instr.operands[1]

                # 仅处理直接尾递归
                if called_func.get_name() != current_func.get_name():
                    i += 1
                    continue

                # 向后扫描，跳过 SCOPE_END，寻找紧随其后的 IRReturn
                j = i + 1
                while j < len(instructions) and instructions[j].opcode is IROpCode.SCOPE_END:
                    j += 1

                if j < len(instructions) and instructions[j].opcode is IROpCode.RETURN:
                    return_instr = instructions[j]
                    call_result = instr.operands[0]  # Variable | None

                    # 验证 return 的值就是 call 的返回值（或均为 void）
                    return_value = return_instr.operands[0]
                    is_tail = (
                                      call_result is None and return_value is None
                              ) or (
                                      call_result is not None
                                      and return_value is not None
                                      and hasattr(return_value, 'get_name')
                                      and hasattr(call_result, 'get_name')
                                      and return_value.get_name() == call_result.get_name()
                              )

                    if is_tail:
                        func_name = current_func.get_name()
                        if func_name not in candidates:
                            candidates[func_name] = []
                        candidates[func_name].append({
                            "call_index": i,
                            "return_index": j,
                            "function": current_func,
                            "call_instr": instr,
                        })

            i += 1

        return {"candidates": candidates}

    # ── 执行阶段 ──────────────────────────────────────────────────────────────

    def execute(self) -> bool:
        """
        执行优化。

        每次只处理一个函数，变换完毕后重新扫描，
        避免多函数场景下的索引漂移问题。
        """
        self._changed = False

        # 先收集所有需要处理的函数名（只取名字，不取索引）
        analysis = self.analyze()
        candidate_func_names = list(analysis.get("candidates", {}).keys())

        if not candidate_func_names:
            return False

        # 逐函数处理：每次处理前重新 analyze 获取当前准确索引
        for func_name in candidate_func_names:
            fresh = self.analyze()
            sites = fresh.get("candidates", {}).get(func_name)
            if sites:
                self._transform_function(func_name, sites)

        return self._changed

    def _transform_function(
            self,
            func_name: str,
            call_sites: list[dict],
    ) -> None:
        """
        对单个函数内的所有尾递归调用点执行变换。

        变换步骤：
          1. 找到函数体的 SCOPE_BEGIN，在其后插入 TCO 循环作用域的 SCOPE_BEGIN
          2. 对每个调用点（从后向前，避免索引漂移）：
             a. 用参数重赋值指令替换 IRCall
             b. 用 IRJump(tco_scope) 替换 IRReturn
          3. 在函数体 SCOPE_END 之前插入 TCO 循环作用域的 SCOPE_END
        """
        instructions = self.builder.get_instructions()
        loop_scope_name = f"{func_name}{_TCO_SCOPE_SUFFIX}"

        # ── Step 1：找到该函数体 SCOPE_BEGIN 的索引 ──────────────────────────
        func_scope_begin_idx = self._find_function_scope_begin(func_name)
        if func_scope_begin_idx is None:
            return

        # ── Step 2：找到该函数体 SCOPE_END 的索引 ────────────────────────────
        func_scope_end_idx = self._find_function_scope_end(func_scope_begin_idx)
        if func_scope_end_idx is None:
            return

        # ── Step 3：从后向前替换每个调用点，避免索引漂移 ─────────────────────
        # 先按 call_index 降序排列
        sorted_sites = sorted(call_sites, key=lambda s: s["call_index"], reverse=True)

        # 记录因插入/删除导致的函数体 SCOPE_END 索引偏移量
        end_idx_offset = 0

        for site in sorted_sites:
            call_idx = site["call_index"]
            return_idx = site["return_index"]
            call_instr: IRInstruction = site["call_instr"]
            func_sym: Function = site["function"]

            # 构建参数重赋值指令序列
            # IRCall.operands = [result_var, function, arguments_dict]
            arguments: dict[str, Reference] = call_instr.operands[2]
            assign_instrs = self._build_param_assigns(func_sym, arguments)

            # 构建 IRJump 指令
            jump_instr = IRJump(loop_scope_name)

            # 从后向前替换，先替换 return（索引更大），再替换 call
            # 替换 IRReturn → IRJump
            instructions[return_idx] = jump_instr

            # 替换 IRCall → 参数重赋值序列
            # 先删除 call 指令，再在原位插入所有 assign 指令
            del instructions[call_idx]
            for offset, assign_instr in enumerate(assign_instrs):
                instructions.insert(call_idx + offset, assign_instr)

            # 由于在 call_idx 处删 1 插 N，后续索引偏移 = N - 1
            delta = len(assign_instrs) - 1
            end_idx_offset += delta

            self._changed = True

        # ── Step 4：插入 TCO 循环作用域的 SCOPE_BEGIN（在函数体 SCOPE_BEGIN 之后）
        tco_scope_begin = IRScopeBegin(loop_scope_name, StructureType.LOOP_CHECK)
        insert_pos = func_scope_begin_idx + 1
        instructions.insert(insert_pos, tco_scope_begin)

        # 插入一条 SCOPE_BEGIN 使后续所有索引 +1
        end_idx_offset += 1

        # ── Step 5：插入 TCO 循环作用域的 SCOPE_END（在函数体 SCOPE_END 之前）
        actual_end_idx = func_scope_end_idx + end_idx_offset
        tco_scope_end = IRScopeEnd(loop_scope_name, StructureType.LOOP_CHECK)
        instructions.insert(actual_end_idx, tco_scope_end)

    # ── 辅助方法 ──────────────────────────────────────────────────────────────

    @staticmethod
    def _build_param_assigns(
            func: Function,
            arguments: dict[str, Reference],
    ) -> list[IRInstruction]:
        """
        将 IRCall 的 arguments 映射回函数形参变量，生成 IRAssign 序列。

        Args:
            func: 被调用函数（即当前函数自身）的符号对象
            arguments: IRCall 携带的实参字典 {param_name: Reference}

        Returns:
            IRAssign 指令列表，顺序与函数参数声明顺序一致
        """
        assigns = []
        for param in func.params:
            param_name = param.var.get_name()
            if param_name in arguments:
                ref = arguments[param_name]
                assigns.append(IRAssign(param.var, ref))
        return assigns

    def _find_function_scope_begin(self, func_name: str) -> int | None:
        """
        在 IRFunction(func_name) 之后找到第一个 SCOPE_BEGIN 的索引。

        Args:
            func_name: 函数名

        Returns:
            SCOPE_BEGIN 指令的索引，找不到则返回 None
        """
        instructions = self.builder.get_instructions()
        in_target_func = False

        for i, instr in enumerate(instructions):
            if instr.opcode is IROpCode.FUNCTION:
                func: Function = instr.operands[0]
                in_target_func = (func.get_name() == func_name)
                continue

            if in_target_func and instr.opcode is IROpCode.SCOPE_BEGIN:
                return i

        return None

    def _find_function_scope_end(self, scope_begin_idx: int) -> int | None:
        """
        给定函数体 SCOPE_BEGIN 的索引，找到其对应的 SCOPE_END 的索引。

        通过括号匹配（depth 计数）实现。

        Args:
            scope_begin_idx: SCOPE_BEGIN 指令的索引

        Returns:
            对应 SCOPE_END 指令的索引，找不到则返回 None
        """
        instructions = self.builder.get_instructions()
        depth = 0

        for i in range(scope_begin_idx, len(instructions)):
            instr = instructions[i]
            if instr.opcode is IROpCode.SCOPE_BEGIN:
                depth += 1
            elif instr.opcode is IROpCode.SCOPE_END:
                depth -= 1
                if depth == 0:
                    return i

        return None
