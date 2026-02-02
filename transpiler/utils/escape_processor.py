# coding=utf-8
"""
处理转义字符

提供字符串转义和反转义功能，支持多种格式（JSON、Python、HTML等）和批量处理。
"""


class EscapeProcessor:
    """自动处理转义字符的工具类

    Attributes:
        escape_map (dict): 转义字符映射表，键为原字符，值为转义后的字符串
        unescape_map (dict): 反向转义映射表，键为转义字符串，值为原字符
    """

    def __init__(self):
        """初始化 EscapeProcessor 实例"""
        # 定义常见的转义字符映射
        self.escape_map = {
            '\\': '\\\\',  # 反斜杠
            '"': '\\"',  # 双引号
            "'": "\\'",  # 单引号
            '\n': '\\n',  # 换行符
            '\r': '\\r',  # 回车符
            '\t': '\\t',  # 制表符
            '\b': '\\b',  # 退格符
            '\f': '\\f',  # 换页符
            '\v': '\\v',  # 垂直制表符
            '\0': '\\0',  # 空字符
        }

        # 反向映射（用于解码）
        self.unescape_map = {v: k for k, v in self.escape_map.items()}

    def escape(self, text: str) -> str:
        """对字符串进行转义处理

        Args:
            text (str): 需要转义的原始字符串

        Returns:
            str: 转义后的字符串
        """
        text = str(text)

        result = text
        # 按照转义字符映射进行替换
        for char, escaped in self.escape_map.items():
            result = result.replace(char, escaped)

        return result

    def unescape(self, text: str) -> str:
        """对已转义的字符串进行解码

        Args:
            text (str): 需要解码的转义字符串

        Returns:
            str: 解码后的原始字符串
        """
        text = str(text)

        result = text
        # 按照反向映射进行替换（注意顺序，长的在前）
        sorted_unescape = sorted(self.unescape_map.items(),
                                 key=lambda x: len(x[0]), reverse=True)

        for escaped, char in sorted_unescape:
            result = result.replace(escaped, char)

        return result

    def escape_for_json(self, text: str) -> str:
        """为JSON格式转义字符串

        Args:
            text (str): 需要转义的原始字符串

        Returns:
            str: 适用于JSON的转义字符串
        """
        text = str(text)

        # 使用json模块处理
        import json
        return json.dumps(text)[1:-1]  # 去掉首尾的双引号

    def escape_for_python_string(self, text: str) -> str:
        """为Python字符串字面量转义

        Args:
            text (str): 需要转义的原始字符串

        Returns:
            str: 适用于Python字符串字面量的转义字符串
        """
        text = str(text)

        # 使用repr函数获取Python字符串表示
        result = repr(text)
        # 去掉首尾的引号
        if result.startswith("'") and result.endswith("'"):
            return result[1:-1]
        elif result.startswith('"') and result.endswith('"'):
            return result[1:-1]
        return result

    def batch_escape(self, texts: list[str], method: str = 'escape') -> list[str]:
        """批量处理多个字符串

        Args:
            texts (list[str]): 需要处理的字符串列表
            method (str): 处理方法，可选值: 'escape', 'unescape', 'json', 'python'

        Returns:
            list[str]: 处理后的字符串列表

        Raises:
            ValueError: 当指定的方法不支持时抛出异常
        """
        methods = {
            'escape': self.escape,
            'unescape': self.unescape,
            'json': self.escape_for_json,
            'python': self.escape_for_python_string
        }

        if method not in methods:
            raise ValueError(f"不支持的方法: {method}")

        processor = methods[method]
        return [processor(text) for text in texts]  # NOQA

    def smart_escape(self, text: str, context: str = 'general') -> str:
        """智能转义 - 根据上下文选择合适的转义方式

        Args:
            text (str): 需要转义的原始字符串
            context (str): 上下文类型，可选值: 'json', 'python', 'html', 'general'

        Returns:
            str: 根据上下文转义后的字符串
        """
        if context == 'json':
            return self.escape_for_json(text)
        elif context == 'python':
            return self.escape_for_python_string(text)
        elif context == 'html':
            return self.escape_html(text)
        else:
            return self.escape(text)

    def escape_html(self, text: str) -> str:
        """HTML实体转义

        Args:
            text (str): 需要进行HTML转义的字符串

        Returns:
            str: HTML转义后的字符串
        """
        html_escape_map = {
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#x27;',
        }

        result = text
        for char, escaped in html_escape_map.items():
            result = result.replace(char, escaped)
        return result


# 便捷函数
def auto_escape(text: str, method: str = 'escape') -> str:
    """便捷的转义函数

    Args:
        text (str): 要转义的文本
        method (str): 转义方法 ('escape', 'unescape', 'json', 'python')

    Returns:
        str: 转义后的字符串

    Raises:
        ValueError: 当指定的方法不支持时抛出异常
    """
    processor = EscapeProcessor()
    methods = {
        'escape': processor.escape,
        'unescape': processor.unescape,
        'json': processor.escape_for_json,
        'python': processor.escape_for_python_string
    }
    if method in methods:
        return methods[method](text)  # NOQA
    else:
        raise ValueError(f"不支持的方法: {method}")


def main():
    """测试 EscapeProcessor 的各种功能

    包括基本转义、不同格式转义、批量处理和便捷函数使用等示例
    """
    # 创建处理器实例
    processor = EscapeProcessor()

    print("=== 基本转义示例 ===")

    print("\n=== 各种转义字符处理 ===")
    test_cases = [
        'Hello "World"',  # 双引号
        "It's a test",  # 单引号
        "Line 1\nLine 2",  # 换行符
        "Tab\there",  # 制表符
        'Path\\to\\file',  # 反斜杠
    ]

    for text in test_cases:
        escaped = processor.escape(text)
        print(f'原文: {repr(text)}')
        print(f'转义: {repr(escaped)}')
        print(f'转义: {escaped}')

        print(f'还原: {repr(processor.unescape(escaped))}')
        print('-' * 40)

    print("\n=== 不同上下文的转义 ===")
    text = 'He said: "It\'s a \"test\""'
    print(f'原文: {text}')
    print(f'JSON转义: {processor.escape_for_json(text)}')
    print(f'Python转义: {processor.escape_for_python_string(text)}')
    print(f'HTML转义: {processor.escape_html(text)}')

    print("\n=== 批量处理 ===")
    texts = ['Hello "World"', "It's great", "Line\nbreak"]
    escaped_texts = processor.batch_escape(texts)
    for original, escaped in zip(texts, escaped_texts):
        print(f'{repr(original)} -> {repr(escaped)}')

    print("\n=== 便捷函数使用 ===")
    result = auto_escape('This is a "test" string with \'quotes\' and \\backslashes\\')
    print(f'便捷转义结果: {repr(result)}')


# 使用示例
if __name__ == "__main__":
    main()
