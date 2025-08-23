# coding=utf-8
import uuid

from transpiler.core.enums import DataType
from transpiler.core.symbols import Variable, Constant, Literal, Symbol
from . import DataBuilder, ScoreboardBuilder, FunctionBuilder, Execute
from ..code_generator_scope import CodeGeneratorScope


class BasicCommands:
    @staticmethod
    def call_macros_function(
            func_name: str,
            objective: str,
            param: dict[str, tuple[bool, str, str | None]]
    ) -> list[str]:
        """
         调用宏函数

        :param func_name:函数路径
        :param objective: 临时记分板
        :param param: 参数 参数名:(是否为引用，路径/具体值,记分板)
        :return: 生成的指令
        """
        args_path = f"args.{uuid.uuid4().hex}"
        commands: list[str] = []
        for name, _ in param.items():
            if name is None:
                continue
            if _[0]:
                commands.append(
                    DataBuilder.modify_storage_set_from_storage(
                        objective,
                        f"{args_path}.{name}",
                        _[2],
                        _[1]
                    )
                )
            else:
                value = _[1].replace("\\","\\\\")
                # 此处可通过merge进行优化生成的指令的效率，但是暂不实现，也可以通过常量池预加载，但是也不实现qwq
                commands.append(
                    DataBuilder.modify_storage_set_value(
                        objective,
                        f"{args_path}.{name}",
                        f'"{value}"'
                    )
                )
        commands.append(
            FunctionBuilder.run_with_source(
                func_name,
                "storage",
                f"{objective} {args_path}"
            )
        )
        return commands

    @staticmethod
    def comment(message: str) -> list[str]:
        """
        生成多行注释，自动处理换行符

        Args:
            message: 注释内容，支持用\n表示换行

        Features:
            - 自动分割换行符
            - 保留空行（生成单独的#）
            - 自动去除行尾空白

        Example:
            Function.comment("第一行\n\n第三行")
            -> ["# 第一行", "#", "# 第三行"]
        """
        lines = message.split('\n')
        processed = []
        for line in lines:
            cleaned = line.rstrip()  # 去除行尾空白
            if cleaned:
                processed.append(f"# {cleaned}")
            else:
                processed.append("#")  # 处理纯空行
        return processed

    class Copy:
        @staticmethod
        def copy_variable_base_type(
                target: Variable,
                target_scope: CodeGeneratorScope,
                target_objective: str,
                source: Variable | Constant,
                source_scope: CodeGeneratorScope,
                source_objective: str
        ):
            if source.dtype == DataType.STRING:
                return DataBuilder.modify_storage_set_from_storage(
                    f"{target_objective}",
                    target_scope.get_symbol_path(target.get_name()),
                    f"{source_objective}",
                    source_scope.get_symbol_path(source.get_name()))
            elif source.dtype in (DataType.INT, DataType.BOOLEAN):
                return ScoreboardBuilder.set_op(
                    target_scope.get_symbol_path(target.get_name()),
                    target_objective,
                    source_scope.get_symbol_path(source.get_name()),
                    source_objective)
            return None

        @staticmethod
        def copy_literal_base_type(
                target: Variable | Constant,
                target_scope: CodeGeneratorScope,
                target_objective: str,
                source: Literal
        ):
            if target.dtype != source.dtype:
                return None
            # 如果目标变量为字符串
            if target.dtype == DataType.STRING:
                return DataBuilder.modify_storage_set_value(
                    target_objective,
                    target_scope.get_symbol_path(target.get_name()),
                    f'"{source.value}"'
                )
            elif target.dtype in (DataType.INT, DataType.BOOLEAN):
                return ScoreboardBuilder.set_score(
                    target_scope.get_symbol_path(target.get_name()), target_objective, int(source.value))
            return None

        @staticmethod
        def copy_score_to_storage(
                target: Variable | Constant,
                target_scope: CodeGeneratorScope,
                target_objective: str
        ):
            return (Execute.execute()
            .store_result_storage(
                target_objective,
                BasicCommands.get_symbol_path(target_scope, target),
                'int',
                1.0
            )
            .run(
                ScoreboardBuilder.get_score(
                    BasicCommands.get_symbol_path(target_scope, target),
                    target_objective
                )
            )
            )

        @staticmethod
        def copy_base_type(
                target: Variable | Constant,
                target_scope: CodeGeneratorScope,
                target_objective: str,
                source: Variable | Constant | Literal,
                source_scope: CodeGeneratorScope,
                source_objective: str
        ) -> str | None:
            if isinstance(source, Literal):
                return BasicCommands.Copy.copy_literal_base_type(
                    target,
                    target_scope,
                    target_objective,
                    source
                )
            else:
                return BasicCommands.Copy.copy_variable_base_type(
                    target,
                    target_scope,
                    target_objective,
                    source,
                    source_scope,
                    source_objective
                )

    @staticmethod
    def get_symbol_path(scope: CodeGeneratorScope, symbol: Symbol | str):
        return scope.get_symbol_path(symbol.get_name() if isinstance(symbol, Symbol) else symbol)
