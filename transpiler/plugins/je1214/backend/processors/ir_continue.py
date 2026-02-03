# coding=utf-8
"""
IRContinue 指令处理器
"""
from transpiler.core.backend import ir_processor, IRProcessor, GenerationContext
from transpiler.core.config import get_project_logger
from transpiler.core.instructions import IRInstruction, IROpCode
from ..backend import JE1214Backend
from ..commands import ReturnBuilder, ScoreboardBuilder


@ir_processor(JE1214Backend, IROpCode.CONTINUE)
class IRContinueProcessor(IRProcessor):
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
            get_project_logger().error("No loop scope found")
            context.add_command("# No loop scope found")
            return
        # 标记循环继续
        context.current_scope.flags[f"continue:{loop_check_path}"] = current_path.count(".") - loop_check_path.count(
            ".") - 1

        context.current_scope.add_command(
            ScoreboardBuilder.set_score(
                f"#continue_{loop_check_path}",
                context.objective,
                1
            )
        )
        # 退出作用域
        context.current_scope.add_command(ReturnBuilder.return_value(0))
