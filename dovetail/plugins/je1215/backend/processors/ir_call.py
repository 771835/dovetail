# coding=utf-8
"""
IRCall 指令处理器
"""
from os import name

from dovetail.core.backend import ir_processor, IRProcessor, GenerationContext
from dovetail.core.enums import FunctionType, PrimitiveDataType
from dovetail.core.instructions import IRInstruction, IROpCode
from dovetail.core.symbols import Variable, Function, Literal, Reference
from ..backend import JE1214Backend
from ..commands import FunctionBuilder, Copy, DataPath, StorageLocation
from ..commands.builtins import CommandRegistry


@ir_processor(JE1214Backend, IROpCode.CALL)
class IRCallProcessor(IRProcessor):
    def process(self, instruction: IRInstruction, context: GenerationContext):
        result: Variable = instruction.get_operands()[0]
        func: Function = instruction.get_operands()[1]
        args: dict[str, Reference[Variable | Literal]] = instruction.get_operands()[2]

        if func.function_type == FunctionType.BUILTIN:
            CommandRegistry.get(func.name).call(result, context, args)
            return
        func_path = self._resolve_func_path(func, context)

        self._fill_arguments(args, func.params, func_path, context)

        self._call_function(func_path, context)

        self._handle_return_value(result, func, func_path, context)

    def _resolve_func_path(self, func: Function, context: GenerationContext) -> str:
        """解析函数的作用域路径"""
        if func.function_type == FunctionType.FUNCTION_UNIMPLEMENTED:
            return f"{context.current_scope.resolve_symbol_scope(func.name).get_absolute_path()}.{func.name}"
        return context.current_scope.resolve_scope(func.name).get_absolute_path()

    def _fill_arguments(
            self,
            args: dict[str, Reference[Variable | Literal]],
            params,
            func_path: str,
            context: GenerationContext,
    ):
        """将实参复制到被调用函数的参数作用域"""
        for (param_name, arg), param in zip(args.items(), params):
            target = DataPath(
                f"{func_path}.{param_name}",
                context.objective,
                StorageLocation.get_storage(param.get_dtype()),
            )
            source = (
                arg.value.value
                if arg.is_literal()
                else DataPath(
                    context.current_scope.get_symbol_path(arg.get_name()),
                    context.objective,
                    StorageLocation.get_storage(arg.get_dtype()),
                )
            )
            context.current_scope.add_command(Copy.copy_all(target, source))

    def _call_function(self, func_path: str, context: GenerationContext):
        """生成函数调用命令"""
        context.current_scope.add_command(
            FunctionBuilder.run(f"{context.namespace}:{func_path.replace('.', '/')}")
        )

    def _handle_return_value(
            self,
            result: Variable | None,
            func: Function,
            func_path: str,
            context: GenerationContext,
    ):
        """处理函数返回值的复制"""
        if func.return_type != PrimitiveDataType.NULL_TYPE and result is not None:
            context.current_scope.add_command(
                Copy.copy(
                    DataPath(
                        context.current_scope.get_symbol_path(result.name),
                        context.objective,
                        StorageLocation.get_storage(result.dtype),
                    ),
                    DataPath(
                        f"return_{hash(func_path)}",
                        context.objective,
                        StorageLocation.get_storage(func.return_type),
                    ),
                )
            )