# coding=utf-8
from typing import Literal, Optional


class FunctionBuilder:
    """
    Static class for building Minecraft Java Edition function commands.
    """

    @staticmethod
    def run(name: str) -> str:
        """
        运行指定名称的函数或函数标签

        Args:
            name: 函数名称（格式：命名空间:路径）或函数标签（格式：#命名空间:标签名）

        Example:
            Function.run("foo:bar") -> "function foo:bar"
        """
        return f"function {name}"

    @staticmethod
    def run_with_arguments(name: str, *args: str) -> str:
        """
        运行函数并传递多个参数（需配合宏功能使用）

        Args:
            name: 函数名称
            *args: 接受任意数量参数，自动处理空格

        Example:
            Function.run_with_arguments("demo", "normal", "has space")
            -> "function demo normal "has space""
        """

        def process_arg(arg: str) -> str:
            # 如果参数包含空格且没有用引号包裹
            if ' ' in arg and not (arg.startswith('"') and arg.endswith('"')):
                return f'"{arg}"'
            return arg

        processed = [process_arg(arg) for arg in args]
        return f"function {name} {' '.join(processed)}"

    @staticmethod
    def run_with_source(
            name: str,
            source_type: Literal["block", "entity", "storage"],
            source: str,
            path: Optional[str] = None
    ) -> str:
        """
        使用NBT数据源运行函数（宏功能）

        Args:
            name: 函数名称
            source_type: 数据源类型（block/entity/storage）
            source: 数据源位置（坐标/选择器/存储ID）
            path: 可选NBT路径

        Examples:
            Function.run_with_source("test", "entity", "@s")
            -> "function test with entity @s"
        """
        cmd = f"function {name} with {source_type} {source}"
        if path:
            cmd += f" {path}"
        return cmd
