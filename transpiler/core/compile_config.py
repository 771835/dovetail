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
        source_path (Path): 源文件路径
        target_path (Path): 目标输出路径
        namespace (str): 命名空间
        optimization_level (OptimizationLevel): 优化等级
        minecraft_version (MinecraftVersion): Minecraft版本信息
        backend_name (str): 后端名称
        debug (bool): 调试模式开关
        no_generate_commands (bool): 不生成指令开关
        output_temp_file (bool): 输出临时文件开关
        enable_recursion (bool): 启用递归开关
        enable_same_name_function_nesting (bool): 启用同名函数嵌套开关
        enable_first_class_functions (bool): 启用函数一等公民开关
        enable_experimental (bool): 启用实验性功能开关
        lib_path (Path): 库文件路径
    """
    source_path: Path
    target_path: Path
    namespace: str
    optimization_level: OptimizationLevel
    minecraft_version: MinecraftVersion
    backend_name: str = ""
    debug: bool = False
    no_generate_commands: bool = False
    output_temp_file: bool = False
    enable_recursion: bool = False
    enable_same_name_function_nesting: bool = False
    enable_first_class_functions: bool = False
    enable_experimental: bool = False
    lib_path: Path = Path("lib").resolve()
