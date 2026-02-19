# coding=utf-8
import ast
from contextlib import contextmanager
from functools import lru_cache
from pathlib import Path
from typing import Callable, Optional

from lark import Transformer, Lark, Tree, v_args
from lark.tree import Meta

from dovetail.core.builtin_annotation import get_annotation
from dovetail.core.compile_config import CompileConfig
from dovetail.core.enums import StructureType, ValueType, DataType
from dovetail.core.enums.types import Array, DataTypeBase, AnnotationCategory
from dovetail.core.errors import report, Errors
from dovetail.core.include_manager import IncludeManager
from dovetail.core.instructions import IRDeclare, IRAssign, IRInstruction, IRScopeBegin, IRScopeEnd
from dovetail.core.ir_builder import IRBuilder
from dovetail.core.lib.library import Library
from dovetail.core.lib.library_mapping import LibraryMapping
from dovetail.core.parser.scope import Scope
from dovetail.core.scope.protocols import ScopeCore
from dovetail.core.symbols import Constant, Variable, Reference, Literal, Function, Class
from dovetail.core.symbols.annotation import Annotation
from dovetail.utils.naming import NameNormalizer
from dovetail.utils.string_similarity import suggest_similar

lark_parser = Lark(open(r".\lark\dovetail.lark", encoding='utf-8').read(), start="program", parser='lalr',
                   cache=".cache", propagate_positions=True)


def parser_code(filepath: Path | str, start=None) -> Tree | None:
    """
    解析代码

    Args:
        filepath (Path | str): 代码文件路径
        start:

    Returns: 返回AST树
    """
    filepath = Path(filepath)
    if not filepath.exists() or not filepath.is_file():
        return None

    with open(filepath, encoding='utf-8') as f:
        code = f.read()
    if start is None:
        return lark_parser.parse(code)
    else:
        return lark_parser.parse(code, start=start)


class ASTTransformer(Transformer):

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
        self.scope_stack: list[ScopeCore] = [self.top_scope]

        self.builtin_function: dict[str, Callable[..., Variable | Constant | Literal]] = {}
        # 包含管理器
        self.include_manager = IncludeManager()
        # IR构建器
        self.builder = IRBuilder()
        #  加载内置库
        self._load_library(LibraryMapping.get("builtins", self.builder))
        if self.config.experimental:
            self._load_library(LibraryMapping.get("experimental", self.builder))
        # 是否发生错误
        self.errored = False

    @lru_cache(maxsize=None)
    def _load_library(self, library: Library):
        try:
            self._append_ir(library.load())
            for function, handler in library.get_functions().items():
                self.current_scope.add_symbol(function)
                self.builtin_function[function.get_name()] = handler
            for constant, value in library.get_constants().items():
                self.current_scope.add_symbol(constant)
                self._append_ir(IRDeclare(constant))
                self._append_ir(IRAssign(constant, value))
            for class_, method_handlers in library.get_classes().items():
                self.current_scope.add_symbol(class_)
                for method_name, handler in method_handlers.items():
                    self.builtin_function[f"{class_.name}:{method_name}"] = handler
        except Exception as e:
            if isinstance(library, Library):
                library_name = library.get_name()
            else:
                library_name = str(library)
            report(
                Errors.LibraryLoad,
                library_name,
                e.__repr__(),
                filepath=self.filepath,
            )
            self.errored = True

    @contextmanager
    def _scoped_environment(self, name: str, scope_type: StructureType):
        """
        作用域管理器
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

    def _get_loop_check_scope_name(self) -> str | None:
        current = self.current_scope
        while current:
            if current.stype == StructureType.LOOP_CHECK:
                return current.name
            elif current.stype in (StructureType.CONDITIONAL, StructureType.LOOP_BODY):
                current = current.parent
            else:
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
            report(
                Errors.CompilerInclude,
                str(filepath),
                "找不到文件",
                filepath=self.filepath,
                line=line,
                column=column
            )
            self.errored = True
            return None

    def _get_dtype(self, type_name, size: Optional[list[int]] = None,
                   meta: Meta = None) -> DataType | Class | Array | DataTypeBase:
        try:
            dtype = DataType.get_by_value(type_name)
            if dtype.is_definable():
                if size is not None:
                    return Array(dtype, size)
                else:
                    return dtype
            else:
                report(
                    Errors.TypeMismatch,
                    "可定义类型",
                    type_name,
                    filepath=self.filepath,
                    line=meta.line if meta is not None else -1,
                    column=meta.column if meta is not None else -1,
                    suggestion=f"{type_name}不适用于此场景"
                )
                self.errored = True
                return DataType.UNDEFINED
        except ValueType:
            pass  # DataType不存在此类型,去查找符号
        dtype = self.current_scope.resolve_symbol(NameNormalizer.normalize(type_name))
        if isinstance(dtype, DataTypeBase):
            if size is not None:
                return Array(dtype, size)
            else:
                return dtype

        report(
            Errors.UndefinedType,
            type_name,
            filepath=self.filepath,
            line=meta.line if meta is not None else -1,
            column=meta.column if meta is not None else -1,
        )
        self.errored = True
        return DataType.UNDEFINED

    def get_ir(self) -> IRBuilder:
        """
        返回IRBuilder

        Returns:
            IRBuilder: IRBuilder对象
        """
        return self.builder

    @v_args(meta=True)
    def var(self, children: list, meta: Meta):
        # 分析数据类型和初始值
        dtype: DataTypeBase = DataType.UNDEFINED
        symbol_name: str
        default_value: Reference | None = None

        if isinstance(children[0], DataTypeBase):  # type ID "?"? ("=" expr)?
            dtype = children[0]
            symbol_name = children[1]
            if len(children) > 2:
                default_value = children[2]
        else:
            symbol_name = children[0]
            if isinstance(children[1], DataTypeBase):
                # ID ("->" | ":") type "?"? ("=" expr)?
                # "let" ID "?"? ("->" | ":") type ("=" expr)?
                dtype = children[1]
                if len(children) > 2:
                    default_value = children[2]
            elif isinstance(children[1], Reference):  # "let" ID "?"? "=" expr
                default_value = children[1]
                dtype = default_value.get_data_type()

        # 检查类型是否正确
        if not dtype.is_definable():
            report(
                Errors.TypeMismatch,
                "可定义类型",
                dtype.get_name(),
                filepath=self.filepath,
                line=meta.line,
                column=meta.column
            )
            self.errored = True
            return None
        if default_value is not None and dtype != default_value.get_data_type():
            report(
                Errors.TypeMismatch,
                dtype.get_name(),
                default_value.get_data_type().get_name(),
                filepath=self.filepath,
                line=meta.line,
                column=meta.column
            )
            self.errored = True
            return None

        variable = Variable(symbol_name, dtype)
        if not self.current_scope.add_symbol(variable):
            report(
                Errors.DuplicateDefinition,
                symbol_name,
                filepath=self.filepath,
                line=meta.line,
                column=meta.column
            )
            self.errored = True
            return None

        self._append_ir(IRDeclare(variable))
        if default_value:
            self._append_ir(IRAssign(variable, default_value))

        return Reference(ValueType.VARIABLE, variable)

    @v_args(meta=True)
    def const(self, children: list, meta: Meta):
        dtype: DataTypeBase
        symbol_name: str
        default_value: Reference
        if isinstance(children[0], DataTypeBase):  # "const" type ID ("=" expr)
            dtype = children[0]
            symbol_name: str = children[1]
            value = children[2]
        else:
            symbol_name = children[0]
            if isinstance(children[1], DataTypeBase):
                dtype = children[1]
                value = children[2]
            else:
                value = children[1]
                dtype = value.get_data_type()

        # 检查类型是否正确
        if not dtype.is_definable():
            report(
                Errors.TypeMismatch,
                "可定义类型",
                dtype.get_name(),
                filepath=self.filepath,
                line=meta.line,
                column=meta.column
            )
            self.errored = True
            return None
        if value is not None and dtype != value.get_data_type():
            report(
                Errors.TypeMismatch,
                dtype.get_name(),
                value.get_data_type().get_name(),
                filepath=self.filepath,
                line=meta.line,
                column=meta.column
            )
            self.errored = True
            return None

        constant = Constant(symbol_name, dtype)
        if not self.current_scope.add_symbol(constant):
            report(
                Errors.DuplicateDefinition,
                symbol_name,
                filepath=self.filepath,
                line=meta.line,
                column=meta.column
            )
            self.errored = True
            return None

        self._append_ir(IRDeclare(constant))
        if value:
            self._append_ir(IRAssign(constant, value))

        return Reference(ValueType.CONSTANT, constant)

    @v_args(meta=True)
    def function(self, children: list, meta: Meta):
        print(children, meta)

    @v_args(meta=True)
    def include(self, children: list, meta: Meta):
        original_filepath: str = str(children[0].value.value)
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

            tree = parser_code(filepath)

            self.transform(tree)
            # 重新设置为原来的文件
            self.filepath = old_filepath
        except Exception as e:
            report(
                Errors.CompilerInclude,
                str(filepath),
                f"无法正确解析文件:{e.__repr__()}",
                filepath=self.filepath,
                line=meta.line,
                column=meta.column
            )
            self.errored = True
            return

    @v_args(meta=True)
    def type(self, children: list, meta: Meta):
        return self._get_dtype(children[0], children[1:] if len(children) >= 2 else None, meta)

    def literal(self, children):
        return children[0]

    @v_args(meta=True)
    def identifier(self, children: list[str] | str, meta: Meta = None):
        if isinstance(children, list):
            symbol_name = children[0]
        else:
            symbol_name = children
        symbol = self.current_scope.resolve_symbol(symbol_name)
        if symbol is None:
            line = -1 if meta is None else meta.line
            column = -1 if meta is None else meta.column
            suggestion = suggest_similar(symbol_name, list(self.current_scope.get_all_symbols().keys()))
            report(
                Errors.UndefinedSymbol,
                symbol_name,
                filepath=self.filepath,
                line=line,
                column=column,
                suggestion=f"你的意思是'{suggestion}'？" if suggestion else None,
            )
            self.errored = True
            return Reference.literal(None)

        # 判断 symbol 的类型
        if isinstance(symbol, Literal):
            value_type = ValueType.LITERAL
        elif isinstance(symbol, Function):
            value_type = ValueType.FUNCTION
        elif isinstance(symbol, Constant):
            value_type = ValueType.CONSTANT
        else:
            value_type = ValueType.VARIABLE
        return Reference(value_type, symbol)

    @v_args(meta=True)
    def annotation(self, children, meta: Meta):
        name = children[0]
        annotation = get_annotation(name)
        if annotation is None:
            report(
                Errors.UndefinedSymbol,
                name,
                filepath=self.filepath,
                line=meta.line,
                column=meta.column
            )
            self.errored = True
            return Annotation("undefined", None, AnnotationCategory.METADATA), {}

        if annotation.params is None:
            return annotation, {}

        if len(children) - 1 != annotation.params:
            report(
                Errors.ArgumentNumberMismatch,
                name,
                str(len(annotation.params)),
                str(len(children) - 1),
                filepath=self.filepath,
                line=meta.line,
                column=meta.column
            )
            return Annotation("undefined", None, AnnotationCategory.METADATA), {}

        return annotation, {arg: param for arg, param in zip(children[1:], annotation.params)}

    def ARRAY_SIZE(self, token):
        return Reference.literal(int(token))

    def INT(self, token):
        return Reference.literal(int(token))

    def FLOAT(self, token):
        return Reference.literal(float(token))

    def STRING(self, token):
        return Reference.literal(ast.literal_eval(token))

    def true(self, token):
        return Reference.literal(True)

    def false(self, token):
        return Reference.literal(False)

    def ID(self, token):
        return str(token)
