# coding=utf-8


class EscapeProcessor:
    """自动处理转义字符的工具类"""

    def __init__(self):
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

    def escape(self, text):
        """
        对字符串进行转义处理
        """
        if not isinstance(text, str):
            text = str(text)

        result = text
        # 按照转义字符映射进行替换
        for char, escaped in self.escape_map.items():
            result = result.replace(char, escaped)

        return result

    def unescape(self, text):
        """
        对已转义的字符串进行解码
        """
        if not isinstance(text, str):
            text = str(text)

        result = text
        # 按照反向映射进行替换（注意顺序，长的在前）
        sorted_unescape = sorted(self.unescape_map.items(),
                                 key=lambda x: len(x[0]), reverse=True)

        for escaped, char in sorted_unescape:
            result = result.replace(escaped, char)

        return result

    def escape_for_json(self, text):
        """
        为JSON格式转义字符串
        """
        if not isinstance(text, str):
            text = str(text)

        # 使用json模块处理
        import json
        return json.dumps(text)[1:-1]  # 去掉首尾的双引号

    def escape_for_python_string(self, text):
        """
        为Python字符串字面量转义
        """
        if not isinstance(text, str):
            text = str(text)

        # 使用repr函数获取Python字符串表示
        result = repr(text)
        # 去掉首尾的引号
        if result.startswith("'") and result.endswith("'"):
            return result[1:-1]
        elif result.startswith('"') and result.endswith('"'):
            return result[1:-1]
        return result

    def batch_escape(self, texts, method='escape'):
        """
        批量处理多个字符串
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
        return [processor(text) for text in texts]

    def smart_escape(self, text, context='general'):
        """
        智能转义 - 根据上下文选择合适的转义方式
        """
        if context == 'json':
            return self.escape_for_json(text)
        elif context == 'python':
            return self.escape_for_python_string(text)
        elif context == 'html':
            return self.escape_html(text)
        else:
            return self.escape(text)

    def escape_html(self, text):
        """
        HTML实体转义
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
def auto_escape(text, method='escape'):
    """
    便捷的转义函数

    Args:
        text: 要转义的文本
        method: 转义方法 ('escape', 'unescape', 'json', 'python')

    Returns:
        转义后的字符串
    """
    processor = EscapeProcessor()
    methods = {
        'escape': processor.escape,
        'unescape': processor.unescape,
        'json': processor.escape_for_json,
        'python': processor.escape_for_python_string
    }

    if method in methods:
        return methods[method](text)
    else:
        raise ValueError(f"不支持的方法: {method}")


# 使用示例
if __name__ == "__main__":
    # 创建处理器实例
    processor = EscapeProcessor()

    print("=== 基本转义示例 ===")
    # 你的例子
    test_text = '\\"'
    escaped = processor.escape(test_text)
    print(f'原文: {repr(test_text)}')
    print(f'转义后: {repr(escaped)}')
    print(f'显示: {escaped}')

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
    escaped_texts = processor.batch_escape(texts, 'escape')
    for original, escaped in zip(texts, escaped_texts):
        print(f'{repr(original)} -> {repr(escaped)}')

    print("\n=== 便捷函数使用 ===")
    result = auto_escape('This is a "test" string with \'quotes\' and \\backslashes\\')
    print(f'便捷转义结果: {repr(result)}')
