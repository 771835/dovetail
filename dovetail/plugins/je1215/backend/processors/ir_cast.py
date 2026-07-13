# coding=utf-8
"""
IRCast 指令处理器
"""
from dovetail.core.backend import ir_processor, IRProcessor, GenerationContext
from dovetail.core.enums import PrimitiveDataType
from dovetail.core.instructions import IRInstruction, IROpCode
from dovetail.core.symbols import Variable, Class, Reference, Literal
from dovetail.utils.logger import get_logger
from dovetail.utils.naming import NameNormalizer
from ..backend import JE1215Backend
from ..commands import CommandRegistry
from ..commands.strlib import to_str
from ..commands.tools import DataPath

logger = get_logger(__name__)

@ir_processor(JE1215Backend, IROpCode.CAST)
class IRCastProcessor(IRProcessor):
    def process(self, instruction: IRInstruction, context: GenerationContext):
        result: Variable = instruction.operands[0]  # NOQA
        dtype: PrimitiveDataType | Class = instruction.operands[1]  # NOQA
        value: Reference[Variable | Literal] = instruction.operands[2]  # NOQA

        result_path = DataPath.from_symbol(context, result)
        value_path = DataPath.from_symbol(context, value) \
            if not value.is_literal() else value.value.value

        if value.get_dtype().is_subclass_of(PrimitiveDataType.INT) and dtype == PrimitiveDataType.STRING:
            # int -> str
            assert isinstance(value_path, (DataPath, int))
            context.add_commands(to_str(result_path, value_path))
        elif value.dtype == PrimitiveDataType.STRING and dtype.is_subclass_of(PrimitiveDataType.INT):
            # str -> int
            assert isinstance(value_path, (DataPath, str))
            CommandRegistry.get(NameNormalizer.normalize("to_integer")).call(result,context, {"value":value} )
        else:
            logger.error(f"未知的类型转换: 从 '{value.dtype}' 转换为 '{dtype}'")
