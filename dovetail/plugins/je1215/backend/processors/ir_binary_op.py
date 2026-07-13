# coding=utf-8
"""
IROp 指令处理器
"""
from typing import cast

from dovetail.core.backend import ir_processor, IRProcessor, GenerationContext
from dovetail.core.enums import BinaryOps, PrimitiveDataType
from dovetail.core.enums.datatypes import DataTypeBase
from dovetail.core.instructions import IRInstruction, IROpCode
from dovetail.core.symbols import Literal, Variable
from dovetail.utils.logger import get_logger
from ..backend import JE1215Backend
from ..commands.binary_op import BinaryOp
from ..commands.strlib import strcat
from ..commands.tools import DataPath

logger = get_logger(__name__)


@ir_processor(JE1215Backend, IROpCode.BINARY_OP)
class IROpProcessor(IRProcessor):  # 仅应支持基本类型运算
    def process(self, instruction: IRInstruction, context: GenerationContext):
        result_path = cast(DataPath, self._get_symbol_path(instruction.operands[0], context))
        op: BinaryOps = instruction.operands[1]

        left: Variable | Literal = instruction.operands[2].value
        left_dtype: DataTypeBase = left.dtype
        left_path = self._get_symbol_path(left, context)

        right: Variable | Literal = instruction.operands[3].value
        right_dtype: DataTypeBase = right.dtype
        right_path = self._get_symbol_path(right, context)

        # 当两者类型为int或boolean时
        if left_dtype.is_subclass_of(PrimitiveDataType.INT) and right_dtype.is_subclass_of(PrimitiveDataType.INT):
            context.add_commands(
                BinaryOp.op_all(result_path, op, cast(int | bool, left_path), cast(int | bool, right_path)))
        elif left_dtype == PrimitiveDataType.STRING == right_dtype:
            context.add_commands(strcat(result_path, cast(str, left_path), cast(str, right_path)))
        else:
            logger.error(f"unsupported operand type(s) for {op}: '{left_dtype}' and '{right_dtype}'")

    def _get_symbol_path(self, data: Variable | Literal,
                         context: GenerationContext) -> DataPath | int | bool | str | None:
        """
        根据符号类型获取对应信息

        对于变量，返回其路径
        对于字面量，返回其值

        Args:
            data: 变量或字面量
            context: 后端生成上下文

        Returns:
            数据路径或字面量的值
        """
        if isinstance(data, Literal):
            return data.value
        return DataPath.from_symbol(context, data)
