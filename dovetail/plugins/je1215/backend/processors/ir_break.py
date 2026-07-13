# coding=utf-8
"""
IRBreak 指令处理器
"""
from dovetail.core.backend import ir_processor, IRProcessor, GenerationContext
from dovetail.core.instructions import IRInstruction, IROpCode
from dovetail.utils.logger import get_logger
from ..backend import JE1215Backend
from ..commands import ReturnBuilder, ScoreboardBuilder

logger = get_logger(__name__)

@ir_processor(JE1215Backend, IROpCode.BREAK)
class IRBreakProcessor(IRProcessor):
    def process(self, instruction: IRInstruction, context: GenerationContext):
        loop_check_name = instruction.get_operands()[0]
        # 查找需要退出的作用域
        for scope in reversed(context.scope_stack):
            if scope.name == loop_check_name:
                loop_check_scope = scope
                current_path = context.current_scope.get_absolute_path()
                loop_check_path = loop_check_scope.get_absolute_path()
                break
        else:
            logger.error("找不到需要被跳出的循环作用域")
            context.add_command("# Can't find a loop scope to break out of")
            return
        # 标记循环已跳出
        context.current_scope.flags[f"break:{loop_check_path}"] = current_path.count(".") - loop_check_path.count(".")

        context.current_scope.add_command(
            ScoreboardBuilder.set_score(
                f"#break_{loop_check_path}",
                context.objective,
                1
            )
        )
        # 退出作用域
        context.current_scope.add_command(ReturnBuilder.return_value(0))
