# coding=utf-8
from pathlib import Path

from attrs import define, field, validators

from transpiler.core.enums.minecraft import MinecraftVersion
from transpiler.core.enums.optimization import OptimizationLevel


@define(slots=True, frozen=True)
class CompileConfig:
    """
    编译配置

    Attributes:
        source_path: 源文件路径
        target_path: 目标输出路径
        namespace: 命名空间
        optimization_level: 优化等级
        minecraft_version: Minecraft版本信息
        backend_name: 后端名称
        debug: 调试模式开关
        no_generate_commands: 不生成指令开关
        output_temp_file: 输出临时文件开关
        enable_recursion: 启用递归开关
        enable_same_name_function_nesting: 启用同名函数嵌套开关
        enable_first_class_functions: 启用函数一等公民开关
        enable_experimental: 启用实验性功能开关
        lib_path: 库文件路径
    """
    source_path: Path = field(validator=validators.instance_of(Path))
    target_path: Path = field(validator=validators.instance_of(Path))
    namespace: str = field(validator=validators.instance_of(str))
    optimization_level: OptimizationLevel = field(validator=validators.instance_of(OptimizationLevel))
    minecraft_version: MinecraftVersion = field(validator=validators.instance_of(MinecraftVersion))
    backend_name: str = field(validator=validators.instance_of(str), default="")
    debug: bool = field(validator=validators.instance_of(bool), default=False)
    no_generate_commands: bool = field(validator=validators.instance_of(bool), default=False)
    output_temp_file: bool = field(validator=validators.instance_of(bool), default=False)
    enable_recursion: bool = field(validator=validators.instance_of(bool), default=False)
    enable_same_name_function_nesting: bool = field(validator=validators.instance_of(bool), default=False)
    enable_first_class_functions: bool = field(validator=validators.instance_of(bool), default=False)
    enable_experimental: bool = field(validator=validators.instance_of(bool), default=False)
    lib_path: Path = field(validator=validators.instance_of(Path), default=Path("lib").resolve())
