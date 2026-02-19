# coding=utf-8
"""
编译期错误定义和报告模块
"""
import os
import random
from typing import Optional

from dovetail.core.config import DEFAULT_RANDOM_SUGGESTION
from dovetail.utils.safe_enum import SafeEnum
import sys
from pathlib import Path


class ErrorType(SafeEnum):
    """错误分类标签"""
    SyntaxError = (1, "语法错误", "源代码结构不符合语言规范")
    SemanticError = (2, "语义错误", "代码逻辑不符合语言语义规则")
    InternalError = (3, "内部错误", "编译器内部逻辑异常")
    RuntimeError = (4, "运行时错误", "执行期间发生的错误")
    SystemError = (5, "系统错误", "外部资源或环境相关错误")
    FatalError = (6, "致命错误", "无法继续编译的严重错误")


class Errors(SafeEnum):
    """具体错误类型，每个错误都属于一个 ErrorType"""

    # ==================== 语法错误 (ErrorType.SyntaxError) ====================
    # 基础语法错误
    InvalidSyntax = (0x1001, "无效语法", "无效语法: %s", ErrorType.SyntaxError)
    MissingToken = (0x1002, "缺少符号", "语法错误: 缺少必要的 '%s'", ErrorType.SyntaxError)
    InvalidOperator = (0x1003, "无效运算符", "无效运算符 '%s'", ErrorType.SyntaxError)
    DuplicateDefinition = (0x1004, "重复定义", "标识符 '%s' 重复定义", ErrorType.SyntaxError)

    # ==================== 语义错误 (ErrorType.SemanticError) ====================
    # 类型系统错误
    TypeMismatch = (0x2001, "类型不匹配", "类型不匹配: 期望 %s，实际为 %s。", ErrorType.SemanticError)
    UndefinedType = (0x2002, "未定义类型", "未定义的类型 '%s'。", ErrorType.SemanticError)
    ArgumentTypeMismatch = (0x2003, "参数类型不匹配", "参数 '%s' 类型不匹配: 期望 %s，实际为 %s。",
                            ErrorType.SemanticError)
    ArgumentNumberMismatch = (0x2004, "参数数量不匹配",
                              "调用函数 '%s' 参数数量不匹配: 期望 %s 个参数，实际为 %s 个参数。",
                              ErrorType.SemanticError)
    NotCallable = (0x2005, "不可调用", "符号 '%s' (类型 %s) 不可调用。", ErrorType.SemanticError)
    PrimitiveTypeOperation = (0x2006, "基本类型操作错误", "不支持的操作：'%s' 不能应用于基本类型 '%s'。",
                              ErrorType.SemanticError)

    # 符号解析错误
    SymbolResolution = (0x3001, "符号解析失败", "%s '%s' 未找到。", ErrorType.SemanticError)
    UndefinedSymbol = (0x3002, "未定义符号", "符号 '%s' 未定义。", ErrorType.SemanticError)
    UndefinedVariable = (0x3003, "未定义变量", "变量 '%s' 未定义。", ErrorType.SemanticError)
    UndefinedFunction = (0x3004, "未定义函数", "函数 '%s' 未定义。", ErrorType.SemanticError)
    SymbolCategory = (0x3005, "符号类别错误", "符号 '%s' 类别不匹配：期望 %s，实际为 %s。", ErrorType.SemanticError)

    # 控制流错误
    InvalidControlFlow = (0x4001, "无效控制流", "控制流错误: %s。", ErrorType.SemanticError)
    RecursionError = (0x4002, "递归错误", "递归错误: %s。", ErrorType.SemanticError)
    RecursionLimit = (0x4003, "递归限制错误", "函数 '%s' 超过最大递归深度限制 (%s)。", ErrorType.SemanticError)

    # 接口与实现错误
    UnimplementedInterfaceMethods = (0x5001, "未实现接口方法", "类未实现接口要求的 %d 个方法: %s。",
                                     ErrorType.SemanticError)
    MissingImplementation = (0x5002, "缺少实现", "功能 '%s' 暂未实现。", ErrorType.SemanticError)
    FunctionNameConflict = (0x5003, "函数名冲突", "函数名称 '%s' 与嵌套作用域 '%s' 冲突。", ErrorType.SemanticError)

    # ==================== 内部错误 (ErrorType.InternalError) ====================
    # 编译器内部错误
    UnexpectedError = (0x6001, "未预期错误", "[内部错误] %s。", ErrorType.InternalError)
    LibraryLoad = (0x6002, "库加载错误", "无法加载库 '%s': %s。", ErrorType.InternalError)
    CompilerInclude = (0x6003, "编译包含错误", "无法包含 '%s': %s。", ErrorType.InternalError)

    # IR类型错误
    IRInvalidType = (0x7001, "IR无效类型", "IR操作数类型无效: %s。", ErrorType.InternalError)
    IRTypeCoercionFailed = (0x7002, "IR类型转换失败", "无法将类型 %s 转换为 %s。", ErrorType.InternalError)

    # IR结构错误
    IRInvalidBlock = (0x7101, "IR无效基本块", "IR基本块结构无效: %s。", ErrorType.InternalError)
    IRInvalidInstruction = (0x7102, "IR无效指令", "IR指令结构无效: %s。", ErrorType.InternalError)

    # IR优化限制错误
    IROptimizationTooComplex = (0x7201, "IR优化过于复杂", "优化 '%s' 过于复杂，超出处理能力。", ErrorType.InternalError)
    IROptimizationTimeout = (0x7202, "IR优化超时", "优化 '%s' 超时。", ErrorType.InternalError)

    # ==================== 运行时错误 (ErrorType.RuntimeError) ====================
    # 代码生成错误
    FunctionTranslationFailed = (0x8001, "函数翻译失败", "函数 '%s' 翻译失败: %s。", ErrorType.RuntimeError)
    VariableMappingFailed = (0x8002, "变量映射失败", "变量 '%s' 映射失败: %s。", ErrorType.RuntimeError)
    InstructionTranslationFailed = (0x8003, "指令翻译失败", "指令 %s 翻译失败: %s。", ErrorType.RuntimeError)
    DataPackGenerationFailed = (0x8004, "数据包生成失败", "数据包生成失败: %s。", ErrorType.RuntimeError)
    NamespaceConflict = (0x8005, "命名空间冲突", "命名空间 '%s' 冲突: %s。", ErrorType.RuntimeError)
    ResourceExhaustion = (0x8006, "资源耗尽", "资源耗尽: %s。", ErrorType.RuntimeError)

    # ==================== 系统错误 (ErrorType.SystemError) ====================
    # 目标平台错误
    UnsupportedTargetVersion = (0x9001, "不支持的目标版本", "不支持的目标版本: %s。", ErrorType.SystemError)
    TargetFeatureNotSupported = (0x9002, "目标功能不支持", "目标平台不支持功能: %s。", ErrorType.SystemError)

    # 输出错误
    DirectoryCreationFailed = (0x9101, "目录创建失败", "无法创建目录 '%s': %s。", ErrorType.SystemError)
    FileWriteFailed = (0x9102, "文件写入失败", "无法写入文件 '%s': %s。", ErrorType.SystemError)
    DiskSpaceInsufficient = (0x9104, "磁盘空间不足", "磁盘空间不足: 需要 %s，可用 %s。", ErrorType.SystemError)

    # 其他系统错误
    VersionCompatibility = (0x9201, "版本兼容性错误", "功能 '%s' 需要版本 %s，当前版本 %s。", ErrorType.SystemError)
    MemoryLimit = (0x9202, "内存限制错误", "操作 '%s' 超过内存限制 (%s)。", ErrorType.SystemError)
    ConfigurationError = (0x9203, "配置错误", "配置错误: %s。", ErrorType.SystemError)


class CompilationError(Exception):
    """
    编译错误
    """
    pass


def read_lines_from_file(file_path, start_line, end_line) -> list[str]:
    """
    读取指定文件的特定几行的内容。

    Args:
        file_path: 文件路径
        start_line: 起始行号（1-based）
        end_line: 结束行号（1-based）

    Returns:
        指定行的内容列表
    """
    lines = []

    with open(file_path, 'r', encoding='utf-8') as file:
        for current_line_number, line in enumerate(file, start=1):
            if start_line <= current_line_number <= end_line:
                lines.append(line.strip("\n"))  # 去除行末换行符和空格
            elif current_line_number > end_line:
                break  # 超过结束行则退出循环

    return lines


def report(
        error: Errors,
        *args: str,
        filepath: Path | str = "<unknown>",
        line: int = -1,
        column: int = -1,
        suggestion: Optional[str] = None,
):
    error_code, error_name, error_details, error_type = error.value
    original_error_name = error.name
    filepath = Path(filepath)

    code = None
    if line != -1 and filepath.exists() and filepath.is_file():
        code = read_lines_from_file(filepath, max(line - 1, 1), line + 1)
    # 尽可能使显示的路径为相对路径
    if filepath.is_relative_to(Path.cwd()):
        filepath = os.path.relpath(filepath, Path.cwd())

    sys.stderr.write(f"发生错误: {error_name}({error_type.name})\n")
    sys.stderr.write(f"文件 '{filepath}', 行 {line}, 纵 {column}\n")

    # 输出错误代码块
    if code:
        sys.stderr.write(f"相关代码:\n")

        for l, linecode in zip(range(max(line - 1, 1), line + 2), code):
            if len(linecode) > 0:
                sys.stderr.write(f" {l} | {linecode}\n")

    # 选择建议
    if suggestion is None:
        suggestion = random.choice(DEFAULT_RANDOM_SUGGESTION)
    sys.stderr.write(f"{error_name}({original_error_name}): {error_details % tuple(args)}{suggestion}\n\n")

    if error_type.value[0] > 3:
        raise CompilationError("编译提前终止")
