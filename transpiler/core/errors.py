# coding=utf-8
from transpiler.core.language_enums import DataType


class CompilationError(Exception):
    """
    编译器错误异常基类
    用法：raise CompilationError("错误描述", line=行号, column=列号, filename="文件名")
    """

    def __init__(self, msg: str, line: int = None,
                 column: int = None, filename: str = None):
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
        """标准错误格式：filename:line:column: error"""
        location = []
        if self.filename:
            location.append(self.filename)
        if self.line is not None:
            location.append(str(self.line))
            if self.column is not None:
                location.append(str(self.column))
            else:
                location.append('0')  # 无列号时默认0
        else:
            return self.msg  # 无位置信息时直接返回消息

        return f"{':'.join(location)}: {self.msg}"

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: {self.msg}>" + """"""


class CompilerSyntaxError(CompilationError):
    """语法错误子类"""

    def __init__(self, msg: str, line: int = None,
                 column: int = None, filename: str = None):
        super().__init__(msg, line=line, column=column, filename=filename)  # 修正参数顺序


class TypeMismatchError(CompilationError):
    """类型错误子类"""

    def __init__(self, expected_type: str | DataType, actual_type: str | DataType,
                 line: int = None, column: int = None, filename: str = None, msg=None):
        if msg is None:
            msg = f"类型不匹配: 期望 {expected_type}，实际为 {actual_type}。"
        super().__init__(msg, line=line, column=column, filename=filename)
        self.expected_type = expected_type
        self.actual_type = actual_type


class UnexpectedError(CompilationError):
    """
    表示编译过程中发生了未预期的内部错误
    用法：raise UnexpectedError("错误描述", line=行号, filename="文件名")
    """

    def __init__(self, msg: str, line: int = None, column: int = None,
                 filename: str = None, context: str = None):
        self.context = context
        full_msg = f"[内部错误] {msg}"
        if context:
            full_msg += f"\n  上下文: {context}"

        # 直接传递完整消息，不进行父类的格式化
        super().__init__(full_msg, line=line, column=column, filename=filename)

    def __str__(self):
        base = super().__str__()
        return (
            f"{base}\n\n"
            "  1.确保使用使用最新版本\n"
            "  2.确定mc版本支持\n"
            "若以上皆无误请提交问题报告于github issues\n"
            "请附上：\n"
            "  1. 最小化复现代码\n"
            "  2. 完整错误日志"
        )


class InvalidSyntaxError(CompilerSyntaxError):
    """无效语法结构错误"""

    def __init__(self, token: str, line: int = None,
                 column: int = None, filename: str = None):
        msg = f"无效语法: 意外的符号 '{token}'"
        super().__init__(msg, line=line, column=column, filename=filename)


class MissingTokenError(CompilerSyntaxError):
    """缺少必要符号错误"""

    def __init__(self, token: str, line: int = None,
                 column: int = None, filename: str = None):
        msg = f"语法错误: 缺少必要的 '{token}'"
        super().__init__(msg, line=line, column=column, filename=filename)


class UndefinedTypeError(TypeMismatchError):
    """使用未定义的类型"""

    def __init__(self, type_name: str, line: int = None,
                 column: int = None, filename: str = None):
        msg = f"未定义的类型 '{type_name}'"
        super().__init__(
            f"<undefined>",
            f"'{type_name}'",
            line=line,
            column=column,
            filename=filename,
            msg=msg
        )


class ArgumentTypeMismatchError(TypeMismatchError):
    """函数参数类型不匹配"""

    def __init__(self, param_name: str, expected: str, actual: str,
                 line: int = None, column: int = None, filename: str = None):
        super().__init__(expected, actual, line=line, column=column, filename=filename)
        self.param_name = param_name


class InvalidOperatorError(CompilerSyntaxError):
    """无效运算符"""

    def __init__(self, op: str, line: int = None,
                 column: int = None, filename: str = None):
        msg = f"无效运算符 '{op}'"
        super().__init__(msg, line=line, column=column, filename=filename)


class DuplicateDefinitionError(CompilerSyntaxError):
    """重复定义"""

    def __init__(self, name: str, line: int = None,
                 column: int = None, filename: str = None):
        msg = f"标识符 '{name}' 重复定义"
        super().__init__(msg, line=line, column=column, filename=filename)


class CompilerImportError(CompilationError):
    """导入错误"""

    def __init__(self, path: str, reason: str, line: int = None,
                 column: int = None, filename: str = None):
        msg = f"无法导入 '{path}': {reason}"
        super().__init__(msg, line=line, column=column, filename=filename)


class UndefinedVariableError(CompilationError):
    """未定义变量"""

    def __init__(self, var_name: str, line: int = None,
                 column: int = None, filename: str = None):
        msg = f"未定义的变量 '{var_name}'"
        super().__init__(msg, line=line, column=column, filename=filename)


class InvalidControlFlowError(CompilationError):
    """非法控制流"""

    def __init__(self, msg: str, line: int = None,
                 column: int = None, filename: str = None):
        super().__init__(
            f"控制流错误: {msg}",
            line=line,
            column=column,
            filename=filename)


class MissingImplementationError(CompilerSyntaxError):
    """未实现的功能错误"""

    def __init__(self, feature: str, line: int = None,
                 column: int = None, filename: str = None):
        msg = f"功能 '{feature}' 暂未实现"
        super().__init__(msg, line=line, column=column, filename=filename)


class RecursionError(CompilationError):
    """递归深度错误"""

    def __init__(self, msg: str, line: int = None,
                 column: int = None, filename: str = None):
        super().__init__(f"递归错误: {msg}",
                         line=line, column=column, filename=filename)


class NotCallableError(TypeMismatchError):
    """不可调用错误"""

    def __init__(self, symbol_name: str, actual_type: str,
                 line: int = None, column: int = None, filename: str = None):
        msg = f"符号 '{symbol_name}' (类型 {actual_type}) 不可调用"
        super().__init__(
            "可调用类型", actual_type,
            line=line, column=column, filename=filename,
            msg=msg)


class SymbolCategoryError(TypeMismatchError):
    """符号类别错误（期望是某种类型的符号但实际是其他类型）"""

    def __init__(self, msg: str, expected: str, actual: str,
                 line: int = None, column: int = None, filename: str = None):
        """
        @param expected: 期望的符号类型描述（如 "Variable", "Function" 等）
        @param actual: 实际的符号类型
        """
        self.msg = msg
        self.expected_category = expected
        self.actual_category = actual
        super().__init__(expected, actual, line=line, column=column, filename=filename, msg=msg)


    def _format_message(self) -> str:
        """覆盖父类方法以提供更具体的错误信息"""
        base = super()._format_message()
        return f"{base}\n  期望类别: {self.expected_category}\n  实际类别: {self.actual_category}"


class UnimplementedInterfaceMethodsError(CompilationError):
    """未实现接口要求的方法"""

    def __init__(self, missing_methods: list[str], line: int = None,
                 column: int = None, filename: str = None):
        self.missing_methods = missing_methods
        methods_str = ', '.join(map(str, missing_methods))  # 明确列出缺失方法
        msg = (
            f"类未实现接口要求的{len(missing_methods)}个方法\n"
            f"缺失方法: {methods_str}\n"
            "请在类中实现这些必需的方法"
        )
        super().__init__(msg, line=line, column=column, filename=filename)


class FunctionNameConflictError(CompilationError):
    """函数名与作用域名冲突的错误"""

    def __init__(self, name: str, scope_name: str,
                 line: int = None, column: int = None, filename: str = None):
        msg = (
            f"函数名称 '{name}' 与嵌套作用域 '{scope_name}' 冲突\n"
            f"这种冲突可能导致作用域解析混乱\n"
            f"解决方案：\n"
            f"  1. 重命名函数\n"
            f"  2. 启用同名函数嵌套支持 (--enable-same-name-function-nesting)\n"
            f"  3. 修改冲突的作用域名"
        )
        super().__init__(msg, line=line, column=column, filename=filename)
        self.func_name = name
        self.scope_name = scope_name
