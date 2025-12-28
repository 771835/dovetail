# coding=utf-8


class NameNormalizer:
    enable = False

    @staticmethod
    def normalize(name: str) -> str:
        """将原始字符串规范化"""
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
        """将规范化后的名称还原为原始字符串"""
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
