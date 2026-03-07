# coding=utf-8
import ast
from contextlib import contextmanager
from functools import lru_cache
from pathlib import Path
from typing import Callable, Any, Optional

from lark import Lark, Tree, v_args, Token
from lark.tree import Meta
from lark.visitors import Interpreter

from dovetail.core import builtin_annotation
from dovetail.core.compile_config import CompileConfig
from dovetail.core.enums import StructureType, DataType, VariableType, MinecraftVersion, MinecraftEdition, \
    FunctionType
from dovetail.core.enums.minecraft import UnknownMinecraftVersionError
from dovetail.core.enums.types import Array, DataTypeBase, AnnotationCategory
from dovetail.core.errors import report, Errors
from dovetail.core.include_manager import IncludeManager
from dovetail.core.instructions import IRDeclare, IRAssign, IRInstruction, IRScopeBegin, IRScopeEnd, IRFunction, \
    IRReturn, IRBreak, IRContinue
from dovetail.core.ir_builder import IRBuilder
from dovetail.core.lib.library import Library
from dovetail.core.lib.library_mapping import LibraryMapping
from dovetail.core.parser.scope import Scope
from dovetail.core.scope.protocols import ScopeCore
from dovetail.core.symbols import Variable, Reference, Literal, Function, Class, Parameter
from dovetail.core.symbols.annotation import Annotation
from dovetail.core.symbols.structure import Structure
from dovetail.core.symbols.typedef import Typedef
from dovetail.utils.annotations import timed
from dovetail.utils.naming import NameNormalizer
from dovetail.utils.string_similarity import suggest_similar

lark_parser = Lark(open(r".\lark\dovetail.lark", encoding='utf-8').read(), start="program", parser='lalr',
                   cache=".cache", propagate_positions=True, maybe_placeholders=True)


@timed("解析用时 {:.5f}.")
def parser_code(filepath: Path | str, start: Optional[str] = None) -> Tree | None:
    """
    解析代码

    Args:
        filepath (Path | str): 代码文件路径
        start (str): 语法解析起点

    Returns: 返回AST树
    """
    filepath = Path(filepath)
    if not filepath.exists() or not filepath.is_file():
        return None

    with open(filepath, encoding='utf-8') as f:
        code = f.read()
    if start is None:
        return lark_parser.parse(code, on_error=lambda e: True)
    else:
        return lark_parser.parse(code, start=start, on_error=lambda e: True)


class ASTTransformer(Interpreter):
    """
    AST访问器

    访问AST并生成IR

    Attributes:
        config(CompileConfig): 编译配置
        filepath(Path): 编译入口文件
        top_scope(Scope): 顶层作用域
        current_scope(Scope): 当前作用域
        scope_stack(list[Scope]): 作用域栈
        builtin_function(dict): 内建函数表
        include_manager(IncludeManager): 导入管理器
        builder(IRBuilder): IR构建器
    """

    def __init__(self, config: CompileConfig, source_path: Path):
        super().__init__()
        self.config = config
        self.filepath = source_path
        self.top_scope = Scope(
            "top",
            None,
            StructureType.GLOBAL
        )
        self.current_scope = self.top_scope
        self.scope_stack: list[Scope] = [self.top_scope]

        self.builtin_function: dict[str, Callable[..., Variable | Literal]] = {}
        # 包含管理器
        self.include_manager = IncludeManager()
        # IR构建器
        self.builder = IRBuilder()
        #  加载内置库
        self._load_library(LibraryMapping.get("builtins", self.builder))
        if self.config.experimental:
            self._load_library(LibraryMapping.get("experimental", self.builder))
        # 编译错误统计
        self.error_count = 0
        self.warning_count = 0

    def __default__(self, tree: Tree) -> list[Any]:
        return self.visit_children(tree)

    @lru_cache(maxsize=None)
    def _load_library(self, library: Library):
        try:
            self._append_ir(library.load())
            for function, handler in library.get_functions().items():
                self.current_scope.add_symbol(function)
                self.builtin_function[function.get_name()] = handler
            for constant, value in library.get_variables().items():
                self.current_scope.add_symbol(constant)
                self._append_ir(IRDeclare(constant))
                self._append_ir(IRAssign(constant, value))
            for class_, method_handlers in library.get_classes().items():
                self.current_scope.add_symbol(class_)
                for method_name, handler in method_handlers.items():
                    self.builtin_function[f"{class_.name}:{method_name}"] = handler
        except Exception as e:
            library_name = library.get_name()
            self._report(
                Errors.LibraryLoad,
                library_name,
                e.__repr__(),
                filepath=self.filepath,
            )

    @contextmanager
    def _scoped_environment(self, name: str, scope_type: StructureType):
        """
        作用域管理器

        Args:
            name: 作用域名称
            scope_type: 作用域类型

        Yields:
            Scope: 新建的作用域
        """
        new_scope = self.current_scope.create_child(name, scope_type)
        self.current_scope = new_scope
        self.scope_stack.append(new_scope)
        self._append_ir(IRScopeBegin(name, scope_type))
        try:
            yield new_scope
        finally:
            if self.current_scope.parent is not None:
                self.current_scope = self.current_scope.parent
                self.scope_stack.pop()
                self._append_ir(IRScopeEnd(name, scope_type))

    def _append_ir(self, instr: list[IRInstruction] | IRInstruction):
        if isinstance(instr, IRInstruction):
            self.builder.insert(instr)
        else:
            for ir_instr in instr:
                self.builder.insert(ir_instr)

    def _get_loop_check_scope_type(self) -> ScopeCore | None:
        """
        逐级向上解析，直到找到第一个类型为 LOOP_CHECK 的作用域，且遇到除条件作用域和循环体作用域时停止

        Returns:
            如果找到返回对应作用域，否则返回 None
        """
        for scope in reversed(self.scope_stack):
            if scope.stype == StructureType.LOOP_CHECK:
                return scope
            elif scope.stype not in (StructureType.CONDITIONAL, StructureType.LOOP_BODY):
                break
        return None

    def _search_include_path(self, filepath: Path, line=-1, column=-1) -> Path | None:
        """
        搜索可能被导入的路径并返回

        Args:
            filepath: 文件路径

        Returns:第一个搜素到的路径
        """
        if filepath.is_absolute():
            return filepath

        search_path: list[Path] = [self.config.lib_path, Path.cwd()]

        include_path = next(
            (d / filepath for d in search_path if (Path(d) / filepath).exists()), None)

        if include_path:
            return include_path
        else:
            self._report(
                Errors.CompilerInclude,
                str(filepath),
                "找不到文件",
                filepath=self.filepath,
                line=line,
                column=column
            )
            return None

    def _decl_variable(self, name: str, dtype: DataTypeBase, value: Optional[Reference] = None,
                       meta: Optional[Meta] = None, mutable: bool = True):
        # 检查类型是否正确
        if not dtype.is_definable():
            self._report(
                Errors.TypeMismatch,
                "可定义类型",
                dtype.get_name(),
                filepath=self.filepath,
                line=meta.line if meta is not None else -1,
                column=meta.column if meta is not None else -1
            )
            return None
        if value is not None and dtype != value.get_dtype():
            self._report(
                Errors.TypeMismatch,
                dtype.get_name(),
                value.get_dtype().get_name(),
                filepath=self.filepath,
                line=meta.line if meta is not None else -1,
                column=meta.column if meta is not None else -1
            )
            return None

        variable = Variable(NameNormalizer.normalize(name), dtype, mutable=mutable)
        if not self.current_scope.add_symbol(variable):
            self._report(
                Errors.DuplicateDefinition,
                name,
                filepath=self.filepath,
                line=meta.line if meta is not None else -1,
                column=meta.column if meta is not None else -1
            )
            return None

        self._append_ir(IRDeclare(variable))
        if value:
            self._append_ir(IRAssign(variable, value))

        return Reference(variable)

    def _report(self,
                error: Errors,
                *args: str,
                filepath: Path | str = "<unknown>",
                line: int = -1,
                column: int = -1,
                suggestion: Optional[str] = None) -> None:
        report(
            error,
            *args,
            filepath=filepath,
            line=line,
            column=column,
            suggestion=suggestion
        )
        self.error_count += 1

    @v_args(meta=True)
    def struct(self, children: list[Tree | Token], meta: Meta):
        # 处理注解
        annotations: dict[Annotation, dict[str, Any]] = {}
        while isinstance(children[0], Tree) and children[0].data == 'annotation':
            annotation: Annotation
            args: dict[str, Any]
            annotation, args = self.visit(children.pop(0))
            annotations[annotation] = args

            # 处理特殊注解
            if annotation.name == "version":
                try:
                    min_version = MinecraftVersion.instance(args.get("min", "1.20.4"))
                except UnknownMinecraftVersionError:
                    self._report(
                        Errors.UnsupportedTargetVersion,
                        args.get("min", "1.20.4"),
                        filepath=self.filepath,
                        line=meta.line,
                        column=meta.column
                    )
                    return
                try:
                    max_version = MinecraftVersion.instance(args.get("max", "1.21.4"))
                except UnknownMinecraftVersionError:
                    self._report(
                        Errors.UnsupportedTargetVersion,
                        args.get("max", "1.21.4"),
                        filepath=self.filepath,
                        line=meta.line,
                        column=meta.column
                    )
                    return

                if self.config.version > max_version or self.config.version < min_version:
                    # 跳过编译该函数
                    return
            elif annotation.name == "target":
                target_edition = MinecraftEdition.from_str(args.get("edition", "java"))
                compiler_edition = self.config.version.edition

                if target_edition != compiler_edition:
                    # 跳过编译该函数
                    return

        name = children.pop(0).value
        fields: dict[str, DataTypeBase] = {}
        for field in children:
            field_name, field_type = self.visit(field)
            fields[field_name] = field_type

        symbol = Structure(NameNormalizer.normalize(name), fields)
        if not self.current_scope.add_symbol(symbol):
            self._report(
                Errors.DuplicateDefinition,
                name,
                filepath=self.filepath,
                line=meta.line,
                column=meta.column
            )

    def struct_field(self, tree: Tree):
        name: str = tree.children.pop(0).value
        dtype: DataTypeBase = self.visit(tree.children.pop(0))
        return name, dtype

    @v_args(meta=True)
    def function(self, children: list[Tree | Token], meta: Meta):
        # 处理注解
        annotations: dict[Annotation, dict[str, Any]] = {}
        while isinstance(children[0], Tree) and children[0].data == 'annotation':
            annotation: Annotation
            args: dict[str, Any]
            annotation, args = self.visit(children.pop(0))
            annotations[annotation] = args

            # 处理特殊注解
            if annotation.name == "version":
                min_version = MinecraftVersion.instance(args.get("min", "1.20.4"))
                max_version = MinecraftVersion.instance(args.get("max", "1.21.4"))
                if self.config.version > max_version or self.config.version < min_version:
                    # 跳过编译该函数
                    return
            elif annotation.name == "target":
                target_edition = MinecraftEdition.from_str(args.get("edition", "java"))
                compiler_edition = self.config.version.edition

                if target_edition != compiler_edition:
                    # 跳过编译该函数
                    return

        params: list[Parameter]
        return_type: DataTypeBase
        name: str
        # 处理函数签名
        if isinstance(children[0], Tree) and children[0].data == 'type':
            # annotation* ("function"|"fn") type ID params (block|pass_stmt)
            return_type = self.visit(children.pop(0))  # type
            name = NameNormalizer.normalize(children.pop(0).value)  # ID
            params = self.visit(children.pop(0))  # params
        else:
            # annotation* ("function"|"fn"|"def") ID params ["->" type] (block|pass_stmt)
            name = NameNormalizer.normalize(children.pop(0).value)
            params = self.visit(children.pop(0))
            if children[0] is not None:
                return_type = self.visit(children.pop(0))
            else:
                return_type = DataType.VOID
                children.pop(0)

        # 当块为无意义指令时直接弹出
        if children[0].data == 'pass_stmt':
            children.pop()

        # 创建函数对象
        function = Function(
            name,
            params,
            return_type,
            FunctionType.FUNCTION if len(children) == 1 else FunctionType.FUNCTION_UNIMPLEMENTED,
            annotations
        )
        # 将函数对象添加到符号表
        self.current_scope.add_symbol(function, force=True)

        # 生成IR指令
        self._append_ir(IRFunction(function))

        if len(children) >= 1:
            with self._scoped_environment(name, StructureType.FUNCTION):  # NOQA
                for param in params:
                    if not self.current_scope.add_symbol(param):
                        self._report(
                            Errors.DuplicateDefinition,
                            param.get_name(),
                            filepath=self.filepath,
                            line=meta.line,
                            column=meta.column
                        )
                self.visit(children.pop(0))

    @v_args(meta=True)
    def let(self, children: list[Tree | Token], meta: Meta):
        dtype: DataTypeBase
        symbol_name: str
        default_value: Reference | None = None

        # 分析数据类型和初始值
        symbol_name = str(children.pop(0).value)
        if isinstance(children[0], Tree) and children[0].data == 'type':
            # "let" ID ":" type ["=" expr]
            dtype = self.visit(children.pop(0))

            if len(children) >= 1 and children[0] is not None:
                default_value = self.visit(children.pop(0))
        else:  # "let" ID "=" expr
            default_value = self.visit(children.pop(0))
            assert isinstance(default_value, Reference)
            # 自动推导类型
            dtype = default_value.get_dtype()

        return self._decl_variable(symbol_name, dtype, default_value, meta)

    @v_args(meta=True)
    def const(self, children: list[Tree | Token], meta: Meta):
        dtype: DataTypeBase
        symbol_name: str
        value: Reference
        if isinstance(children[0], Tree) and children[0].data == "type":
            # "const" type ID "=" expr
            dtype = self.visit(children[0])  # type
            symbol_name: str = children[1].value  # ID
            value = self.visit(children[2])  # expr
        else:
            # "const" ID [":" type] "=" expr
            symbol_name = children[0].value  # ID
            if children[1] is None:
                value = self.visit(children[2])  # expr
                # 自动推导类型
                dtype = value.get_dtype()
            else:
                dtype = self.visit(children[1])  # type
                value = self.visit(children[2])  # expr

        return self._decl_variable(symbol_name, dtype, value, meta, mutable=False)

    def params(self, tree: Tree) -> list[Parameter]:
        params: list[Parameter] = []
        for param in tree.children:
            params.append(self.visit(param))
        return params

    @v_args(meta=True)
    def param(self, children: list[Tree | Token], meta: Meta):
        name: str
        dtype: DataTypeBase
        is_mut: bool = False

        if children.pop(0) is not None:
            is_mut = True

        if isinstance(children[0], Tree) and children[0].data == "type":
            # [MUT] type ID ("=" expr)?
            dtype = self.visit(children.pop(0))  # type
            name: str = NameNormalizer.normalize(children.pop(0).value)  # ID
        else:
            # [MUT] ID ":" type ("=" expr)?
            name: str = NameNormalizer.normalize(children.pop(0).value)  # ID
            dtype = self.visit(children.pop(0))  # type

        default_value: Reference | None = None
        if len(children) >= 1:
            default_value = self.visit(children.pop(0))

            if default_value.get_dtype() != dtype:
                self._report(
                    Errors.TypeMismatch,
                    default_value.get_dtype().get_name(),
                    dtype.get_name(),
                    filepath=self.filepath,
                    line=meta.line,
                    column=meta.column
                )
                # 发生错误时返回无默认值的参数对象
                return Parameter(Variable(name, dtype, VariableType.PARAMETER))

        return Parameter(Variable(name, dtype, VariableType.PARAMETER), True, default_value)

    @v_args(meta=True)
    def return_stmt(self, children: list[Tree | Token], meta: Meta):
        value: Reference | None
        # 获取返回值
        if len(children) >= 1:
            value = self.visit(children.pop(0))

            # 当所返回的类型为变量或常量时
            if isinstance(value.value, Variable):
                value.value.var_type = VariableType.RETURN
        else:
            value = None

        # 获取函数定义的返回类型
        function_scope = next(scope for scope in reversed(self.scope_stack) if scope.stype == StructureType.FUNCTION)
        if function_scope is None:
            self._report(
                Errors.InvalidControlFlow,
                "return在函数之外",
                filepath=self.filepath,
                line=meta.line,
                column=meta.column
            )
            return

        if value is not None:
            function_symbol: Function | None = function_scope.parent.find_symbol(function_scope.name)

            if function_symbol.return_type != value.get_dtype():
                self._report(
                    Errors.TypeMismatch,
                    function_symbol.return_type.get_name(),
                    value.get_dtype().get_name(),
                    filepath=self.filepath,
                    line=meta.line,
                    column=meta.column
                )
                return

        self._append_ir(IRReturn(value))

    @v_args(meta=True)
    def break_stmt(self, _: list[Tree | Token], meta: Meta):
        # 获取循环所在的作用域
        loop_scope = self._get_loop_check_scope_type()

        if loop_scope is None:
            self._report(
                Errors.InvalidControlFlow,
                "break 语句必须在循环中",
                filepath=self.filepath,
                line=meta.line,
                column=meta.column
            )
            return

        self._append_ir(IRBreak(loop_scope.name))

    @v_args(meta=True)
    def continue_stmt(self, _: list[Tree | Token], meta: Meta):
        # 获取循环所在的作用域
        loop_scope = self._get_loop_check_scope_type()

        if loop_scope is None:
            self._report(
                Errors.InvalidControlFlow,
                "continue 语句必须在循环中",
                filepath=self.filepath,
                line=meta.line,
                column=meta.column
            )
            return

        self._append_ir(IRContinue(loop_scope.name))

    @v_args(meta=True)
    def include(self, children: list, meta: Meta):
        original_filepath: str = self.visit(children.pop(0)).value.value
        # 判断是否为内置库
        if library := LibraryMapping.get(original_filepath, self.builder):
            self._load_library(library)
            return

        filepath = self._search_include_path(Path(original_filepath), meta.line, meta.column)
        if filepath is None or self.include_manager.has_path(filepath):
            return

        self.include_manager.add_include_path(filepath)

        # 处理导入的文件
        try:
            old_filepath = self.filepath

            children = parser_code(filepath)

            self.visit(children)
            # 重新设置为原来的文件
            self.filepath = old_filepath
        except Exception as e:
            self._report(
                Errors.CompilerInclude,
                str(filepath),
                f"无法正确解析文件:{e.__repr__()}",
                filepath=self.filepath,
                line=meta.line,
                column=meta.column
            )

    @v_args(meta=True)
    def type(self, children: list[Token | Tree | int], meta: Meta) -> DataType | Class | Array | DataTypeBase:
        original_name: str = children.pop(0).value  # type: ignore

        try:
            dtype = DataType.get_by_value(original_name)
        except ValueError:
            dtype = self.current_scope.resolve_symbol(NameNormalizer.normalize(original_name))

            # 展开类型别名
            if isinstance(dtype, Typedef):
                dtype = dtype.dtype

            if not isinstance(dtype, DataTypeBase):
                self._report(
                    Errors.UndefinedType,
                    original_name,
                    filepath=self.filepath,
                    line=meta.line,
                    column=meta.column,
                )
                return DataType.UNDEFINED

        if dtype.is_definable():
            if len(children) >= 1:
                return Array(dtype, children)
            else:
                return dtype
        else:
            self._report(
                Errors.TypeMismatch,
                "可定义类型",
                original_name,
                filepath=self.filepath,
                line=meta.line,
                column=meta.column,
                suggestion=f"{original_name} 不可被定义"
            )
            return DataType.UNDEFINED

    @v_args(meta=True)
    def typedef(self, children: list[Token | Tree | int], meta: Meta):
        original_type: DataTypeBase = self.visit(children.pop(0))
        new_name: str = children.pop(0).value
        new_type = Typedef(new_name, original_type)
        if not self.current_scope.add_symbol(new_type):
            self._report(
                Errors.DuplicateDefinition,
                new_name,
                filepath=self.filepath,
                line=meta.line,
                column=meta.column
            )
        return None

    def null(self, _: Tree):
        return Reference.literal(None)

    def paren(self, tree: Tree) -> Reference[Literal | Variable | Class | Function]:
        return self.visit(tree.children[-1])

    def literal(self, tree: Tree):
        token: Token = tree.children.pop()  # NOQA
        match token.type:
            case "STRING":
                return Reference.literal(ast.literal_eval(token))
            case "ARRAY_SIZE":
                return Reference.literal(int(token))
            case "INT":
                return Reference.literal(int(token))
            case "FLOAT":
                return Reference.literal(float(token))
            case "true":
                return Reference.literal(True)
            case "false":
                return Reference.literal(False)
            case _:
                return Reference.literal(str(token))

    @v_args(meta=True)
    def identifier(self, children: list[str] | str, meta: Meta):
        if isinstance(children, list):
            symbol_name = children.pop()
        else:
            symbol_name = children
        symbol = self.current_scope.resolve_symbol(NameNormalizer.normalize(symbol_name))
        if symbol is None:
            suggestion = suggest_similar(NameNormalizer.normalize(symbol_name),
                                         list(self.current_scope.get_all_symbols().keys()))
            self._report(
                Errors.UndefinedSymbol,
                symbol_name,
                filepath=self.filepath,
                line=meta.line,
                column=meta.column,
                suggestion=f"你的意思是'{suggestion}'？" if suggestion else None,
            )
            return Reference.literal(None)

        return Reference(symbol)

    @v_args(meta=True)
    def annotation(self, children: list[str], meta: Meta) -> tuple[Annotation, dict[str, str]]:
        name = children.pop(0)
        annotation = builtin_annotation.get_annotation(name)
        if annotation is None:
            self._report(
                Errors.UndefinedSymbol,
                name,
                filepath=self.filepath,
                line=meta.line,
                column=meta.column
            )
            return Annotation("undefined", None, AnnotationCategory.METADATA), {}

        if annotation.params is None:
            if len(children) >= 1:
                self._report(
                    Errors.ArgumentNumberMismatch,
                    name,
                    "0",
                    str(len(children)),
                    filepath=self.filepath,
                    line=meta.line,
                    column=meta.column
                )
            return annotation, {}

        if len(children) != len(annotation.params):
            self._report(
                Errors.ArgumentNumberMismatch,
                name,
                str(len(annotation.params)),
                str(len(children)),
                filepath=self.filepath,
                line=meta.line,
                column=meta.column
            )
            return Annotation("undefined", None, AnnotationCategory.METADATA), {}

        return annotation, {arg: param for arg, param in zip(children, annotation.params)}
