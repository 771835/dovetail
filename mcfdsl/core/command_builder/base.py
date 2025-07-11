# coding=utf-8
from typing import Any

from mcfdsl.core._interfaces import ISymbol
from mcfdsl.core.command_builder._data import Data
from mcfdsl.core.command_builder._scoreboard import Scoreboard
from mcfdsl.core.language_enums import DataType
from mcfdsl.core.symbols.class_ import Class


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
        def copy_variable(from_: ISymbol, to: ISymbol):
            if from_.data_type != to.data_type:
                return None
            if from_.data_type == DataType.STRING:
                return Data.modify_storage_set_from_storage(
                    to.get_storage_path(),
                    to.get_unique_name(),
                    to.get_storage_path(),
                    from_.get_unique_name())
            elif from_.data_type in (DataType.INT, DataType.BOOLEAN):
                return Scoreboard.set_op(
                    to.get_unique_name(),
                    to.objective,
                    from_.get_unique_name(),
                    from_.objective)
            elif from_.data_type == DataType.NULL:
                return None  # TODO:实现null类型的使用 / null类型压根不可能被允许声明(纯粹增加我的实现负担)
            elif isinstance(from_.data_type, Class):
                return None  # TODO: 自定义复制，此处暂不实现
            return None

        @staticmethod
        def copy_literal(to: ISymbol, value: Any):
            if type(value) not in (str, int, bool):
                return None
            elif type == str and to.data_type != DataType.STRING:
                return None

            if to.data_type == DataType.STRING:
                return Data.modify_storage_set_value(
                    to.get_storage_path(), to.get_unique_name(), f"\"{value}\"")
            elif to.data_type in (DataType.INT, DataType.BOOLEAN):
                return Scoreboard.set_score(
                    to.get_unique_name(), to.objective, int(value))
            return None
