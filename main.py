# coding=utf-8
import argparse
import json
import sys
import time
import warnings
from contextlib import chdir
from pathlib import Path

from antlr4 import FileStream, CommonTokenStream
from antlr4.error.ErrorListener import ErrorListener
from jsonschema import validate, ValidationError

from transpiler.core import registry
from transpiler.core.errors import CompilationError
from transpiler.core.generator_config import GeneratorConfig, OptimizationLevel, MinecraftVersion
from transpiler.core.instructions import IRScopeEnd, IRScopeBegin
from transpiler.core.ir_builder import IRBuilder
from transpiler.core.ir_generator import MCGenerator
from transpiler.core.optimize.optimizer import Optimizer
from transpiler.core.parser import transpilerLexer
from transpiler.core.parser import transpilerParser
from transpiler.core.scope import Scope
from transpiler.plugins.load_plugin.plugin_loader import plugin_loader
from transpiler.utils.ir_serializer import IRSymbolSerializer
from transpiler.utils.mixin_manager import Mixin, Inject, At, CallbackInfoReturnable
from transpiler.utils.naming import NameNormalizer


@Mixin(ErrorListener)  # 相比于正常继承，使用mixin会慢0.001-0.01左右，但是可以减少代码量，而且好酷qwq
class ErrorListenerMixin:
    @staticmethod
    @Inject("syntaxError", At(At.HEAD), cancellable=True)
    def syntaxError(ci: CallbackInfoReturnable, self, recognizer, offending_symbol, line, column, msg, e):
        sys.stderr.write(f"Syntax error at line {line}:{column} - {msg} \n")
        ci.cancel()


class Compile:
    """
    分析并编译mcdl代码
    """

    pack_config_schema = {
        "type": "object",
        "title": "目录配置文件",
        "properties": {
            "main": {
                "type": "string",
            }
        },
        "required": ["main"]
    }

    def __init__(self, config: GeneratorConfig):
        self.config = config

    def compile(self, source_path: Path, target_path: Path):
        """
        编译文件并生成数据包

        :param source_path: 代码数据
        :param target_path: 目标生成路径
        :return:
        """
        source_path = Path(source_path)
        target_path = Path(target_path)
        self._load_plugin("load_plugin")
        self._load_plugin("je1204")
        if source_path.exists():
            if source_path.is_file():
                return self._compile_file(source_path, target_path)
            else:
                return self._compile_directory(source_path, target_path)
        else:
            raise FileNotFoundError(f"{source_path} does not exist")

    def _load_plugin(self, plugin_name: str):
        plugin_loader.load_plugin(plugin_name)

    def _compile_directory(self, source_path: Path, target_path: Path):
        pack_config_path = source_path / "pack.config"
        if not pack_config_path.exists() or not pack_config_path.is_file():
            print(f"Error: The path '{pack_config_path}' is not a file.")
            return -1
        # 尝试解析配置文件
        try:
            with open(pack_config_path, encoding='utf-8') as f:
                pack_config = json.load(f)
            if not isinstance(pack_config, dict):
                print("Error: The file 'pack.config' has an invalid format.")
                return -1
            # 检查配置文件格式是否正确
            validate(instance=pack_config, schema=self.pack_config_schema)
        except (json.JSONDecodeError, ValidationError):
            print("Error: The file 'pack.config' has an invalid format.")
            return -1
        return self._compile_file(Path(source_path / pack_config["main"]).resolve(), target_path, source_path)

    def _compile_file(self, source_path: Path, target_path: Path, cwd_path: Path | None = None):
        cwd_path = cwd_path or source_path.parent
        if not source_path.exists():
            print(f"Error: The path '{source_path}' is not valid.")
            return -1
        tree = self._parser_file(source_path)
        generator: MCGenerator = MCGenerator(self.config)
        target_path.mkdir(parents=True, exist_ok=True)
        with chdir(cwd_path):
            try:
                ir_build_start_time = time.time()
                generator.visit(tree)
                print(f"IR生成用时：{time.time() - ir_build_start_time}")
                ir_builder = generator.get_ir()
                ir_optimize_start_time = time.time()
                ir_builder = Optimizer(ir_builder, self.config).optimize()
                print(f"IR优化用时：{time.time() - ir_optimize_start_time}")
                if self.config.output_temp_file:
                    with open(target_path / f"{self.config.namespace}.mcdc", "wb") as f:
                        f.write(IRSymbolSerializer.dump(ir_builder, f"mcdc-{repr(self.config.minecraft_version)}"))

                if self.config.debug:
                    print("最终ir")
                    self._print_ir_builder(ir_builder)
                if not self.config.no_generate_commands:
                    # 输出到target目录
                    if self.config.backend_name:
                        used_backend = registry.backends.get(self.config.backend_name, None)
                        if used_backend is None:
                            print(f"找不到名为{self.config.backend_name}的后端")
                            return -1
                    else:
                        for name, backend in registry.backends.items():
                            if backend.is_support(self.config):
                                print(f"自动选择{name}后端")
                                used_backend = backend
                                break
                        else:
                            print(f"找不到可用后端")
                            return -1

                    code_generator_start_time = time.time()
                    used_backend(ir_builder, target_path, self.config).generate_commands()
                    print(f"最终代码生成与写入总用时：{time.time() - code_generator_start_time}")
            except CompilationError as e:
                time.sleep(0.1)  # 保证前面的输出完成
                if generator:
                    self._print_error_info(generator.scope_stack)
                print(e.__repr__())
                if self.config.debug:
                    # 重新抛出异常显示错误详情
                    raise
                return -1
            except Exception:
                time.sleep(0.1)
                if generator:
                    self._print_error_info(generator.scope_stack)
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
        # 节点显示：作用域名 (类型)
        scope_type_str = f" ({node.type.value})" if node.type else ""
        line = f"{prefix}{'└── ' if is_tail else '├── '}{node.name}{scope_type_str}"
        print(line)

        # 处理子节点
        children = node.children
        for index, child in enumerate(children):
            new_prefix = prefix + ("    " if is_tail else "│   ")
            Compile._print_scope_tree(
                child, new_prefix, index == len(children) - 1)

    @staticmethod
    def _print_error_info(scope_stack: list[Scope]):
        # 定义作用域树打印函数

        # 打印错误信息
        print("\n⚠️ Compilation Error ⚠️")
        print("Current scope structure:")
        Compile._print_scope_tree(scope_stack[0])

        # 打印当前作用域栈（调用链）
        print("\nScope call stack:")
        for i, scope in enumerate(scope_stack):
            indent = "  " * i
            type_str = f" ({scope.type.value})" if scope.type else ""
            print(f"{indent}{scope.name}{type_str}")


if __name__ == "__main__":
    args_parser = argparse.ArgumentParser(description="dovetail")
    args_parser.add_argument('input', type=str, help='输入文件路径')
    args_parser.add_argument('--minecraft_version', '-mcv', metavar='version', type=str, help='游戏版本',
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
    args_parser.add_argument('--disable-warnings', action='store_true', help='禁用警告')
    args_parser.add_argument('--disable-names-normalizer', action='store_true', help='禁用命名规范化')
    args_parser.add_argument('--debug', action='store_true', help='启用调试模式')
    args_parser.add_argument('--debug-mixin', action='store_true',
                             help='奇奇怪怪的修改(警告:这将会严重破坏编译器的功能)')

    args = args_parser.parse_args()
    if args.debug_mixin:
        import transpiler.easter_egg

        transpiler.easter_egg.main()
    NameNormalizer.enable = not args.disable_names_normalizer
    if args.disable_warnings:
        @Mixin(warnings, force=True)
        class WarningsMixin:
            @staticmethod
            @Inject("warn", At(At.HEAD), cancellable=True)
            def inject_warn(ci, *_args, **_kwargs):
                ci.cancel()

    compile_obj = Compile(
        GeneratorConfig(
            args.namespace or "namespace",
            OptimizationLevel(args.O),
            MinecraftVersion.from_str(args.minecraft_version),
            args.backend_name,
            args.debug,
            args.no_generate_commands,
            args.output_temp_file,
            args.enable_recursion,
            args.enable_same_name_function_nesting,
            False,
            args.enable_experimental,
            Path(args.lib_path).resolve() if args.lib_path else Path(__file__).parent / "lib"
        )
    )
    sys.exit(
        compile_obj.compile(
            args.input,
            args.output or "target"
        )
    )
