# coding=utf-8
"""
编译期错误定义和报告模块
"""
import os
import random
import sys
from pathlib import Path
from typing import Optional

from dovetail.core.config import DEFAULT_SUGGESTIONS
from dovetail.utils.safe_enum import SafeEnum


class ErrorType(SafeEnum):
    """错误分类标签"""
    SyntaxError = (1, "语法错误", "源代码结构不符合语言规范")
    SemanticError = (2, "语义错误", "代码逻辑不符合语言语义规则")
    InternalError = (3, "内部错误", "编译器内部逻辑异常")
    RuntimeError = (4, "运行时错误", "执行期间发生的错误")
    SystemError = (5, "系统错误", "外部资源或环境相关错误")
    FatalError = (6, "致命错误", "无法继续编译的严重错误")


class Errors(SafeEnum):
    """具体错误类型"""

    # ==================== 语法错误 (ErrorType.SyntaxError) ====================
    # 基础语法错误
    InvalidSyntax = (0x1001, "无效语法", "无效语法: %s", ErrorType.SyntaxError)
    MissingToken = (0x1002, "缺少符号", "语法错误: 缺少必要的 '%s'", ErrorType.SyntaxError)
    InvalidOperator = (0x1003, "无效运算符", "无效运算符 '%s'", ErrorType.SyntaxError)
    DuplicateDefinition = (0x1004, "重复定义", "标识符 '%s' 重复定义", ErrorType.SyntaxError)

    # 注解相关错误
    InvalidAnnotation = (0x1005, "无效注解", "注解 '@%s' 无效或不存在。", ErrorType.SyntaxError)
    AnnotationArgumentError = (0x1006, "注解参数错误", "注解 '@%s' 参数错误: %s。", ErrorType.SyntaxError)

    # 类型声明错误
    InvalidTypeDeclaration = (0x1007, "无效类型声明", "类型声明无效: %s。", ErrorType.SyntaxError)
    InvalidArrayDimension = (0x1008, "无效数组维度", "数组维度 '%s' 无效，必须是正整数或标识符。", ErrorType.SyntaxError)
    NullableTypeError = (0x1009, "可空类型错误", "基本类型 '%s' 不能标记为可空，仅对象类型允许使用 '?'。",
                         ErrorType.SyntaxError)

    # Include 错误
    IncludePathError = (0x100A, "包含路径错误", "include 路径 '%s' 格式错误或无效。", ErrorType.SyntaxError)
    CircularInclude = (0x100B, "循环包含", "检测到循环包含: %s", ErrorType.SyntaxError)

    # 类/结构体/枚举错误
    EmptyStructDefinition = (0x100C, "空结构体定义", "结构体 '%s' 定义为空。", ErrorType.SyntaxError)
    InvalidEnumMember = (0x100D, "无效枚举成员", "枚举成员 '%s' 定义无效: %s。", ErrorType.SyntaxError)
    InvalidClassInheritance = (0x100E, "无效类继承", "类 '%s' 继承声明无效: %s。", ErrorType.SyntaxError)

    # 函数/方法错误
    InvalidFunctionSignature = (0x100F, "无效函数签名", "函数 '%s' 签名无效: %s。", ErrorType.SyntaxError)
    InvalidParameterDeclaration = (0x1010, "无效参数声明", "参数 '%s' 声明无效: %s。", ErrorType.SyntaxError)
    MissingTypeAnnotation = (0x1011, "缺少类型注解", "参数 '%s' 缺少必要的类型注解。", ErrorType.SyntaxError)
    DefaultParameterPosition = (0x1012, "默认参数位置错误", "带默认值的参数 '%s' 必须在无默认值参数之后。",
                                ErrorType.SyntaxError)

    # Typedef 错误
    TypedefRedefinition = (0x1013, "类型别名重定义", "类型别名 '%s' 已定义。", ErrorType.SyntaxError)

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

    CompareTypeMismatch = (0x2007, "比较对象类型不匹配", "比较对象类型不匹配 '%s' 和 '%s' 不可比较。",
                           ErrorType.SemanticError)

    # 所有权与可变性错误
    MutabilityViolation = (0x2007, "可变性冲突", "尝试修改不可变变量 '%s'。", ErrorType.SemanticError)
    InvalidMutUsage = (0x2008, "无效 mut 使用", "'mut' 关键字不能应用于类型 '%s'。", ErrorType.SemanticError)
    MutArgumentMismatch = (0x2009, "mut 参数不匹配", "参数 '%s' 需要 'mut' 修饰但未提供。", ErrorType.SemanticError)

    # 数组相关错误
    ArrayDimensionMismatch = (0x2010, "数组维度不匹配", "数组维度不匹配: 期望 %s 维，实际为 %s 维。",
                              ErrorType.SemanticError)
    ArraySizeUndefined = (0x2011, "数组大小未定义", "数组大小 '%s' 无法在编译期确定。", ErrorType.SemanticError)
    InvalidArrayLiteral = (0x2012, "无效数组字面量", "数组字面量类型不一致: %s。", ErrorType.SemanticError)

    # 可空类型错误
    NullableAccessError = (0x2013, "可空类型访问错误", "尝试访问可能为 null 的对象 '%s'，需要先进行 null 检查。",
                           ErrorType.SemanticError)
    NullAssignmentError = (0x2014, "null 赋值错误", "不能将 null 赋值给非可空类型 '%s'。", ErrorType.SemanticError)

    # F-string 错误
    FStringExpressionError = (0x2015, "F-string 表达式错误", "F-string 中的表达式 '%s' 无效: %s。",
                              ErrorType.SemanticError)

    # 成员访问错误
    InvalidMemberAccess = (0x2016, "无效成员访问", "类型 '%s' 没有成员 '%s'。", ErrorType.SemanticError)
    PrivateMemberAccess = (0x2017, "私有成员访问", "不能访问类 '%s' 的私有成员 '%s'。", ErrorType.SemanticError)

    # 数组/迭代器错误
    NotIterable = (0x2018, "不可迭代", "类型 '%s' 不可迭代，不能用于增强 for 循环。", ErrorType.SemanticError)
    InvalidArrayAccess = (0x2019, "无效数组访问", "索引类型必须为整数，实际为 '%s'。", ErrorType.SemanticError)

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
    BreakOutsideLoop = (0x4004, "break 在循环外", "'break' 语句只能在循环内使用。", ErrorType.SemanticError)
    ContinueOutsideLoop = (0x4005, "continue 在循环外", "'continue' 语句只能在循环内使用。", ErrorType.SemanticError)
    ReturnTypeMismatch = (0x4006, "返回类型不匹配", "返回值类型 '%s' 与声明类型 '%s' 不匹配。", ErrorType.SemanticError)
    MissingReturnStatement = (0x4007, "缺少返回语句", "函数 '%s' 声明了返回类型 '%s' 但缺少 return 语句。",
                              ErrorType.SemanticError)

    # 接口与实现错误
    UnimplementedInterfaceMethods = (0x5001, "未实现接口方法", "类未实现接口要求的 %d 个方法: %s。",
                                     ErrorType.SemanticError)
    MissingImplementation = (0x5002, "缺少实现", "功能 '%s' 暂未实现。", ErrorType.SemanticError)
    FunctionNameConflict = (0x5003, "函数名冲突", "函数名称 '%s' 与嵌套作用域 '%s' 冲突。", ErrorType.SemanticError)

    # 常量相关错误
    ConstantReassignment = (0x5004, "常量重新赋值", "不能对常量 '%s' 重新赋值。", ErrorType.SemanticError)
    ConstantRequiresInitialization = (0x5005, "常量需要初始化", "常量 '%s' 声明时必须初始化。", ErrorType.SemanticError)

    # 注解语义错误
    AnnotationNotApplicable = (0x5006, "注解不适用", "注解 '@%s' 不能应用于 %s。", ErrorType.SemanticError)
    ConflictingAnnotations = (0x5007, "注解冲突", "注解 '@%s' 与 '@%s' 冲突。", ErrorType.SemanticError)

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

    # 输入输出错误
    DirectoryCreationFailed = (0x9101, "目录创建失败", "无法创建目录 '%s': %s。", ErrorType.SystemError)
    FileSizeTooLarge = (0x9103, "文件体积过大", "无法解析文件 '%s': 文件体积 %s 超过最大允许体积 %s", ErrorType.SystemError)
    FileWriteFailed = (0x9102, "文件写入失败", "无法写入文件 '%s': %s。", ErrorType.SystemError)
    DiskSpaceInsufficient = (0x9104, "磁盘空间不足", "磁盘空间不足: 需要 %s，可用 %s。", ErrorType.SystemError)

    # 其他系统错误
    VersionCompatibility = (0x9201, "版本兼容性错误", "功能 '%s' 需要版本 %s，当前版本 %s。", ErrorType.SystemError)
    MemoryLimit = (0x9202, "内存限制错误", "操作 '%s' 超过内存限制 (%s)。", ErrorType.SystemError)
    ConfigurationError = (0x9203, "配置错误", "配置错误: %s。", ErrorType.SystemError)
    FileNotFound = (0x9204, "找不到文件错误", "文件 '%s' 不存在。", ErrorType.SystemError)


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

    with open(file_path, encoding='utf-8') as file:
        for current_line_number, line in enumerate(file, start=1):
            if start_line <= current_line_number <= end_line:
                lines.append(line.strip("\n"))  # 去除行末换行符和空格
            elif current_line_number > end_line:
                break  # 超过结束行则退出循环

    return lines


count = 0


def report(
        error: Errors,
        *args: str,
        filepath: Path | str = "<unknown>",
        line: int = -1,
        column: int = -1,
        suggestion: Optional[str] = None
) -> None:
    """
    报告一个错误

    Args:
        error: 报告错误的类型
        *args: 错误提示参数
        filepath: 错误发生文件
        line: 错误发生具体行数
        column: 错误发生具体列数
        suggestion: 错误修复建议

    Raises:
        CompilationError: 当错误类型为RuntimeError、SystemError、FatalError时引发（如果 should_raise 为 True）
    """
    global count
    count += 1
    if count % 10 == 0:
        sys.stderr.write(f"第 {count} 个报错了，再接再厉！")
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
        suggestion = random.choice(DEFAULT_SUGGESTIONS)
    sys.stderr.write(f"{error_name}({original_error_name}): {error_details % tuple(args)}{suggestion}\n\n")
