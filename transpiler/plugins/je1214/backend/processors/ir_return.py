# coding=utf-8
"""
IRReturn 指令处理器
"""
from transpiler.core.backend import ir_processor, IRProcessor, GenerationContext
from transpiler.core.enums import StructureType
from transpiler.core.instructions import IRInstruction, IROpCode
from transpiler.core.symbols import Variable, Constant, Literal
from ..backend import JE1214Backend
from ..commands import ScoreboardBuilder, ReturnBuilder
from ..commands.copy import Copy
from ..commands.tools import DataPath, StorageLocation


@ir_processor(JE1214Backend, IROpCode.RETURN)
class IRReturnProcessor(IRProcessor):
    def process(self, instruction: IRInstruction, context: GenerationContext):
        return_value: Variable | Constant | Literal = instruction.get_operands()[0].value
        # 查找需要退出的函数作用域
        for scope in reversed(context.scope_stack):
            if scope.scope_type == StructureType.FUNCTION:
                function_scope = scope
                current_path = context.current_scope.get_absolute_path()
                func_path = function_scope.get_absolute_path()
                break
        else:
            print("[Error] No function scope found")
            context.add_command("# No function scope found")
            return
        if return_value:  # 如果存在返回值
            return_path = DataPath(
                f"return_{hash(func_path)}",
                context.objective,
                StorageLocation.get_storage(return_value.dtype)
            )
            if isinstance(return_value, Literal):
                context.current_scope.add_command(
                    Copy.copy_literals(
                        return_path,
                        return_value.value,
                    )
                )
            else:
                context.current_scope.add_command(
                    Copy.copy(
                        return_path,
                        DataPath(
                            context.current_scope.get_symbol_path(return_value.name),
                            context.objective,
                            StorageLocation.get_storage(return_value.dtype)
                        )
                    )
                )

        # 标记函数已返回
        function_scope.flags[f"return:{func_path}"] = current_path.count(".") - func_path.count(".")

        context.current_scope.add_command(
            ScoreboardBuilder.set_score(
                f"#return_{func_path}",
                context.objective,
                1
            )
        )
        # 退出作用域
        context.current_scope.add_command(ReturnBuilder.return_value(0))
