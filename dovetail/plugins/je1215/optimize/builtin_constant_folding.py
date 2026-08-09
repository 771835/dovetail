# coding=utf-8
from typing import cast, Optional

from dovetail.core.compile_config import CompileConfig
from dovetail.core.ir_builder import IRBuilder

from dovetail.core.optimize.base import IROptimizationPass
from dovetail.core.optimize.pass_metadata import PassMetadata, PassPhase
from dovetail.core.optimize.pass_registry import register_pass
from dovetail.core.enums import OptimizationLevel, ValueType, FunctionType
from dovetail.core.instructions import IROpCode, IRAssign
from dovetail.core.symbols import Reference, Function, Variable
from dovetail.utils.constants_operator import number_to_int32
from dovetail.utils.naming import NameNormalizer


@register_pass(PassMetadata(
    name="builtin_constant_folding",
    display_name="内建函数常量折叠",
    description="对全常量参数的纯内建函数调用进行编译时求值",
    level=OptimizationLevel.O1,
    phase=PassPhase.TRANSFORM,
    depends_on=("constant_folding",),  # 先让符号传播跑一轮
    provided_features=("simplified_arithmetic",),
))
class BuiltinConstantFoldingPass(IROptimizationPass):

    def __init__(self, builder: IRBuilder, config: CompileConfig):
        self.builder = builder
        self.config = config

    def execute(self) -> bool:
        changed = False
        iterator = self.builder.__iter__()

        while True:
            try:
                instr = next(iterator)
            except StopIteration:
                break

            if instr.opcode != IROpCode.CALL:
                continue

            result, func, args = cast(tuple[Optional[Variable], Function, dict[str, Reference]], instr.operands)

            # 检查是否为内置函数
            if func.function_type != FunctionType.BUILTIN:
                continue

            # 检查所有参数是否为字面量
            if not all(
                    ref.value_type == ValueType.LITERAL
                    for ref in args.values()
            ):
                continue

            # 求值
            arg_values = {name: ref.value.value for name, ref in args.items()}

            optimized = True
            try:
                match NameNormalizer.denormalize(func.name):
                    case "abs":
                        if result:
                            new_val = number_to_int32(abs(arg_values["value"]))
                            iterator.set_current(IRAssign(result, Reference.literal(new_val)))
                        else:
                            iterator.remove_current()
                    case "min":
                        if result:
                            new_val = number_to_int32(min(arg_values["a"], arg_values["b"]))
                            iterator.set_current(IRAssign(result, Reference.literal(new_val)))
                        else:
                            iterator.remove_current()
                    case "max":
                        if result:
                            new_val = number_to_int32(min(arg_values["a"], arg_values["b"]))
                            iterator.set_current(IRAssign(result, Reference.literal(new_val)))
                        else:
                            iterator.remove_current()
                    case "strcat_fast":
                        if result:
                            new_val = str(arg_values["a"]) + str(arg_values["b"])
                            iterator.set_current(IRAssign(result, Reference.literal(new_val)))
                        else:
                            iterator.remove_current()
                    case "strlen":
                        if result:
                            new_val = len(str(arg_values["s"]))
                            iterator.set_current(IRAssign(result, Reference.literal(new_val)))
                        else:
                            iterator.remove_current()
                    case "substring":
                        if result:
                            new_val = str(arg_values["s"])[int(arg_values["start"]):int(arg_values["end"])]
                            iterator.set_current(IRAssign(result, Reference.literal(new_val)))
                        else:
                            iterator.remove_current()
                    case _:
                        optimized = False

            except (TypeError, ValueError, ZeroDivisionError):
                continue

            changed = changed or optimized

        return changed
