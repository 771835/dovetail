# coding=utf-8
"""
IRCall 指令处理器
"""
from transpiler.core.backend import ir_processor, IRProcessor, GenerationContext
from transpiler.core.enums import FunctionType, DataType
from transpiler.core.instructions import IRInstruction, IROpCode
from transpiler.core.symbols import Variable, Constant, Function, Literal, Reference
from ..backend import JE1214Backend
from ..commands import FunctionBuilder
from ..commands.builtins import CommandRegistry
from ..commands.copy import Copy
from ..commands.tools import DataPath, StorageLocation


@ir_processor(JE1214Backend, IROpCode.CALL)
class IRCallProcessor(IRProcessor):
    def process(self, instruction: IRInstruction, context: GenerationContext):
        result: Variable | Constant = instruction.get_operands()[0]
        func: Function = instruction.get_operands()[1]
        args: dict[str, Reference[Variable | Constant | Literal]] = instruction.get_operands()[2]
        if func.function_type == FunctionType.BUILTIN:
            CommandRegistry.get(func.name).handle(result, context, args)
            # TODO 内置函数支持
            # BuiltinFuncMapping.get(func.get_name())(result, self, args)
            return
        jump_scope = context.current_scope.resolve_scope(func.name)
        for (param_name, arg), param in zip(args.items(), func.params):
            if arg.is_literal():
                context.current_scope.add_command(
                    Copy.copy_literals(
                        DataPath(
                            jump_scope.get_symbol_path(param_name),
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
                            jump_scope.get_symbol_path(param_name),
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
        context.current_scope.add_command(
            FunctionBuilder.run(
                f"{context.namespace}:{jump_scope.get_absolute_path('/')}"
            )
        )
        if func.return_type != DataType.NULL and result is not None:
            context.current_scope.add_command(
                Copy.copy(
                    DataPath(
                        context.current_scope.get_symbol_path(result.name),
                        context.objective,
                        StorageLocation.get_storage(result.dtype)
                    ),
                    DataPath(
                        f"return_{hash(jump_scope.get_absolute_path())}",
                        context.objective,
                        StorageLocation.get_storage(func.return_type)
                    )
                )
            )
