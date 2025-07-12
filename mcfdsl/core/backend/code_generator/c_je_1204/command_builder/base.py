# coding=utf-8
from mcfdsl.core.backend.code_generator.c_je_1204.code_generator_scope import CodeGeneratorScope
from mcfdsl.core.backend.code_generator.c_je_1204.command_builder import DataBuilder, ScoreboardBuilder
from mcfdsl.core.language_enums import DataType
from mcfdsl.core.symbols import Variable, Class, Constant, Literal


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
        def copy_variable(from_: Variable | Constant, from_scope: CodeGeneratorScope, from_objective: str, to: Variable,
                          to_scope: CodeGeneratorScope, to_objective: str):
            if from_.dtype == DataType.STRING:
                return DataBuilder.modify_storage_set_from_storage(
                    f"{to_scope.namespace}:{to_objective}",
                    to_scope.get_symbol_path(to.get_name()),
                    f"{from_scope.namespace}:{from_objective}",
                    from_scope.get_symbol_path(from_.get_name()))
            elif from_.dtype in (DataType.INT, DataType.BOOLEAN):
                return ScoreboardBuilder.set_op(
                    to_scope.get_symbol_path(to.get_name()),
                    to_objective,
                    from_scope.get_symbol_path(from_.get_name()),
                    from_objective)
            else:  # Class
                return None  # TODO: 类复制，此处暂不实现

        @staticmethod
        def copy_literal(to: Variable | Constant, to_scope: CodeGeneratorScope, to_objective: str, value: Literal):

            if to.dtype == DataType.STRING:
                return DataBuilder.modify_storage_set_value(
                    f"{to_scope.namespace}:{to_objective}", to_scope.get_symbol_path(to.get_name()), f"\"{value.value}\"")
            elif to.dtype in (DataType.INT, DataType.BOOLEAN):
                return ScoreboardBuilder.set_score(
                    to_scope.get_symbol_path(to.get_name()), to_objective, int(value.value))
            else:
                return None # TODO: 类复制，此处暂不实现
