# coding=utf-8
"""
遍历AST，生成中间指令
"""
import itertools
import os.path
from contextlib import contextmanager
from functools import lru_cache
from pathlib import Path
from typing import Callable

from antlr4 import FileStream, CommonTokenStream

from transpiler.core.compile_config import CompileConfig
from transpiler.core.enums.operations import UnaryOps, BinaryOps, CompareOps
from transpiler.core.enums.types import FunctionType, DataTypeBase, DataType, StructureType, ValueType, VariableType, \
    ClassType
from transpiler.core.errors import *
from transpiler.core.include_manager import IncludeManager
from transpiler.core.instructions import *
from transpiler.core.ir_builder import IRBuilder
from transpiler.core.lib.library import Library
from transpiler.core.lib.library_mapping import LibraryMapping
from transpiler.core.parser.transpilerLexer import transpilerLexer
from transpiler.core.parser.transpilerParser import transpilerParser
from transpiler.core.parser.transpilerVisitor import transpilerVisitor
from transpiler.core.result import Result
from transpiler.core.scope import Scope
from transpiler.core.symbols import *
from transpiler.utils.naming import NameNormalizer


class IRGenerator(transpilerVisitor):
    """IR生成器 - 遍历AST并生成中间表示"""

    def __init__(self, config: CompileConfig):
        self._current_ctx = None
        self.config = config
        self.top_scope = Scope(
            "global",
            None,
            StructureType.GLOBAL
        )
        self.current_scope = self.top_scope
        self.include_manager = IncludeManager()  # 包含管理器
        self.builtin_func_table: dict[str, Callable[..., Variable | Constant | Literal]] = {}
        self.scope_stack = [self.top_scope]
        self.counter = itertools.count()
        self.filename = os.path.relpath(config.namespace, Path.cwd())
        self.ir_builder = IRBuilder()

        #  加载内置库
        self._load_library(LibraryMapping.get("builtins", self.ir_builder))
        if self.config.enable_experimental:
            self._load_library(LibraryMapping.get("experimental", self.ir_builder))

    @lru_cache(maxsize=None)
    def _load_library(self, library: Library):
        try:
            self._add_ir_instruction(library.load())
            for function, handler in library.get_functions().items():
                self.current_scope.add_symbol(function)
                self.builtin_func_table[function.get_name()] = handler
            for constant, value in library.get_constants().items():
                self.current_scope.add_symbol(constant)
                self._add_ir_instruction(IRDeclare(constant))
                self._add_ir_instruction(IRAssign(constant, value))
            for class_, method_handlers in library.get_classes().items():
                self.current_scope.add_symbol(class_)
                for method_name, handler in method_handlers.items():
                    self.builtin_func_table[f"{class_.name}:{method_name}"] = handler
        except Exception as e:
            raise LibraryLoadError(
                library.get_name(),
                e.__repr__(),
                line=self._get_current_line(),
                column=self._get_current_column(),
                filename=self.filename
            ) from e

    @contextmanager
    def _scoped_environment(self, name: str, scope_type: StructureType):
        """
        作用域管理器
        """
        new_scope = self.current_scope.create_child(name, scope_type)
        self.current_scope = new_scope
        self.scope_stack.append(new_scope)
        self._add_ir_instruction(IRScopeBegin(name, scope_type))
        try:
            yield new_scope
        finally:
            if self.current_scope.exist_parent():
                self.current_scope = self.current_scope.get_parent()
                self.scope_stack.pop()
                self._add_ir_instruction(IRScopeEnd(name, scope_type))

    def _add_ir_instruction(self, instructions: IRInstruction | list[IRInstruction]):
        if isinstance(instructions, IRInstruction):
            instructions = [instructions]
        for instruction in instructions:
            self.ir_builder.insert(instruction)

    def _get_loop_check_scope_name(self) -> str | None:
        current = self.current_scope
        while current:
            if current.stype == StructureType.LOOP_CHECK:
                return current.get_name()
            elif current.stype in (StructureType.CONDITIONAL, StructureType.LOOP_BODY):
                current = current.parent
            else:
                break
        return None

    def get_ir(self) -> IRBuilder:
        """
        返回IRBuilder

        :return: IRBuilder对象
        """
        return self.ir_builder

    def _validate_function_call_with_result(
            self,
            func_symbol: Function,
            argument_list: list,
    ) -> dict[str, Reference]:
        """
        验证函数调用参数并返回参数字典

        Args:
            func_symbol: 被调用的函数符号
            argument_list: 参数列表

        Returns:
            dict[str, Reference]: 参数名到参数值引用的映射字典

        Raises:
            InvalidSyntaxError: 当参数数量不匹配时
            ArgumentTypeMismatchError: 当参数类型不匹配时
        """

        min_args: int = sum(not param.optional for param in func_symbol.params)
        max_args: int = len(func_symbol.params)
        # 参数字典
        args_dict: dict[str, Reference] = {}

        # 检查参数数量是否在有效范围内
        if len(argument_list) > max_args:
            raise InvalidSyntaxError(
                f"参数数量不匹配: 期望最多 {max_args} 个参数，实际 {len(argument_list)} 个",
                line=self._get_current_line(),
                column=self._get_current_column(),
                filename=self.filename
            )
        elif len(argument_list) < min_args:
            raise InvalidSyntaxError(
                f"参数数量不匹配: 期望至少 {min_args} 个参数，实际 {len(argument_list)} 个",
                line=self._get_current_line(),
                column=self._get_current_column(),
                filename=self.filename
            )

        # 效验数据并记录参数字典
        for i, (arg_ref, param) in enumerate(itertools.zip_longest(argument_list, func_symbol.params)):
            arg_value = arg_ref or param.default
            args_dict[param.get_name()] = arg_value
            # 类型检查
            if not arg_value.get_data_type().is_subclass_of(param.get_data_type()):
                raise ArgumentTypeMismatchError(
                    param_name=param.get_name(),
                    expected=param.get_data_type(),
                    actual=arg_value.get_data_type(),
                    line=self._get_current_line(),
                    column=self._get_current_column(),
                    filename=self.filename
                )

        return args_dict

    def _process_call_arguments(
            self,
            func_symbol: Function,
            argument_list_ctx: transpilerParser.ArgumentListContext = None,
            instance_ref: Reference = None
    ) -> dict[str, Reference]:
        """
        处理函数/方法调用的参数

        Args:
            func_symbol: 被调用的函数/方法符号
            argument_list_ctx: 参数列表上下文，如果没有则为None
            instance_ref: 实例引用（用于方法调用），如果没有则为None

        Returns:
            dict[str, Reference]: 参数名到参数值的映射字典
        """

        argument_references: list[Reference] = []

        if instance_ref is not None and func_symbol.params:
            argument_references.append(instance_ref)
        if argument_list_ctx.exprList() and argument_list_ctx.exprList().expr():
            for expr in argument_list_ctx.exprList().expr():
                argument_references.append(self.visit(expr).value)

        return self._validate_function_call_with_result(func_symbol, argument_references)

    def _process_function_declaration(
            self,
            ctx: transpilerParser.FunctionDeclContext | transpilerParser.MethodDeclContext,
            func_type: FunctionType,
            check_name_conflict: bool = False,
            process_annotations: bool = False
    ) -> Result:
        """通用函数/方法声明处理"""
        function_name = NameNormalizer.normalize(ctx.ID().getText())
        return_type = self._get_type_definition(ctx.type_().getText(), True) if ctx.type_() else DataType.NULL

        # 检查重复定义
        if self.current_scope.has_symbol(function_name):
            raise DuplicateDefinitionError(
                function_name,
                line=self._get_current_line(),
                column=self._get_current_column(),
                filename=self.filename
            )

        # 检查函数名冲突
        if check_name_conflict and not self.config.enable_same_name_function_nesting:
            current = self.current_scope
            while current:
                if current.get_name() == function_name:
                    raise FunctionNameConflictError(
                        name=function_name,
                        scope_name=current.get_name(),
                        line=self._get_current_line(),
                        column=self._get_current_column(),
                        filename=self.filename
                    )
                current = current.parent

        # 处理参数列表
        parameters: list[Parameter] = []
        param_context: transpilerParser.ParamListContext = ctx.paramList()
        if param_context.paramDecl():
            for param_declaration in param_context.paramDecl():
                param_name = NameNormalizer.normalize(param_declaration.ID().getText())
                param_type = self._get_type_definition(param_declaration.type_().getText())
                param_default = self.visit(param_declaration.expr()).value if param_declaration.expr() else None
                if param_default and param_default.get_data_type() != param_type:
                    raise ArgumentTypeMismatchError(
                        param_name,
                        param_type,
                        param_default.get_data_type(),
                        self._get_current_line(),
                        self._get_current_column(),
                        self.filename
                    )
                parameters.append(
                    Parameter(
                        Variable(
                            param_name,
                            param_type,
                            VariableType.PARAMETER
                        ),
                        param_declaration.expr() is not None,
                        param_default
                    )
                )

        # 处理注解
        annotations = []
        if process_annotations:
            annotations = [annotation.ID().getText() for annotation in ctx.annotation()]

        # 创建函数对象
        func = Function(
            function_name,
            parameters,
            return_type,
            func_type,
            annotations
        )

        # 添加到符号表
        if not self.current_scope.add_symbol(func):
            raise DuplicateDefinitionError(
                function_name,
                line=self._get_current_line(),
                column=self._get_current_column(),
                filename=self.filename
            )
        self._add_ir_instruction(IRFunction(func))

        # 创建作用域并处理函数体
        with self._scoped_environment(function_name, StructureType.FUNCTION):
            for param_declaration in parameters:
                if not self.current_scope.add_symbol(param_declaration):
                    raise DuplicateDefinitionError(
                        param_declaration.get_name(),
                        line=self._get_current_line(),
                        column=self._get_current_column(),
                        filename=self.filename
                    )
                self._add_ir_instruction(IRDeclare(param_declaration.var))

            # 处理函数体
            self.visit(ctx.block())

        return Result(Reference(ValueType.FUNCTION, func))

    def _resolve_identifier(self, identifier_name: str) -> Symbol:
        """
        解析标识符并返回对应的符号

        Args:
            identifier_name: 标识符名称

        Returns:
            Symbol: 解析到的符号对象

        Raises:
            UndefinedVariableError: 当标识符未定义时
            SymbolCategoryError: 当标识符类型不正确时
        """
        resolved_symbol: Symbol = self.current_scope.resolve_symbol(NameNormalizer.normalize(identifier_name))
        if resolved_symbol is None:
            raise UndefinedSymbolError(
                identifier_name,
                line=self._get_current_line(),
                column=self._get_current_column(),
                filename=self.filename
            )
        if not isinstance(resolved_symbol, (Variable, Constant, Parameter, Function, Class)):
            raise SymbolCategoryError(
                identifier_name,
                expected="Variable/Constant/Function",
                actual=resolved_symbol.__class__.__name__,
                line=self._get_current_line(),
                column=self._get_current_column(),
                filename=self.filename
            )
        if isinstance(resolved_symbol, Parameter):
            return resolved_symbol.var
        return resolved_symbol

    def _check_recursion(self, func_name: str, func_symbol: Function):
        if not self.config.enable_recursion:  # 未启用递归
            current = self.current_scope
            while current:
                if (current.get_name() == func_name
                        and current.stype == StructureType.FUNCTION
                        and current.get_parent().find_symbol(func_name) is func_symbol):
                    raise CompileRecursionError(
                        f"函数 '{func_name}' 检测到递归调用，但递归支持未启用，启用递归请使用参数--enable-recursion",
                        line=self._get_current_line(),
                        column=self._get_current_column(),
                        filename=self.filename
                    )
                current = current.parent

    @staticmethod
    def _parse_fstring(format_string: str) -> tuple[str, ...]:
        parts: list[str] = []  # 存储解析结果（交替为文本和变量）
        current_text = ''  # 当前累积的普通文本
        index = 0  # 当前字符索引

        while index < len(format_string):
            # 处理双花括号转义
            if index + 1 < len(format_string) and format_string[index] == '{' and format_string[index + 1] == '{':
                current_text += '{'
                index += 2
            elif index + 1 < len(format_string) and format_string[index] == '}' and format_string[index + 1] == '}':
                current_text += '}'
                index += 2
            elif format_string[index] == '{':
                # 遇到单花括号，开始变量解析
                parts.append(current_text)
                current_text = ''
                start = index + 1
                end = start
                while end < len(format_string) and format_string[end] != '}':
                    end += 1
                variable = format_string[start:end]
                parts.append(variable)
                index = end + 1
            else:
                # 普通字符，添加到 current_text
                current_text += format_string[index]
                index += 1

        # 添加最后剩余的普通文本
        if current_text:
            parts.append(current_text)
        return tuple(parts)

    def _process_fstring(self, value: str) -> Reference[Variable]:
        """处理格式化字符串的解析和IR生成"""
        # 解析字符串结构
        parts = self._parse_fstring(value[2:-1])  # 去掉前缀和首尾引号

        # 初始化结果变量
        result_var = self._create_temp_var(DataType.STRING, "fstring")
        self._add_ir_instruction(IRDeclare(result_var))
        self._add_ir_instruction(IRAssign(result_var, Reference(ValueType.LITERAL,
                                                                Literal(DataType.STRING, ""))))

        # 逐段处理字符串内容
        for i, part in enumerate(parts):
            if i % 2 == 0:  # 文本段
                result_var = self._append_text_to_result(result_var, part)
            else:  # 变量段
                result_var = self._append_variable_to_result(result_var, part)

        return Reference(ValueType.VARIABLE, result_var)

    def _create_temp_var(self, dtype: DataTypeBase, prefix: str) -> Variable:
        """创建带唯一编号的临时变量"""
        temp_var = Variable(f"{prefix}_{next(self.counter)}", dtype)
        if not self.current_scope.add_symbol(temp_var):
            return self._create_temp_var(dtype, prefix)

        return temp_var

    def _append_text_to_result(self, current_var: Variable, text: str) -> Variable:
        """将文本内容追加到结果字符串"""
        new_var = self._create_temp_var(DataType.STRING, "fstring")
        self._add_ir_instruction(IRDeclare(new_var))
        self._add_ir_instruction(IROp(new_var, BinaryOps.ADD,
                                      Reference(ValueType.VARIABLE, current_var),
                                      Reference.literal(text)))
        return new_var

    def _append_variable_to_result(self, current_var: Variable, var_name: str) -> Variable:
        """将变量内容追加到结果字符串"""
        # 解析变量符号
        var_symbol = self.current_scope.resolve_symbol(NameNormalizer.normalize(var_name))
        if var_symbol is None:
            raise UndefinedVariableError(var_name, self._get_current_line(), self._get_current_column())
        if isinstance(var_symbol, Parameter):
            var_symbol = var_symbol.var
        elif not isinstance(var_symbol, (Variable, Constant)):
            raise SymbolCategoryError(
                var_name,
                expected="Variable/Constant",
                actual=var_symbol.__class__.__name__,
                line=self._get_current_line(),
                column=self._get_current_column(),
                filename=self.filename
            )

        # 创建类型转换临时变量
        if var_symbol.dtype != DataType.STRING:
            cast_var = self._create_temp_var(DataType.STRING, "cast")
            self._add_ir_instruction(IRDeclare(cast_var))
            self._add_ir_instruction(IRCast(cast_var, DataType.STRING,
                                            Reference(ValueType.VARIABLE, var_symbol)))
        else:
            # 对于string类型不进行转换
            cast_var = var_symbol
        # 拼接字符串
        new_var = self._create_temp_var(DataType.STRING, "fstring")
        self._add_ir_instruction(IRDeclare(new_var))
        self._add_ir_instruction(IROp(new_var, BinaryOps.ADD,
                                      Reference(ValueType.VARIABLE, current_var),
                                      Reference(ValueType.VARIABLE, cast_var)))
        return new_var

    def _resolve_type_symbol(self, type_name: str) -> Class | None:
        """解析类型名称对应的符号（仅限类/类型定义）"""
        symbol = self.current_scope.resolve_symbol(type_name)
        if isinstance(symbol, Class):
            return symbol
        return None

    def _get_type_definition(
            self,
            type_name: str,
            allow_null=False) -> DataType | Class:
        """获取类型的具体定义（内置类型返回DataType，类返回Class实例）null特殊处理"""
        type_name = NameNormalizer.normalize(type_name)
        try:
            if builtin_type := DataType.get_by_value(type_name):
                if builtin_type == DataType.NULL and not allow_null:
                    raise UndefinedTypeError(
                        type_name,
                        line=self._get_current_line(),
                        column=self._get_current_column(),
                        filename=self.filename
                    )
                return builtin_type
        except ValueError:
            pass  # DataType不存在此类型,去寻找符号
        if symbol := self._resolve_type_symbol(type_name):
            if symbol:
                return symbol
        raise UndefinedTypeError(
            type_name,
            line=self._get_current_line(),
            column=self._get_current_column(),
            filename=self.filename
        )

    def _get_current_line(self):
        if self._current_ctx:
            return self._current_ctx.start.line
        return -1

    def _get_current_column(self):
        if self._current_ctx:
            return self._current_ctx.start.column
        return -1

    def _ternary(self, cond, a, b):
        if_id = next(self.counter)

        result_var = self._create_temp_var(DataType.NULL, "ternary")  # 此处数据类型需要根据后文得出
        self._add_ir_instruction(IRDeclare(result_var))
        with self._scoped_environment(f"ternary_{if_id}_a", StructureType.CONDITIONAL) as a_scope:
            a_ref = self.visit(a).value
            self._add_ir_instruction(IRAssign(result_var, a_ref))

        with self._scoped_environment(f"ternary_{if_id}_b", StructureType.CONDITIONAL) as b_scope:
            b_ref = self.visit(b).value
            self._add_ir_instruction(IRAssign(result_var, b_ref))
        # 将结果类型修改为实际类型
        result_var.dtype = a_ref.get_data_type()
        if a_ref.get_data_type() != b_ref.get_data_type():
            raise TypeMismatchError(
                expected_type=a_ref.get_data_type(),
                actual_type=b_ref.get_data_type(),
                line=self._get_current_line(),
                column=self._get_current_column(),
                filename=self.filename
            )

        cond_ref = self.visit(cond).value
        self._add_ir_instruction(IRCondJump(cond_ref.value, a_scope.name, b_scope.name))
        return result_var

    @staticmethod
    def check_subset(list_primary, list_candidate) -> tuple[bool, set]:
        """
        检查主列表是否为候选列表的子集并返回缺失元素

        函数将验证 list_primary 的所有元素是否都存在于 list_candidate 中
        （不考虑元素顺序和重复值）。如果不是子集，则返回缺失元素集合。

        Parameters:
            list_primary (list): 待检查的主列表（可能是子集）
            list_candidate (list): 作为候选超集的列表

        Returns:
            tuple: 包含两个元素的元组
                - bool: 子集验证结果，True表示主列表是子集
                - set: 缺失元素集合（当是子集时返回空集合）

        Example:
            >>> IRGenerator.check_subset(['苹果', '香蕉'], ['苹果', '香蕉', '橙子'])
            (True, set())

            >>> IRGenerator.check_subset(['苹果', '葡萄'], ['苹果', '香蕉'])
            (False, {'葡萄'})

        Note:
            1. 由于使用集合操作，重复元素会被自动去重
            2. 结果中的元素顺序可能与原列表不同
            3. 缺失元素集合使用set类型保证元素唯一性
        """
        set_primary = set(list_primary)
        set_candidate = set(list_candidate)

        is_subset_result = set_primary.issubset(set_candidate)
        missing_elements = set_primary - set_candidate if not is_subset_result else set()

        return is_subset_result, missing_elements

    def visit(self, tree) -> Result:
        """
        遍历ast树
        """
        previous_ctx = self._current_ctx
        self._current_ctx = tree

        result = tree.accept(self)
        if not isinstance(result, Result) and not isinstance(tree, transpilerParser.ProgramContext):
            raise UnexpectedError(f"意外的错误:result结果为{type(result)},需要{Result}")
        self._current_ctx = previous_ctx
        return result

    def visitVarDecl(self, ctx: transpilerParser.VarDeclContext):
        """处理变量声明"""
        var_name = NameNormalizer.normalize(ctx.ID().getText())
        dtype: DataTypeBase = self._get_type_definition(ctx.type_().getText()) if ctx.type_() else DataType.NULL
        var_value: Reference | None = None

        if ctx.expr():  # 如果存在初始值
            result = self.visit(ctx.expr())  # 处理初始化表达式
            # 如果没有显式指定类型，则根据初始值推断类型
            if dtype == DataType.NULL:
                dtype = result.value.get_data_type()
                if dtype == DataType.NULL:
                    raise TypeMismatchError(
                        expected_type="any type",
                        actual_type="null (initial value has null type)",
                        line=self._get_current_line(),
                        column=self._get_current_column(),
                        filename=self.filename,
                        msg="变量不能初始化为null类型"
                    )
            # 如果指定了类型，则进行类型检查
            elif dtype != result.value.get_data_type():
                raise TypeMismatchError(
                    expected_type=dtype,
                    actual_type=result.value.get_data_type(),
                    line=self._get_current_line(),
                    column=self._get_current_column(),
                    filename=self.filename
                )

            var_value = result.value

            # 检查是否存在类型（显式指定或推断出的）
            if dtype == DataType.NULL:
                raise TypeMismatchError(
                    expected_type="any type",
                    actual_type="null (no type specified and no initial value to infer from)",
                    line=self._get_current_line(),
                    column=self._get_current_column(),
                    filename=self.filename,
                    msg="变量声明必须指定类型或提供初始值以推断类型"
                )

        var = Variable(
            var_name,
            dtype
        )

        if not self.current_scope.add_symbol(var):  # 添加符号失败
            raise DuplicateDefinitionError(
                var_name,
                line=self._get_current_line(),
                column=self._get_current_column(),
                filename=self.filename
            )

        self._add_ir_instruction(IRDeclare(var))
        if var_value:
            self._add_ir_instruction(IRAssign(var, var_value))

        return Result(Reference(ValueType.VARIABLE, var))

    def visitConstDecl(self, ctx: transpilerParser.ConstDeclContext):
        name = NameNormalizer.normalize(ctx.ID().getText())
        dtype: DataTypeBase = self._get_type_definition(ctx.type_().getText()) if ctx.type_() else DataType.NULL
        result = self.visit(ctx.expr())  # 处理初始化表达式
        # 如果没有显式指定类型，则根据初始值推断类型
        if dtype == DataType.NULL:
            dtype = result.value.get_data_type()
        # 如果指定了类型，则进行类型检查
        elif dtype != result.value.get_data_type():
            raise TypeMismatchError(
                expected_type=dtype,
                actual_type=result.value.get_data_type(),
                line=self._get_current_line(),
                column=self._get_current_column(),
                filename=self.filename
            )

        value = result.value

        # 检查是否存在类型（显式指定或推断出的）
        if dtype == DataType.NULL:
            raise TypeMismatchError(
                expected_type="any type",
                actual_type="null (no type specified and no initial value to infer from)",
                line=self._get_current_line(),
                column=self._get_current_column(),
                filename=self.filename,
                msg="变量声明必须指定类型或提供初始值以推断类型"
            )

        constant = Constant(
            name,
            dtype
        )

        if not self.current_scope.add_symbol(constant):
            raise DuplicateDefinitionError(
                name,
                line=self._get_current_line(),
                column=self._get_current_column(),
                filename=self.filename
            )

        self._add_ir_instruction(IRDeclare(constant))
        self._add_ir_instruction(IRAssign(constant, value))
        return Result(Reference(ValueType.CONSTANT, constant))

    def visitFunctionDecl(self, ctx: transpilerParser.FunctionDeclContext):
        return self._process_function_declaration(
            ctx,
            FunctionType.FUNCTION,
            check_name_conflict=True,
            process_annotations=True
        )

    def visitMethodDecl(self, ctx: transpilerParser.MethodDeclContext):
        return self._process_function_declaration(
            ctx,
            FunctionType.METHOD
        )

    def visitClassDecl(self, ctx: transpilerParser.ClassDeclContext):
        class_name = NameNormalizer.normalize(ctx.ID().getText())
        types = ctx.type_()
        # 使用规则显式检查
        parent: Class | None = self._get_type_definition(
            types[0].getText()) if ctx.EXTENDS() else None
        # 接口位置取决于EXTENDS是否存在
        interface: Class | None = self._get_type_definition(
            types[1].getText()) if ctx.EXTENDS() and ctx.IMPLEMENTS() else (
            self._get_type_definition(
                types[0].getText()) if not ctx.EXTENDS() and ctx.IMPLEMENTS() else None
        )
        properties: set[Variable] = set()
        methods: set[Function] = set()

        class_ = Class(
            class_name,
            methods=methods,
            interface=interface,
            parent=parent,
            properties=properties
        )

        if not self.current_scope.add_symbol(class_):
            raise DuplicateDefinitionError(
                class_name,
                line=self._get_current_line(),
                column=self._get_current_column(),
                filename=self.filename
            )
        self._add_ir_instruction(IRClass(class_))

        with self._scoped_environment(class_name, StructureType.CLASS):
            # 处理继承
            if parent:
                raise MissingImplementationError(
                    "类继承",
                    line=self._get_current_line(),
                    column=self._get_current_column(),
                    filename=self.filename
                )  # TODO:处理继承

            # 处理实例属性和方法
            property_ctx: transpilerParser.ClassPropertyDeclContext
            for property_ctx in ctx.classPropertyDecl():
                class_property = Variable(
                    property_ctx.ID().getText(),
                    self._get_type_definition(property_ctx.type_().getText())
                )
                if not self.current_scope.add_symbol(class_property):
                    raise DuplicateDefinitionError(
                        class_property.name,
                        line=self._get_current_line(),
                        column=self._get_current_column(),
                        filename=self.filename
                    )
                properties.add(class_property)

            for method in ctx.methodDecl():
                methods.add(self.visit(method).value.value)

            if interface:
                current_interface = interface
                interfaces_method = []
                while interface:
                    interfaces_method += current_interface.methods
                    current_interface = current_interface.interface

                pending_implementation_methods = self.check_subset(interfaces_method, [m.get_name() for m in methods])
                if len(pending_implementation_methods[1]) != 0:
                    raise UnimplementedInterfaceMethodsError(
                        missing_methods=pending_implementation_methods[1],
                        line=self._get_current_line(),
                        column=self._get_current_column(),
                        filename=self.filename
                    )

        return Result(Reference(ValueType.CLASS, class_))

    def visitInterfaceDecl(self, ctx: transpilerParser.InterfaceDeclContext):
        class_name = NameNormalizer.normalize(ctx.ID().getText())
        extends = self._get_type_definition(ctx.type_().getText())
        properties: set[Variable] = set()
        methods: set[Function] = set()

        class_ = Class(class_name,
                       methods=methods,
                       interface=None,
                       parent=extends,
                       properties=properties,
                       type=ClassType.INTERFACE)

        if not self.current_scope.add_symbol(class_):
            raise DuplicateDefinitionError(
                class_name,
                line=self._get_current_line(),
                column=self._get_current_column(),
                filename=self.filename
            )
        self._add_ir_instruction(IRClass(class_))

        with self._scoped_environment(class_name, StructureType.CLASS):
            # 处理继承
            if extends:
                raise MissingImplementationError(
                    "类继承",
                    line=self._get_current_line(),
                    column=self._get_current_column(),
                    filename=self.filename
                )  # TODO:处理继承
            # 处理字段和方法
            for method in ctx.methodDecl():
                methods.add(self.visit(method).value.value)

        return Result(Reference(ValueType.CLASS, class_))

    def visitCondition(self, ctx: transpilerParser.ConditionContext):
        result = self.visit(ctx.expr())
        # 评估条件表达式
        if result.value.get_data_type() != DataType.BOOLEAN:
            raise InvalidSyntaxError(
                ctx.expr().getText(),
                line=self._get_current_line(),
                column=self._get_current_column(),
                filename=self.filename
            )
        return result

    def visitLiteral(self, ctx: transpilerParser.LiteralContext):
        value: str = ctx.getText()
        if value == 'true' or value == 'false':
            return Result.from_literal(value == 'true', DataType.BOOLEAN)
        elif value == 'null':
            return Result.from_literal(None, DataType.NULL)
        elif value[0] == 'f':
            return Result(self._process_fstring(value))
        elif value.isdigit():
            return Result.from_literal(int(value), DataType.INT)
        else:
            return Result.from_literal(value[1:-1], DataType.STRING)

    def visitParenExpr(self, ctx: transpilerParser.ParenExprContext):
        return self.visit(ctx.expr())

    def visitCompareExpr(self, ctx):
        left_operand: Reference = self.visit(ctx.expr(0)).value
        right_operand: Reference = self.visit(ctx.expr(1)).value
        operator_text = ctx.getChild(1).getText()
        if left_operand.get_data_type() != right_operand.get_data_type():
            raise TypeMismatchError(
                expected_type=left_operand.get_data_type(),
                actual_type=right_operand.get_data_type(),
                line=self._get_current_line(),
                column=self._get_current_column(),
                filename=self.filename
            )
        # 生成唯一结果变量
        result_variable = self._create_temp_var(DataType.BOOLEAN, "result_variable")

        self._add_ir_instruction(IRDeclare(result_variable))
        self._add_ir_instruction(IRCompare(result_variable, CompareOps(operator_text), left_operand, right_operand))

        return Result(Reference(ValueType.VARIABLE, result_variable))

    def visitLogicalAndExpr(self, ctx: transpilerParser.LogicalAndExprContext):
        left_operand: Reference = self.visit(ctx.expr(0)).value
        right_operand: Reference = self.visit(ctx.expr(1)).value

        if left_operand.get_data_type() != DataType.BOOLEAN or right_operand.get_data_type() != DataType.BOOLEAN:
            raise TypeMismatchError(
                expected_type="boolean与boolean",
                actual_type=f"{left_operand.get_data_type()}和{right_operand.get_data_type()}",
                line=ctx.expr(0).start.line,
                column=ctx.expr(0).start.column,
                filename=self.filename
            )
        # 生成唯一结果变量
        result_var = self._create_temp_var(DataType.BOOLEAN, "bool")
        temp_var = self._create_temp_var(DataType.INT, "calc")

        self._add_ir_instruction(IRDeclare(temp_var))
        self._add_ir_instruction(IROp(temp_var, BinaryOps.ADD, left_operand, right_operand))
        self._add_ir_instruction(IRDeclare(result_var))
        self._add_ir_instruction(
            IRCompare(
                result_var,
                CompareOps.EQ,
                Reference(ValueType.VARIABLE, temp_var),
                Reference.literal(2)
            )
        )
        return Result(Reference(ValueType.VARIABLE, result_var))

    def visitLogicalOrExpr(self, ctx: transpilerParser.LogicalOrExprContext):
        left: Reference = self.visit(ctx.expr(0)).value
        right: Reference = self.visit(ctx.expr(1)).value

        if left.get_data_type() != DataType.BOOLEAN or right.get_data_type() != DataType.BOOLEAN:
            raise TypeMismatchError(
                expected_type="boolean与boolean",
                actual_type=f"{left.get_data_type()}和{right.get_data_type()}",
                line=ctx.expr(0).start.line,
                column=ctx.expr(0).start.column,
                filename=self.filename
            )
        # 生成唯一结果变量
        result_var = self._create_temp_var(DataType.BOOLEAN, "bool")
        temp_var = self._create_temp_var(DataType.INT, "calc")

        self._add_ir_instruction(IRDeclare(temp_var))
        self._add_ir_instruction(IROp(temp_var, BinaryOps.ADD, left, right))
        self._add_ir_instruction(IRDeclare(result_var))
        self._add_ir_instruction(
            IRCompare(
                result_var,
                CompareOps.NE,
                Reference(ValueType.VARIABLE, temp_var),
                Reference.literal(0),
            )
        )
        return Result(Reference(ValueType.VARIABLE, result_var))

    def visitLogicalNotExpr(self, ctx: transpilerParser.LogicalNotExprContext):
        value_ref = self.visit(ctx.expr()).value
        result_var = self._create_temp_var(DataType.BOOLEAN, "bool")
        self._add_ir_instruction(IRDeclare(result_var))
        self._add_ir_instruction(IRUnaryOp(result_var, UnaryOps.NOT, value_ref))
        return Result(Reference(ValueType.VARIABLE, result_var))

    def visitIdentifierExpr(self, ctx: transpilerParser.IdentifierExprContext):
        return Result(Reference(ValueType.VARIABLE, self._resolve_identifier(ctx.ID().getText())))

    def visitLocalAssignmentExpr(self, ctx: transpilerParser.LocalAssignmentExprContext):
        var_name = ctx.ID().getText()
        expr_result = self.visit(ctx.expr())
        var_symbol = self._resolve_identifier(var_name)
        if isinstance(var_symbol, Constant):
            raise ASTSyntaxError(
                f"不能修改常量 '{var_name}'",
                line=self._get_current_line(),
                column=self._get_current_column(),
                filename=self.filename
            )
        elif not isinstance(var_symbol, Variable):
            raise SymbolCategoryError(
                var_name,
                expected="Variable",
                actual=var_symbol.__class__.__name__,
                line=self._get_current_line(),
                column=self._get_current_column(),
                filename=self.filename
            )

        # 类型检查
        if var_symbol.dtype != expr_result.value.get_data_type():
            raise TypeMismatchError(
                expected_type=var_symbol.dtype,
                actual_type=expr_result.value.get_data_type(),
                line=self._get_current_line(),
                column=self._get_current_column(),
                filename=self.filename
            )

        self._add_ir_instruction(IRAssign(var_symbol, expr_result.value))

        return Result(Reference(ValueType.VARIABLE, var_symbol))

    def visitMemberAssignmentExpr(self, ctx: transpilerParser.MemberAssignmentExprContext):
        instance_ref = self.visit(ctx.expr(0)).value
        instance_type = instance_ref.get_data_type()
        field_name = NameNormalizer.normalize(ctx.ID().getText())
        value = self.visit(ctx.expr(1)).value
        if not isinstance(instance_type, Class):
            raise PrimitiveTypeOperationError(
                "修改属性",
                instance_type.get_name(),
                line=self._get_current_line(),
                column=self._get_current_column(),
                filename=self.filename
            )
        # 搜索被修改的变量或常量
        member_symbol = next(
            (
                symbol for symbol in instance_type.properties
                if symbol.get_name() == field_name
            ),
            None
        )
        if member_symbol is None:
            raise UndefinedVariableError(
                field_name,
                line=self._get_current_line(),
                column=self._get_current_column(),
                filename=self.filename
            )
        self._add_ir_instruction(IRSetProperty(instance_ref.value, field_name, value))
        return Result(value)

    def visitArrayAssignmentExpr(self, ctx: transpilerParser.ArrayAssignmentExprContext):
        array = self.visit(ctx.expr(0)).value
        index = self.visit(ctx.expr(1)).value
        value = self.visit(ctx.expr(2)).value
        array_type = array.get_data_type()
        if not isinstance(array_type, Class):
            raise PrimitiveTypeOperationError(
                "数组修改",
                array_type.get_name(),
                line=self._get_current_line(),
                column=self._get_current_column(),
                filename=self.filename
            )
        setitem_method = method_symbol = next(
            (
                method for method in array_type.methods
                if method.get_name() == NameNormalizer.normalize("__setitem__")
            ),
            None
        )
        if method_symbol is None:
            raise UndefinedFunctionError(
                NameNormalizer.normalize("__setitem__"),
                line=self._get_current_line(),
                column=self._get_current_column(),
                filename=self.filename
            )
        if setitem_method.function_type != FunctionType.LIBRARY:
            self._add_ir_instruction(
                IRCallMethod(
                    None,
                    array_type,
                    setitem_method,
                    self._validate_function_call_with_result(setitem_method, [array, index, value])
                )
            )
        else:
            self.builtin_func_table[f"{array_type.get_name()}:__setitem__"](array, index, value)
        return Result(value)

    def visitFactorExpr(self, ctx: transpilerParser.FactorExprContext):
        left = self.visit(ctx.expr(0))
        right = self.visit(ctx.expr(1))
        op = ctx.getChild(1).getText()

        if left.value.get_data_type() != right.value.get_data_type():
            if (left.value.get_data_type() not in (DataType.BOOLEAN, DataType.INT)
                    or right.value.get_data_type() not in (DataType.BOOLEAN, DataType.INT)):
                raise TypeMismatchError(
                    expected_type=left.value.get_data_type(),
                    actual_type=right.value.get_data_type(),
                    line=self._get_current_line(),
                    column=self._get_current_column(),
                    filename=self.filename
                )
        if left.value.get_data_type() == DataType.STRING:
            raise InvalidOperatorError(
                op.value,
                line=self._get_current_line(),
                column=self._get_current_column(),
                filename=self.filename
            )

        # 生成唯一结果变量
        result_var = self._create_temp_var(left.value.get_data_type(), "calc")

        self._add_ir_instruction(IRDeclare(result_var))
        self._add_ir_instruction(IROp(result_var, BinaryOps(op), left.value, right.value))
        return Result(Reference(ValueType.VARIABLE, result_var))

    def visitTermExpr(self, ctx: transpilerParser.TermExprContext):
        left = self.visit(ctx.expr(0))
        right = self.visit(ctx.expr(1))
        left_type: DataTypeBase = left.value.get_data_type()
        right_type: DataTypeBase = right.value.get_data_type()

        op = BinaryOps(ctx.getChild(1).getText())

        if not left_type.is_subclass_of(right_type) and not right_type.is_subclass_of(left_type):
            raise TypeMismatchError(
                expected_type=left_type,
                actual_type=right_type,
                line=self._get_current_line(),
                column=self._get_current_column(),
                filename=self.filename
            )

        if left_type == DataType.STRING and op != BinaryOps.ADD:
            raise InvalidOperatorError(
                str(op.value),
                line=self._get_current_line(),
                column=self._get_current_column(),
                filename=self.filename
            )

        # 生成唯一结果变量
        result_type = left_type
        if left_type == DataType.BOOLEAN or left_type == DataType.BOOLEAN:
            #  类型提升
            result_type = DataType.INT
        result_var = self._create_temp_var(result_type, "calc")

        self._add_ir_instruction(IRDeclare(result_var))
        self._add_ir_instruction(IROp(result_var, op, left.value, right.value))
        return Result(Reference(ValueType.VARIABLE, result_var))

    def visitNegExpr(self, ctx: transpilerParser.NegExprContext):
        expr_result = self.visit(ctx.expr()).value
        if expr_result.get_data_type() not in (DataType.BOOLEAN, DataType.INT):
            raise TypeMismatchError(
                expected_type="int/boolean",
                actual_type=expr_result.value,
                line=self._get_current_line(),
                column=self._get_current_column(),
                filename=self.filename
            )
        if expr_result.value_type != ValueType.LITERAL:
            self._add_ir_instruction(
                IROp(
                    expr_result.value,
                    BinaryOps.MUL,
                    expr_result,
                    Reference.literal(-1)
                )
            )
            return Result(Reference(ValueType.VARIABLE, expr_result.value))
        else:
            return Result(Reference.literal(expr_result.value.value * -1))

    def visitTernaryPythonicExpr(self, ctx: transpilerParser.TernaryPythonicExprContext):
        return Result(Reference(ValueType.VARIABLE, self._ternary(ctx.expr(1), ctx.expr(0), ctx.expr(2))))

    def visitTernaryTraditionalExpr(self, ctx: transpilerParser.TernaryTraditionalExprContext):
        return Result(Reference(ValueType.VARIABLE, self._ternary(ctx.expr(0), ctx.expr(1), ctx.expr(2))))

    def visitFunctionCall(self, ctx: transpilerParser.FunctionCallContext):
        symbol: Symbol = self.visit(ctx.expr()).value.value
        symbol_name: str = symbol.get_name()
        if isinstance(symbol, Function):
            # 检测递归
            self._check_recursion(symbol_name, symbol)
            # 解析参数
            args_dict = self._process_call_arguments(symbol, ctx.argumentList())
            # 调用函数
            if symbol.function_type == FunctionType.LIBRARY:
                result_var = self.builtin_func_table[symbol.get_name()](**args_dict)
            else:
                result_var = self._create_temp_var(symbol.return_type, "result")
                if symbol.return_type != DataType.NULL:
                    self._add_ir_instruction(IRDeclare(result_var))
                    self._add_ir_instruction(IRCall(result_var, symbol, args_dict))
                else:
                    self._add_ir_instruction(IRCall(None, symbol, args_dict))

            return Result(Reference(ValueType.VARIABLE, result_var))
        elif isinstance(symbol, Class):
            if init_func := next(
                    (method for method in list(symbol.methods) if
                     method.get_name() == NameNormalizer.normalize("__init__")), None):
                instance = self._create_temp_var(symbol, "instance")
                self._add_ir_instruction(IRDeclare(instance))
                self._add_ir_instruction(
                    IRNewObj(
                        instance,
                        symbol
                    )
                )
                # 解析参数
                args_dict = self._process_call_arguments(
                    init_func,
                    ctx.argumentList(),
                    Reference(ValueType.VARIABLE, instance)
                )
                # 调用函数
                if init_func.function_type == FunctionType.LIBRARY:
                    self.builtin_func_table[f"{symbol.get_name()}:__init__"](**args_dict)
                else:
                    self._add_ir_instruction(IRCallMethod(None, symbol, init_func, args_dict))
                return Result(Reference(ValueType.VARIABLE, instance))

            raise NotCallableError(
                symbol_name,
                symbol.__class__.__name__,
                line=self._get_current_line(),
                column=self._get_current_column(),
                filename=self.filename
            )
        else:
            raise NotCallableError(
                symbol_name,
                symbol.__class__.__name__,
                line=self._get_current_line(),
                column=self._get_current_column(),
                filename=self.filename
            )

    def visitMethodCall(self, ctx: transpilerParser.MethodCallContext):
        instance_ref = self.visit(ctx.expr()).value
        instance_type = instance_ref.get_data_type()
        method_name = NameNormalizer.normalize(ctx.ID().getText())
        if not isinstance(instance_type, Class):
            raise PrimitiveTypeOperationError(
                "方法调用",
                instance_type.get_name(),
                line=self._get_current_line(),
                column=self._get_current_column(),
                filename=self.filename
            )
        # 搜索被调用的符号
        method_symbol = next(
            (
                method for method in instance_type.methods
                if method.get_name() == method_name
            ),
            None
        )
        if method_symbol is None:
            raise UndefinedFunctionError(
                method_name,
                line=self._get_current_line(),
                column=self._get_current_column(),
                filename=self.filename
            )

        args_dict = self._process_call_arguments(method_symbol, ctx.argumentList(), instance_ref)
        if method_symbol.function_type == FunctionType.LIBRARY:
            result_var = self.builtin_func_table[f"{instance_type.get_name()}:{method_symbol.get_name()}"](**args_dict)
        else:
            result_var = self._create_temp_var(method_symbol.return_type, "result")
            self._add_ir_instruction(IRDeclare(result_var))
            self._add_ir_instruction(IRCallMethod(result_var, instance_type, method_symbol, args_dict))
        if method_symbol.return_type != DataType.NULL:
            return Result(Reference(ValueType.VARIABLE, result_var))
        else:
            return Result(Reference.variable("result_null", DataType.NULL))

    def visitMemberAccess(self, ctx: transpilerParser.MemberAccessContext):
        instance_ref = self.visit(ctx.expr()).value
        instance_type = instance_ref.get_data_type()
        property_name = NameNormalizer.normalize(ctx.ID().getText())
        if not isinstance(instance_type, Class):
            raise PrimitiveTypeOperationError(
                "成员访问",
                instance_type.get_name(),
                line=self._get_current_line(),
                column=self._get_current_column(),
                filename=self.filename
            )
        # 搜索被访问的变量或常量
        member_symbol = next(
            (
                symbol for symbol in itertools.chain(instance_type.properties)
                if symbol.get_name() == property_name
            ),
            None
        )
        if member_symbol is None:
            raise UndefinedVariableError(
                property_name,
                line=self._get_current_line(),
                column=self._get_current_column(),
                filename=self.filename
            )
        result_var = self._create_temp_var(member_symbol.dtype, "result")
        self._add_ir_instruction(
            IRGetProperty(
                result_var,
                instance_ref.value,
                property_name
            )
        )
        return Result(Reference(ValueType.VARIABLE, result_var))

    def visitArrayAccess(self, ctx: transpilerParser.ArrayAccessContext):
        array = self.visit(ctx.expr(0)).value
        index = self.visit(ctx.expr(1)).value
        array_type = array.get_data_type()
        if not isinstance(array_type, Class):
            raise PrimitiveTypeOperationError(
                "数组访问",
                array_type.get_name(),
                line=self._get_current_line(),
                column=self._get_current_column(),
                filename=self.filename
            )
        getitem_method = method_symbol = next(
            (
                method for method in array_type.methods
                if method.get_name() == NameNormalizer.normalize("__getitem__")
            ),
            None
        )
        if method_symbol is None:
            raise UndefinedFunctionError(
                "__getitem__",
                line=self._get_current_line(),
                column=self._get_current_column(),
                filename=self.filename
            )
        if getitem_method.function_type != FunctionType.LIBRARY:
            result_var = self._create_temp_var(array_type, "result")
            self._add_ir_instruction(
                IRCallMethod(
                    result_var,
                    array_type,
                    getitem_method,
                    self._validate_function_call_with_result(getitem_method, [array, index])
                )
            )
        else:
            result_var = self.builtin_func_table[f"{array_type.get_name()}:__getitem__"](array, index)
        return Result(Reference(ValueType.VARIABLE, result_var))

    def visitBlock(self, ctx: transpilerParser.BlockContext):
        # 遍历子节点
        self.visitChildren(ctx)
        return Result(None)

    def visitWhileStmt(self, ctx: transpilerParser.WhileStmtContext):
        loop_identifier = next(self.counter)
        with self._scoped_environment(f"while_{loop_identifier}_check", StructureType.LOOP_CHECK) as loop_check:
            with self._scoped_environment(f"while_{loop_identifier}_body", StructureType.LOOP_BODY) as loop_body:
                self.visit(ctx.block())

            # 从检查函数调用循环体
            condition_value = self.visit(ctx.condition()).value.value

            self._add_ir_instruction(IRCondJump(condition_value, loop_body.name))
            self._add_ir_instruction(IRCondJump(condition_value, loop_check.name))
        self._add_ir_instruction(IRJump(loop_check.name))

    def visitForStmt(self, ctx: transpilerParser.ForStmtContext):
        for_control: transpilerParser.ForControlContext = ctx.forControl()
        if for_control:  # 传统for循环
            loop_identifier = next(self.counter)
            if for_control.forInit():
                # 处理初始化表达式
                if for_control.forInit().varDecl():
                    self.visit(for_control.forInit().varDecl())
                else:
                    self.visit(for_control.forInit().expr())
            # 创建循环检查作用域
            with self._scoped_environment(f"for_{loop_identifier}_check", StructureType.LOOP_CHECK) as loop_check:
                with self._scoped_environment(f"for_{loop_identifier}_body", StructureType.LOOP_BODY) as loop_body:

                    # 处理循环体
                    self.visit(ctx.block())

                    # 处理更新表达式
                    if ctx.forControl().forUpdate():
                        self.visit(ctx.forControl().forUpdate().expr())
                # 处理条件表达式
                if for_control.condition():
                    condition_value = self.visit(for_control.condition()).value.value
                else:
                    condition_value = Literal(DataType.BOOLEAN, True)

                self._add_ir_instruction(IRCondJump(condition_value, loop_body.name))
                self._add_ir_instruction(IRCondJump(condition_value, loop_check.name))

            self._add_ir_instruction(IRJump(loop_check.name))
        else:  # 增强for循环
            raise MissingImplementationError(
                "增强for循环",
                line=self._get_current_line(),
                column=self._get_current_column(),
                filename=self.filename
            )  # TODO:增强for循环实现
        return Result(None)

    def visitIfStmt(self, ctx: transpilerParser.IfStmtContext):
        # 生成唯一ID
        if_identifier = next(self.counter)
        # 计算条件表达式
        condition_ref = self.visit(ctx.condition()).value

        # 创建if分支作用域
        with self._scoped_environment(f"if_{if_identifier}", StructureType.CONDITIONAL) as if_scope:
            self.visit(ctx.block(0))
        # 创建else分支作用域
        if ctx.block(1):
            with self._scoped_environment(f"else_{if_identifier}", StructureType.CONDITIONAL) as else_scope:
                self.visit(ctx.block(1))
            self._add_ir_instruction(IRCondJump(condition_ref.value, if_scope.name, else_scope.name))
        else:
            self._add_ir_instruction(IRCondJump(condition_ref.value, if_scope.name))
        return Result(None)

    def visitReturnStmt(self, ctx: transpilerParser.ReturnStmtContext):
        result_dtype: DataTypeBase = DataType.NULL
        result_var_ref: Reference[Variable | Constant | Literal] | None = None
        if ctx.expr():
            result_var_ref = self.visit(ctx.expr()).value
            result_dtype = result_var_ref.get_data_type()
            if isinstance(result_var_ref.value, (Constant, Variable)):
                result_var_ref.value.var_type = VariableType.RETURN
        self._add_ir_instruction(IRReturn(result_var_ref))
        # 检查返回值的类型是否正确
        current = self.current_scope
        while current:
            if current.stype == StructureType.FUNCTION:
                break
            current = current.parent
        else:
            raise InvalidControlFlowError(
                msg="return在函数之外",
                line=self._get_current_line(),
                column=self._get_current_column(),
                filename=self.filename
            )
        func_name = current.get_name()
        func_symbol: Function | None = current.get_parent().find_symbol(func_name)
        if func_symbol.return_type != result_dtype:
            raise TypeMismatchError(
                expected_type=func_symbol.return_type,
                actual_type=result_dtype,
                line=self._get_current_line(),
                column=self._get_current_column(),
                filename=self.filename
            )
        return Result(None)

    def visitIncludeStmt(self, ctx: transpilerParser.IncludeStmtContext):
        original_include_path: str = str(self.visit(ctx.literal()).value.value.value)
        search_path: list[Path] = [self.config.lib_path, Path.cwd()]
        include_path: Path = Path(original_include_path)

        # 检查是否已经导入过
        if self.include_manager.has_path(include_path):
            return Result(None)

        # 判断是否为内置库
        if library := LibraryMapping.get(original_include_path, self.ir_builder):
            self._load_library(library)
            self.include_manager.add_include_path(include_path)
            return Result(None)

        include_path = next(
            (d / original_include_path for d in search_path if (Path(d) / original_include_path).exists()), None)
        if include_path:
            self.include_manager.add_include_path(include_path)
        else:
            raise CompilerIncludeError(
                include_path.resolve(),
                "找不到文件",
                line=self._get_current_line(),
                column=self._get_current_column(),
                filename=self.filename
            )

        # 处理导入的文件
        try:
            old_filename = self.filename
            self.filename = os.path.relpath(include_path, Path.cwd())
            input_stream = FileStream(self.filename, encoding='utf-8')
            lexer = transpilerLexer(input_stream)
            stream = CommonTokenStream(lexer)
            parser = transpilerParser(stream)
            tree = parser.program()

            # 访问并处理导入的文件
            self.visit(tree)
            # 重新回到原来的文件
            self.filename = old_filename
        except Exception as e:
            raise CompilerIncludeError(
                os.path.relpath(include_path, Path.cwd()),
                e.__repr__(),
                line=self._get_current_line(),
                column=self._get_current_column(),
                filename=self.filename
            )

        return Result(None)

    def visitContinueStmt(self, ctx: transpilerParser.ContinueStmtContext):
        loop_scope_name = self._get_loop_check_scope_name()
        if loop_scope_name is None:
            raise InvalidControlFlowError(
                "continue 语句只能在循环结构中使用",
                line=self._get_current_line(),
                column=self._get_current_column(),
                filename=self.filename
            )
        self._add_ir_instruction(IRContinue(loop_scope_name))
        return Result(None)

    def visitBreakStmt(self, ctx: transpilerParser.ContinueStmtContext):
        loop_scope_name = self._get_loop_check_scope_name()
        if loop_scope_name is None:
            raise InvalidControlFlowError(
                "break 语句只能在循环结构中使用",
                line=self._get_current_line(),
                column=self._get_current_column(),
                filename=self.filename
            )
        self._add_ir_instruction(IRBreak(loop_scope_name))
        return Result(None)
