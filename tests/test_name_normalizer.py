# coding=utf-8
import unittest
from dovetail.utils.naming import NameNormalizer  # 请替换 your_module 为你的文件名


class TestNameNormalizer(unittest.TestCase):

    def setUp(self):
        # 每个测试前确保 enable 为 True
        NameNormalizer.enable = True

    def tearDown(self):
        # 每个测试后重置，防止污染其他测试
        NameNormalizer.enable = False

    def test_disabled_mode(self):
        """测试 enable=False 时，原样返回"""
        NameNormalizer.enable = False
        self.assertEqual(NameNormalizer.normalize("CamelCase"), "CamelCase")
        self.assertEqual(NameNormalizer.denormalize("CamelCase"), "CamelCase")

    def test_lowercase_and_digits(self):
        """测试小写字母和数字应保持不变"""
        self.assertEqual(NameNormalizer.normalize("abc123"), "abc123")
        self.assertEqual(NameNormalizer.denormalize("abc123"), "abc123")

    def test_uppercase_conversion(self):
        """测试大写字母转换为 _+小写"""
        self.assertEqual(NameNormalizer.normalize("A"), "_a")
        self.assertEqual(NameNormalizer.normalize("ABC"), "_a_b_c")
        self.assertEqual(NameNormalizer.denormalize("_a_b_c"), "ABC")

    def test_underscore_escaping(self):
        """测试下划线转换为双下划线"""
        self.assertEqual(NameNormalizer.normalize("_"), "__")
        self.assertEqual(NameNormalizer.normalize("a_b"), "a__b")
        self.assertEqual(NameNormalizer.denormalize("a__b"), "a_b")

    def test_special_characters(self):
        # "!" ASCII=33, base36=x（1位）→ _1x
        self.assertEqual(NameNormalizer.normalize("!"), "_1x")
        # " " ASCII=32, base36=w（1位）→ _1w
        self.assertEqual(NameNormalizer.normalize(" "), "_1w")
        self.assertEqual(NameNormalizer.denormalize("_1x"), "!")
        self.assertEqual(NameNormalizer.denormalize("_1w"), " ")

    def test_complex_combination(self):
        """测试多种情况组合"""
        original = "Camel_Case! 123"
        # C -> _c, a -> a, m -> m, e -> e, l -> l, _ -> __, C -> _c, a -> a, s -> s, e -> e, ! -> ___33___, ' ' -> ___32___
        # 结果: _camel____c_ase___33______32___123
        normalized = NameNormalizer.normalize(original)
        self.assertEqual(NameNormalizer.denormalize(normalized), original)

    def test_empty_string(self):
        """测试空字符串"""
        self.assertEqual(NameNormalizer.normalize(""), "")
        self.assertEqual(NameNormalizer.denormalize(""), "")

    def test_round_trip_consistency(self):
        """
        验证一致性：无论什么字符，只要是 NameNormalizer 允许处理的，
        反规范化后必须等于原始输入。
        """
        test_strings = [
            "Simple",
            "Complex_Name_With_Numbers_123",
            "Special!@#$%^&*()_+",
            "Unicode_Test_中文",  # 只要 ord() 能处理，通常没问题
            "___"  # 边界测试
        ]
        for s in test_strings:
            norm = NameNormalizer.normalize(s)
            denorm = NameNormalizer.denormalize(norm)
            self.assertEqual(denorm, s, f"Failed for input: {s}")

    def test_invalid_denormalization(self):
        """测试非预期的输入（健壮性检查）"""
        # 故意传入一个不符合规范的字符串，验证denormalize不会崩
        invalid_input = "___999abc"  # 这是一个无效的ASCII定义
        # 代码逻辑中 try...except 会跳过，应返回原样
        result = NameNormalizer.denormalize(invalid_input)
        self.assertIn("abc", result)


if __name__ == '__main__':
    unittest.main()
