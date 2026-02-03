# coding=utf-8
"""
编译错误类定义
"""
from pathlib import Path

from transpiler.core.enums.types import DataTypeBase

__all__ = [
    # 基础异常类
    'CompilationError',

    # 编译阶段错误
    'ASTError',
    'IROptimizationError',
    'GenerationError',

    # AST阶段细分错误
    'ASTSyntaxError',
    'ASTSemanticError',
    'ASTInternalError',

    # 具体错误类型
    'InvalidSyntaxError',
    'MissingTokenError',
    'InvalidOperatorError',
    'DuplicateDefinitionError',
    'TypeMismatchError',
    'UndefinedTypeError',
    'ArgumentTypeMismatchError',
    'NotCallableError',
    'PrimitiveTypeOperationError',
    'SymbolResolutionError',
    'UndefinedSymbolError',
    'UndefinedVariableError',
    'UndefinedFunctionError',
    'SymbolCategoryError',
    'ControlFlowError',
    'InvalidControlFlowError',
    'CompileRecursionError',
    'RecursionLimitError',
    'InterfaceError',
    'UnimplementedInterfaceMethodsError',
    'CompileNotImplementedError',
    'MissingImplementationError',
    'FunctionNameConflictError',
    'UnexpectedError',
    'LibraryLoadError',
    'CompilerIncludeError',

    # IR优化阶段错误
    'IRTypeError',
    'IRStructureError',
    'IROptimizationLimitError',

    # 代码生成阶段错误
    'CodeGenerationError',
    'TargetError',
    'OutputError',

    # 其他错误
    'MemoryLimitError',
    'VersionCompatibilityError',
]


class CompilationError(Exception):
    """
    编译器错误异常基类

    用法：raise CompilationError("错误描述", line=行号, column=列号, filename="文件名")

    Attributes:
        msg: 错误消息
        line: 行号
        column: 列号
        filename: 文件名
        full_msg: 完整格式化的错误消息
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
        self.full_msg = self._format_message()
        super().__init__(self.full_msg)

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
        return f"{self.__class__.__name__}:{self.full_msg}"


# ==================== 其他错误 ====================

class VersionCompatibilityError(CompilationError):
    """版本兼容性错误"""

    def __init__(self, feature: str, required_version: str, current_version: str,
                 line: int = None, column: int = None, filename: str = None):
        msg = f"功能 '{feature}' 需要版本 {required_version}，当前版本 {current_version}"
        super().__init__(msg, line=line, column=column, filename=filename)
        self.feature = feature
        self.required_version = required_version
        self.current_version = current_version


class MemoryLimitError(CompilationError):
    """内存限制错误"""

    def __init__(self, operation: str, limit: str, line: int = None,
                 column: int = None, filename: str = None):
        msg = f"操作 '{operation}' 超过内存限制 ({limit})"
        super().__init__(msg, line=line, column=column, filename=filename)
        self.operation = operation
        self.limit = limit


# ==================== 编译阶段错误 ====================

class ASTError(CompilationError):
    """AST遍历阶段错误"""
    pass


class IROptimizationError(CompilationError):
    """IR优化阶段错误"""
    pass


class GenerationError(CompilationError):
    """最终代码生成阶段错误"""
    pass


# ==================== AST阶段细分 ====================

class ASTSyntaxError(ASTError):
    """AST中的语法错误"""
    pass


class ASTSemanticError(ASTError):
    """AST中的语义错误"""
    pass


class ASTInternalError(ASTError):
    """AST内部错误"""
    pass


# ==================== 具体错误类型 ====================

class InvalidSyntaxError(ASTSyntaxError):
    """无效语法结构错误"""

    def __init__(self, reason: str, line: int = None,
                 column: int = None, filename: str = None):
        msg = f"无效语法: {reason}"
        super().__init__(msg, line=line, column=column, filename=filename)


class MissingTokenError(ASTSyntaxError):
    """缺少必要符号错误"""

    def __init__(self, token: str, line: int = None,
                 column: int = None, filename: str = None):
        msg = f"语法错误: 缺少必要的 '{token}'"
        super().__init__(msg, line=line, column=column, filename=filename)


class InvalidOperatorError(ASTSyntaxError):
    """无效运算符"""

    def __init__(self, op: str, line: int = None,
                 column: int = None, filename: str = None):
        msg = f"无效运算符 '{op}'"
        super().__init__(msg, line=line, column=column, filename=filename)


class DuplicateDefinitionError(ASTSyntaxError):
    """重复定义"""

    def __init__(self, name: str, line: int = None,
                 column: int = None, filename: str = None):
        msg = f"标识符 '{name}' 重复定义"
        super().__init__(msg, line=line, column=column, filename=filename)


class TypeMismatchError(ASTSemanticError):
    """类型错误基类"""

    def __init__(self, expected_type: str | DataTypeBase, actual_type: str | DataTypeBase,
                 line: int = None, column: int = None, filename: str = None, msg=None):
        if msg is None:
            msg = f"类型不匹配: 期望 {expected_type}，实际为 {actual_type}。"
        super().__init__(msg, line=line, column=column, filename=filename)
        self.expected_type = expected_type
        self.actual_type = actual_type


class UndefinedTypeError(TypeMismatchError):
    """使用未定义的类型"""

    def __init__(self, type_name: str | DataTypeBase, line: int = None,
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

    def __init__(self, param_name: str, expected: str | DataTypeBase, actual: str | DataTypeBase,
                 line: int = None, column: int = None, filename: str = None):
        super().__init__(expected, actual, line=line, column=column, filename=filename)
        self.param_name = param_name


class NotCallableError(TypeMismatchError):
    """不可调用错误"""

    def __init__(self, symbol_name: str, actual_type: str,
                 line: int = None, column: int = None, filename: str = None):
        msg = f"符号 '{symbol_name}' (类型 {actual_type}) 不可调用"
        super().__init__(
            "可调用类型", actual_type,
            line=line, column=column, filename=filename,
            msg=msg)


class PrimitiveTypeOperationError(ASTSemanticError):
    """对基本类型执行了不允许的操作"""

    def __init__(self, operation: str, type_name: str,
                 line: int = None, column: int = None, filename: str = None):
        msg = f"不支持的操作：'{operation}' 不能应用于基本类型 '{type_name}'"
        super().__init__(msg, line=line, column=column, filename=filename)


class SymbolResolutionError(ASTSemanticError):
    """符号解析错误基类"""

    def __init__(self, symbol_name: str, category: str,
                 msg: str = None, line: int = None, column: int = None, filename: str = None):
        msg = msg or f"{category} '{symbol_name}' 未找到"
        super().__init__(msg, line=line, column=column, filename=filename)


class UndefinedSymbolError(SymbolResolutionError):
    """未定义变量"""

    def __init__(self, var_name: str, line: int = None,
                 column: int = None, filename: str = None):
        super().__init__(var_name, "符号", line=line, column=column, filename=filename)


class UndefinedVariableError(SymbolResolutionError):
    """未定义变量"""

    def __init__(self, var_name: str, line: int = None,
                 column: int = None, filename: str = None):
        super().__init__(var_name, "变量", line=line, column=column, filename=filename)


class UndefinedFunctionError(SymbolResolutionError):
    """未定义函数"""

    def __init__(self, func_name: str, line: int = None,
                 column: int = None, filename: str = None):
        super().__init__(func_name, "函数", line=line, column=column, filename=filename)


class SymbolCategoryError(SymbolResolutionError):
    """符号类别错误（期望是某种类型的符号但实际是其他类型）"""

    def __init__(self, symbol_name: str, expected: str, actual: str,
                 line: int = None, column: int = None, filename: str = None):
        """
        :param symbol_name: 符号名称
        :param expected: 期望的符号类型描述（如 "Variable", "Function" 等）
        :param actual: 实际的符号类型
        """
        self.expected_category = expected
        self.actual_category = actual
        self.symbol_name = symbol_name
        msg = f"符号 '{symbol_name}' 类别不匹配：期望 {expected}，实际为 {actual}"
        super().__init__(symbol_name, "", msg, line, column, filename)


class ControlFlowError(ASTSemanticError):
    """控制流错误基类"""
    pass


class InvalidControlFlowError(ControlFlowError):
    """非法控制流"""

    def __init__(self, msg: str, line: int = None,
                 column: int = None, filename: str = None):
        super().__init__(
            f"控制流错误: {msg}",
            line=line,
            column=column,
            filename=filename)


class CompileRecursionError(ControlFlowError):
    """递归深度错误"""

    def __init__(self, msg: str, line: int = None,
                 column: int = None, filename: str = None):
        super().__init__(f"递归错误: {msg}",
                         line=line, column=column, filename=filename)


class RecursionLimitError(CompileRecursionError):
    """递归深度限制错误"""

    def __init__(self, func_name: str, max_depth: int, line: int = None,
                 column: int = None, filename: str = None):
        msg = f"函数 '{func_name}' 超过最大递归深度限制 ({max_depth})"
        super().__init__(msg, line=line, column=column, filename=filename)
        self.func_name = func_name
        self.max_depth = max_depth


class InterfaceError(ASTSemanticError):
    """接口相关错误"""
    pass


class UnimplementedInterfaceMethodsError(InterfaceError):
    """未实现接口要求的方法"""

    def __init__(self, missing_methods: set[str], line: int = None,
                 column: int = None, filename: str = None):
        self.missing_methods = missing_methods
        methods_str = ', '.join(map(str, missing_methods))  # 明确列出缺失方法
        msg = (
            f"类未实现接口要求的{len(missing_methods)}个方法\n"
            f"缺失方法: {methods_str}\n"
            "请在类中实现这些必需的方法"
        )
        super().__init__(msg, line=line, column=column, filename=filename)


class CompileNotImplementedError(ASTSemanticError):
    """未实现功能错误基类"""
    pass


class MissingImplementationError(CompileNotImplementedError):
    """未实现的功能错误"""

    def __init__(self, feature: str, line: int = None,
                 column: int = None, filename: str = None):
        msg = f"功能 '{feature}' 暂未实现"
        super().__init__(msg, line=line, column=column, filename=filename)


class FunctionNameConflictError(CompileNotImplementedError):
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


class UnexpectedError(ASTInternalError):
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
            "若以上皆无误请提交问题报告于github的issues\n"
            "请附上：\n"
            "  1. 最小化复现代码\n"
            "  2. 完整错误日志"
        )


class LibraryLoadError(ASTInternalError):
    """库加载错误"""

    def __init__(self, library_name: str, reason: str, line: int = None,
                 column: int = None, filename: str = None):
        msg = f"无法加载库 '{library_name}': {reason}"
        super().__init__(msg, line=line, column=column, filename=filename)
        self.library_name = library_name
        self.reason = reason


class CompilerIncludeError(ASTError):
    """包含错误"""

    def __init__(self, path: str | Path, reason: str, line: int = None,
                 column: int = None, filename: str = None):
        msg = f"无法包含 '{path}': {reason}"
        super().__init__(msg, line=line, column=column, filename=filename)


# ==================== IR优化阶段错误 ====================
class IRTypeError(IROptimizationError):
    """IR类型错误"""
    pass


class IRStructureError(IROptimizationError):
    """IR结构错误"""
    pass


class IROptimizationLimitError(IROptimizationError):
    """优化限制错误"""
    pass


# ==================== 代码生成阶段错误 ====================
class CodeGenerationError(GenerationError):
    """代码生成错误"""
    pass


class TargetError(GenerationError):
    """目标平台错误"""
    pass


class OutputError(GenerationError):
    """输出错误"""
    pass
