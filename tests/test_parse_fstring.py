# coding=utf-8
"""
parse_fstring_iter() 测试

测试策略：覆盖字面量、单表达式、多表达式、嵌套大括号、
转义大括号、空字符串等边界情况。
"""
import unittest

from dovetail.core.parser.parser import parse_fstring_iter


class TestParseFstringIter(unittest.TestCase):

    def _collect(self, fstring: str) -> list[tuple[str, str]]:
        return list(parse_fstring_iter(fstring))

    def test_plain_string_no_expr(self):
        """纯字面量，无表达式"""
        result = self._collect('"hello world"')
        self.assertEqual(result, [("literal", "hello world")])

    def test_single_expression(self):
        """单个表达式"""
        result = self._collect('f"Hello, {name}"')
        self.assertEqual(result, [
            ("literal", "Hello, "),
            ("expr", "name"),
        ])

    def test_expression_only(self):
        """仅有表达式，无字面量"""
        result = self._collect('f"{value}"')
        self.assertEqual(result, [("expr", "value")])

    def test_multiple_expressions(self):
        """多个表达式"""
        result = self._collect('f"{a} and {b}"')
        self.assertEqual(result, [
            ("expr", "a"),
            ("literal", " and "),
            ("expr", "b"),
        ])

    def test_expression_at_start(self):
        """表达式在开头"""
        result = self._collect('f"{x} items"')
        self.assertEqual(result, [
            ("expr", "x"),
            ("literal", " items"),
        ])

    def test_expression_at_end(self):
        """表达式在结尾"""
        result = self._collect('f"count: {n}"')
        self.assertEqual(result, [
            ("literal", "count: "),
            ("expr", "n"),
        ])

    def test_escaped_braces_literal(self):
        """{{ 和 }} 应被解析为字面量 { 和 }"""
        result = self._collect('f"{{not an expr}}"')
        self.assertEqual(result, [("literal", "{not an expr}")])

    def test_nested_expression(self):
        """嵌套大括号的表达式（如函数调用）"""
        result = self._collect('f"{foo(a, b)}"')
        self.assertEqual(result, [("expr", "foo(a, b)")])

    def test_empty_fstring(self):
        """空 f-string 不应崩溃，不应产生任何输出"""
        result = self._collect('f""')
        self.assertEqual(result, [])

    def test_empty_plain_string(self):
        """空普通字符串"""
        result = self._collect('""')
        self.assertEqual(result, [])

    def test_consecutive_expressions(self):
        """两个连续表达式，中间无分隔"""
        result = self._collect('f"{a}{b}"')
        self.assertEqual(result, [
            ("expr", "a"),
            ("expr", "b"),
        ])

    def test_expression_with_string_inside(self):
        """表达式内部含有字符串（防止内层大括号干扰）"""
        result = self._collect('f"{foo(\\"bar\\")}"')
        self.assertIn(("expr", 'foo("bar")'), result)

    def test_non_fstring_plain(self):
        """非 f-string 前缀的普通字符串"""
        result = self._collect('"just a string"')
        self.assertEqual(result, [("literal", "just a string")])


if __name__ == "__main__":
    unittest.main()