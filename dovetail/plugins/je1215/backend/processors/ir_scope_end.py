# coding=utf-8
"""
IRScopeEnd 指令处理器
"""
from dovetail.core.backend import ir_processor, IRProcessor, GenerationContext
from dovetail.core.enums import StructureType
from dovetail.core.instructions import IROpCode
from ..commands import DataBuilder
from ..backend import JE1215Backend


@ir_processor(JE1215Backend, IROpCode.SCOPE_END)
class IRScopeEndProcessor(IRProcessor):
    def process(self, instruction, context: GenerationContext):
        space_type: StructureType = instruction.operands[1]
        if space_type not in (StructureType.CLASS, StructureType.ENUM):
            if context.config.debug:
                context.add_command("# 清理作用域的变量")
            context.add_command(DataBuilder.remove_storage(context.objective, context.current_scope.get_absolute_path()))
        context.pop_scope()
