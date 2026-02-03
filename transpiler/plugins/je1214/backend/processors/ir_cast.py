# coding=utf-8
"""
IRCast 指令处理器
"""
from transpiler.core.backend import ir_processor, IRProcessor, GenerationContext
from transpiler.core.config import get_project_logger
from transpiler.core.enums import DataType
from transpiler.core.instructions import IRInstruction, IROpCode
from transpiler.core.symbols import Variable, Constant, Class, Reference, Literal
from ..backend import JE1214Backend
from ..commands.strlib import to_str, to_int
from ..commands.tools import DataPath, StorageLocation


@ir_processor(JE1214Backend, IROpCode.CAST)
class IRCastProcessor(IRProcessor):
    def process(self, instruction: IRInstruction, context: GenerationContext):
        result: Variable | Constant = instruction.operands[0]
        dtype: DataType | Class = instruction.operands[1]
        value: Reference[Variable | Constant | Literal] = instruction.operands[2]

        result_path = DataPath(
            context.current_scope.get_symbol_path(result),
            context.objective,
            StorageLocation.get_storage(result.dtype)
        )
        value_path = DataPath(
            context.current_scope.get_symbol_path(value),
            context.objective,
            StorageLocation.get_storage(value.get_data_type())
        ) if not value.is_literal() else value.value.value

        # int -> str
        if value.get_data_type().is_subclass_of(DataType.INT) and dtype == DataType.STRING:
            context.add_commands(to_str(result_path, value_path))
        elif value == DataType.STRING and dtype.is_subclass_of(DataType.INT):
            # str -> int
            context.add_commands(to_int(result_path, value_path))
        else:
            get_project_logger().error("Unsupported data type")
