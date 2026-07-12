# coding=utf-8
"""
IRDeclare 指令处理器
"""
from dovetail.core.backend import ir_processor, IRProcessor, GenerationContext
from dovetail.core.enums import PrimitiveDataType
from dovetail.core.enums.datatypes import ArrayType,  DictType, ListType
from dovetail.core.instructions import IRInstruction, IROpCode
from dovetail.core.symbols import Variable
from ..backend import JE1214Backend
from ..commands import DataBuilder


@ir_processor(JE1214Backend, IROpCode.DECLARE)
class IRDeclareProcessor(IRProcessor):
    def process(self, instruction: IRInstruction, context: GenerationContext):
        var: Variable = instruction.operands[0]
        context.current_scope.add_symbol(var)

        # 对复合类型进行初始化
        if isinstance(var.dtype, ArrayType):
            if var.dtype.dtype == PrimitiveDataType.BOOLEAN: # 由于语言中没有long的类型，故暂不允许设置[L;]的数组
                initial_value = "[B;]"
            else:
                initial_value = "[I;]"

            # /data modify storage {target} {path} set value {value}
            context.current_scope.add_command(
                DataBuilder.modify_storage_set_value(
                    context.current_scope.get_symbol_path(var),
                    context.objective,
                    initial_value
                )
            )
        elif isinstance(var.dtype, DictType):
            # /data modify storage {target} {path} set value {}
            context.current_scope.add_command(
                DataBuilder.modify_storage_set_value(
                    context.current_scope.get_symbol_path(var),
                    context.objective,
                    "{}"
                )
            )
        elif isinstance(var.dtype, ListType):
            # /data modify storage {target} {path} set value []
            context.current_scope.add_command(
                DataBuilder.modify_storage_set_value(
                    context.current_scope.get_symbol_path(var),
                    context.objective,
                    "[]"
                )
            )
