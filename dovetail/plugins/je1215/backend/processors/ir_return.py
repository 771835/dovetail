# coding=utf-8
"""
IRReturn 指令处理器
"""
from typing import Optional

from dovetail.core.backend import ir_processor, IRProcessor, GenerationContext
from dovetail.core.enums import StructureType
from dovetail.core.instructions import IRInstruction, IROpCode
from dovetail.core.symbols import Reference
from dovetail.utils.logger import get_logger
from ..backend import JE1215Backend
from ..commands import ScoreboardBuilder, ReturnBuilder
from ..commands.copy import Copy
from ..commands.tools import DataPath, StorageLocation

logger = get_logger(__name__)

@ir_processor(JE1215Backend, IROpCode.RETURN)
class IRReturnProcessor(IRProcessor):
    def process(self, instruction: IRInstruction, context: GenerationContext):
        return_value_ref: Optional[Reference] =  instruction.operands[0] if instruction.operands else None
        # 查找需要退出的函数作用域
        for scope in reversed(context.scope_stack):
            if scope.scope_type == StructureType.FUNCTION:
                function_scope = scope
                current_path = context.current_scope.get_absolute_path()
                func_path = function_scope.get_absolute_path()
                break
        else:
            logger.error("找不到需要函数作用域")
            context.add_command("# Can't find a function scope to return")
            return
        if return_value_ref:  # 如果存在返回值
            return_path = DataPath(
                f"return_{hash(func_path)}",
                context.objective,
                StorageLocation.get_storage(return_value_ref.dtype)
            )
            if return_value_ref.is_literal():
                context.current_scope.add_command(
                    Copy.copy_literals(
                        return_path,
                        return_value_ref.value.value,
                    )
                )
            else:
                context.current_scope.add_command(
                    Copy.copy(
                        return_path,
                        DataPath.from_symbol(context, return_value_ref)
                    )
                )

        # 标记函数已返回
        context.current_scope.flags[f"return:{func_path}"] = current_path.count(".") - func_path.count(".")

        context.current_scope.add_command(
            "# 设置返回哨兵值"
        )
        context.current_scope.add_command(
            ScoreboardBuilder.set_score(
                f"#return_{func_path}",
                context.objective,
                1
            )
        )
        # 退出作用域
        context.current_scope.add_command(ReturnBuilder.return_value(0))
