# coding=utf-8
import time
from pathlib import Path
from typing import Optional

from lark import Lark, Tree

from dovetail.core.config import MAX_FILE_SIZE, get_project_logger
from dovetail.core.errors import report, Errors
from dovetail.utils.logger import get_logger

# 初始化 Lark 解析器
lark_parser = Lark(
    open(r".\lark\dovetail.lark", encoding='utf-8').read(),
    start=["program", "expr"],
    parser='lalr',
    cache=".lark_cache",
    propagate_positions=True,
    maybe_placeholders=True
)


def parser_code(code: str, start: Optional[str] = None) -> Optional[Tree]:
    """
    解析代码生成 AST

    Args:
        code: 代码
        start: 语法解析起点（可选）

    Returns:
        AST 树，如果文件不存在或解析失败则返回 None
    """

    parse_start = start if start is not None else "program"

    return lark_parser.parse(code, start=parse_start)  # , on_error=lambda e: True)


def parser_file(filepath: Path | str, start: Optional[str] = None) -> Optional[Tree]:
    """
    解析代码文件生成 AST

    Args:
        filepath: 代码文件路径
        start: 语法解析起点（可选）

    Returns:
        AST 树，如果文件不存在或解析失败则返回 None
    """
    start_time = time.perf_counter()

    filepath = Path(filepath)
    if not filepath.exists() or not filepath.is_file():
        return None

    if filepath.stat().st_size >= MAX_FILE_SIZE:
        report(
            Errors.ResourceExhaustion,
            f"文件体积过大，最大支持{MAX_FILE_SIZE}字节，实际{filepath.stat().st_size}字节",
            filepath=filepath,
            suggestion="单文件战神"
        )
        return None

    with open(filepath, encoding='utf-8') as f:
        code = f.read()

    tree = parser_code(code, start=start)

    elapsed = time.perf_counter() - start_time
    logger = get_project_logger() or get_logger("time")
    logger.info(f"解析文件 '{filepath.name}' 用时 {elapsed:.5f}.")
    return tree


def parse_fstring_iter(fstring: str):
    """
    逐个 yield (type, content)
    type: 'literal' 或 'expr'
    """
    if fstring.startswith(('f"', "f'")):
        content = fstring[2:-1]
    else:
        content = fstring

    i = 0
    n = len(content)
    literal_start = 0

    while i < n:
        char = content[i]

        if char == '{':
            if i + 1 < n and content[i + 1] == '{':
                i += 2
                continue

            # yield 当前字面量
            if i > literal_start:
                yield 'literal', content[literal_start:i].replace('{{', '{').replace('}}', '}')

            # 提取表达式
            i += 1
            expr_start = i
            depth = 1
            in_str = False
            quote = None

            while i < n and depth > 0:
                c = content[i]

                if c in '"\'':
                    if not in_str:
                        in_str = True
                        quote = c
                    elif c == quote and (i == 0 or content[i - 1] != '\\'):
                        in_str = False

                if not in_str:
                    if c == '{':
                        depth += 1
                    elif c == '}':
                        depth -= 1

                if depth > 0:
                    i += 1

            yield 'expr', content[expr_start:i]
            i += 1
            literal_start = i

        elif char == '}':
            if i + 1 < n and content[i + 1] == '}':
                i += 2
            else:
                i += 1
        else:
            i += 1

    # 最后的字面量
    if literal_start < n:
        yield 'literal', content[literal_start:].replace('{{', '{').replace('}}', '}')
