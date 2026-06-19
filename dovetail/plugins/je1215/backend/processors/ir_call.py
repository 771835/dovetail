# coding=utf-8
"""
IRCall 指令处理器
"""

from dovetail.core.backend import ir_processor, IRProcessor, GenerationContext
from dovetail.core.enums import FunctionType, PrimitiveDataType
from dovetail.core.instructions import IRInstruction, IROpCode
from dovetail.core.symbols import Variable, Function, Literal, Reference
from ..backend import JE1214Backend
from ..commands import FunctionBuilder, Copy, DataPath, StorageLocation, LiteralPoolTools
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
        elif func.function_type == FunctionType.EXTERN:
            self._handle_ffi(result, func, args, func.all_metadata(), context)

            return

        func_path = self._resolve_func_path(func, context)

        self._fill_arguments(args, func.params, context.objective, func_path, context)

        self._call_function(context.namespace, func_path, context)

        self._handle_return_value(result, func, context.objective, func_path, context)

    def _resolve_func_path(self, func: Function, context: GenerationContext) -> str:
        """解析函数的作用域路径"""
        if func.function_type == FunctionType.FUNCTION_UNIMPLEMENTED:
            return f"{context.current_scope.resolve_symbol_scope(func.name).get_absolute_path()}.{func.name}"
        return context.current_scope.resolve_scope(func.name).get_absolute_path()

    def _fill_arguments(
            self,
            args: dict[str, Reference[Variable | Literal]],
            params,
            objective: str,
            func_path: str,
            context: GenerationContext,
    ):
        """将实参复制到被调用函数的参数作用域"""
        for (param_name, arg), param in zip(args.items(), params):
            target = DataPath(
                f"{func_path}.{param_name}",
                objective,
                StorageLocation.get_storage(param.get_dtype()),
            )
            source = (
                arg.value.value
                if arg.is_literal()
                else DataPath(
                    context.current_scope.get_symbol_path(arg.get_name()),
                    objective,
                    StorageLocation.get_storage(arg.get_dtype()),
                )
            )
            context.current_scope.add_command(Copy.copy_all(target, source))

    def _call_function(self, namespace: str, func_path: str, context: GenerationContext):
        """生成函数调用命令"""
        context.current_scope.add_command(
            FunctionBuilder.run(f"{namespace}:{func_path.replace('.', '/')}")
        )

    def _handle_return_value(
            self,
            result: Variable | None,
            func: Function,
            objective: str,
            func_path: str,
            context: GenerationContext,
    ):
        """处理函数返回值的复制"""
        if func.return_type != PrimitiveDataType.VOID and result is not None:
            context.current_scope.add_command(
                Copy.copy(
                    DataPath(
                        context.current_scope.get_symbol_path(result.name),
                        objective,
                        StorageLocation.get_storage(result.dtype),
                    ),
                    DataPath(
                        f"return_{hash(func_path)}",
                        objective,
                        StorageLocation.get_storage(func.return_type),
                    ),
                )
            )

    def _handle_ffi(
            self,
            result: Variable | None,
            func: Function,
            args: dict[str, Reference[Variable | Literal]],
            metadata: dict[str, str],
            ctx: GenerationContext
    ):
        func_path: str = metadata.get("path", "")
        objective: str = metadata.get("objective", ctx.objective)
        abi: str = metadata.get("abi", "dovetail")

        match abi:
            case "clang-mc":
                # 根据clang-mc wiki 《调用约定》传入实参

                # 由于dict不保证元素顺序，因此根据func的参数确定传参顺序
                for i, param in enumerate(func.params):
                    if args[param.get_name()].is_literal():
                        argument_path = LiteralPoolTools.get_literal_path_str(args[param.get_name()].value.value)
                    else:
                        argument_path = ctx.current_scope.get_symbol_path(args[param.get_name()])
                    if i <= 7:
                        ctx.current_scope.add_command(
                            Copy.copy(DataPath(f"r{i}", objective), DataPath(argument_path, ctx.objective)))
                    else:
                        #TODO: 支持通过push继续传参
                        pass

                # 调用函数
                self._call_function(*func_path.split(":", maxsplit=1), ctx)  # noqa

                # 写入返回值
                if result is not None and func.return_type != PrimitiveDataType.VOID:
                    ctx.current_scope.add_command(
                        Copy.copy(
                            DataPath(
                                ctx.current_scope.get_symbol_path(result.name),
                                ctx.objective,
                                StorageLocation.get_storage(result.dtype),
                            ),
                            DataPath(
                                f"rax",
                                objective
                            ),
                        )
                    )

            case "dovetail":
                self._fill_arguments(args, func.params, objective, func_path, ctx)

                self._call_function(*func_path.split(":", maxsplit=1), ctx)  # noqa

                self._handle_return_value(result, func, objective, func_path, ctx)
            case _:
                # 供插件自行通过猴子补丁实现
                getattr(self, f"_handle_ffi_{abi}")(result, func, args, metadata, ctx)
