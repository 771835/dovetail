from __future__ import annotations

import sys

from antlr4.error.ErrorListener import ErrorListener

from mcfdsl.McFuncDSLParser import McFuncDSLParser, McFuncDSLLexer
from mcfdsl.McFuncDSLParser.McFuncDSLVisitor import *
from mcfdsl.core.McGenerator import MCGenerator

class ThrowingErrorListener(ErrorListener):
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        raise RuntimeError(f"Syntax error at line {line}:{column} - {msg}")

    def reportAmbiguity(self, recognizer, dfa, startIndex, stopIndex, exact, ambigAlts, configs):
        pass

    def reportAttemptingFullContext(self, recognizer, dfa, startIndex, stopIndex, conflictingAlts, configs):
        pass

    def reportContextSensitivity(self, recognizer, dfa, startIndex, stopIndex, prediction, configs):
        pass

def compile(source_path):
    input_stream = FileStream(source_path)
    lexer = McFuncDSLLexer.McFuncDSLLexer(input_stream)
    lexer.removeErrorListeners()
    lexer.addErrorListener(ThrowingErrorListener())
    stream = CommonTokenStream(lexer)
    parser = McFuncDSLParser.McFuncDSLParser(stream)
    parser.removeErrorListeners()
    parser.addErrorListener(ThrowingErrorListener())


    try:
        tree = parser.program()
        generator = MCGenerator()
        generator.visit(tree)
    except RuntimeError as e:
        sys.stderr.write(f"Compilation aborted due to syntax error: {e}")
        return  # 直接返回，不执行后续代码生成
    except Exception as e:
        # 定义作用域树打印函数
        def print_scope_tree(node, prefix="", is_tail=True):
            """递归打印作用域树结构"""
            # 节点显示：作用域名 (类型)
            type_str = f" ({node.type.value})" if node.type else ""
            line = f"{prefix}{'└── ' if is_tail else '├── '}{node.name}{type_str}"
            print(line)

            # 处理子节点
            children = node.children
            for i, child in enumerate(children):
                new_prefix = prefix + ("    " if is_tail else "│   ")
                print_scope_tree(child, new_prefix, i == len(children) - 1)

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

        # 重新抛出异常显示错误详情
        raise
    generator._generate_commands()
    # 输出到target目录


if __name__ == "__main__":
    compile("b.mcdl")
