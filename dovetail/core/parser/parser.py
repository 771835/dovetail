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
    - parser_code: 代码解析函数，将源代码转换为 AST
    - ASTTransformer: AST 访问器类，实现语法制导翻译

使用示例：
    >>> config = CompileConfig(...)
    >>> transformer = ASTTransformer(config, Path("main.mcdl"))
    >>> ast_tree = parser_code("main.mcdl")
    >>> transformer.visit(ast_tree)
    >>> ir_builder = transformer.builder
"""
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
from dovetail.core.enums import (
    StructureType, DataType, VariableType,
    MinecraftVersion, MinecraftEdition, FunctionType
)
from dovetail.core.enums.minecraft import UnknownMinecraftVersionError
from dovetail.core.enums.types import Array, DataTypeBase, AnnotationCategory
from dovetail.core.errors import report, Errors
from dovetail.core.include_manager import IncludeManager
from dovetail.core.instructions import (
    IRDeclare, IRAssign, IRInstruction, IRScopeBegin,
    IRScopeEnd, IRFunction, IRReturn, IRBreak, IRContinue
)
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

# 初始化 Lark 解析器
lark_parser = Lark(
    open(r".\lark\dovetail.lark", encoding='utf-8').read(),
    start="program",
    parser='lalr',
    cache=".cache",
    propagate_positions=True,
    maybe_placeholders=True
)


@timed("解析用时 {:.5f}.")
def parser_code(filepath: Path | str, start: Optional[str] = None) -> Tree | None:
    """
    解析代码文件生成 AST

    Args:
        filepath: 代码文件路径
        start: 语法解析起点（可选）

    Returns:
        AST 树，如果文件不存在或解析失败则返回 None
    """
    filepath = Path(filepath)
    if not filepath.exists() or not filepath.is_file():
        return None

    with open(filepath, encoding='utf-8') as f:
        code = f.read()

    parse_start = start if start is not None else "program"
    return lark_parser.parse(code, start=parse_start, on_error=lambda e: True)


class ASTTransformer(Interpreter):
    """
    AST 访问器 - 遍历语法树并生成中间表示（IR）

    Attributes:
        config: 编译配置
        filepath: 当前编译的源文件路径
        top_scope: 顶层作用域
        current_scope: 当前活动作用域
        scope_stack: 作用域栈
        builtin_function: 内建函数处理器映射表
        include_manager: 导入管理器
        builder: IR 构建器
        error_count: 编译错误计数
        warning_count: 编译警告计数
    """

    def __init__(self, config: CompileConfig, source_path: Path):
        super().__init__()
        self.config = config
        self.filepath = source_path

        # 初始化作用域
        self.top_scope = Scope("top", None, StructureType.GLOBAL)
        self.current_scope = self.top_scope
        self.scope_stack: list[Scope] = [self.top_scope]

        # 初始化内建函数表
        self.builtin_function: dict[str, Callable[..., Variable | Literal]] = {}

        # 初始化管理器
        self.include_manager = IncludeManager()
        self.builder = IRBuilder()

        # 加载内置库
        self._load_library(LibraryMapping.get("builtins", self.builder))
        if self.config.experimental:
            self._load_library(LibraryMapping.get("experimental", self.builder))

        # 错误统计
        self.error_count = 0
        self.warning_count = 0

    def __default__(self, tree: Tree) -> list[Any]:
        """默认访问处理 - 递归访问所有子节点"""
        return self.visit_children(tree)

    # ==================== 辅助方法 ====================

    @lru_cache(maxsize=None)
    def _load_library(self, library: Library):
        """加载库并注册符号和处理器"""
        try:
            self._append_ir(library.load())

            # 注册函数符号和处理器
            for function, handler in library.get_functions().items():
                self.current_scope.add_symbol(function)
                self.builtin_function[function.get_name()] = handler

            # 注册常量
            for constant, value in library.get_variables().items():
                self.current_scope.add_symbol(constant)
                self._append_ir(IRDeclare(constant))
                self._append_ir(IRAssign(constant, value))

            # 注册类和方法
            for class_, method_handlers in library.get_classes().items():
                self.current_scope.add_symbol(class_)
                for method_name, handler in method_handlers.items():
                    self.builtin_function[f"{class_.name}:{method_name}"] = handler

        except Exception as e:
            self._report(
                Errors.LibraryLoad,
                library.get_name(),
                e.__repr__(),
                filepath=self.filepath,
            )

    @contextmanager
    def _scoped_environment(self, name: str, scope_type: StructureType):
        """
        作用域上下文管理器

        Args:
            name: 作用域名称
            scope_type: 作用域类型

        Yields:
            新创建的作用域
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
        """追加 IR 指令到构建器"""
        if isinstance(instr, IRInstruction):
            self.builder.insert(instr)
        else:
            for ir_instr in instr:
                self.builder.insert(ir_instr)

    def _get_loop_check_scope_type(self) -> ScopeCore | None:
        """
        向上查找最近的 LOOP_CHECK 作用域

        遇到条件作用域和循环体作用域继续查找，遇到其他类型停止

        Returns:
            找到的循环作用域，未找到则返回 None
        """
        for scope in reversed(self.scope_stack):
            if scope.stype == StructureType.LOOP_CHECK:
                return scope
            elif scope.stype not in (StructureType.CONDITIONAL, StructureType.LOOP_BODY):
                break
        return None

    def _search_include_path(self, filepath: Path, line=-1, column=-1) -> Path | None:
        """
        搜索导入文件的实际路径

        Args:
            filepath: 待搜索的文件路径
            line: 代码行号（用于错误报告）
            column: 代码列号（用于错误报告）

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
            self._report(
                Errors.CompilerInclude,
                str(filepath),
                "找不到文件",
                filepath=self.filepath,
                line=line,
                column=column
            )
            return None

    def _get_meta_line_column(self, meta: Optional[Meta]) -> tuple[int, int]:
        """从 Meta 对象提取行列号"""
        if meta is None:
            return -1, -1
        return meta.line, meta.column

    def _decl_variable(
            self,
            name: str,
            dtype: DataTypeBase,
            value: Optional[Reference] = None,
            meta: Optional[Meta] = None,
            mutable: bool = True
    ) -> Optional[Reference]:
        """
        声明变量并进行类型检查

        Args:
            name: 变量名
            dtype: 数据类型
            value: 初始值（可选）
            meta: 元数据（用于错误报告）
            mutable: 是否可变

        Returns:
            变量引用，声明失败则返回 None
        """
        line, column = self._get_meta_line_column(meta)

        # 检查类型是否可定义
        if not dtype.is_definable():
            self._report(
                Errors.TypeMismatch,
                "可定义类型",
                dtype.get_name(),
                filepath=self.filepath,
                line=line,
                column=column
            )
            return None

        # 检查初始值类型匹配
        if value is not None and dtype != value.get_dtype():
            self._report(
                Errors.TypeMismatch,
                dtype.get_name(),
                value.get_dtype().get_name(),
                filepath=self.filepath,
                line=line,
                column=column
            )
            return None

        # 创建变量符号
        variable = Variable(NameNormalizer.normalize(name), dtype, mutable=mutable)
        if not self.current_scope.add_symbol(variable):
            self._report(
                Errors.DuplicateDefinition,
                name,
                filepath=self.filepath,
                line=line,
                column=column
            )
            return None

        # 生成 IR
        self._append_ir(IRDeclare(variable))
        if value:
            self._append_ir(IRAssign(variable, value))

        return Reference(variable)

    def _report(
            self,
            error: Errors,
            *args: str,
            filepath: Path | str = "<unknown>",
            line: int = -1,
            column: int = -1,
            suggestion: Optional[str] = None
    ) -> None:
        """报告编译错误并增加计数"""
        report(
            error,
            *args,
            filepath=filepath,
            line=line,
            column=column,
            suggestion=suggestion
        )
        self.error_count += 1

    def _process_annotations(
            self,
            children: list[Tree | Token]
    ) -> dict[Annotation, dict[str, Any]]:
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

    def _should_skip_for_version(
            self,
            annotations: dict[Annotation, dict[str, Any]],
            meta: Meta
    ) -> bool:
        """
        根据版本注解判断是否跳过编译

        Args:
            annotations: 注解字典
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
                    self._report(
                        Errors.UnsupportedTargetVersion,
                        args.get("min", "1.20.4"),
                        filepath=self.filepath,
                        line=meta.line,
                        column=meta.column
                    )
                    return True

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
                    return True

                if not (min_version <= self.config.version <= max_version):
                    return True

            # 处理 @target 注解
            elif annotation.name == "target":
                target_edition = MinecraftEdition.from_str(args.get("edition", "java"))
                compiler_edition = self.config.version.edition

                if target_edition != compiler_edition:
                    return True

        return False

    # ==================== 访问器方法 ====================

    @v_args(meta=True)
    def struct(self, children: list[Tree | Token], meta: Meta):
        """处理结构体定义"""
        # 处理注解
        annotations = self._process_annotations(children)

        # 检查版本和目标平台
        if self._should_skip_for_version(annotations, meta):
            return

        # 解析结构体
        name = children.pop(0).value
        fields: dict[str, DataTypeBase] = {}
        for field in children:
            field_name, field_type = self.visit(field)
            fields[field_name] = field_type

        # 添加符号
        symbol = Structure(NameNormalizer.normalize(name), fields)
        if not self.current_scope.add_symbol(symbol):
            self._report(
                Errors.DuplicateDefinition,
                name,
                filepath=self.filepath,
                line=meta.line,
                column=meta.column
            )

    def struct_field(self, children: list[Tree | Token]) -> tuple[str, DataTypeBase]:
        """处理结构体字段"""
        name: str = children.pop(0).value
        dtype: DataTypeBase = self.visit(children.pop(0))
        return name, dtype

    @v_args(meta=True)
    def function(self, children: list[Tree | Token], meta: Meta):
        """处理函数定义"""
        # 处理注解
        annotations = self._process_annotations(children)

        # 检查版本和目标平台
        if self._should_skip_for_version(annotations, meta):
            return

        # 解析函数签名
        params: list[Parameter]
        return_type: DataTypeBase
        name: str

        if isinstance(children[0], Tree) and children[0].data == 'type':
            # annotation* ("function"|"fn") type ID params (block|pass_stmt)
            return_type = self.visit(children.pop(0))
            name = NameNormalizer.normalize(children.pop(0).value)
            params = self.visit(children.pop(0))
        else:
            # annotation* ("function"|"fn"|"def") ID params ["->" type] (block|pass_stmt)
            name = NameNormalizer.normalize(children.pop(0).value)
            params = self.visit(children.pop(0))
            if children[0] is not None:
                return_type = self.visit(children.pop(0))
            else:
                return_type = DataType.VOID
                children.pop(0)

        # 跳过 pass 语句
        if children and children[0].data == 'pass_stmt':
            children.pop()

        # 创建函数符号
        func_type = (FunctionType.FUNCTION if children
                     else FunctionType.FUNCTION_UNIMPLEMENTED)
        function = Function(name, params, return_type, func_type, annotations)
        self.current_scope.add_symbol(function, force=True)

        # 生成 IR
        self._append_ir(IRFunction(function))

        # 处理函数体
        if children:
            with self._scoped_environment(name, StructureType.FUNCTION):  # NOQA
                # 添加参数到作用域
                for param in params:
                    if not self.current_scope.add_symbol(param):
                        self._report(
                            Errors.DuplicateDefinition,
                            param.get_name(),
                            filepath=self.filepath,
                            line=meta.line,
                            column=meta.column
                        )
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

        return self._decl_variable(symbol_name, dtype, default_value, meta)

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

        return self._decl_variable(symbol_name, dtype, value, meta, mutable=False)

    def params(self, tree: Tree) -> list[Parameter]:
        """处理参数列表"""
        return [self.visit(param) for param in tree.children]

    @v_args(meta=True)
    def param(self, children: list[Tree | Token], meta: Meta) -> Parameter:
        """处理单个参数定义"""
        name: str
        dtype: DataTypeBase
        is_mutable: bool = children.pop(0) is not None

        # 解析参数类型和名称
        if isinstance(children[0], Tree) and children[0].data == "type":
            # [MUT] type ID ("=" expr)?
            dtype = self.visit(children.pop(0))
            name = NameNormalizer.normalize(children.pop(0).value)
        else:
            # [MUT] ID ":" type ("=" expr)?
            name = NameNormalizer.normalize(children.pop(0).value)
            dtype = self.visit(children.pop(0))

        # 处理默认值
        default_value: Reference | None = None
        if children:
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
                # 错误时返回无默认值的参数
                return Parameter(Variable(name, dtype, VariableType.PARAMETER))

        return Parameter(
            Variable(name, dtype, VariableType.PARAMETER),
            is_mutable,
            default_value
        )

    @v_args(meta=True)
    def return_stmt(self, children: list[Tree | Token], meta: Meta):
        """处理 return 语句"""
        # 获取返回值
        value: Reference | None = None
        if children:
            value = self.visit(children.pop(0))

            # 标记返回值的变量类型
            if isinstance(value.value, Variable):
                value.value.var_type = VariableType.RETURN

        # 查找所在函数的作用域
        function_scope = next(
            (scope for scope in reversed(self.scope_stack)
             if scope.stype == StructureType.FUNCTION),
            None
        )

        if function_scope is None:
            self._report(
                Errors.InvalidControlFlow,
                "return 在函数之外",
                filepath=self.filepath,
                line=meta.line,
                column=meta.column
            )
            return

        # 类型检查
        if value is not None:
            function_symbol: Function | None = function_scope.parent.find_symbol(function_scope.name)

            if function_symbol is None:
                self._report(
                    Errors.InvalidControlFlow,
                    f"找不到函数{function_scope.name}的符号信息",
                    filepath=self.filepath,
                    line=meta.line,
                    column=meta.column
                )

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
        """处理 break 语句"""
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
        """处理 continue 语句"""
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
        """处理导入语句"""
        original_filepath: str = self.visit(children.pop(0)).value.value

        # 检查是否为内置库
        if library := LibraryMapping.get(original_filepath, self.builder):
            self._load_library(library)
            return

        # 搜索文件路径
        filepath = self._search_include_path(
            Path(original_filepath),
            meta.line,
            meta.column
        )

        if filepath is None or self.include_manager.has_path(filepath):
            return

        self.include_manager.add_include_path(filepath)

        # 递归解析导入的文件
        try:
            old_filepath = self.filepath
            self.filepath = filepath

            ast_tree = parser_code(filepath)
            self.visit(ast_tree)

            # 恢复原文件路径
            self.filepath = old_filepath

        except Exception as e:
            self._report(
                Errors.CompilerInclude,
                str(filepath),
                f"无法正确解析文件: {e.__repr__()}",
                filepath=self.filepath,
                line=meta.line,
                column=meta.column
            )

    @v_args(meta=True)
    def type(
            self,
            children: list[Token | Tree | int],
            meta: Meta
    ) -> DataType | Class | Array | DataTypeBase:
        """处理类型声明"""
        original_name: str = children.pop(0).value

        # 尝试解析内置类型
        try:
            dtype = DataType.get_by_value(original_name)
        except ValueError:
            # 解析自定义类型
            dtype = self.current_scope.resolve_symbol(
                NameNormalizer.normalize(original_name)
            )

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

        # 检查类型是否可定义
        if dtype.is_definable():
            # 处理数组类型
            if children:
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
        """处理类型别名定义"""
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

    def null(self, _: Tree) -> Reference:
        """处理 null 字面量"""
        return Reference.literal(None)

    def paren(self, tree: Tree) -> Reference:
        """处理括号表达式"""
        return self.visit(tree.children[-1])

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
            case "FLOAT":
                return Reference.literal(float(token))
            case "true":
                return Reference.literal(True)
            case "false":
                return Reference.literal(False)
            case _:
                return Reference.literal(str(token))

    @v_args(meta=True)
    def identifier(self, children: list[str] | str, meta: Meta) -> Reference:
        """处理标识符引用"""
        symbol_name = children.pop() if isinstance(children, list) else children
        symbol = self.current_scope.resolve_symbol(
            NameNormalizer.normalize(symbol_name)
        )

        if symbol is None:
            # 提供相似符号建议
            suggestion = suggest_similar(
                NameNormalizer.normalize(symbol_name),
                list(self.current_scope.get_all_symbols().keys())
            )
            self._report(
                Errors.UndefinedSymbol,
                symbol_name,
                filepath=self.filepath,
                line=meta.line,
                column=meta.column,
                suggestion=f"你的意思是 '{suggestion}'？" if suggestion else None,
            )
            return Reference.literal(None)

        return Reference(symbol)

    @v_args(meta=True)
    def annotation(
            self,
            children: list[str],
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
        name = children.pop(0)
        annotation = builtin_annotation.get_annotation(name)

        # 检查注解是否存在
        if annotation is None:
            self._report(
                Errors.UndefinedSymbol,
                name,
                filepath=self.filepath,
                line=meta.line,
                column=meta.column
            )
            return self._undefined_annotation()

        # 处理无参数注解
        if annotation.params is None:
            if children:
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

        # 检查参数数量匹配
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
            return self._undefined_annotation()

        # 构建参数字典（参数名 -> 参数值）
        return annotation, dict(zip(annotation.params, children))

    @staticmethod
    def _undefined_annotation() -> tuple[Annotation, dict]:
        """返回一个未定义的注解占位符"""
        return Annotation("undefined", None, AnnotationCategory.METADATA), {}
