# coding=utf-8
from __future__ import annotations

import argparse
import contextlib
import io
import os.path
import sys
import time

from antlr4 import FileStream, CommonTokenStream
from antlr4.error.ErrorListener import ErrorListener

from transpiler.core.backend.code_generator.c_je_1204 import CodeGenerator
from transpiler.core.backend.optimizer.o_je_1204 import Optimizer
from transpiler.core.backend.specification import MinecraftVersion
from transpiler.core.errors import CompilationError
from transpiler.core.generator_config import GeneratorConfig, OptimizationLevel
from transpiler.core.instructions import IRScopeBegin, IRScopeEnd
from transpiler.core.ir_generator import MCGenerator
from transpiler.core.parser import transpilerLexer
from transpiler.core.parser import transpilerParser


class ThrowingErrorListener(ErrorListener):
    buffer = io.StringIO()
    error = False

    def syntaxError(self, recognizer, offending_symbol, line, column, msg, e):
        self.error = True
        self.buffer.write(f"Syntax error at line {line}:{column} - {msg} \n")

    def reportAmbiguity(
            self,
            recognizer,
            dfa,
            start_index,
            stop_index,
            exact,
            ambig_alts,
            configs):
        pass

    def reportAttemptingFullContext(
            self,
            recognizer,
            dfa,
            start_index,
            stop_index,
            conflicting_alts,
            configs):
        pass

    def reportContextSensitivity(
            self,
            recognizer,
            dfa,
            start_index,
            stop_index,
            prediction,
            configs):
        pass


def compile_file(source_path, target_path,
                 config: GeneratorConfig):
    source_path = os.path.abspath(source_path)
    target_path = os.path.abspath(target_path)
    with contextlib.chdir(os.path.dirname(source_path)):
        start_time = time.time()
        input_stream = FileStream(source_path, "utf-8")
        lexer = transpilerLexer.transpilerLexer(input_stream)
        lexer.removeErrorListeners()
        listener = ThrowingErrorListener()
        lexer.addErrorListener(listener)
        stream = CommonTokenStream(lexer)
        parser = transpilerParser.transpilerParser(stream)
        parser.removeErrorListeners()
        parser.addErrorListener(listener)

        def print_error_info():
            # 定义作用域树打印函数
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
                    print_scope_tree(
                        child, new_prefix, index == len(children) - 1)

            # 打印错误信息
            print("\n⚠️ Compilation Error ⚠️")
            print("Current scope structure:")
            print_scope_tree(generator.top_scope)

            # 打印当前作用域栈（调用链）
            print("\nScope call stack:")
            for i, scope in enumerate(generator.scope_stack):
                indent = "  " * i
                type_str = f" ({scope.type.value})" if scope.type else ""
                print(f"{indent}{scope.name}{type_str}")

        try:
            tree = parser.program()
            if listener.error:
                sys.stderr.write(listener.buffer.getvalue())
                return -1
            generator = MCGenerator(config)
            generator.visit(tree)
            # 输出到target目录
            ir_builder = generator.get_generate_ir()
            ir_builder = Optimizer(ir_builder, config).optimize()
            if not config.no_generate_commands:
                CodeGenerator(ir_builder, target_path, config).generate_commands()
            depth = 0
            for i in ir_builder:
                if isinstance(i, IRScopeEnd):
                    depth -= 1
                sys.stdout.write(depth * "    " + repr(i) + "\n")
                if isinstance(i, IRScopeBegin):
                    depth += 1

            print(f""" 耗时{time.time() - start_time}
原始生成指令{len(ir_builder.get_instructions())}条""")
        except CompilationError as e:
            time.sleep(0.1)  # 保证前面的输出完成
            print_error_info()
            time.sleep(0.1)
            sys.stderr.write(e.__repr__())
            if config.debug:
                # 重新抛出异常显示错误详情
                raise
            return -1
        except Exception:
            time.sleep(0.1)

            print_error_info()
            time.sleep(0.1)
            print("意外的错误，以下为详细堆栈信息")
            time.sleep(0.1)
            # 重新抛出异常显示错误详情
            raise

    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="mcDSL")
    parser.add_argument('input', type=str, help='输入文件路径')
    parser.add_argument('--minecraft_version', '-mcv', metavar='version', type=str, help='游戏版本',
                        default="1.20.4")
    parser.add_argument(
        '--output',
        '-o',
        metavar='path',
        type=str,
        help='输出文件路径')
    parser.add_argument(
        '--namespace',
        '-n',
        metavar='namespace',
        type=str,
        help='输出数据包命名空间')

    parser.add_argument('-O', metavar='level', type=int, choices=[0, 1, 2, 3], default=1,
                        help='优化级别')
    parser.add_argument('--no-generate-commands', action='store_true', help='不生成指令')
    parser.add_argument('--enable-recursion', action='store_true', help='启用递归(需后端支持)')
    parser.add_argument('--enable-same-name-function-nesting', action='store_true', help='启用同名函数嵌套')
    parser.add_argument('--enable-experimental', action='store_true', help='启用扩展模式')

    parser.add_argument('--debug', action='store_true',
                        help='启用调试模式')

    args = parser.parse_args()
    sys.exit(compile_file(args.input, args.output or "target",
                          GeneratorConfig(args.namespace or "namespace", OptimizationLevel(args.O),
                                          MinecraftVersion.from_str(args.minecraft_version), args.debug,
                                          args.no_generate_commands,
                                          args.enable_recursion,
                                          args.enable_same_name_function_nesting,
                                          args.enable_experimental)))
