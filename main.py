# coding=utf-8
"""主程序"""
import argparse
import json
import logging
import sys
from contextlib import chdir
from pathlib import Path

import fastjsonschema

from dovetail.core.backend import BackendFactory
from dovetail.core.compile_config import CompileConfig
from dovetail.core.config import CACHE_FILE_PREFIX, PACK_CONFIG_VALIDATOR, set_project_logger, PROJECT_NAME, \
    get_project_logger
from dovetail.core.enums.minecraft import MinecraftVersion
from dovetail.core.enums.optimization import OptimizationLevel
from dovetail.core.errors import CompilationError
from dovetail.core.errors import report, Errors
from dovetail.core.ir_builder import IRBuilder
from dovetail.core.parser.parser import ASTVisitor, parser_code
from dovetail.plugins.plugin_loader.loader import plugin_loader
from dovetail.utils.annotations import timed
from dovetail.utils.ir_serializer import IRSymbolSerializer
from dovetail.utils.logger import get_logger
from dovetail.utils.naming import NameNormalizer


class Compiler:
    """
    编译mcdl代码

    Attributes:
        config (CompileConfig): 编译器配置对象
        backend_name (str): 后端名(不填时自动选择)
        generate (bool): 生成指令
        output_temp_file (bool): 输出临时文件
    """

    def __init__(
            self,
            config: CompileConfig,
            backend_name: str = None,
            generate: bool = True,
            output_temp_file: bool = False
    ):
        """
        初始化编译器

        Args:
            config (CompileConfig): 编译器配置对象
            backend_name (str): 后端名(不填时自动选择)
            generate (bool): 是否生成指令
            output_temp_file (bool): 输出临时文件
        """
        self.config = config
        self.backend_name = backend_name
        self.generate = generate
        self.output_temp_file = output_temp_file
        self.logger = get_project_logger()

    def compile(self, source_path: Path, target_path: Path) -> int:
        """
        编译文件并生成数据包

        Args:
            source_path (Path): 源文件路径
            target_path (Path): 目标路径

        Returns:
            int: 编译结果状态码，0表示成功，非0表示失败
        """
        plugin_loader.load_plugin("plugin_loader")
        if source_path.exists():
            if source_path.is_file():
                return self._compile_file(source_path, target_path)
            else:
                return self._compile_directory(source_path, target_path)
        else:
            report(
                Errors.FileNotFound,
                str(source_path),
                filepath=source_path,
                suggestion="仔细检查你的路径w",
            )
            return -1

    def _compile_directory(self, source_path: Path, target_path: Path) -> int:
        """
        编译目录中的所有文件

        Args:
            source_path (Path): 源目录路径
            target_path (Path): 目标目录路径

        Returns:
            int: 编译结果状态码，0表示成功，非0表示失败
        """
        pack_config_path = source_path / "pack.config"
        if not pack_config_path.exists() or not pack_config_path.is_file():
            report(
                Errors.ConfigurationError,
                "文件 pack.config 不存在或不是一个文件",
                filepath=pack_config_path
            )
            raise CompilationError("文件 pack.config 不存在或不是一个文件")
        # 尝试解析配置文件
        try:
            with open(pack_config_path, encoding='utf-8') as config_file:
                pack_config_data: dict = json.load(config_file)
            # 检查配置文件格式是否正确
            PACK_CONFIG_VALIDATOR(pack_config_data)
        except (json.JSONDecodeError, fastjsonschema.JsonSchemaException):
            report(
                Errors.ConfigurationError,
                "文件 pack.config 格式无效",
                filepath=pack_config_path,
                suggestion="确认编译配置正确吗?"
            )
            raise CompilationError("文件 pack.config 格式无效")

        if pack_config_data.get("description"):
            self.config.description = pack_config_data["description"]

        return self._compile_file(Path(source_path / pack_config_data["main"]).resolve(), target_path, source_path)

    def _compile_file(
            self,
            source_path: Path,
            target_dir_path: Path,
            working_directory: Path | None = None
    ) -> int | None:
        """
        编译单个文件

        Args:
            source_path (Path): 源文件路径
            target_dir_path (Path): 目标目录路径
            working_directory (Optional[Path]): 工作目录路径，默认为源文件所在目录

        Returns:
            int: 编译结果状态码，0表示成功，非0表示失败
        """
        source_path = source_path.resolve()
        working_directory = working_directory or source_path.parent

        if not source_path.exists():
            self.logger.error(f"The path '{source_path}' is not valid.")
            return -1

        generator = None

        with chdir(working_directory):
            try:
                tree = parser_code(source_path)
                print(tree.pretty())

                ASTVisitor(self.config, source_path).visit(tree)

                # builder = self._build_and_optimize_ir(generator, tree)
                ir_builder = IRBuilder()

                if self.output_temp_file:
                    self._write_temp_file(ir_builder, target_dir_path)

                if self.generate:
                    self._generate_backend_code(ir_builder, target_dir_path)
            except CompilationError as e:

                self.logger.critical(e.__repr__())
                if self.config.debug:
                    # 重新抛出异常显示错误详情
                    raise
                return -1
            except Exception as e:
                # 重新抛出异常显示错误详情
                raise CompilationError("意外的错误") from e

    @timed("写入临时文件用时{:.3f}s")
    def _write_temp_file(self, builder: IRBuilder, target_dir_path: Path):
        """
        写入临时文件

        Args:
            builder (IRBuilder): IR构建器
            target_dir_path (Path): 目标目录路径
        """
        temp_file = target_dir_path / f"{self.config.namespace}{CACHE_FILE_PREFIX}"
        with open(temp_file, "wb") as f:
            f.write(IRSymbolSerializer.dump(builder))

    @timed("最终代码生成与写入用时{:.3f}s")
    def _generate_backend_code(self, builder: IRBuilder, target_path: Path):
        """
        生成后端代码

        Args:
            builder (IRBuilder): IR构建器
            target_path (Path): 目标目录路径
        """
        BackendFactory.auto_select(self.config, self.backend_name)(builder, target_path, self.config).generate()


def main():
    """主函数"""
    args_parser = argparse.ArgumentParser(description="dovetail")
    args_parser.add_argument('input', type=str, help='输入文件路径')
    args_parser.add_argument('--minecraft-version', '-mcv', metavar='version', type=str, help='游戏版本',
                             default="1.21.4")
    args_parser.add_argument('--output', '-o', metavar='path', type=str, help='输出文件路径')
    args_parser.add_argument('--lib-path', '-l', metavar='path', type=str, help='强制指定标准库路径')
    args_parser.add_argument('--backend', '-b', metavar='name', type=str, help='强制指定后端名称', default="")
    args_parser.add_argument('--namespace', '-n', metavar='namespace', type=str, help='输出数据包命名空间')
    args_parser.add_argument('-O', metavar='level', type=int, choices=[0, 1, 2, 3], default=2, help='优化级别')
    args_parser.add_argument('--no-generate-commands', '-ngc', action='store_true', help='不生成指令')
    args_parser.add_argument('--output-temp-file', action='store_true', help='生成中间文件')
    args_parser.add_argument('--recursion', action='store_true', help='启用递归(需后端支持)')
    args_parser.add_argument('--same-name-function-nesting', action='store_true', help='启用同名函数嵌套')
    # args_parser.add_argument('--first-class-functions', action='store_true',help='启用函数一等公民(所有代码都未适配，开不开都那样)')
    args_parser.add_argument('--experimental', action='store_true', help='启用扩展模式(测试性功能)')
    args_parser.add_argument('--disable-names-normalize', action='store_true', help='禁用命名规范化')
    args_parser.add_argument('--debug', action='store_true', help='启用调试模式')

    parsed_args = args_parser.parse_args()
    source_path = Path(parsed_args.input)
    target_path = Path(parsed_args.output or "target")
    NameNormalizer.enable = not parsed_args.disable_names_normalize
    set_project_logger(get_logger(PROJECT_NAME, logging.DEBUG if parsed_args.debug else logging.INFO))
    compiler = Compiler(
        CompileConfig(
            parsed_args.namespace or "namespace",
            OptimizationLevel(parsed_args.O),
            MinecraftVersion.instance(parsed_args.minecraft_version),
            parsed_args.debug,
            parsed_args.recursion,
            parsed_args.same_name_function_nesting,
            False,
            parsed_args.experimental,
            Path(parsed_args.lib_path).resolve() if parsed_args.lib_path else Path("lib").resolve(),
            "A datapack of Minecraft"
        ),
        parsed_args.backend,
        generate=not parsed_args.no_generate_commands,
        output_temp_file=parsed_args.output_temp_file
    )
    sys.exit(compiler.compile(source_path, target_path))


if __name__ == "__main__":
    main()
