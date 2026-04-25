# coding=utf-8
"""
AST 转换器模块 - Dovetail 编译器前端

本模块实现了基于 Lark 解析器的 AST 访问器，负责：
- 遍历抽象语法树（AST）
- 执行语义分析和类型检查
- 生成中间表示（IR）指令
- 管理符号表和作用域
- 处理导入和库加载

主要组件：
    - ASTVisitor: AST 访问器类，实现语义分析

使用示例：
    >>> config = CompileConfig(...)
    >>> visitor = ASTVisitor(config, Path("main.mcdl"))
    >>> ast_tree = parser_file("main.mcdl")
    >>> visitor.visit(ast_tree)
    >>> ir_builder = visitor.builder
"""
import ast
import itertools
import typing
from contextlib import contextmanager
from functools import lru_cache
from pathlib import Path
from typing import Callable, Any, Optional

from lark import Tree, v_args, Token, LarkError
from lark.tree import Meta
from lark.visitors import Interpreter

from dovetail.core import builtin_annotation
from dovetail.core.compile_config import CompileConfig
from dovetail.core.enums import (
    StructureType, PrimitiveDataType, VariableType,
    MinecraftVersion, MinecraftEdition, FunctionType, ValueType, BinaryOps, UnaryOps, CompareOps
)
from dovetail.core.enums.minecraft import UnknownMinecraftVersionError
from dovetail.core.enums.types import DataTypeBase, AnnotationCategory
from dovetail.core.errors import report, Errors
from dovetail.core.parser.components.include_manager import IncludeManager, CircularIncludeException
from dovetail.core.instructions import (
    IRDeclare, IRAssign, IRFunction, IRReturn, IRBreak, IRContinue, IRCondJump, IRJump, IRBinaryOp,
    IRUnaryOp, IRCall, IRScopeBegin, IRScopeEnd, IRCast
)
from dovetail.core.ir_builder import IRBuilder
from dovetail.core.lib.library import Library
from dovetail.core.lib.library_mapping import LibraryMapping
from dovetail.core.parser.parser import parser_file, parse_fstring_iter, parser_code
from dovetail.core.parser.scope import Scope
from dovetail.core.parser.components.declaration_handler import DeclarationHandler
from dovetail.core.parser.components.error_reporter import ErrorReporter
from dovetail.core.parser.components.ir_emitter import IREmitter
from dovetail.core.parser.components.symbol_resolver import SymbolResolver
from dovetail.core.parser.components.type_checker import TypeChecker
from dovetail.core.scope.protocols import ScopeCore
from dovetail.core.symbols import Variable, Reference, Literal, Function, Class, Parameter
from dovetail.core.symbols.annotation import Annotation
from dovetail.core.symbols.structure import Structure
from dovetail.core.symbols.typedef import Typedef
from dovetail.utils.naming import NameNormalizer

_n = NameNormalizer.normalize
_dn = NameNormalizer.denormalize


class ASTVisitor(Interpreter):
    """
    AST 访问器 - 遍历语法树并生成中间表示（IR）

    Attributes:
        config: 编译配置
        filepath: 当前编译的源文件路径
        builtin_function: 内建函数处理器映射表
        include_manager: 导入管理器
        builder: IR 构建器
    """

    def __init__(self, config: CompileConfig, entry_file: Path):
        super().__init__()
        self.config = config
        self.filepath = entry_file

        # 初始化内建函数表
        self.builtin_function: dict[str, Callable[..., Variable | Literal | None]] = {}

        # 初始化组件
        self.error_reporter = ErrorReporter(entry_file)
        self.builder = IRBuilder()
        self.ir_emitter = IREmitter(self.builder)

        # 初始化作用域及符号表
        self.symbol_resolver = SymbolResolver(
            Scope("top", None, StructureType.GLOBAL),
            self.error_reporter
        )

        self.type_checker = TypeChecker(self.error_reporter)

        self.declaration_handler = DeclarationHandler(
            self.symbol_resolver,
            self.type_checker,
            self.ir_emitter,
            self.error_reporter
        )

        self.include_manager = IncludeManager(self.error_reporter, entry_file)

        self.counter = itertools.count()

        # 加载内置库
        self._load_library(LibraryMapping.get("builtins", self.symbol_resolver, self.ir_emitter, self.error_reporter))
        if self.config.experimental:
            self._load_library(
                LibraryMapping.get("experimental", self.symbol_resolver, self.ir_emitter, self.error_reporter))

    def __default__(self, tree: Tree) -> list[Any]:
        """默认访问处理 - 递归访问所有子节点"""
        return self.visit_children(tree)

    # ==================== 辅助方法 ====================
    @contextmanager
    def _push_scope(self, name: str, scope_type: StructureType):
        self.ir_emitter.emit(IRScopeBegin(name, scope_type))
        with self.symbol_resolver.push_scope(name, scope_type) as scope:
            yield scope
        self.ir_emitter.emit(IRScopeEnd(name, scope_type))

    @lru_cache(maxsize=None)
    def _load_library(self, library: Library | None):
        """加载库并注册符号和处理器"""
        if library is None:
            return
        try:
            library.load()

            # 注册函数符号和处理器
            for function, handler in library.get_functions().items():
                self.symbol_resolver.add_symbol(function)
                self.builtin_function[function.get_name()] = handler

            # 注册常量
            for constant, value in library.get_variables().items():
                self.symbol_resolver.add_symbol(constant)
                self.ir_emitter.emit(IRDeclare(constant))
                self.ir_emitter.emit(IRAssign(constant, value))

            # 注册类和方法
            for class_, method_handlers in library.get_classes().items():
                self.symbol_resolver.add_symbol(class_)
                for method_name, handler in method_handlers.items():
                    self.builtin_function[f"{class_.name}:{method_name}"] = handler

        except Exception as e:
            self.error_reporter.report(
                Errors.LibraryLoad,
                library.get_name(),
                e.__repr__()
            )

    def _get_loop_check_scope_type(self) -> ScopeCore | None:
        """
        向上查找最近的 LOOP_CHECK 作用域

        遇到条件作用域和循环体作用域继续查找，遇到其他类型停止

        Returns:
            找到的循环作用域，未找到则返回 None
        """
        for scope in reversed(self.symbol_resolver.scope_stack):
            if scope.stype == StructureType.LOOP_CHECK:
                return scope
            elif scope.stype not in (StructureType.CONDITIONAL, StructureType.LOOP_BODY):
                break
        return None

    def _search_include_path(self, filepath: Path, meta: Meta) -> Path | None:
        """
        搜索导入文件的实际路径

        Args:
            filepath: 待搜索的文件路径
            meta: 代码元信息（用于错误报告）

        Returns:
            找到的完整路径，未找到则返回 None
        """
        if filepath.is_absolute():
            return filepath

        search_paths: list[Path] = [self.config.lib_path, Path.cwd()]
        include_path = next(
            (d / filepath for d in search_paths if (Path(d) / filepath).exists()),
            None
        )

        if include_path:
            return include_path
        else:
            self.error_reporter.report(
                Errors.IncludePathError,
                str(filepath),
                meta=meta
            )
            return None

    def _process_annotations(self, children: list[Tree | Token]) -> dict[Annotation, dict[str, Any]]:
        """
        提取并处理注解列表

        Args:
            children: AST 子节点列表（会被修改）

        Returns:
            注解映射表 {注解对象: 参数字典}
        """
        annotations: dict[Annotation, dict[str, Any]] = {}

        while (isinstance(children[0], Tree) and
               children[0].data == 'annotation'):
            annotation, args = self.visit(children.pop(0))
            annotations[annotation] = args

        return annotations

    def _should_skip_for_annotation(
            self,
            annotations: dict[Annotation, dict[str, Any]],
            symbol_name: str,
            meta: Meta
    ) -> bool:
        """
        根据注解判断是否跳过编译

        Args:
            annotations: 注解字典
            symbol_name: 符号对象
            meta: 元数据

        Returns:
            True 表示应该跳过，False 表示继续编译
        """
        for annotation, args in annotations.items():
            # 处理 @version 注解
            if annotation.name == "version":
                try:
                    min_version = MinecraftVersion.instance(args.get("min", "1.20.4"))
                except UnknownMinecraftVersionError:
                    self.error_reporter.report(
                        Errors.UnsupportedTargetVersion,
                        args.get("min", "1.20.4"),
                        meta=meta
                    )
                    return True

                try:
                    max_version = MinecraftVersion.instance(args.get("max", "1.21.4"))
                except UnknownMinecraftVersionError:
                    self.error_reporter.report(
                        Errors.UnsupportedTargetVersion,
                        args.get("max", "1.21.4"),
                        meta=meta
                    )
                    return True

                if not (min_version <= self.config.version <= max_version):
                    return True

            # 处理 @target 注解
            elif annotation.name == "target":
                target_edition = MinecraftEdition.from_str(args.get("edition", "java"))
                compiler_edition = self.config.version.edition

                if target_edition != compiler_edition:
                    return True

            # 处理 @if_not_exists 注解
            elif annotation.name == "if_not_exists":
                if self.symbol_resolver.current_scope.resolve_symbol(symbol_name) is not None:
                    return True

            # 处理 @if_symbol 注解
            elif annotation.name == "if_symbol":
                name: str = args.get("name", "")
                type_: str = args.get("type", "any")

                symbol = self.symbol_resolver.current_scope.resolve_symbol(name)

                if symbol is None:
                    return True

                match type_:
                    case "class":
                        if isinstance(symbol, Class):
                            return True
                    case "function":
                        if isinstance(symbol, Function):
                            return True
                    case "variable":
                        if isinstance(symbol, Variable):
                            return True
                    case _:
                        return True
                return False

            # 处理 @deprecated 注解
            elif annotation.name == "deprecated":
                return self.config.disable_deprecated_function
        return False

    def _process_call_arguments(
            self,
            symbol: Function,
            args: list[tuple[Reference, bool]],
            meta: Meta
    ) -> dict[str, Reference]:
        """
        处理函数/方法调用的参数

        根据符号形参填写实参并生成dict

        Args:
            symbol: 函数
            args: 实参列表
            meta: 调用处元数据

        Returns:
            参数名到参数值的映射字典
        """

        min_args: int = sum(not param.is_optional() for param in symbol.params)
        max_args: int = len(symbol.params)
        # 参数字典
        args_dict: dict[str, Reference] = {}

        # 检查参数数量是否在有效范围内
        if not min_args <= len(args) <= max_args:
            self.error_reporter.report(
                Errors.ArgumentNumberMismatch,
                symbol.name,
                f"{min_args}-{max_args}",
                str(len(args)),
                meta=meta
            )
            return args_dict

        # 效验数据并记录参数字典
        for i, (arg, param) in enumerate(itertools.zip_longest(args, symbol.params)):
            assert isinstance(param, Parameter)
            arg_value: Reference
            if arg is not None:
                arg_value, is_mutable = arg
            else:
                # 形参和缺省值必然存在一个，因此void()不可能被调用
                arg_value = param.default or Reference.void()
                is_mutable = param.mutable
            args_dict[param.get_name()] = arg_value
            # 类型检查
            if not arg_value.get_dtype().is_subclass_of(param.get_dtype()):
                self.error_reporter.report(
                    Errors.ArgumentTypeMismatch,
                    symbol.name,
                    str(param.get_dtype()),
                    str(arg_value.get_dtype()),
                    meta=meta
                )

            if param.mutable != is_mutable:
                self.error_reporter.report(
                    Errors.MutArgumentMismatch,
                    param.get_name(),
                    meta=meta
                )

        return args_dict

    # ==================== 访问器方法 ====================

    @v_args(meta=True)
    def struct(self, children: list[Tree | Token], meta: Meta):
        """处理结构体定义"""
        # 处理注解
        annotations = self._process_annotations(children)

        # 解析结构体
        name = children.pop(0).value

        # 检查版本和目标平台
        if self._should_skip_for_annotation(annotations, name, meta):
            return

        fields: dict[str, DataTypeBase] = {}
        for field in children:
            field_name, field_type = self.visit(field)
            fields[field_name] = field_type
        symbol = Structure(_n(name), fields)

        # 添加符号
        self.symbol_resolver.add_symbol(symbol, meta)

    def struct_field(self, tree: Tree) -> tuple[str, DataTypeBase]:
        """处理结构体字段"""
        name_token: Token = tree.children.pop(0)  # NOQA
        dtype_tree: Tree = tree.children.pop(0)  # NOQA
        name: str = name_token.value
        dtype: DataTypeBase = self.visit(dtype_tree)
        return name, dtype

    @v_args(meta=True)
    def function(self, children: list[Tree | Token], meta: Meta):
        """处理函数定义"""
        # 处理注解
        annotations = self._process_annotations(children)

        # 解析函数签名
        # annotation* ("function"|"fn"|"def") ID params ["->" type] (block|pass_stmt)
        params: list[Parameter]
        name: str = _n(children.pop(0).value)

        # 检查版本和目标平台
        if self._should_skip_for_annotation(annotations, name, meta):
            return

        params = self.visit(children.pop(0))
        if children[0] is not None:
            return_type: DataTypeBase = self.visit(children.pop(0))
        else:
            return_type: DataTypeBase = PrimitiveDataType.VOID
            children.pop(0)

        # 跳过 pass 语句
        if children and children[0].data == 'pass_stmt':
            children.pop()

        # 创建函数符号
        func_type = (FunctionType.FUNCTION if children
                     else FunctionType.FUNCTION_UNIMPLEMENTED)
        function = Function(name, params, return_type, func_type, annotations)
        self.symbol_resolver.add_symbol(function, meta, True)

        # 生成 IR
        self.ir_emitter.emit(IRFunction(function))

        # 处理函数体
        if children:
            with self._push_scope(name, StructureType.FUNCTION):  # NOQA
                with self.error_reporter.context(f"函数 {_dn(name)}"):
                    # 添加参数到作用域
                    for param in params:
                        self.symbol_resolver.add_symbol(param.var, meta)
                        self.ir_emitter.emit(IRDeclare(param.var))
                    # 访问函数体
                    self.visit(children.pop(0))

    @v_args(meta=True)
    def let(self, children: list[Tree | Token], meta: Meta) -> Optional[Reference]:
        """处理变量声明 (let)"""
        dtype: DataTypeBase
        symbol_name: str
        default_value: Reference | None = None

        symbol_name = str(children.pop(0).value)

        if isinstance(children[0], Tree) and children[0].data == 'type':
            # "let" ID ":" type ["=" expr]
            dtype = self.visit(children.pop(0))
            if children and children[0] is not None:
                default_value = self.visit(children.pop(0))
        else:
            # "let" ID "=" expr (类型推导)
            default_value = self.visit(children.pop(0))
            assert isinstance(default_value, Reference)
            dtype = default_value.get_dtype()

        return self.declaration_handler.declare_variable(symbol_name, dtype, default_value, meta)

    @v_args(meta=True)
    def const(self, children: list[Tree | Token], meta: Meta) -> Optional[Reference]:
        """处理常量声明 (const)"""
        dtype: DataTypeBase
        symbol_name: str
        value: Reference

        if isinstance(children[0], Tree) and children[0].data == "type":
            # "const" type ID "=" expr
            dtype = self.visit(children[0])
            symbol_name = children[1].value
            value = self.visit(children[2])
        else:
            # "const" ID [":" type] "=" expr
            symbol_name = children[0].value
            if children[1] is None:
                # 类型推导
                value = self.visit(children[2])
                dtype = value.get_dtype()
            else:
                dtype = self.visit(children[1])
                value = self.visit(children[2])

        return self.declaration_handler.declare_variable(symbol_name, dtype, value, meta, False)

    def params(self, tree: Tree) -> list[Parameter]:
        """处理参数列表"""
        return [self.visit(param) for param in tree.children if isinstance(param, Tree)]

    @v_args(meta=True)
    def param(self, children: list[Tree | Token], meta: Meta) -> Parameter:
        """处理单个参数定义"""
        name: str
        dtype: DataTypeBase
        is_mutable: bool = children.pop(0) is not None

        # 解析参数类型和名称
        # [MUT] ID ":" type ("=" expr)?
        name = _n(children.pop(0).value)
        dtype = self.visit(children.pop(0))

        # 处理默认值
        default_value: Reference
        if children:
            default_value = self.visit(children.pop(0))

            if default_value.get_dtype() != dtype:
                self.error_reporter.report(
                    Errors.TypeMismatch,
                    default_value.get_dtype().get_name(),
                    dtype.get_name(),
                    meta=meta
                )
                # 错误时返回无默认值的参数
                return Parameter(Variable(name, dtype, VariableType.PARAMETER))

            return Parameter(Variable(name, dtype, VariableType.PARAMETER), is_mutable, default_value)

        return Parameter(
            Variable(name, dtype, VariableType.PARAMETER),
            is_mutable
        )

    @v_args(meta=True)
    def for_loop(self, children: list[Tree | Token], meta: Meta):
        """处理 for 循环"""
        if isinstance(children[0], Tree) and children[0].data == "type":
            # "for" "(" type ID ":" expr ")" block // 增强for循环
            dtype = self.visit(children.pop(0))
            self.error_reporter.report(
                Errors.MissingImplementation,
                "增强for循环",
                meta=meta
            )
            return
        else:
            # "for" "(" [let | expr] ";" [condition] ";" [expr] ")" block // 传统for循环
            init, condition, expr, block = children
            if init is not None:
                # 处理初始化表达式
                self.visit(init)

            loop_count = next(self.counter)

            # 创建循环作用域
            with self._push_scope(f"for_check_{loop_count}", StructureType.LOOP_CHECK) as loop_check:  # NOQA
                # 处理条件表达式
                if condition:
                    condition_value = self.visit(condition).value
                else:
                    condition_value = Literal(PrimitiveDataType.BOOLEAN, True)

                # 处理循环体
                with self._push_scope(f"for_body_{loop_count}", StructureType.LOOP_BODY) as loop_body:  # NOQA
                    self.visit(block)
                    # 处理更新表达式
                    if expr:
                        self.visit(expr)

                self.ir_emitter.emit(IRCondJump(condition_value, loop_body.name))
                self.ir_emitter.emit(IRCondJump(condition_value, loop_check.name))
            self.ir_emitter.emit(IRJump(loop_check.name))

    def while_loop(self, tree: Tree):
        # "while" "(" [condition] ")" block
        loop_count = next(self.counter)
        condition: Tree | None
        block: Tree
        condition, block = tree.children
        with self._push_scope(f"while_check_{loop_count}", StructureType.LOOP_CHECK) as loop_check:  # NOQA
            with self._push_scope(f"while_body_{loop_count}", StructureType.LOOP_BODY) as loop_body:  # NOQA
                self.visit(block)

            if condition is not None:
                # 从检查函数调用循环体
                condition_value = self.visit(condition).value

                self.ir_emitter.emit(IRCondJump(condition_value, loop_body.name))
                self.ir_emitter.emit(IRCondJump(condition_value, loop_check.name))
            else:
                self.ir_emitter.emit(IRJump(loop_body.name))
        self.ir_emitter.emit(IRJump(loop_check.name))

    @v_args(meta=True)
    def if_stmt(self, children: list[Tree | Token], meta: Meta):
        # "if" "(" [condition] ")" block ("else" (if_stmt|block))?
        count = next(self.counter)
        # 计算条件表达式
        condition: Reference[Variable | Literal] = self.visit(children.pop(0))

        # 创建if分支作用域
        with self._push_scope(f"if_{count}", StructureType.CONDITIONAL) as if_scope:  # NOQA
            self.visit(children.pop(0))
        # 创建else分支作用域
        if children:
            with self._push_scope(f"else_{count}", StructureType.CONDITIONAL) as else_scope:  # NOQA
                self.visit(children.pop(0))
            self.ir_emitter.emit(IRCondJump(condition.value, if_scope.name, else_scope.name))
        else:
            self.ir_emitter.emit(IRCondJump(condition.value, if_scope.name))

    @v_args(meta=True)
    def free(self, _: list[Tree | Token], meta: Meta):
        report(
            Errors.MissingImplementation,
            "free 命令较为危险，故暂不实现(此错误不会影响编译)",
            filepath=self.filepath,
            line=meta.line,
            column=meta.column,
        )

    @v_args(meta=True)
    def condition(self, children: list[Tree | Token], meta: Meta):
        """条件语句"""
        value: Reference = self.visit(children.pop(0))

        if value.value_type not in (ValueType.VARIABLE, ValueType.LITERAL):
            self.error_reporter.report(
                Errors.SymbolCategory,
                value.get_name(),
                "VARIABLE/LITERAL",
                value.value_type.name,
                meta=meta
            )
            return Reference.literal(False)

        if not value.get_dtype().is_subclass_of(PrimitiveDataType.INT):
            self.error_reporter.report(
                Errors.TypeMismatch,
                "boolean/int",
                value.get_dtype().get_name(),
                meta=meta
            )
            return Reference.literal(False)

        return value

    @v_args(meta=True)
    def return_stmt(self, children: list[Tree | Token], meta: Meta):
        """处理 return 语句"""
        # 获取返回值
        value: Reference | None = None
        if children:
            value: Reference = self.visit(children.pop(0))
            # 标记返回值的变量类型
            if isinstance(value.value, Variable):
                value.value.var_type = VariableType.RETURN

        # 查找所在函数的作用域
        function_scope = next(
            (scope for scope in reversed(self.symbol_resolver.scope_stack)
             if scope.stype == StructureType.FUNCTION),
            None
        )

        if function_scope is None:
            self.error_reporter.report(
                Errors.InvalidControlFlow,
                "return 在函数之外",
                meta=meta
            )
            return
        function_scope: Scope

        # 类型检查
        if value is not None:
            function_symbol: Function | None = function_scope.parent.find_symbol(function_scope.name)

            if function_symbol is None:
                self.error_reporter.report(
                    Errors.InvalidControlFlow,
                    f"找不到函数{function_scope.name}的符号信息",
                    meta=meta
                )

            if function_symbol.return_type != value.get_dtype():
                self.error_reporter.report(
                    Errors.ReturnTypeMismatch,
                    value.get_dtype().get_name(),
                    function_symbol.return_type.get_name(),
                    meta=meta
                )
                return

        self.ir_emitter.emit(IRReturn(value))

    @v_args(meta=True)
    def break_stmt(self, _: list[Tree | Token], meta: Meta):
        """处理 break 语句"""
        loop_scope = self._get_loop_check_scope_type()

        if loop_scope is None:
            self.error_reporter.report(
                Errors.BreakOutsideLoop,
                meta=meta
            )
            return

        self.ir_emitter.emit(IRBreak(loop_scope.name))

    @v_args(meta=True)
    def continue_stmt(self, _: list[Tree | Token], meta: Meta):
        """处理 continue 语句"""
        loop_scope = self._get_loop_check_scope_type()

        if loop_scope is None:
            self.error_reporter.report(
                Errors.ContinueOutsideLoop,
                meta=meta
            )
            return

        self.ir_emitter.emit(IRContinue(loop_scope.name))

    @v_args(meta=True)
    def include(self, children: list, meta: Meta):
        """处理包含语句"""
        original_filepath: str = self.visit(children.pop(0)).value.value

        # 检查是否为内置库
        if library := LibraryMapping.get(original_filepath, self.symbol_resolver, self.ir_emitter, self.error_reporter):
            self._load_library(library)
            return

        # 搜索文件路径
        filepath = self._search_include_path(
            Path(original_filepath),
            meta
        )

        if filepath is None or filepath in self.include_manager:
            return

        self.include_manager.add_include_path(filepath)

        # 解析导入的文件
        try:
            old_filepath = self.filepath
            self.filepath = filepath
            self.error_reporter.set_filepath(filepath)

            with self.include_manager.including(filepath):
                ast_tree = parser_file(filepath, error_reporter=self.error_reporter)
                if ast_tree is None:
                    #  parser_file 内部已经进行过错误报告，因此无需重复报告
                    return
                self.visit(ast_tree)

            # 恢复原文件路径
            self.filepath = old_filepath
            self.error_reporter.set_filepath(old_filepath)

        except CircularIncludeException:  # 存在循环依赖则跳过解析
            pass
        except Exception as e:
            self.error_reporter.report(
                Errors.CompilerInclude,
                str(filepath),
                f"无法正确解析文件: {e.__repr__()}",
                meta=meta
            )

    @v_args(meta=True)
    def type(
            self,
            children: list[Token | Tree | int],
            meta: Meta
    ) -> PrimitiveDataType | Class | DataTypeBase:
        """处理类型声明"""
        original_name: str = children.pop(0).value

        # 尝试解析内置类型
        try:
            dtype = PrimitiveDataType.get_by_value(original_name)
        except ValueError:
            # 解析自定义类型
            dtype = self.symbol_resolver.resolve_symbol(_n(original_name), meta)

            # 展开类型别名
            if isinstance(dtype, Typedef):
                dtype = dtype.dtype

            if not isinstance(dtype, DataTypeBase):
                self.error_reporter.report(
                    Errors.UndefinedType,
                    original_name,
                    meta=meta
                )
                return PrimitiveDataType.UNDEFINED

        # 检查类型是否可定义
        if self.type_checker.check_definable(dtype, meta):
            return dtype
        else:
            return PrimitiveDataType.UNDEFINED

    @v_args(meta=True)
    def typedef(self, children: list[Token | Tree], meta: Meta):
        """处理类型别名定义"""
        original_type: DataTypeBase = self.visit(children.pop(0))
        new_name: str = children.pop(0).value  # NOQA

        new_type = Typedef(new_name, original_type)
        if not self.symbol_resolver.add_symbol(new_type):
            self.error_reporter.report(  # 将会报两个错误
                Errors.TypedefRedefinition,
                new_name,
                meta=meta
            )

    @v_args(meta=True)
    def factor(self, children: list[Token | Tree], meta: Meta):
        left: Reference = self.visit(children.pop(0))
        op: str = children.pop(0).value  # NOQA
        right: Reference = self.visit(children.pop(0))
        if not self.type_checker.check_binary_op_compatibility(left.get_dtype(), right.get_dtype(), op, meta):
            return Reference.literal(-1)

        # 生成结果变量
        result_type = self.type_checker.infer_binary_op_type(left.get_dtype(), right.get_dtype())

        result_var = self.ir_emitter.emit_binary_calc(left, BinaryOps(op), right, result_type)
        return Reference(result_var)

    term = factor

    @v_args(meta=True)
    def compare(self, children: list[Token | Tree], meta: Meta):
        left: Reference = self.visit(children.pop(0))
        op = children.pop(0).value  # NOQA
        right: Reference = self.visit(children.pop(0))
        if not left.get_dtype().is_subclass_of(right.get_dtype()) and not right.get_dtype().is_subclass_of(
                left.get_dtype()):
            # 当两方类型不同时不进行比较
            self.error_reporter.report(
                Errors.CompareTypeMismatch,
                repr(left.get_dtype()),
                repr(right.get_dtype()),
                meta=meta
            )
            return Reference.literal(False)

        # 生成比较指令
        result_variable = self.ir_emitter.emit_comparison(left, CompareOps(op), right)
        return Reference(result_variable)

    @v_args(meta=True)
    def unary_minus(self, children: list[Token | Tree], meta: Meta) -> Reference:
        op: typing.Literal['+', '-'] = children.pop(0).value  # NOQA
        value: Reference = self.visit(children.pop(0))
        if value.get_dtype() not in [PrimitiveDataType.BOOLEAN, PrimitiveDataType.INT]:
            self.error_reporter.report(
                Errors.InvalidOperator,
                op,
                meta=meta
            )
            return value

        if op == "+":
            return value

        if value.is_literal():
            return Reference.literal(value.value.value * -1)
        else:
            result_var = self.ir_emitter.emit_binary_calc(
                value,
                BinaryOps.MUL,
                Reference.literal(-1),
                PrimitiveDataType.INT
            )
            return Reference(result_var)

    @v_args(meta=True)
    def logical_not(self, children: list[Token | Tree], meta: Meta):
        value: Reference = self.visit(children.pop(0))

        if value.get_dtype() not in [PrimitiveDataType.BOOLEAN, PrimitiveDataType.INT]:
            self.error_reporter.report(
                Errors.InvalidOperator,
                "not",
                meta=meta
            )
            return value

        if value.is_literal():
            return Reference.literal(not value.value.value)
        else:
            result_var = self.ir_emitter.create_temp_var_declared(PrimitiveDataType.BOOLEAN, "boolean")
            self.ir_emitter.emit(
                IRUnaryOp(
                    result_var,
                    UnaryOps.NOT,
                    value
                )
            )
            return Reference(result_var)

    @v_args(meta=True)
    def logical_and(self, children: list[Token | Tree], meta: Meta):
        # 生成唯一结果变量
        result_var = self.ir_emitter.create_temp_var_declared(PrimitiveDataType.BOOLEAN, "boolean")
        and_id = next(self.counter)

        # 计算左侧数据的值
        left: Reference = self.visit(children.pop(0))
        if not PrimitiveDataType.BOOLEAN.is_subclass_of(left.get_dtype()):
            self.error_reporter.report(
                Errors.TypeMismatch,
                "boolean",
                left.get_dtype().get_name(),
                meta=meta
            )
            return Reference.literal(False)

        with self._push_scope(f"and_{and_id}", StructureType.CONDITIONAL):  # NOQA
            # 当第一个条件为假时调用
            self.ir_emitter.emit(IRAssign(result_var, Reference.literal(False)))

        with self._push_scope(f"and_{and_id}_2", StructureType.CONDITIONAL):  # NOQA
            # 短路计算，仅第一个条件为真时调用此处
            right: Reference = self.visit(children.pop(0))
            if not PrimitiveDataType.BOOLEAN.is_subclass_of(right.get_dtype()):
                self.error_reporter.report(
                    Errors.TypeMismatch,
                    "boolean",
                    f"{right.get_dtype()}",
                    meta=meta
                )
                return Reference.literal(False)
            self.ir_emitter.emit(IRAssign(result_var, right))

        self.ir_emitter.emit(IRCondJump(left.value, f"and_{and_id}_2", f"and_{and_id}"))
        return Reference(result_var)

    @v_args(meta=True)
    def logical_or(self, children: list[Token | Tree], meta: Meta):
        # 生成唯一结果变量
        result_var = self.ir_emitter.create_temp_var_declared(PrimitiveDataType.BOOLEAN, "boolean")
        or_id = next(self.counter)

        self.ir_emitter.emit(IRDeclare(result_var))

        # 计算左侧数据的值
        left: Reference = self.visit(children.pop(0))
        if not PrimitiveDataType.BOOLEAN.is_subclass_of(left.get_dtype()):
            self.error_reporter.report(
                Errors.TypeMismatch,
                "boolean",
                f"{left.get_dtype()}",
                meta=meta
            )
            return Reference.literal(False)

        with self._push_scope(f"or_{or_id}", StructureType.CONDITIONAL):  # NOQA
            # 当第一个条件为真时调用
            self.ir_emitter.emit(IRAssign(result_var, Reference.literal(True)))

        with self._push_scope(f"or_{or_id}_2", StructureType.CONDITIONAL):  # NOQA
            # 短路计算，仅第一个条件不为真时调用此处
            right: Reference = self.visit(children.pop(0))
            if not PrimitiveDataType.BOOLEAN.is_subclass_of(right.get_dtype()):
                self.error_reporter.report(
                    Errors.TypeMismatch,
                    "boolean",
                    f"{right.get_dtype()}",
                    meta=meta
                )
                return Reference.literal(False)
            self.ir_emitter.emit(IRAssign(result_var, right))

        self.ir_emitter.emit(IRCondJump(left.value, f"or_{or_id}", f"or_{or_id}_2"))
        return Reference(result_var)

    @v_args(meta=True)
    def local_assignment(self, children: list[Token | Tree], meta: Meta):
        variable_ref: Reference = self.visit(children.pop(0))
        if variable_ref.value_type != ValueType.VARIABLE:
            self.error_reporter.report(
                Errors.SymbolCategory,
                variable_ref.get_name(),
                "variable",
                variable_ref.value_type.name,
                meta=meta
            )
            return None
        variable: Variable = variable_ref.value
        if not variable.is_mutable():
            self.error_reporter.report(
                Errors.MutabilityViolation,
                variable.name,
                meta=meta
            )
            return None

        op: typing.Literal["+=", "-=", "*=", "/=", "%=", "="] = children.pop(0).value

        value: Reference = self.visit(children.pop(0))

        if variable.dtype != value.get_dtype():
            self.error_reporter.report(
                Errors.TypeMismatch,
                variable.dtype.get_name(),
                value.get_dtype().get_name(),
                meta=meta
            )
            return None

        if op == "=":
            self.ir_emitter.emit(IRAssign(variable, value))
        else:
            self.ir_emitter.emit(IRBinaryOp(variable, BinaryOps(op[0]), variable_ref, value))

        return variable_ref

    @v_args(meta=True)
    def function_call(self, children: list[Token | Tree], meta: Meta):
        function: Function = self.visit(children.pop(0)).value
        args: list[tuple[Reference, bool]] = self.visit(children.pop(0))
        if not isinstance(function, Function):
            self.error_reporter.report(
                Errors.NotCallable,
                function.get_name(),
                f"{function.__class__.__name__}",
                meta=meta
            )
            return Reference.literal(None)

        args_dict = self._process_call_arguments(function, args, meta)
        # 调用函数
        if function.function_type == FunctionType.LIBRARY:
            with self.error_reporter.context(f"调用内建函数 {function.name} 位于 {meta.line}:{meta.column}"):
                # 由于对内置函数的调用过程中的错误无行列信息提示，极难调试，故在此记录上下文
                result_var = self.builtin_function[function.get_name()](**args_dict)
            if result_var is not None:
                return Reference(result_var)
            else:
                return Reference.void()
        else:
            if function.return_type != PrimitiveDataType.VOID and function.return_type.is_definable():
                result_var = self.ir_emitter.create_temp_var_declared(function.return_type, "result")
                self.ir_emitter.emit(IRCall(result_var, function, args_dict))
                return Reference(result_var)
            else:
                self.ir_emitter.emit(IRCall(None, function, args_dict))
                return Reference.void()

    @v_args(meta=True)
    def arguments(self, children: list[Token | Tree], _: Meta) -> list[tuple[Reference, bool]]:
        return [self.visit(child) for child in children]

    @v_args(meta=True)
    def argument(self, children: list[Token | Tree], _: Meta) -> tuple[Reference, bool]:
        is_mutable = bool(children.pop(0))
        value = self.visit(children.pop(0))
        return value, is_mutable

    def null(self, _: Tree) -> Reference:
        """处理 null 字面量"""
        return Reference.literal(None)

    def literal(self, tree: Tree) -> Reference:
        """处理字面量"""
        token: Token = tree.children.pop()  # NOQA

        match token.type:
            case "STRING":
                return Reference.literal(ast.literal_eval(token))
            case "ARRAY_SIZE":
                return Reference.literal(int(token))
            case "INT":
                return Reference.literal(int(token))
            case "TRUE":
                return Reference.literal(True)
            case "FALSE":
                return Reference.literal(False)
            case _:
                return Reference.literal(str(token))

    @v_args(meta=True)
    def fstring(self, children: list[Token | Tree], meta: Meta):
        """处理f-string"""
        result = self.ir_emitter.create_temp_var_declared(PrimitiveDataType.STRING, "fstring")
        self.ir_emitter.emit(IRAssign(result, Reference.literal("")))
        for index, (data_type, data) in enumerate(parse_fstring_iter(children.pop().value)):
            if data_type == 'literal':
                # 直接赋值或将字面量加到结果变量末尾
                if index == 0:
                    self.ir_emitter.emit(
                        IRAssign(
                            result,
                            Reference.literal(data)
                        )
                    )
                else:
                    self.ir_emitter.emit(
                        IRBinaryOp(
                            result,
                            BinaryOps.ADD,
                            Reference(result),
                            Reference.literal(data)
                        )
                    )
            else:
                try:
                    with self.error_reporter.context(f"格式化字符串 {meta.line}:{meta.column}"):
                        expr: Reference = self.visit(parser_code(data, "expr"))
                except LarkError as e:
                    self.error_reporter.report(
                        Errors.FStringExpressionError,
                        data,
                        e.__repr__(),
                        meta=meta
                    )
                    break

                expr_str: Variable
                if expr.get_dtype() == PrimitiveDataType.STRING:
                    expr_str = expr.value
                elif expr.get_dtype().is_definable() and isinstance(expr.get_dtype(), PrimitiveDataType):
                    expr_str = self.ir_emitter.create_temp_var_declared(PrimitiveDataType.STRING, "fstring")
                    self.ir_emitter.emit(IRCast(expr_str, PrimitiveDataType.STRING, expr))
                else:
                    self.error_reporter.report(
                        Errors.FStringExpressionError,
                        data,
                        "不支持的字符串转换",
                        meta=meta
                    )
                    break

                # 进行拼接
                self.ir_emitter.emit(
                    IRBinaryOp(
                        result,
                        BinaryOps.ADD,
                        Reference(result),
                        Reference(expr_str)
                    )
                )
        return Reference(result)

    @v_args(meta=True)
    def identifier(self, children: list[str] | str, meta: Meta) -> Reference:
        """处理标识符引用"""
        symbol_name = children.pop() if isinstance(children, list) else children
        symbol = self.symbol_resolver.resolve_symbol(_n(symbol_name), meta)

        if symbol is None:
            return Reference.literal(None)

        return Reference(symbol)

    @v_args(meta=True)
    def annotation(
            self,
            children: list[Tree | Token],
            meta: Meta
    ) -> tuple[Annotation, dict[str, str]]:
        """
        处理注解声明

        Args:
            children: 注解名称和参数列表
            meta: 元数据

        Returns:
            (注解对象, 参数字典)，出错时返回未定义注解和空字典
        """
        name: str = children.pop(0).value
        annotation = builtin_annotation.get_annotation(name)

        # 检查注解是否存在
        if annotation is None:
            self.error_reporter.report(
                Errors.InvalidAnnotation,
                name,
                meta=meta
            )
            return self._undefined_annotation()

        # 处理无参数注解
        if annotation.params is None:
            if children:
                self.error_reporter.report(
                    Errors.ArgumentNumberMismatch,
                    name,
                    "0",
                    str(len(children)),
                    meta=meta
                )
            return annotation, {}

        # 检查参数数量匹配
        if len(children) != len(annotation.params):
            self.error_reporter.report(
                Errors.ArgumentNumberMismatch,
                name,
                str(len(annotation.params)),
                str(len(children)),
                meta=meta
            )
            return self._undefined_annotation()

        # 访问所有参数值并构建参数字典（参数名 -> 参数值）
        param_values = [self.visit(child).value.value for child in children]
        return annotation, dict(zip(annotation.params, param_values))

    @staticmethod
    def _undefined_annotation() -> tuple[Annotation, dict]:
        """返回一个未定义的注解占位符"""
        return Annotation("undefined", None, AnnotationCategory.METADATA), {}
