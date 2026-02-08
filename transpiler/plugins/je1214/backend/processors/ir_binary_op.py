# coding=utf-8
"""
IROp 指令处理器
"""
from transpiler.core.backend import ir_processor, IRProcessor, GenerationContext
from transpiler.core.config import get_project_logger
from transpiler.core.enums import BinaryOps, DataType
from transpiler.core.enums.types import DataTypeBase
from transpiler.core.instructions import IRInstruction, IROpCode
from transpiler.core.symbols import Constant, Literal, Variable
from ..backend import JE1214Backend
from ..commands.binary_op import BinaryOp
from ..commands.strlib import strcat
from ..commands.tools import DataPath, StorageLocation


@ir_processor(JE1214Backend, IROpCode.BINARY_OP)
class IROpProcessor(IRProcessor):  # 仅应支持基本类型运算
    def process(self, instruction: IRInstruction, context: GenerationContext):
        result_path = self._get_symbol_path(instruction.operands[0], context)
        op: BinaryOps = instruction.operands[1]

        left: Variable | Constant | Literal = instruction.operands[2].value
        left_dtype: DataTypeBase = left.dtype
        left_path = self._get_symbol_path(left, context)

        right: Variable | Constant | Literal = instruction.operands[3].value
        right_dtype: DataTypeBase = right.dtype
        right_path = self._get_symbol_path(right, context)

        # 当两者类型为int或boolean时
        if left_dtype.is_subclass_of(DataType.INT) and right_dtype.is_subclass_of(DataType.INT):
            context.add_commands(BinaryOp.op_all(result_path, op, left_path, right_path))
        elif left_dtype == DataType.STRING == right_dtype:
            context.add_commands(strcat(result_path, left_path, right_path))
        else:
            get_project_logger().error(f"unsupported operand type(s) for {op}: '{left_dtype}' and '{right_dtype}'")

    def _get_symbol_path(self, value: Variable | Constant | Literal,
                         context: GenerationContext) -> DataPath | int | bool | str:
        if isinstance(value, Literal):
            return value.value
        return DataPath(
            context.current_scope.get_symbol_path(value),
            context.objective,
            StorageLocation.get_storage(value.dtype)
        )
