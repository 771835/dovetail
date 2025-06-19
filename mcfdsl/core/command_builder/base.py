from typing import Any

from mcfdsl.core._interfaces import ISymbol
from mcfdsl.core.class_ import Class
from mcfdsl.core.command_builder._data import Data
from mcfdsl.core.command_builder._scoreboard import Scoreboard
from mcfdsl.core.language_types import DataType
from mcfdsl.core.utils.type_utils import TypeUtils

minecraft_version = ["1.20.4"]


class BasicCommands:
    @staticmethod
    def comment(message: str) -> str:
        return f"# {message}"

    class Copy:
        @staticmethod
        def copy_variable(from_: ISymbol, to: ISymbol):
            if from_.data_type != to.data_type:
                return None
            if from_.data_type == DataType.STRING:
                return Data.modify_storage_set_from_storage(f"{to.scope.namespace}:{to.objective}", to.get_unique_name(), f"{from_.scope.namespace}:{from_.objective}", from_.get_unique_name())
            elif from_.data_type in (DataType.INT, DataType.BOOLEAN):
                return Scoreboard.set_op(to.objective, to.get_unique_name(), from_.get_unique_name(), from_.objective)
            elif from_.data_type == DataType.SELECTOR:
                return None # selector选择器类型由编译期模拟，非实际存储，故无需复制
            elif isinstance(from_.data_type, Class):
                return None # TODO: 自定义复制，此处暂不实现
            return None

        @staticmethod
        def copy_literal(to: ISymbol, value: Any):
            if TypeUtils.infer(value) != to.data_type:
                return None

            if to.data_type == DataType.STRING:
                return Data.modify_storage_set_value(f"{to.scope.namespace}:{to.objective}", to.get_unique_name(), f"\"{value}\"")
            elif to.data_type in (DataType.INT, DataType.BOOLEAN):
                return Scoreboard.set_score(to.get_unique_name(), to.objective, int(value))
            return None

