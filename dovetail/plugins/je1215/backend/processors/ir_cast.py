# coding=utf-8
"""
IRCast 指令处理器
"""
from dovetail.core.backend import ir_processor, IRProcessor, GenerationContext
from dovetail.core.config import get_project_logger
from dovetail.core.enums import PrimitiveDataType
from dovetail.core.instructions import IRInstruction, IROpCode
from dovetail.core.symbols import Variable, Class, Reference, Literal
from ..backend import JE1214Backend
from ..commands.strlib import to_str, to_int
from ..commands.tools import DataPath, StorageLocation


@ir_processor(JE1214Backend, IROpCode.CAST)
class IRCastProcessor(IRProcessor):
    def process(self, instruction: IRInstruction, context: GenerationContext):
        result: Variable = instruction.operands[0]  # NOQA
        dtype: PrimitiveDataType | Class = instruction.operands[1]  # NOQA
        value: Reference[Variable | Literal] = instruction.operands[2]  # NOQA

        result_path = DataPath(
            context.current_scope.get_symbol_path(result),
            context.objective,
            StorageLocation.get_storage(result.dtype)
        )
        value_path = DataPath(
            context.current_scope.get_symbol_path(value),
            context.objective,
            StorageLocation.get_storage(value.get_dtype())
        ) if not value.is_literal() else value.value.value

        if value.get_dtype().is_subclass_of(PrimitiveDataType.INT) and dtype == PrimitiveDataType.STRING:
            # int -> str
            assert isinstance(value_path, (DataPath, int))
            context.add_commands(to_str(result_path, value_path))
        elif value.dtype == PrimitiveDataType.STRING and dtype.is_subclass_of(PrimitiveDataType.INT):
            # str -> int
            assert isinstance(value_path, (DataPath, str))
            context.add_commands(to_int(result_path, value_path, context.namespace))
        else:
            get_project_logger().error(f"Unsupported type conversion: Convert from {value.dtype} to {dtype}")
