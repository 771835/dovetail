# coding=utf-8
"""
IRAssign 指令处理器
"""
from transpiler.core.backend import ir_processor, IRProcessor, GenerationContext
from transpiler.core.instructions import IRInstruction, IROpCode
from ..backend import JE1214Backend
from ..commands.copy import Copy
from ..commands.tools import DataPath, StorageLocation


@ir_processor(JE1214Backend, IROpCode.ASSIGN)
class IRAssignProcessor(IRProcessor):
    def process(self, instruction: IRInstruction, context: GenerationContext):
        target, source = instruction.operands
        context.add_command(
            Copy.copy(
                DataPath(
                    context.current_scope.get_symbol_path(target.get_name()),
                    context.objective,
                    StorageLocation.get_storage(target.dtype)
                ),
                DataPath(
                    context.current_scope.get_symbol_path(source.get_name()),
                    context.objective,
                    StorageLocation.get_storage(source.get_data_type())
                ),

            )
        )
