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
import re
import typing
from contextlib import contextmanager
from functools import lru_cache
from itertools import batched
from pathlib import Path
from typing import Callable, Any, Optional

from lark import Tree, v_args, Token, LarkError
from lark.tree import Meta
from lark.visitors import Interpreter

from dovetail.core.annotations.base import AnnotationTarget
from dovetail.core.annotations.spec import Annotation
from dovetail.core.compile_config import CompileConfig
from dovetail.core.enums import (
    StructureType, PrimitiveDataType, FunctionType,
    ValueType, BinaryOps, UnaryOps, CompareOps
)
from dovetail.core.enums.datatypes import DataTypeBase, ListType, ArrayType, DictType
from dovetail.core.errors import Errors
from dovetail.core.instructions import (
    IRDeclare, IRAssign, IRFunction, IRReturn, IRBreak, IRContinue, IRCondJump, IRJump, IRBinaryOp,
    IRUnaryOp, IRCall, IRScopeBegin, IRScopeEnd, IRIndexGet, IROpCode, IRStructDef, IRStructNew
)
from dovetail.core.ir_builder import IRBuilder
from dovetail.core.lib.library_mapping import LibraryMapping
from dovetail.core.parser.components.annotation_processor import AnnotationProcessor
from dovetail.core.parser.components.error_reporter import ErrorReporter
from dovetail.core.parser.components.include_manager import IncludeManager, CircularIncludeException
from dovetail.core.parser.components.ir_emitter import IREmitter
from dovetail.core.parser.components.symbol_resolver import SymbolResolver
from dovetail.core.parser.components.type_checker import TypeChecker
from dovetail.core.parser.parser import parser_file, parse_fstring_iter, parser_code
from dovetail.core.parser.scope import Scope
from dovetail.core.symbols import Variable, Reference, Literal, Function, Class, Parameter
from dovetail.core.symbols.base import MethodHost
from dovetail.core.symbols.structure import Structure
from dovetail.core.symbols.typedef import Typedef
from dovetail.utils.naming import NameDecorator

_n = NameDecorator.normalize
_dn = NameDecorator.denormalize

_SIMPLE_IDENT = re.compile(r'^[A-Za-z_][A-Za-z0-9_]*$')


def _try_fast_path_expr(
        data: str,
        symbol_resolver: SymbolResolver,
        meta
) -> Reference | None:
    """
    快速路径：纯标识符直接查符号表，跳过 lark 解析。
    不匹配则返回 None，交给原始路径处理。
    """
    data = data.strip()
    if not _SIMPLE_IDENT.match(data):
        return None
    symbol = symbol_resolver.resolve_symbol(_n(data), meta)
    if symbol is None:
        return None
    return Reference(symbol)

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
        self.builtin_function: dict[str, Optional[Callable[..., Variable | Literal | None]]] = {}

        # 初始化组件
        self.error_reporter = ErrorReporter(entry_file)
        self.builder = IRBuilder()

        self.type_checker = TypeChecker(self.error_reporter)

        # 初始化作用域及符号表
        self.symbol_resolver = SymbolResolver(
            Scope("top", None, StructureType.GLOBAL),
            self.error_reporter
        )

        self.annotation_processor = AnnotationProcessor(config, self.error_reporter, self.symbol_resolver)

        self.ir_emitter = IREmitter(
            self.builder,
            self.error_reporter,
            self.type_checker,
            self.symbol_resolver
        )

        self.include_manager = IncludeManager(self.error_reporter, entry_file, self.config)

        self.counter = itertools.count()

        # 加载内置库
        self._load_library("builtins")

        if self.config.experimental:
            self._load_library("experimental")

    # ==================== 辅助方法 ====================
    @contextmanager
    def _push_scope(self, name: str, scope_type: StructureType):
        self.ir_emitter.emit(IRScopeBegin(name, scope_type))
        with self.symbol_resolver.push_scope(name, scope_type) as scope:
            yield scope
        self.ir_emitter.emit(IRScopeEnd(name, scope_type))

    @lru_cache(maxsize=None)
    def _load_library(self, library_name: str):
        """加载库并注册符号和处理器"""
        library = LibraryMapping.get(library_name, self.symbol_resolver, self.ir_emitter, self.error_reporter,
                                     self.config)
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
                    self.builtin_function[f"{class_.name}::{method_name}"] = handler

        except Exception as e:
            self.error_reporter.report(Errors.LibraryLoad, library.get_name(), e.__repr__())

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
               children[0].data == 'annotation'):  # noqa
            annotation, args = self.visit(children.pop(0))  # noqa
            annotations[annotation] = args

        return annotations

    def _process_call_arguments(self, symbol: Function, args: list[Reference], meta: Meta) \
            -> dict[str, Reference]:
        """
        处理函数/方法调用的参数

        根据符号形参填写实参并生成dict=

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
            arg_ref: Reference
            if arg is not None:
                arg_ref = arg
            else:
                # 形参和缺省值必然存在一个，因此void()不可能被调用
                arg_ref = param.default or Reference.void()
            args_dict[param.get_name()] = arg_ref
            # 类型检查
            self.type_checker.check_type_match(
                param.dtype,
                arg_ref.dtype,
                f"函数 {symbol.name} 的参数 '{param.var.name}' 类型不匹配",
                meta
            )

        return args_dict

    def _emit_logical_op(self, op: typing.Literal["and", "or"], meta: Meta, children: list) -> Reference:
        """短路逻辑运算的统一实现"""
        result_var = self.ir_emitter.create_temp_var_declared(PrimitiveDataType.BOOLEAN, "boolean")
        op_id = next(self.counter)

        # 计算左操作数
        left: Reference = self.visit(children.pop(0))
        if not self.type_checker.check_boolean_type(left.dtype, meta):
            return Reference.literal(False)

        # scope_1: 短路分支 —— and 时赋值 False, or 时赋值 True
        with self._push_scope(f"{op}_{op_id}", StructureType.CONDITIONAL):
            self.ir_emitter.emit(IRAssign(result_var, Reference.literal(op == "or")))

        # scope_2: 求值分支 —— 访问右操作数并赋值
        with self._push_scope(f"{op}_{op_id}_2", StructureType.CONDITIONAL):
            right: Reference = self.visit(children.pop(0))
            if not self.type_checker.check_boolean_type(right.dtype, meta):
                return Reference.literal(False)
            self.ir_emitter.emit(IRAssign(result_var, right))

        # and: 左真→求右(scope_2), 左假→短路(scope_1)
        # or:  左真→短路(scope_1), 左假→求右(scope_2)
        if op == "and":
            self.ir_emitter.emit(IRCondJump(left, f"{op}_{op_id}_2", f"{op}_{op_id}"))
        else:
            self.ir_emitter.emit(IRCondJump(left, f"{op}_{op_id}", f"{op}_{op_id}_2"))

        return Reference(result_var)

    # ==================== 访问器方法 ====================

    @v_args(meta=True)
    def struct(self, meta: Meta, children: list):
        """处理结构体定义"""
        # 处理注解
        raw_annotations = self._process_annotations(children)

        # 解析结构体
        name = _n(children.pop(0).value)

        # PRE_SYMBOL 阶段处理注解
        pre, ctx = self.annotation_processor.process_pre(raw_annotations, name, AnnotationTarget.STRUCT, meta)
        if pre and pre.skip:
            return

        # 处理结构体字段

        fields: dict[str, DataTypeBase] = {}
        for field in children:
            assert isinstance(field, Tree)
            field_name, field_type = self.visit(field)
            fields[field_name] = field_type

        symbol = Structure(name, fields, {})

        # POST_SYMBOL阶段处理注解
        self.annotation_processor.process_post(raw_annotations, ctx, symbol)

        # 添加符号
        self.symbol_resolver.add_symbol(symbol, meta=meta)
        self.ir_emitter.emit(IRStructDef(symbol))

    @v_args(meta=True)
    def struct_field(self, meta: Meta, children: list[Tree | Token]) -> tuple[str, DataTypeBase]:
        """处理结构体字段"""
        name_token: Token = children.pop(0)  # NOQA
        dtype_tree: Tree = children.pop(0)  # NOQA
        name: str = name_token.value
        dtype: DataTypeBase = self.visit(dtype_tree)
        if not self.type_checker.check_definable(dtype, meta):
            return name, PrimitiveDataType.UNDEFINED
        return name, dtype

    @v_args(meta=True)
    def function(self, meta: Meta, children: list[Tree | Token]):
        """处理函数定义"""
        # 处理注解
        raw_annotations = self._process_annotations(children)

        # 解析函数签名
        # annotation* ("function"|"fn"|"def") ID params ["->" type] (block|pass_stmt)
        params: list[Parameter]
        name: str = _n(children.pop(0).value)

        # PRE_SYMBOL阶段处理注解
        pre, ctx = self.annotation_processor.process_pre(raw_annotations, name, AnnotationTarget.FUNCTION, meta)
        if pre and pre.skip:
            return

        # 处理形参
        params = self.visit(children.pop(0))  # noqa
        if children[0] is not None:
            return_type: DataTypeBase = self.visit(children.pop(0))  # noqa
        else:
            return_type: DataTypeBase = PrimitiveDataType.VOID
            children.pop(0)

        # 跳过 pass 语句
        if children and children[0].data == 'pass_stmt':
            children.pop()

        # 创建函数符号
        func_type = (FunctionType.FUNCTION if children
                     else FunctionType.FUNCTION_UNIMPLEMENTED)
        function = Function(name, params, return_type, func_type)
        self.symbol_resolver.add_symbol(function, True, meta)

        # 生成 IR
        self.ir_emitter.emit(IRFunction(function))

        # POST_SYMBOL 阶段处理注解
        self.annotation_processor.process_post(raw_annotations, ctx, function)

        # 处理函数体
        if children:
            with self._push_scope(name, StructureType.FUNCTION):  # NOQA
                with self.error_reporter.context(f"函数 {_dn(name)}"):
                    # 添加参数到作用域，批量写入以减少性能损耗(虽然经过我的测试，耗时更长了，代码还跟史一样)
                    param_vars = [param.var for param in params]
                    self.symbol_resolver.current_scope.symbols.update((v.name, v) for v in param_vars)
                    self.ir_emitter.emits(IRDeclare(v) for v in param_vars)
                    # 访问函数体
                    self.visit(children.pop(0))  # noqa

                    # 末尾强制补return
                    if self.builder.peek().opcode != IROpCode.RETURN:
                        self.ir_emitter.emit(IRReturn(Reference.default(return_type)))

    @v_args(meta=True)
    def let(self, meta: Meta, children: list[Tree | Token]) -> Optional[Reference]:
        """处理变量声明 (let)"""
        dtype: DataTypeBase
        symbol_name: str
        default_value: Reference | None = None

        symbol_name = str(children.pop(0).value)

        if isinstance(children[0], Tree) and children[0].data == 'type':
            # "let" ID ":" type ["=" expr]
            dtype = self.visit(children.pop(0))  # noqa
            if children and children[0] is not None:
                default_value = self.visit(children.pop(0))  # noqa
        else:
            # "let" ID "=" expr (类型推导)
            default_value = self.visit(children.pop(0))  # noqa
            assert isinstance(default_value, Reference)
            dtype = default_value.get_dtype()

        return self.ir_emitter.declare_variable(symbol_name, dtype, default_value, meta)

    @v_args(meta=True)
    def const(self, meta: Meta, children: list[Tree | Token]) -> Optional[Reference]:
        """处理常量声明 (const)"""
        dtype: DataTypeBase
        symbol_name: str
        value: Reference

        # "const" ID [":" type] "=" expr
        symbol_name = children[0].value  # noqa
        if children[1] is None:
            # 类型推导
            value = self.visit(children[2])  # noqa
            dtype = value.get_dtype()
        else:
            dtype = self.visit(children[1])  # noqa
            value = self.visit(children[2])  # noqa

        return self.ir_emitter.declare_variable(symbol_name, dtype, value, meta, False)

    def params(self, tree: Tree) -> list[Parameter]:
        """处理参数列表"""
        return [self.visit(param) for param in tree.children if isinstance(param, Tree)]

    @v_args(meta=True)
    def param(self, meta: Meta, children: list[Tree | Token]) -> Parameter:
        """处理单个参数定义"""
        name: str
        dtype: DataTypeBase

        # 解析参数类型和名称
        # ID ":" type ("=" expr)?
        name = _n(children.pop(0).value)  # noqa
        dtype = self.visit(children.pop(0))  # noqa
        if not self.type_checker.check_definable(dtype, meta):
            dtype = PrimitiveDataType.UNDEFINED

        # 处理默认值
        default_value: Reference
        if children:
            default_value = self.visit(children.pop(0))  # noqa

            if default_value.get_dtype() != dtype:
                self.error_reporter.report(
                    Errors.TypeMismatch,
                    default_value.get_dtype().get_name(),
                    dtype.get_name(),
                    meta=meta
                )
                # 错误时返回无默认值的参数
                return Parameter.new(name, dtype, Reference.default(dtype))

            return Parameter.new(name, dtype, default_value)

        return Parameter.new(name, dtype)

    @v_args(meta=True)
    def for_loop(self, meta: Meta, children: list[Tree | Token]):
        """处理 for 循环"""
        if isinstance(children[0], Tree) and children[0].data == "type":
            # "for" "(" type ID ":" expr ")" block // 增强for循环
            dtype = self.visit(children.pop(0))  # noqa
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
                self.visit(init)  # noqa

            loop_count = next(self.counter)

            # 创建循环作用域
            with self._push_scope(f"for_check_{loop_count}", StructureType.LOOP_CHECK) as loop_check:  # NOQA
                # 处理条件表达式
                if condition:
                    condition_ref = self.visit(condition)  # noqa
                else:
                    condition_ref = Reference.literal(True)

                # 处理循环体
                with self._push_scope(f"for_body_{loop_count}", StructureType.LOOP_BODY) as loop_body:  # NOQA
                    self.visit(block)  # noqa
                    # 处理更新表达式
                    if expr:
                        self.visit(expr)  # noqa

                self.ir_emitter.emit(IRCondJump(condition_ref, loop_body.name))
                self.ir_emitter.emit(IRCondJump(condition_ref, loop_check.name))
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
                condition_ref = self.visit(condition)

                self.ir_emitter.emit(IRCondJump(condition_ref, loop_body.name))
                self.ir_emitter.emit(IRCondJump(condition_ref, loop_check.name))
            else:
                self.ir_emitter.emit(IRJump(loop_body.name))
        self.ir_emitter.emit(IRJump(loop_check.name))

    @v_args(meta=True)
    def if_stmt(self, _: Meta, children: list):
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
            self.ir_emitter.emit(IRCondJump(condition, if_scope.name, else_scope.name))
        else:
            self.ir_emitter.emit(IRCondJump(condition, if_scope.name))

    @v_args(meta=True)
    def condition(self, meta: Meta, children: list):
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
    def return_stmt(self, meta: Meta, children: list):
        """处理 return 语句"""
        # 获取返回值
        value: Reference | None = None
        if children:
            value: Reference = self.visit(children.pop(0))

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
            func: Function | None = function_scope.parent.find_symbol(function_scope.name)

            if func is None:
                self.error_reporter.report(
                    Errors.InvalidControlFlow,
                    f"找不到函数 {function_scope.name} 的符号信息",
                    meta=meta
                )
                return

            if func.return_type == value.dtype == PrimitiveDataType.VOID:
                self.ir_emitter.emit(IRReturn())
                return

            if func.return_type != value.dtype:
                self.error_reporter.report(
                    Errors.ReturnTypeMismatch,
                    value.dtype.get_name(),
                    func.return_type.get_name(),
                    meta=meta
                )
                return

        self.ir_emitter.emit(IRReturn(value))

    @v_args(meta=True)
    def break_stmt(self, meta: Meta, _: list[Tree | Token]):
        """处理 break 语句"""
        loop_scope = self.symbol_resolver.resolve_scope(StructureType.LOOP_BODY)

        if loop_scope is None:
            self.error_reporter.report(Errors.BreakOutsideLoop, meta=meta)
            return

        self.ir_emitter.emit(IRBreak(loop_scope.name))

    @v_args(meta=True)
    def continue_stmt(self, meta: Meta, _: list[Tree | Token]):
        """处理 continue 语句"""
        loop_scope = self.symbol_resolver.resolve_scope(StructureType.LOOP_BODY)

        if loop_scope is None:
            self.error_reporter.report(Errors.ContinueOutsideLoop, meta=meta)
            return

        self.ir_emitter.emit(IRContinue(loop_scope.name))

    @v_args(meta=True)
    def include(self, meta: Meta, children: list):
        """处理包含语句"""
        original_filepath: str = self.visit(children.pop(0)).value.value

        # 检查是否为内置库
        if LibraryMapping.has(original_filepath):
            self._load_library(original_filepath)
            return

        # 搜索文件路径
        filepath = self.include_manager.search_include_path(Path(original_filepath), meta)

        if filepath is None or filepath in self.include_manager:
            return

        self.include_manager.add_include_path(filepath)

        # 解析导入的文件
        try:
            old_filepath = self.filepath
            self.filepath = filepath
            self.error_reporter.set_filepath(filepath)

            with self.include_manager.including(filepath, meta):
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
            meta: Meta,
            children: list[Token | Tree | int]
    ) -> PrimitiveDataType | Class | DataTypeBase:
        """处理类型声明"""
        dtype: DataTypeBase = PrimitiveDataType.UNDEFINED
        original_name: str = children.pop(0).value
        is_can_null: bool = bool(children.pop())  # NOQA

        # 解析类型参数
        types: list[DataTypeBase] = []
        while children:
            child: Token | Tree | int = children.pop(0)

            if not isinstance(child, Tree):
                self.error_reporter.report(
                    Errors.InvalidSyntax,
                    f"类型 {original_name} 的类型参数 '{child}' 不是合法的子类型参数",
                    meta=child.meta if hasattr(child, "meta") and isinstance(child.meta, Meta) else meta
                )
                return PrimitiveDataType.UNDEFINED

            types.append(self.visit(child))

        # 尝试解析内置类型
        try:
            match original_name:
                case "list":
                    dtype = ListType(types.pop(0))
                case "array":
                    dtype = ArrayType(types.pop(0))
                case "dict":
                    dtype = DictType(types.pop(0), types.pop(0))
                case _:
                    dtype = PrimitiveDataType.get_by_value(original_name)
        except IndexError:
            self.error_reporter.report(
                Errors.TypeArgumentNumberMismatch,
                original_name,
                meta=meta
            )
        except ValueError:
            # 解析自定义类型
            symbol = self.symbol_resolver.resolve_symbol(_n(original_name), meta)

            # 展开类型别名
            if isinstance(symbol, Typedef):
                dtype = symbol.dtype
            elif isinstance(symbol, DataTypeBase):
                dtype = symbol
            else:  # 既不是类型别名又不是直接类型
                self.error_reporter.report(
                    Errors.UndefinedType,
                    original_name,
                    meta=meta
                )
                return PrimitiveDataType.UNDEFINED

        return dtype

    @v_args(meta=True)
    def typedef(self, meta: Meta, children: list[Tree]):
        """处理类型别名定义"""
        original_type: DataTypeBase = self.visit(children.pop(0))
        new_name: str = children.pop(0).value  # NOQA

        new_type = Typedef(new_name, original_type)
        if not self.symbol_resolver.add_symbol(new_type):
            # 将会报两个错误
            self.error_reporter.report(Errors.TypedefRedefinition, new_name, meta=meta)

    @v_args(meta=True)
    def factor(self, meta: Meta, children: list):
        left: Reference = self.visit(children.pop(0))
        op: str = children.pop(0).value  # NOQA
        right: Reference = self.visit(children.pop(0))
        if not self.type_checker.check_binary_op_compatibility(left.get_dtype(), right.get_dtype(), op, meta):
            return Reference.literal(-1)

        # 生成结果变量
        result_var = self.ir_emitter.emit_binary_calc(left, BinaryOps(op), right)
        return Reference(result_var)

    term = factor

    @v_args(meta=True)
    def compare(self, meta: Meta, children: list):
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
    def unary_minus(self, meta: Meta, children: list) -> Reference:
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
            result_var = self.ir_emitter.emit_binary_calc(value, BinaryOps.MUL, Reference.literal(-1))
            return Reference(result_var)

    @v_args(meta=True)
    def logical_not(self, meta: Meta, children: list):
        value: Reference = self.visit(children.pop(0))

        if value.get_dtype() not in [PrimitiveDataType.BOOLEAN, PrimitiveDataType.INT]:
            self.error_reporter.report(Errors.InvalidOperator, "not", meta=meta)
            return value

        if value.is_literal():
            return Reference.literal(not value.value.value)
        else:
            result_var = self.ir_emitter.create_temp_var_declared(PrimitiveDataType.BOOLEAN, "boolean")
            self.ir_emitter.emit(IRUnaryOp(result_var, UnaryOps.NOT, value))
            return Reference(result_var)

    @v_args(meta=True)
    def logical_and(self, meta: Meta, children: list):
        return self._emit_logical_op("and", meta, children)

    @v_args(meta=True)
    def logical_or(self, meta: Meta, children: list):
        return self._emit_logical_op("or", meta, children)

    @v_args(meta=True)
    def local_assign(self, meta: Meta, children: list):
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
        if not variable.mutable:
            self.error_reporter.report(
                Errors.ConstantReassignment,
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
    def function_call(self, meta: Meta, children: list):
        function: Function = self.visit(children.pop(0)).value
        args: list[Reference] = self.visit(children.pop(0))

        # 检查符号类型
        if not isinstance(function, Function):
            self.error_reporter.report(
                Errors.NotCallable,
                function.get_name(),
                f"{function.__class__.__name__}",
                meta=meta
            )
            return Reference.undefined()

        # 检查递归
        if not self.config.recursion:
            cs = self.symbol_resolver.current_scope
            while cs:
                if cs.name == function.name:
                    self.error_reporter.report(
                        Errors.RecursionError,
                        f"递归调用是不被允许的",
                        meta=meta
                    )
                    return Reference.undefined()
                cs = cs.parent

        args_dict = self._process_call_arguments(function, args, meta)
        # 调用函数
        if function.func_type == FunctionType.LIBRARY:
            # 由于对内建函数的调用过程中的错误无行列信息提示，极难调试，故在此记录上下文
            with self.error_reporter.context(f"调用内建函数 {function.name} 位于 {meta.line}:{meta.column}"):
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
    def arguments(self, _: Meta, children: list[Tree]) -> list[Reference]:
        return [self.visit(child) for child in children]

    @v_args(meta=True)
    def argument(self, _: Meta, children: list) -> Reference:
        value = self.visit(children.pop(0))
        return value

    @v_args(meta=True)
    def index_get(self, meta: Meta, children: list):
        """索引读取"""
        container: Reference[Variable] = self.visit(children.pop(0))
        index: Reference[Variable | Literal] = self.visit(children.pop(0))
        # 先检查内置类型
        dtype = container.get_dtype()
        ret_dtype: DataTypeBase

        if isinstance(dtype, (DictType, ListType, ArrayType)):
            if isinstance(dtype, DictType):
                ret_dtype = dtype.value_dtype
            else:
                ret_dtype = dtype.dtype

            result = self.ir_emitter.create_temp_var_declared(ret_dtype)

            self.ir_emitter.emit(IRIndexGet(result, container, index))
            return Reference(result)
        elif isinstance(dtype, MethodHost):
            # 对于可调用类型的数据，尝试调用__getitem__方法
            method = dtype.get_method(_n("__getitem__"))
            if method is None:
                self.error_reporter.report(
                    Errors.MagicMethodNotImplemented,
                    repr(dtype),  # noqa
                    "__getitem__",
                    "索引读取",
                    meta=meta
                )
                return Reference.void()
            result = self.ir_emitter.create_temp_var_declared(method.return_type)

            # self.ir_emitter.emit(IRCallMethod(result, container, method, ...))
            # TODO: 调用具体方法
            ...
        elif isinstance(dtype, PrimitiveDataType):
            self.error_reporter.report(Errors.PrimitiveTypeOperation, "数组访问", dtype.get_name(), meta=meta)
        else:
            self.error_reporter.report(Errors.InvalidOperator, f"[{index!r}]", meta=meta)
        return Reference.void()

    @v_args(meta=True)
    def index_set(self, meta: Meta, children: list[Tree | Token]):
        pass  # TODO: 实现索引写入

    @v_args(meta=True)
    def member_access(self, meta: Meta, children: list[Tree]):
        expr_ref: Reference = self.visit(children.pop(0))

    def null(self, _: Tree) -> Reference:
        """处理 null 字面量"""
        return Reference.literal(None)

    def literal(self, tree: Tree) -> Reference:
        """处理字面量"""
        token: Token = tree.children.pop()  # NOQA

        match token.type:
            case "STRING":
                return Reference.literal(ast.literal_eval(token))
            case "INT":
                return Reference.literal(int(token))
            case "TRUE":
                return Reference.literal(True)
            case "FALSE":
                return Reference.literal(False)
            case _:
                return Reference.literal(str(token))

    @v_args(meta=True)
    def fstring(self, meta: Meta, children: list[Token | Tree]):
        """处理f-string"""
        result = self.ir_emitter.emit_fstring_init()
        for index, (data_type, data) in enumerate(parse_fstring_iter(children.pop().value)):
            if data_type == 'literal':
                if data_type == 'literal':
                    self.ir_emitter.emit_fstring_append_literal(result, data, index == 0)
            else:
                try:
                    with self.error_reporter.context(f"格式化字符串 {meta.line}:{meta.column}"):
                        # ── 快速路径：纯标识符，跳过 lark ──────────────────
                        expr = _try_fast_path_expr(
                            data,
                            self.symbol_resolver,
                            meta
                        )
                        # ── 慢速路径：复杂表达式，走 lark ───────────────────
                        if expr is None:
                            expr: Reference = self.visit(parser_code(data, "expr"))
                except LarkError as e:
                    self.error_reporter.report(Errors.FStringExpressionError, data, e.__repr__(), meta=meta)
                    break

                appended = self.ir_emitter.emit_fstring_append_expr(result, expr)
                if appended is None:
                    self.error_reporter.report(Errors.FStringExpressionError, data, "不支持的字符串转换", meta=meta)
                    break
        return Reference(result)

    @v_args(meta=True)
    def struct_init(self, meta, children: list):
        """处理结构体实例化: Point{x: 1, y: 2}"""
        struct_name = _n(children.pop(0).value)
        symbol = self.symbol_resolver.resolve_symbol(struct_name, meta)

        if not isinstance(symbol, Structure):
            self.error_reporter.report(Errors.UndefinedType, struct_name, meta=meta)
            return Reference.undefined()

        # 验证字段并收集初始值
        field_values: dict[str, Reference] = {}
        for fname, fvalue_tree in batched(children, 2):
            fvalue: Reference = self.visit(fvalue_tree)
            if fname not in symbol.fields:
                self.error_reporter.report(Errors.InvalidMemberAccess, fname, meta=meta)
                continue
            self.type_checker.check_type_match(
                symbol.fields[fname], fvalue.get_dtype(),
                f"结构体 {struct_name} 字段 {fname}", meta
            )
            field_values[fname] = fvalue

        # 生成 IR
        var = self.ir_emitter.create_temp_var_declared(symbol, "struct")
        self.ir_emitter.emit(IRStructNew(var, symbol, field_values))
        return Reference(var)

    @v_args(meta=True)
    def identifier(self, meta: Meta, children: list[str]) -> Reference:
        """处理标识符引用"""
        symbol_name = children.pop()
        symbol = self.symbol_resolver.resolve_symbol(_n(symbol_name), meta)

        if symbol is None:
            # resolve_symbol 内已经报过错了，无需重复报错
            return Reference.undefined()

        return Reference(symbol)

    @v_args(meta=True)
    def annotation(self, meta: Meta, children: list) -> tuple[Annotation, dict[str, Any]]:
        """
        处理注解声明

        Args:
            children: 注解名称和参数列表
            meta: 元数据

        Returns:
            (注解对象, 参数字典)，出错时返回未定义注解和空字典
        """
        name = children.pop(0).value
        spec, param_dict, ok = self.annotation_processor.validate_and_resolve(name, children, meta)
        if not ok:
            return self.annotation_processor.undefined_annotation()

        if spec is None:
            spec = self.annotation_processor.undefined_annotation()[0]
            param_dict = {}

        if param_dict is None and spec.params:  # 需要visit填充实参
            # 访问所有参数值并构建参数字典（参数名 -> 参数值）
            param_values = [self.visit(child).value.value for child in children]
            param_dict = dict(zip(spec.params, param_values))

        return spec, param_dict  # noqa
