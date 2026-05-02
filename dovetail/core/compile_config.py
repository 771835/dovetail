# coding=utf-8
"""
编译任务配置

该文件提供编译器配置类，用于记录每次编译任务的配置信息
"""
from pathlib import Path

from attrs import define

from dovetail.core.enums.minecraft import MinecraftVersion
from dovetail.core.enums.optimization import OptimizationLevel


@define(slots=True, hash=True)
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
        disable_deprecated_function (bool): 禁用废弃函数编译
        experimental (bool): 启用实验性功能开关
        lib_path (Path): 库文件路径
        description (str): 数据包描述
    """
    namespace: str
    optimization_level: OptimizationLevel
    version: MinecraftVersion
    debug: bool = False
    recursion: bool = False
    same_name_function_nesting: bool = False
    first_class_functions: bool = False
    disable_deprecated_function: bool = False
    experimental: bool = False
    lib_path: Path = Path("lib").resolve()
    description: str = ""
