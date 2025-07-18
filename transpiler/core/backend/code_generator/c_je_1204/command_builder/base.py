# coding=utf-8
from ..code_generator_scope import CodeGeneratorScope
from . import DataBuilder, ScoreboardBuilder
from transpiler.core.language_enums import DataType
from transpiler.core.symbols import Variable, Constant, Literal


class BasicCommands:
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
        def copy_variable_base_type(target: Variable,
                                    target_scope: CodeGeneratorScope, target_objective: str,
                                    source: Variable | Constant, source_scope: CodeGeneratorScope,
                                    source_objective: str):
            if source.dtype == DataType.STRING:
                return DataBuilder.modify_storage_set_from_storage(
                    f"{target_scope.namespace}:{target_objective}",
                    target_scope.get_symbol_path(target.get_name()),
                    f"{source_scope.namespace}:{source_objective}",
                    source_scope.get_symbol_path(source.get_name()))
            elif source.dtype in (DataType.INT, DataType.BOOLEAN):
                return ScoreboardBuilder.set_op(
                    target_scope.get_symbol_path(target.get_name()),
                    target_objective,
                    source_scope.get_symbol_path(source.get_name()),
                    source_objective)
            else:  # Class
                return None

        @staticmethod
        def copy_literal_base_type(target: Variable | Constant, target_scope: CodeGeneratorScope, target_objective: str,
                                   source: Literal):

            if target.dtype == DataType.STRING:
                return DataBuilder.modify_storage_set_value(
                    f"{target_scope.namespace}:{target_objective}", target_scope.get_symbol_path(target.get_name()),
                    f"\"{source.value}\"")
            elif target.dtype in (DataType.INT, DataType.BOOLEAN):
                return ScoreboardBuilder.set_score(
                    target_scope.get_symbol_path(target.get_name()), target_objective, int(source.value))
            else:  # Class
                return None
