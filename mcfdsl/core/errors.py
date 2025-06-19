class CompilationError(Exception):
    """
    编译器错误异常基类
    用法：raise CompilationError("错误描述", line=行号, column=列号, filename="文件名")
    """

    def __init__(self, msg: str, line: int = None, column: int = None, filename: str = None):
        # 基础错误信息
        self.msg = msg

        # 代码位置信息
        self.line = line
        self.column = column
        self.filename = filename

        # 构建完整错误信息
        full_msg = self._format_message()
        super().__init__(full_msg)

    def _format_message(self) -> str:
        """格式化错误信息为：文件名:行号:列号: 错误描述"""
        location = []
        if self.filename:
            location.append(f"文件 {self.filename}")
        if self.line is not None:
            location.append(f"第 {self.line} 行")
            if self.column is not None:
                location.append(f"第 {self.column} 列")
        return f"{':'.join(location)}: {self.msg}" if location else self.msg

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: {self.msg}>"+""""""



class CompilerSyntaxError(CompilationError):
    """ 语法错误子类 """
    def __init__(self, msg: str, line: int = None, column: int = None, filename: str = None):
        super().__init__(msg, line, filename, column)

class TypeMismatchError(CompilationError):
    """ 类型错误子类 """
    def __init__(self, msg: str, line: int = None, column: int = None, filename: str = None):
        super().__init__(msg, line, filename, column)


class UnexpectedError(CompilationError):
    """
    表示编译过程中发生了未预期的内部错误
    用法：raise UnexpectedError("错误描述", line=行号, filename="文件名")
    """

    def __init__(self, msg: str, line: int = None, column: int = None, filename: str = None, context: str = None):
        # 添加上下文信息
        self.context = context

        # 构造友好错误信息
        full_msg = f"[内部错误] {msg}"
        if context:
            full_msg += f"\n上下文: {context}"

        super().__init__(full_msg, line=line, column=column, filename=filename)

    def __repr__(self) -> str:
        return f"<UnexpectedError: {self.msg}>" + """
    若你的代码符合mcfp标准且语法正确，请在 Github 提出 issue并尽量给出最小化测试样例
    """