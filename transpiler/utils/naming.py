# coding=utf-8
"""
命名规范化工具模块。

该模块提供了一个 `NameNormalizer` 类，用于将字符串名称规范化为特定格式，
并在需要时能够还原为原始字符串。主要用于处理标识符中不兼容的字符。
"""

class NameNormalizer:
    """
    提供名称规范化与反规范化功能的工具类。

    该类可以根据启用状态对字符串进行规范化处理，
    处理包括大写字母转小写并加前缀下划线、下划线转义、特殊字符编码等。
    """

    enable = False

    @staticmethod
    def normalize(name: str) -> str:
        """
        将原始字符串规范化为兼容格式。

        规范化规则如下：
        - 大写字母替换为 "_小写形式"
        - 连续下划线 "__" 表示原始的下划线
        - 非字母数字或下划线的字符替换为 "___ASCII码___"

        Args:
            name (str): 原始字符串名称

        Returns:
            str: 规范化后的字符串
        """
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
                new_name += f"___{str(ord(char))}___"
        return new_name

    @staticmethod
    def denormalize(normalized_name: str) -> str:
        """
        将规范化后的名称还原为原始字符串。

        该方法会反向解析规范化后的字符串：
        - "_小写字母" 转换为原始大写字母
        - "__" 转换为原始下划线
        - "___ASCII码___" 转换为原始特殊字符

        Args:
            normalized_name (str): 已规范化的字符串名称

        Returns:
            str: 还原后的原始字符串
        """
        if not NameNormalizer.enable:
            return normalized_name
        original = ""
        i = 0
        n = len(normalized_name)

        while i < n:
            if normalized_name[i] == '_':
                # 检查特殊字符标记 (___ASCII___)
                if i + 2 < n and normalized_name[i:i + 3] == '___':
                    # 找到结束标记
                    j = i + 3
                    while j + 2 < n and normalized_name[j:j + 3] != '___':
                        j += 1

                    if j + 2 < n and normalized_name[j:j + 3] == '___':
                        # 提取ASCII码
                        ascii_str = normalized_name[i + 3:j]
                        try:
                            char_code = int(ascii_str)
                            original += chr(char_code)
                            i = j + 3  # 跳过结束标记
                            continue
                        except ValueError:
                            # 处理无效ASCII码
                            pass

                # 检查双下划线 (原始下划线)
                if i + 1 < n and normalized_name[i + 1] == '_':
                    original += '_'
                    i += 2
                    continue

                # 检查大写字母标记 (_后跟小写字母)
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
