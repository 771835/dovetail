# coding=utf-8
"""
IRCall 指令处理器
"""
from typing import Optional

from dovetail.core.backend import ir_processor, IRProcessor, GenerationContext
from dovetail.core.enums import FunctionType, PrimitiveDataType, StructureType
from dovetail.core.instructions import IRInstruction, IROpCode
from dovetail.core.symbols import Variable, Function, Literal, Reference
from dovetail.utils.logger import get_logger
from ..backend import JE1215Backend
from ..commands import FunctionBuilder, Copy, DataPath, StorageLocation, LiteralPoolTools, DataBuilder
from ..commands.builtins import CommandRegistry

logger = get_logger(__name__)


@ir_processor(JE1215Backend, IROpCode.CALL)
class IRCallProcessor(IRProcessor):

    # ── 主入口 ────────────────────────────────────────────────────────────────

    def process(self, instruction: IRInstruction, context: GenerationContext):
        result: Variable | None = instruction.get_operands()[0]
        func: Function = instruction.get_operands()[1]
        args: dict[str, Reference[Variable | Literal]] = instruction.get_operands()[2]
        needs_stack_save: bool = instruction.metadata.get("needs_stack_save", False)
        live_vars: set[str] = instruction.metadata.get("live_vars", set())

        match func.func_type:
            case FunctionType.BUILTIN:
                CommandRegistry.get(func.name).call(result, context, args)
            case FunctionType.EXTERN:
                self._handle_ffi(result, func, args, func.all_metadata(), context)
            case _:
                self._handle_user_call(result, func, args, context, needs_stack_save, live_vars)

    # ── 用户函数调用 ──────────────────────────────────────────────────────────

    def _handle_user_call(
            self,
            result: Variable | None,
            func: Function,
            args: dict[str, Reference[Variable | Literal]],
            context: GenerationContext,
            needs_stack_save: bool,
            live_vars: set[str]
    ):
        """普通用户函数调用：填参数 → 调用 → 取返回值"""
        func_path = self._resolve_func_path(func, context)
        objective = context.objective
        if needs_stack_save:
            logger.debug(f"Function call '{func}' save stack frame")
            self._save_stack_frame(objective, context, result, live_vars)
        self._fill_arguments(args, func.params, objective, func_path, context)
        self._emit_call(context.namespace, func_path, context)
        if needs_stack_save:
            self._load_stack_frame(objective, context, result, live_vars)
        self._copy_return_value(result, func, objective, func_path, context)

    # ── 参数与返回值 ──────────────────────────────────────────────────────────

    def _resolve_func_path(self, func: Function, context: GenerationContext) -> str:
        """解析函数的作用域路径"""
        if func.func_type == FunctionType.FUNCTION_UNIMPLEMENTED:
            scope = context.current_scope.resolve_symbol_scope(func.name)
        else:
            scope = context.current_scope.resolve_scope(func.name)
        return scope.get_absolute_path()

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
            source = self._resolve_arg_source(arg, context)
            context.current_scope.add_command(Copy.copy_all(target, source))

    def _resolve_arg_source(self, arg: Reference[Variable | Literal], context: GenerationContext, ) -> DataPath | str:
        """将实参解析为 DataPath 或字面量"""
        if arg.is_literal():
            return arg.value.value  # noqa
        return DataPath(
            context.current_scope.get_symbol_path(arg.get_name()),
            context.objective,
            StorageLocation.get_storage(arg.get_dtype()),
        )

    def _copy_return_value(self, result: Variable | None, func: Function, objective: str, func_path: str,
                           context: GenerationContext):
        """将函数返回值复制到 result 变量"""
        if func.return_type == PrimitiveDataType.VOID or result is None:
            return
        context.current_scope.add_command(
            Copy.copy(
                DataPath.from_symbol(context, result),
                DataPath(
                    f"return_{hash(func_path)}",
                    objective,
                    StorageLocation.get_storage(func.return_type),
                )
            )
        )

    # ── 保存与加载栈帧 ──────────────────────────────────────────────────────────
    def _collect_score_vars(
            self,
            context: GenerationContext,
            exclude_path: str = "",
            live_vars: Optional[set[str]] = None
    ) -> set[str]:
        """收集当前函数作用域内所有活跃的记分板变量的路径"""
        score_vars: set[str] = set()
        for scope in reversed(context.scope_stack):
            for symbol in scope.symbols.values():
                if symbol.get_dtype() in (PrimitiveDataType.INT, PrimitiveDataType.BOOLEAN):
                    symbol_path = scope.get_symbol_path(symbol)
                    if symbol_path != exclude_path:
                        if live_vars is None or symbol.get_name() in live_vars:
                            # 如果存在活跃变量集合则比对名称
                            score_vars.add(symbol_path)
            if scope.scope_type == StructureType.FUNCTION:
                break
        else:
            raise RuntimeError("未找到 FUNCTION 作用域，作用域结构无效")
        return score_vars

    def _get_current_function_scope(self, context: GenerationContext):
        """获取当前函数作用域"""
        func_scope = next(
            (s for s in reversed(context.scope_stack) if s.scope_type == StructureType.FUNCTION),
            None,
        )
        if func_scope is None:
            raise RuntimeError("未找到 FUNCTION 作用域，作用域结构无效")
        return func_scope

    def _save_stack_frame(self, objective: str, context: GenerationContext, result: Optional[Variable],
                          live_vars: set[str]):
        """保存栈帧"""
        func_scope = self._get_current_function_scope(context)
        result_path = context.current_scope.get_symbol_path(result) if result else ""

        # 保存当前函数的存储
        context.add_command(Copy.copy(
            DataPath("temp_stack_frame.storage", objective, StorageLocation.STORAGE),
            DataPath(func_scope.get_absolute_path(), objective, StorageLocation.STORAGE))
        )

        # 保存当前函数所有存储在计分板上的数字
        score_vars = self._collect_score_vars(context, result_path, live_vars)

        for score_var in score_vars:
            context.add_command(Copy.copy(
                DataPath(f"temp_stack_frame.score.\"{score_var}\"", objective, StorageLocation.STORAGE),
                DataPath(score_var, objective)))

        # 将栈帧保存
        context.add_command(
            DataBuilder.modify_storage_append_from_storage(
                objective, "__stack_frame__",
                objective, "temp_stack_frame"
            )
        )

    def _load_stack_frame(self, objective: str, context: GenerationContext, result: Optional[Variable],
                          live_vars: set[str]):
        """加载栈帧（pop）并还原，跳过 result 以保留返回值"""
        func_scope = self._get_current_function_scope(context)
        result_path = context.current_scope.get_symbol_path(result) if result else ""

        # pop 栈顶
        context.add_command(
            DataBuilder.modify_storage_set_from_storage(
                objective, "temp_stack_frame",
                objective, "__stack_frame__[-1]"
            )
        )

        context.add_command(DataBuilder.remove_storage(objective, "__stack_frame__[-1]"))

        # 还原 storage（排除 result 所在的 storage 路径）
        # 先整体还原
        context.current_scope.add_command(Copy.copy(
            DataPath(func_scope.get_absolute_path(), objective, StorageLocation.STORAGE),
            DataPath("temp_stack_frame.storage", objective, StorageLocation.STORAGE),
        ))

        # 收集并应用
        score_vars = self._collect_score_vars(context, result_path, live_vars)

        for score_var in score_vars:
            context.add_command(Copy.copy(
                DataPath(score_var, objective),
                DataPath(f"temp_stack_frame.score.\"{score_var}\"", objective, StorageLocation.STORAGE)))

    # ── 调用命令生成 ──────────────────────────────────────────────────────────

    def _emit_call(self, namespace: str, func_path: str, context: GenerationContext):
        """生成函数调用命令"""
        context.current_scope.add_command(
            FunctionBuilder.run(f"{namespace}:{func_path.replace('.', '/')}")
        )

    # ── FFI 调用 ──────────────────────────────────────────────────────────────

    def _handle_ffi(
            self,
            result: Variable | None,
            func: Function,
            args: dict[str, Reference[Variable | Literal]],
            metadata: dict[str, str],
            context: GenerationContext,
    ):
        """外部函数接口调用"""
        func_path: str = metadata.get("path", "")
        objective: str = metadata.get("objective", context.objective)
        abi: str = metadata.get("abi", "dovetail")

        match abi:
            case "clang-mc":
                self._ffi_clang_mc(result, func, args, func_path, objective, context)
            case "dovetail":
                self._ffi_dovetail(result, func, args, func_path, objective, context)
            case _:
                # 供插件自行通过猴子补丁实现
                getattr(self, f"_handle_ffi_{abi}")(result, func, args, metadata, context)

    def _ffi_clang_mc(
            self,
            result: Variable | None,
            func: Function,
            args: dict[str, Reference[Variable | Literal]],
            func_path: str,
            objective: str,
            context: GenerationContext,
    ):
        """clang-mc 调用约定：r0-r7 传参，rax 返回"""
        # 按参数声明顺序传入（dict 不保序，以 func.params 为准）
        for i, param in enumerate(func.params):
            arg_path = self._resolve_ffi_arg_path(args[param.get_name()], context)
            if i <= 7:
                context.current_scope.add_command(
                    Copy.copy(DataPath(f"r{i}", objective), DataPath(arg_path, context.objective))
                )
            else:
                # TODO: 支持通过 push 继续传参
                pass

        namespace, path = func_path.split(":", maxsplit=1)
        self._emit_call(namespace, path, context)

        if result is not None and func.return_type != PrimitiveDataType.VOID:
            context.current_scope.add_command(
                Copy.copy(
                    DataPath.from_symbol(context, result),
                    DataPath("rax", objective),
                )
            )

    def _ffi_dovetail(
            self,
            result: Variable | None,
            func: Function,
            args: dict[str, Reference[Variable | Literal]],
            func_path: str,
            objective: str,
            context: GenerationContext,
    ):
        """dovetail ABI：复用标准填参和返回值逻辑"""
        self._fill_arguments(args, func.params, objective, func_path, context)

        namespace, path = func_path.split(":", maxsplit=1)
        self._emit_call(namespace, path, context)

        self._copy_return_value(result, func, objective, func_path, context)

    def _resolve_ffi_arg_path(
            self,
            arg: Reference[Variable | Literal],
            context: GenerationContext,
    ) -> str:
        """将 FFI 实参解析为路径字符串（供 clang-mc 约定使用）"""
        if arg.is_literal():
            return LiteralPoolTools.get_literal_path_str(arg.value.value)
        return context.current_scope.get_symbol_path(arg.get_name())
