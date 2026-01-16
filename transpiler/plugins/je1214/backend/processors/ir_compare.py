# coding=utf-8
"""
IRCompare 指令处理器
"""
from transpiler.core.backend import ir_processor, IRProcessor, GenerationContext
from transpiler.core.enums import ValueType
from transpiler.core.instructions import IRInstruction, IROpCode
from ..backend import JE1214Backend
from ..commands.compare import Compare
from ..commands.tools import DataPath, StorageLocation


@ir_processor(JE1214Backend, IROpCode.COMPARE)
class IRCompareProcessor(IRProcessor):
    def process(self, instr: IRInstruction, context: GenerationContext):
        result, op, a, b = instr.operands
        result_path = DataPath(
            context.current_scope.get_symbol_path(result.get_name()),
            context.objective,
            StorageLocation.SCORE
        )
        if a.value_type == ValueType.LITERAL:
            a_path = a.value.value
        else:
            a_path = DataPath(
                context.current_scope.get_symbol_path(a.get_name()),
                context.objective,
                StorageLocation.get_storage(a.get_data_type())
            )
        if b.value_type == ValueType.LITERAL:
            b_path = b.value.value
        else:
            b_path = DataPath(
                context.current_scope.get_symbol_path(b.get_name()),
                context.objective,
                StorageLocation.get_storage(b.get_data_type())
            )
        context.add_commands(
            Compare.compare(
                result_path,
                op,
                a_path,
                b_path
            )
        )
