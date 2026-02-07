# coding=utf-8
"""
IRCall 指令处理器
"""
from transpiler.core.backend import ir_processor, IRProcessor, GenerationContext
from transpiler.core.enums import FunctionType, DataType
from transpiler.core.instructions import IRInstruction, IROpCode
from transpiler.core.symbols import Variable, Constant, Function, Literal, Reference
from ..backend import JE1214Backend
from ..commands import FunctionBuilder, Copy, DataPath, StorageLocation
from ..commands.builtins import CommandRegistry


@ir_processor(JE1214Backend, IROpCode.CALL)
class IRCallProcessor(IRProcessor):
    def process(self, instruction: IRInstruction, context: GenerationContext):
        result: Variable | Constant = instruction.get_operands()[0]
        func: Function = instruction.get_operands()[1]
        args: dict[str, Reference[Variable | Constant | Literal]] = instruction.get_operands()[2]
        if func.function_type == FunctionType.BUILTIN:
            # 搜索内置函数
            CommandRegistry.get(func.name).handle(result, context, args)
            return

        # 查找将要调用的函数的作用域路径
        if func.function_type == FunctionType.FUNCTION_UNIMPLEMENTED:  # 如果函数为向前引用则推测作用域地址

            func_path = f"{context.current_scope.resolve_symbol_scope(func.name).get_absolute_path()}.{func.name}"
        else:
            func_path = context.current_scope.resolve_scope(func.name).get_absolute_path()

        # 填充参数
        for (param_name, arg), param in zip(args.items(), func.params):
            if arg.is_literal():
                context.current_scope.add_command(
                    Copy.copy_literals(
                        DataPath(
                            f"{func_path}.{param_name}",
                            context.objective,
                            StorageLocation.get_storage(param.get_data_type())
                        ),
                        arg.value.value
                    )
                )
            else:
                context.current_scope.add_command(
                    Copy.copy(
                        DataPath(
                            f"{func_path}.{param_name}",
                            context.objective,
                            StorageLocation.get_storage(param.get_data_type())
                        ),
                        DataPath(
                            context.current_scope.get_symbol_path(arg.get_name()),
                            context.objective,
                            StorageLocation.get_storage(arg.get_data_type())
                        )
                    )
                )

        # 调用函数
        context.current_scope.add_command(
            FunctionBuilder.run(
                f"{context.namespace}:{func_path.replace('.', '/')}"
            )
        )
        # 处理返回值
        if func.return_type != DataType.NULL and result is not None:
            context.current_scope.add_command(
                Copy.copy(
                    DataPath(
                        context.current_scope.get_symbol_path(result.name),
                        context.objective,
                        StorageLocation.get_storage(result.dtype)
                    ),
                    DataPath(
                        f"return_{hash(func_path)}",
                        context.objective,
                        StorageLocation.get_storage(func.return_type)
                    )
                )
            )
