from __future__ import annotations

import sys

from antlr4.error.ErrorListener import ErrorListener

from mcfdsl.McFuncDSLParser import McFuncDSLParser, McFuncDSLLexer
from mcfdsl.McFuncDSLParser.McFuncDSLVisitor import *
from mcfdsl.core.errors import CompilationError
from mcfdsl.core.generator import MCGenerator


class ThrowingErrorListener(ErrorListener):
    def syntaxError(self, recognizer, offending_symbol, line, column, msg, e):
        raise RuntimeError(f"Syntax error at line {line}:{column} - {msg}")

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


def compile_mcdl(source_path):
    input_stream = FileStream(source_path, "utf-8")
    lexer = McFuncDSLLexer.McFuncDSLLexer(input_stream)
    lexer.removeErrorListeners()
    lexer.addErrorListener(ThrowingErrorListener())
    stream = CommonTokenStream(lexer)
    parser = McFuncDSLParser.McFuncDSLParser(stream)
    parser.removeErrorListeners()
    parser.addErrorListener(ThrowingErrorListener())

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
        generator = MCGenerator()
        generator.visit(tree)
        # 输出到target目录
        generator._generate_commands()
    except RuntimeError as e:
        sys.stderr.write(f"Compilation aborted due to syntax error: {e}")
        return 1  # 直接返回，不执行后续代码生成
    except CompilationError as e:
        print_error_info()
        sys.stderr.write(e.__repr__())
        raise
    except Exception as e:
        print_error_info()
        # 重新抛出异常显示错误详情
        raise

    return 0


if __name__ == "__main__":
    compile_mcdl("b.mcdl")
