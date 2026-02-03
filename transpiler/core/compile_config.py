# coding=utf-8
from pathlib import Path

from attrs import define

from transpiler.core.enums.minecraft import MinecraftVersion
from transpiler.core.enums.optimization import OptimizationLevel


@define(slots=True, frozen=True)
class CompileConfig:
    """
    编译配置

    Attributes:
        namespace (str): 命名空间
        optimization_level (OptimizationLevel): 优化等级
        version (MinecraftVersion): Minecraft版本信息
        debug (bool): 调试模式开关
        recursion (bool): 启用递归开关
        same_name_function_nesting (bool): 启用同名函数嵌套开关
        first_class_functions (bool): 启用函数一等公民开关
        experimental (bool): 启用实验性功能开关
        lib_path (Path): 库文件路径
    """
    namespace: str
    optimization_level: OptimizationLevel
    version: MinecraftVersion
    debug: bool = False
    recursion: bool = False
    same_name_function_nesting: bool = False
    first_class_functions: bool = False
    experimental: bool = False
    lib_path: Path = Path("lib").resolve()
