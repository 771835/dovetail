# coding=utf-8
import argparse
import json
import sys
import time
from contextlib import chdir
from pathlib import Path

import fastjsonschema
from antlr4 import FileStream, CommonTokenStream

from transpiler.core import registry
from transpiler.core.compile_config import CompileConfig
from transpiler.core.config import CACHE_FILE_PREFIX, PACK_CONFIG_VALIDATOR
from transpiler.core.enums.minecraft import MinecraftVersion
from transpiler.core.enums.optimization import OptimizationLevel
from transpiler.core.errors import CompilationError
from transpiler.core.instructions import IRScopeEnd, IRScopeBegin
from transpiler.core.ir_builder import IRBuilder
from transpiler.core.ir_generator import IRGenerator
from transpiler.core.optimize.optimizer import Optimizer
from transpiler.core.parser import transpilerLexer, transpilerParser
from transpiler.plugins.plugin_loader.loader import plugin_loader
from transpiler.utils.ir_serializer import IRSymbolSerializer
from transpiler.utils.naming import NameNormalizer


class Compiler:
    """
    分析并编译mcdl代码
    """

    def __init__(self, config: CompileConfig):
        self.config = config

    def compile(self):
        """
        编译文件并生成数据包
        """
        self._load_plugin("plugin_loader")
        if self.config.source_path.exists():
            if self.config.source_path.is_file():
                return self._compile_file(self.config.source_path, self.config.target_path)
            else:
                return self._compile_directory(self.config.source_path, self.config.target_path)
        else:
            raise FileNotFoundError(f"{self.config.source_path} does not exist")

    def _load_plugin(self, plugin_name: str):
        plugin_loader.load_plugin(plugin_name)

    def _compile_directory(self, source_path: Path, target_path: Path):
        pack_config_path = source_path / "pack.config"
        if not pack_config_path.exists() or not pack_config_path.is_file():
            print(f"Error: The path '{pack_config_path}' is not a file.")
            return -1
        # 尝试解析配置文件
        try:
            with open(pack_config_path, encoding='utf-8') as config_file:
                pack_config_data = json.load(config_file)
            if not isinstance(pack_config_data, dict):
                print("Error: The file 'pack.config' has an invalid format.")
                return -1
            # 检查配置文件格式是否正确
            PACK_CONFIG_VALIDATOR(pack_config_data)
        except (json.JSONDecodeError, fastjsonschema.JsonSchemaException):
            print(f"Error: The file 'pack.config' has an invalid format.")
            return -1
        return self._compile_file(Path(source_path / pack_config_data["main"]).resolve(), target_path, source_path)

    def _compile_file(self, source_path: Path, target_dir_path: Path, working_directory: Path | None = None):
        working_directory = working_directory or source_path.parent
        if not source_path.exists():
            print(f"Error: The path '{source_path}' is not valid.")
            return -1
        tree = self._parser_file(source_path)
        generator: IRGenerator = IRGenerator(self.config)
        with chdir(working_directory):
            try:
                ir_build_start_time = time.time()
                generator.visit(tree)
                print(f"IR生成用时：{time.time() - ir_build_start_time}")
                ir_builder = generator.get_ir()
                ir_optimize_start_time = time.time()
                ir_builder = Optimizer(ir_builder, self.config).optimize()
                print(f"IR优化用时：{time.time() - ir_optimize_start_time}")
                if self.config.output_temp_file:
                    with open(target_dir_path / f"{self.config.namespace}{CACHE_FILE_PREFIX}", "wb") as f:
                        f.write(IRSymbolSerializer.dump(ir_builder))

                if self.config.debug:
                    print("最终ir")
                    self._print_ir_builder(ir_builder)
                if not self.config.no_generate_commands:
                    # 输出到target目录
                    if self.config.backend_name:
                        current_backend = registry.backends.get(self.config.backend_name, None)
                        if current_backend is None:
                            print(f"找不到名为{self.config.backend_name}的后端")
                            return -1
                    else:
                        for name, backend in registry.backends.items():
                            if backend.is_support(self.config):
                                print(f"自动选择{name}后端")
                                current_backend = backend
                                break
                        else:
                            print(f"找不到可用后端")
                            return -1

                    code_generator_start_time = time.time()
                    current_backend(ir_builder, target_dir_path, self.config).generate()
                    print(f"最终代码生成与写入总用时：{time.time() - code_generator_start_time}")
            except CompilationError as e:
                time.sleep(0.1)  # 保证前面的输出完成
                if generator:
                    print("作用域结构:")
                    self._print_scope_tree(generator.scope_stack[0])
                print(e.__repr__())
                if self.config.debug:
                    # 重新抛出异常显示错误详情
                    raise
                return -1
            except Exception:
                time.sleep(0.1)
                print("意外的错误，以下为详细堆栈信息")
                time.sleep(0.1)
                # 重新抛出异常显示错误详情
                raise

    @staticmethod
    def _print_ir_builder(ir_builder: IRBuilder):
        depth = 0
        for i in ir_builder:
            if isinstance(i, IRScopeEnd):
                depth -= 1
            print(depth * "    " + repr(i))
            if isinstance(i, IRScopeBegin):
                depth += 1

    @staticmethod
    def _parser_file(file_path: Path) -> transpilerParser.transpilerParser.ProgramContext | None:
        if file_path.exists() and file_path.is_file():
            input_stream = FileStream(str(file_path.resolve()), "utf-8")
            lexer = transpilerLexer.transpilerLexer(input_stream)
            stream = CommonTokenStream(lexer)
            parser = transpilerParser.transpilerParser(stream)

            return parser.program()
        else:
            return None

    @staticmethod
    def _print_scope_tree(node, prefix="", is_tail=True):
        """递归打印作用域树结构"""
        # 更明确的变量名
        scope_type_display = f" ({node.stype.value})" if node.stype else ""
        tree_line = f"{prefix}{'└── ' if is_tail else '├── '}{node.name}{scope_type_display}"
        print(tree_line)

        # 子节点处理
        child_nodes = node.children
        for child_index, child_node in enumerate(child_nodes):
            child_prefix = prefix + ("    " if is_tail else "│   ")
            Compiler._print_scope_tree(
                child_node, child_prefix, child_index == len(child_nodes) - 1)


def main():
    """主函数"""
    args_parser = argparse.ArgumentParser(description="dovetail")
    args_parser.add_argument('input', type=str, help='输入文件路径')
    args_parser.add_argument('--minecraft-version', '-mcv', metavar='version', type=str, help='游戏版本',
                             default="1.20.4")
    args_parser.add_argument('--output', '-o', metavar='path', type=str, help='输出文件路径')
    args_parser.add_argument('--lib-path', '-L', metavar='path', type=str, help='强制指定标准库路径')
    args_parser.add_argument('--backend-name', '-B', metavar='name', type=str, help='强制指定后端名称', default="")
    args_parser.add_argument('--namespace', '-n', metavar='namespace', type=str, help='输出数据包命名空间')
    args_parser.add_argument('-O', metavar='level', type=int, choices=[0, 1, 2, 3], default=2, help='优化级别')
    args_parser.add_argument('--no-generate-commands', action='store_true', help='不生成指令')
    args_parser.add_argument('--output-temp-file', action='store_true', help='生成中间文件')
    args_parser.add_argument('--enable-recursion', action='store_true', help='启用递归(需后端支持)')
    args_parser.add_argument('--enable-same-name-function-nesting', action='store_true', help='启用同名函数嵌套')
    # args_parser.add_argument('--enable-first-class-functions', action='store_true',help='启用函数一等公民(所有代码都未适配，开不开都那样)')
    args_parser.add_argument('--enable-experimental', action='store_true', help='启用扩展模式(测试性功能)')
    args_parser.add_argument('--disable-names-normalizer', action='store_true', help='禁用命名规范化')
    args_parser.add_argument('--debug', action='store_true', help='启用调试模式')
    args_parser.add_argument('--easter-egg', action='store_true',
                             help='奇奇怪怪的修改(警告:这将会严重破坏编译器的功能)')

    parsed_args = args_parser.parse_args()
    source_path = Path(parsed_args.input)
    target_path = Path(parsed_args.output or "target")
    if parsed_args.easter_egg:
        import transpiler.easter_egg
        transpiler.easter_egg.main()
    NameNormalizer.enable = not parsed_args.disable_names_normalizer
    compiler = Compiler(
        CompileConfig(
            source_path,
            target_path,
            parsed_args.namespace or "namespace",
            OptimizationLevel(parsed_args.O),
            MinecraftVersion.from_str(parsed_args.minecraft_version),
            parsed_args.backend_name,
            parsed_args.debug,
            parsed_args.no_generate_commands,
            parsed_args.output_temp_file,
            parsed_args.enable_recursion,
            parsed_args.enable_same_name_function_nesting,
            False,
            parsed_args.enable_experimental,
            Path(parsed_args.lib_path).resolve() if parsed_args.lib_path else Path("lib").resolve()
        )
    )
    sys.exit(compiler.compile())


if __name__ == "__main__":
    main()
