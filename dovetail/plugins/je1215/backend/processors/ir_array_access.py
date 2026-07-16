# coding=utf-8
"""
IRArrayAccess 指令处理器
"""
from typing import cast

from dovetail.core.backend import ir_processor, IRProcessor, GenerationContext
from dovetail.core.instructions import IRInstruction, IROpCode
from dovetail.core.symbols import Variable, Reference
from dovetail.utils.naming import NameNormalizer
from ..backend import JE1215Backend
from ..commands import Copy, DataPath, StorageLocation
from ..commands.builtins import CommandRegistry


@ir_processor(JE1215Backend, IROpCode.INDEX_GET)
class IRArrayAccessProcessor(IRProcessor):
    def process(self, instruction: IRInstruction, context: GenerationContext):
        result, array, index = cast("tuple[Variable, Reference, Reference]", instruction.operands)


        if index.is_literal():
            array_path = context.current_scope.get_symbol_path(array)
            # 生成复制数据的指令
            context.add_command(Copy.copy(
                DataPath.from_symbol(context, result),
                DataPath(
                    f"{array_path}[{index.value.value}]",
                    context.objective,
                    StorageLocation.STORAGE
                )
            ))
            return
        else: # 调用宏函数
            if StorageLocation.get_storage(result.dtype) == StorageLocation.STORAGE: # (string等数据)
                CommandRegistry.get(NameNormalizer.normalize("array_access_to_storage")).call(
                    result,
                    context,
                    {
                        "array": array,
                        "index": index
                    }
                )
            else: # SCORE (int, bool等值)
                CommandRegistry.get(NameNormalizer.normalize("array_access_to_score")).call(
                    result,
                    context,
                    {
                        "array": array,
                        "index": index
                    }
                )