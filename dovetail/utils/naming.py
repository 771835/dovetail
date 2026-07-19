# coding=utf-8
"""
命名规范化工具模块。
"""
import sys


class NameNormalizer:
    enable = False

    @staticmethod
    def _to_base36(n: int) -> str:
        if n == 0:
            return '0'
        digits = []
        while n:
            digits.append('0123456789abcdefghijklmnopqrstuvwxyz'[n % 36])
            n //= 36
        return ''.join(reversed(digits))

    @staticmethod
    def _to_base36_fixed(n: int) -> tuple[str, str]:
        """返回 (长度前缀数字字符, base36字符串)"""
        b36 = NameNormalizer._to_base36(n)
        return str(len(b36)), b36  # 长度前缀 + 内容

    @staticmethod
    def normalize(name: str) -> str:
        """
        将原始字符串规范化为兼容格式。

        规范化规则如下：
        - 大写字母替换为 "_小写形式"
        - 连续下划线 "__" 表示原始的下划线
        - 非字母数字或下划线的字符替换为 "_{后面编码的长度}{36进制编码的字符}"

        在 Windows 平台下，对于aux、com1、com2、prn、con、nul等会返回"_0_{对应字符}",不受命名归一化是否开启影响。

        Args:
            name (str): 原始字符串名称

        Returns:
            str: 规范化后的字符串
        """

        if sys.platform.startswith("win") and  name in ("aux","com1","com2","prn","con","nul"):
            return f"_0_{name}"

        if not NameNormalizer.enable:
            return name
        new_name = ""
        for char in name:
            if char.isupper():
                new_name += f"_{char.lower()}"
            elif char == "_":
                new_name += "__"
            elif char.isdigit() or char.islower():
                new_name += char
            else:
                prefix, b36 = NameNormalizer._to_base36_fixed(ord(char))
                new_name += f"_{prefix}{b36}"
        return new_name

    @staticmethod
    def denormalize(normalized_name: str) -> str:
        """
        将规范化后的名称还原为原始字符串。

        该方法会反向解析规范化后的字符串

        Args:
            normalized_name (str): 已规范化的字符串名称

        Returns:
            str: 还原后的原始字符串
        """
        if normalized_name.startswith('_0_'):
            return normalized_name[3:]

        if not NameNormalizer.enable:
            return normalized_name
        original = ""
        i = 0
        n = len(normalized_name)

        while i < n:
            if normalized_name[i] == '_':
                # 特殊字符：_ 后跟数字 1-9（长度前缀）
                if i + 1 < n and normalized_name[i + 1].isdigit() and normalized_name[i + 1] != '0':
                    length = int(normalized_name[i + 1])
                    start = i + 2
                    end = start + length
                    if end <= n:
                        ascii_str = normalized_name[start:end]
                        try:
                            char_code = int(ascii_str, 36)
                            original += chr(char_code)
                            i = end
                            continue
                        except ValueError:
                            # 处理无效的36进制 unicode 码
                            pass

                # 双下划线（原始下划线）
                if i + 1 < n and normalized_name[i + 1] == '_':
                    original += '_'
                    i += 2
                    continue

                # 大写字母标记
                if i + 1 < n and normalized_name[i + 1].islower():
                    original += normalized_name[i + 1].upper()
                    i += 2
                    continue

                # 处理单个下划线（不符合规范的情况）
                original += '_'
                i += 1
            else:
                # 普通字符（数字或小写字母）
                original += normalized_name[i]
                i += 1

        return original
