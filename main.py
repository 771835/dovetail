# coding=utf-8
from __future__ import annotations
import argparse
import io
import os
import sys
import time
import contextlib
from antlr4 import FileStream, CommonTokenStream
from antlr4.error.ErrorListener import ErrorListener

from mcfdsl.core.DSLParser import McFuncDSLLexer
from mcfdsl.core.DSLParser import McFuncDSLParser
from mcfdsl.core.errors import CompilationError
from mcfdsl.core.generator import MCGenerator
from mcfdsl.core.ir.ir_specification import OptimizationLevel


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


def compile_mcdl(source_path, target_path, optimization_level: OptimizationLevel):
    source_path = os.path.abspath(source_path)
    target_path = os.path.abspath(target_path)
    with contextlib.chdir(os.path.dirname(source_path)):
        start_time = time.time()
        input_stream = FileStream(source_path, "utf-8")
        lexer = McFuncDSLLexer.McFuncDSLLexer(input_stream)
        lexer.removeErrorListeners()
        listener = ThrowingErrorListener()
        lexer.addErrorListener(listener)
        stream = CommonTokenStream(lexer)
        parser = McFuncDSLParser.McFuncDSLParser(stream)
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
                    print_scope_tree(child, new_prefix, index == len(children) - 1)

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
                return 1
            generator = MCGenerator("mc_dsl")
            generator.visit(tree)
            # 输出到target目录
            ir_builder = generator.get_generate_ir()
            for i in ir_builder:
                sys.stdout.write(repr(i) + "\n")
            print(f" 耗时{time.time() - start_time}，原始生成指令{len(ir_builder._instructions)}条")
        except CompilationError as e:
            time.sleep(0.1)  # 保证前面的输出完成
            print_error_info()
            time.sleep(0.1)
            sys.stderr.write(e.__repr__())
            raise
        except Exception:
            time.sleep(0.1)
            print_error_info()
            # 重新抛出异常显示错误详情
            raise

    return 0


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="mcDSL")
    parser.add_argument('input', type=str, help='输入文件路径')
    parser.add_argument('--minecraft_version', '-mcv', metavar='version', type=str, help='生成游戏版本', default="1.20.4")
    parser.add_argument('--output', '-o', metavar='output', type=str, help='输出文件路径')
    parser.add_argument('-O', metavar='level', type=int, choices=[0, 1, 2], default=0,
                        help='优化级别')

    args = parser.parse_args()

    sys.exit(compile_mcdl(args.input, args.output or "target", OptimizationLevel(args.O)))
