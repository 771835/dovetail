# coding=utf-8
import argparse
import sys
import time
from pathlib import Path
from contextlib import chdir

start_time = time.time()

from transpiler.core.instructions import IRScopeEnd, IRScopeBegin
from transpiler.core.scope import Scope
from transpiler.utils.ir_serializer import IRSymbolSerializer

from transpiler.core.errors import CompilationError
from transpiler.core.ir_generator import MCGenerator

from antlr4 import FileStream, CommonTokenStream
from antlr4.error.ErrorListener import ErrorListener

from transpiler.core.backend.code_generator.c_je_1204 import CodeGenerator
from transpiler.core.backend.optimizer.o_je_1204 import Optimizer
from transpiler.core.backend.specification import MinecraftVersion
from transpiler.core.generator_config import GeneratorConfig, OptimizationLevel
from transpiler.core.parser import transpilerLexer
from transpiler.core.parser import transpilerParser
from transpiler.utils.mixin_manager import Mixin, Inject, At, CallbackInfoReturnable


@Mixin(ErrorListener)  # 相比于正常继承，使用mixin会慢0.001-0.01左右，但是可以减少代码量，而且好酷qwq
class ErrorListenerMixin:
    @staticmethod
    @Inject("syntaxError", At(At.HEAD), cancellable=True)
    def syntaxError(ci: CallbackInfoReturnable, self, recognizer, offending_symbol, line, column, msg, e):
        sys.stderr.write(f"Syntax error at line {line}:{column} - {msg} \n")
        ci.cancel()


class Compile:
    def __init__(self, config: GeneratorConfig):
        self.config = config

    def compile(self, source_path: Path, target_path: Path):
        source_path = Path(source_path)
        target_path = Path(target_path)
        source_dir = source_path.parent if source_path.is_file() else Path.cwd()
        s_t = time.time()
        tree = self.parser_file(source_path)
        print(f"AST分析用时：{time.time() - s_t}")
        if not tree:
            print("file not found!")
            return -1
        generator: MCGenerator = MCGenerator(self.config)
        with chdir(source_dir):
            try:
                s_t = time.time()
                generator.visit(tree)
                print(f"IR生成用时：{time.time() - s_t}")

                ir_builder = generator.get_ir()
                s_t = time.time()
                ir_builder = Optimizer(ir_builder, self.config).optimize()
                print(f"IR优化用时：{time.time() - s_t}")
                if self.config.output_temp_file:
                    with open(target_path.with_name(f"{target_path.stem}.mcdc"), "wb") as f:
                        f.write(IRSymbolSerializer.dump(ir_builder, "eb9a736010764a6da0a3448874db8e2c"))
                    print(IRSymbolSerializer(ir_builder).serialize())

                    depth = 0
                    for i in ir_builder:
                        if isinstance(i, IRScopeEnd):
                            depth -= 1
                        print(depth * "    " + repr(i))
                        if isinstance(i, IRScopeBegin):
                            depth += 1
                if not self.config.no_generate_commands:
                    # 输出到target目录
                    s_t = time.time()
                    CodeGenerator(ir_builder, target_path, self.config).generate_commands()
                    print(f"最终代码生成与写入总用时：{time.time() - s_t}")
                print(f"构建总用时 {time.time() - start_time}")
            except CompilationError as e:
                time.sleep(0.1)  # 保证前面的输出完成
                if generator:
                    self.print_error_info(generator.scope_stack)
                print(e.__repr__())
                if self.config.debug:
                    # 重新抛出异常显示错误详情
                    raise
                return -1
            except Exception:
                time.sleep(0.1)
                if generator:
                    self.print_error_info(generator.scope_stack)
                print("意外的错误，以下为详细堆栈信息")
                time.sleep(0.1)
                # 重新抛出异常显示错误详情
                raise

    @staticmethod
    def parser_file(file_path: str | Path) -> transpilerParser.transpilerParser.ProgramContext | None:
        try:
            input_stream = FileStream(str(Path(file_path).absolute()), "utf-8")
            lexer = transpilerLexer.transpilerLexer(input_stream)
            stream = CommonTokenStream(lexer)
            parser = transpilerParser.transpilerParser(stream)
            return parser.program()
        except FileNotFoundError:
            return None

    @staticmethod
    def print_scope_tree(node, prefix="", is_tail=True):
        """递归打印作用域树结构"""
        # 节点显示：作用域名 (类型)
        scope_type_str = f" ({node.type.value})" if node.type else ""
        line = f"{prefix}{'└── ' if is_tail else '├── '}{node.name}{scope_type_str}"
        print(line)

        # 处理子节点
        children = node.children
        for index, child in enumerate(children):
            new_prefix = prefix + ("    " if is_tail else "│   ")
            Compile.print_scope_tree(
                child, new_prefix, index == len(children) - 1)

    @staticmethod
    def print_error_info(scope_stack: list[Scope]):
        # 定义作用域树打印函数

        # 打印错误信息
        print("\n⚠️ Compilation Error ⚠️")
        print("Current scope structure:")
        Compile.print_scope_tree(scope_stack[0])

        # 打印当前作用域栈（调用链）
        print("\nScope call stack:")
        for i, scope in enumerate(scope_stack):
            indent = "  " * i
            type_str = f" ({scope.type.value})" if scope.type else ""
            print(f"{indent}{scope.name}{type_str}")


if __name__ == "__main__":
    args_parser = argparse.ArgumentParser(description="dovetail")
    args_parser.add_argument('input', type=str, help='输入文件路径')
    #args_parser.add_argument('--input', metavar='path', type=str, help='输入文件路径')
    args_parser.add_argument('--minecraft_version', '-mcv', metavar='version', type=str, help='游戏版本',
                             default="1.20.4")
    args_parser.add_argument(
        '--output',
        '-o',
        metavar='path',
        type=str,
        help='输出文件路径')
    args_parser.add_argument(
        '--lib-path',
        '-L',
        metavar='path',
        type=str,
        help='强制指定标准库路径')

    args_parser.add_argument(
        '--namespace',
        '-n',
        metavar='namespace',
        type=str,
        help='输出数据包命名空间')

    args_parser.add_argument('-O', metavar='level', type=int, choices=[0, 1, 2, 3], default=2, help='优化级别')
    args_parser.add_argument('--no-generate-commands', action='store_true', help='不生成指令')
    args_parser.add_argument('--output-temp-file', action='store_true', help='生成中间文件')
    args_parser.add_argument('--enable-recursion', action='store_true', help='启用递归(需后端支持)')
    args_parser.add_argument('--enable-same-name-function-nesting', action='store_true', help='启用同名函数嵌套')
    # args_parser.add_argument('--enable-first-class-functions', action='store_true',help='启用函数一等公民(所有代码都未适配，开不开都那样)')
    args_parser.add_argument('--enable-experimental', action='store_true', help='启用扩展模式(测试性功能)')
    args_parser.add_argument('--disable-warnings', action='store_true', help='禁用警告')
    args_parser.add_argument('--debug', action='store_true', help='启用调试模式')
    args_parser.add_argument('--wtf-mixin', action='store_true',
                             help='来点神奇的mixin(警告:这将会严重破坏编译器的功能)')

    args = args_parser.parse_args()
    if args.wtf_mixin:
        import transpiler.easter_egg

        transpiler.easter_egg.main()
    if args.disable_warnings:
        import warnings


        @Mixin(warnings, force=True)
        class WarningsMixin:
            @staticmethod
            @Inject("warn", At(At.HEAD), cancellable=True)
            def inject_warn(ci, *args, **kwargs):
                ci.cancel()

    compile_obj = Compile(
        GeneratorConfig(
            args.namespace or "namespace",
            OptimizationLevel(args.O),
            MinecraftVersion.from_str(args.minecraft_version),
            args.debug,
            args.no_generate_commands,
            args.output_temp_file,
            args.enable_recursion,
            args.enable_same_name_function_nesting,
            False,
            args.enable_experimental,
            Path(args.lib_path).absolute() if args.lib_path else Path(__file__).parent / "lib"
        )
    )
    sys.exit(
        compile_obj.compile(
            args.input,
            args.output or "target"
        )
    )
