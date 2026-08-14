# coding=utf-8
import ast
import hashlib
import pickle
import time
from collections.abc import Generator
from pathlib import Path
from typing import Optional

from lark import Lark, Tree

from dovetail.core.config import MAX_FILE_SIZE, CACHE_FILE_PREFIX
from dovetail.core.errors import report, Errors
from dovetail.core.parser.components import ErrorReporter
from dovetail.utils.logger import get_logger
from dovetail.utils.resource import resolve_project_path

# 初始化 Lark 解析器
_LARK_GRAMMAR_PATH = Path(resolve_project_path("lark/dovetail.lark"))
_lark_grammar_text = _LARK_GRAMMAR_PATH.read_text(encoding='utf-8')

lark_parser = Lark(
    _lark_grammar_text,
    start=["program", "expr"],
    parser='lalr',
    cache=".lark_cache",
    propagate_positions=True,
    maybe_placeholders=True
)

# 语法文件的 MD5，用作缓存 key 的一部分
# 语法变了 → 所有 .mcdc 缓存自动失效
_GRAMMAR_HASH: str = hashlib.md5(_lark_grammar_text.encode()).hexdigest()

logger = get_logger(__name__)


def _get_ast_cache_path(filepath: Path) -> Path:
    """
    根据源文件路径，返回对应的 AST 缓存文件路径（同目录，后缀 .mcdc）
    """
    return filepath.with_suffix(CACHE_FILE_PREFIX)


def _compute_file_hash(content: str) -> str:
    """
    计算源文件内容的 MD5
    """
    return hashlib.md5(content.encode()).hexdigest()


def _load_ast_cache(cache_path: Path, file_hash: str, start: str) -> Optional[Tree]:
    """
    尝试从 .mcdc 缓存文件中读取 AST。

    缓存格式（pickle）：
        {
            "grammar_hash": str,   # 语法文件 MD5
            "file_hash":    str,   # 源文件 MD5
            "start":        str,   # 解析起点，如 "program"
            "tree":         Tree,  # 序列化的 Lark AST
        }

    任意字段不匹配则视为缓存失效，返回 None。
    """
    if not cache_path.exists():
        return None
    try:
        with open(cache_path, 'rb') as f:
            cached = pickle.load(f)
        if (
                cached.get("grammar_hash") == _GRAMMAR_HASH
                and cached.get("file_hash") == file_hash
                and cached.get("start") == start
        ):
            return cached["tree"]
    except Exception:
        # 缓存损坏或格式不兼容，静默忽略，重新解析即可
        pass
    return None


def _save_ast_cache(cache_path: Path, file_hash: str, start: str, tree: Tree) -> None:
    """
    将 AST 写入 .mcdc 缓存文件。
    写入失败不影响主流程，静默忽略。
    """
    try:
        with open(cache_path, 'wb') as f:
            pickle.dump({
                "grammar_hash": _GRAMMAR_HASH,
                "file_hash": file_hash,
                "start": start,
                "tree": tree,
            }, f, protocol=pickle.HIGHEST_PROTOCOL)
    except Exception:
        pass


def parser_code(code: str, start: Optional[str] = None) -> Tree:
    """
    解析代码生成 AST

    Args:
        code: 代码
        start: 语法解析起点（可选）

    Returns:
        AST 树
    """
    parse_start = start if start is not None else "program"
    return lark_parser.parse(code, start=parse_start)


def parser_file(filepath: Path, start: Optional[str] = None, error_reporter: Optional[ErrorReporter] = None) -> \
        Optional[Tree]:
    """
    解析代码文件生成 AST。
    若源文件内容与语法文件均未变更，则直接从 .mcdc 缓存中读取 AST，跳过解析。

    Args:
        filepath: 代码文件路径
        start: 语法解析起点（可选）
        error_reporter: 错误报告器，不填则默认使用原始报告函数

    Returns:
        AST 树，如果文件不存在或解析失败则返回 None
    """
    _report = error_reporter.report if error_reporter is not None else report
    start_time = time.perf_counter()
    parse_start = start if start is not None else "program"

    if not filepath.exists() or not filepath.is_file():
        _report(Errors.FileNotFound, str(filepath))
        return None

    if filepath.stat().st_size >= MAX_FILE_SIZE:
        _report(
            Errors.FileSizeTooLarge,
            str(filepath),
            str(filepath.stat().st_size),
            str(MAX_FILE_SIZE),
            f"文件体积过大，最大支持{MAX_FILE_SIZE}字节，实际{filepath.stat().st_size}字节",
            suggestion="单文件战神"
        )
        return None

    with open(filepath, encoding='utf-8') as f:
        code = f.read()

    file_hash = _compute_file_hash(code)
    cache_path = _get_ast_cache_path(filepath)

    # 尝试命中缓存
    tree = _load_ast_cache(cache_path, file_hash, parse_start)
    if tree is not None:
        elapsed = time.perf_counter() - start_time
        logger.info(f"解析文件 '{filepath.name}' 命中缓存，用时 {elapsed:.3f}s.")
        return tree

    # 缓存未命中，正常解析并写回缓存
    tree = parser_code(code, start=start)
    _save_ast_cache(cache_path, file_hash, parse_start, tree)

    elapsed = time.perf_counter() - start_time
    logger.info(f"解析文件 '{filepath.name}' 用时 {elapsed:.3f}s.")
    return tree


def parse_fstring_iter(fstring: str) -> Generator[tuple[str, str], None, None]:
    """
    逐个 yield (type, content)
    type: 'literal' 或 'expr'
    """
    if fstring.startswith(('f"', "f'")):
        content = ast.literal_eval((fstring[1:]))
    else:
        content = ast.literal_eval(fstring)

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
