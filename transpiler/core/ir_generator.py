# coding=utf-8
"""
遍历AST，生成中间指令
"""
import itertools
from contextlib import contextmanager
from pathlib import Path
from typing import Callable
from functools import lru_cache

from antlr4 import FileStream, CommonTokenStream

from transpiler.core.enums import *
from transpiler.core.errors import *
from transpiler.core.generator_config import GeneratorConfig
from transpiler.core.include_manager import IncludeManager
from transpiler.core.instructions import *
from transpiler.core.ir_builder import IRBuilder
from transpiler.core.lib.library import Library
from transpiler.core.lib.library_mapping import StdBuiltinMapping
from transpiler.core.parser.transpilerLexer import transpilerLexer
from transpiler.core.parser.transpilerParser import transpilerParser
from transpiler.core.parser.transpilerVisitor import transpilerVisitor
from transpiler.core.result import Result
from transpiler.core.scope import Scope
from transpiler.core.symbols import *
from transpiler.utils.naming import NameNormalizer


class MCGenerator(transpilerVisitor):
    """"
    遍历ast，生成ir
    """

    def __init__(self, config: GeneratorConfig):
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
        self.cnt = itertools.count()
        self.filename = "<main>"
        self.ir_builder: IRBuilder = IRBuilder()

        #  加载内置库
        self._load_library(StdBuiltinMapping.get("builtins", self.ir_builder))
        if self.config.enable_experimental:
            self._load_library(StdBuiltinMapping.get("experimental", self.ir_builder))

    @lru_cache(maxsize=None)
    def _load_library(self, library: Library):
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

        # TODO: 实现其他加载

    @contextmanager
    def scoped_environment(self, name: str, scope_type: StructureType):
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
            if current.type == StructureType.LOOP_CHECK:
                return current.get_name()
            elif current.type in (StructureType.CONDITIONAL, StructureType.LOOP_BODY):
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
            if param.get_data_type() != arg_value.get_data_type():
                raise ArgumentTypeMismatchError(
                    param_name=param.get_name(),
                    expected=param.get_data_type().name,
                    actual=arg_value.get_data_type().name,
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

        args_list: list[Reference] = []

        if instance_ref is not None and func_symbol.params:
            args_list.append(instance_ref)
        if argument_list_ctx.exprList() and argument_list_ctx.exprList().expr():
            for expr in argument_list_ctx.exprList().expr():
                args_list.append(self.visit(expr).value)

        return self._validate_function_call_with_result(func_symbol, args_list)

    def _process_function_declaration(
            self,
            ctx: transpilerParser.FunctionDeclContext | transpilerParser.MethodDeclContext,
            func_type: FunctionType,
            check_name_conflict: bool = False,
            process_annotations: bool = False
    ) -> Result:
        """通用函数/方法声明处理"""
        func_name = NameNormalizer.normalize(ctx.ID().getText())
        return_type = self._get_type_definition(ctx.type_().getText(), True) if ctx.type_() else DataType.NULL

        # 检查重复定义
        if self.current_scope.has_symbol(func_name):
            raise DuplicateDefinitionError(
                func_name,
                line=self._get_current_line(),
                column=self._get_current_column(),
                filename=self.filename
            )

        # 检查函数名冲突（仅函数需要）
        if check_name_conflict and not self.config.enable_same_name_function_nesting:
            current = self.current_scope
            while current:
                if current.get_name() == func_name:
                    raise FunctionNameConflictError(
                        name=func_name,
                        scope_name=current.get_name(),
                        line=self._get_current_line(),
                        column=self._get_current_column(),
                        filename=self.filename
                    )
                current = current.parent

        # 处理参数列表
        params_list: list[Parameter] = []
        params: transpilerParser.ParamListContext = ctx.paramList()
        if params.paramDecl():
            for param in params.paramDecl():
                param_name = param.ID().getText()
                param_type = self._get_type_definition(param.type_().getText())
                param_default = self.visit(param.expr()).value if param.expr() else None
                if param_default and param_default.get_data_type() != param_type:
                    raise ArgumentTypeMismatchError(
                        param_name,
                        param_type,
                        param_default.get_data_type(),
                        self._get_current_line(),
                        self._get_current_column(),
                        self.filename
                    )
                var = Variable(
                    param_name,
                    param_type,
                    VariableType.PARAMETER
                )
                params_list.append(
                    Parameter(
                        var,
                        param.expr() is not None,
                        param_default
                    )
                )

        # 处理注解
        annotations = []
        if process_annotations:
            annotations = [annotation.ID().getText() for annotation in ctx.annotation()]

        # 创建函数对象
        func = Function(
            func_name,
            params_list,
            return_type,
            func_type,
            annotations
        )

        # 添加到符号表
        if not self.current_scope.add_symbol(func):
            raise DuplicateDefinitionError(
                func_name,
                line=self._get_current_line(),
                column=self._get_current_column(),
                filename=self.filename
            )
        self._add_ir_instruction(IRFunction(func))

        # 创建作用域并处理函数体
        with self.scoped_environment(func_name, StructureType.FUNCTION):
            for param in params_list:
                if not self.current_scope.add_symbol(param):
                    raise DuplicateDefinitionError(
                        param.get_name(),
                        line=self._get_current_line(),
                        column=self._get_current_column(),
                        filename=self.filename
                    )
                self._add_ir_instruction(IRDeclare(param.var))

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
        symbol: Symbol = self.current_scope.resolve_symbol(NameNormalizer.normalize(identifier_name))
        if symbol is None:
            raise UndefinedSymbolError(
                identifier_name,
                line=self._get_current_line(),
                column=self._get_current_column(),
                filename=self.filename
            )
        if not isinstance(symbol, (Variable, Constant, Parameter, Function, Class)):
            raise SymbolCategoryError(
                identifier_name,
                expected="Variable/Constant/Function",
                actual=symbol.__class__.__name__,
                line=self._get_current_line(),
                column=self._get_current_column(),
                filename=self.filename
            )
        if isinstance(symbol, Parameter):
            return symbol.var
        return symbol

    def _check_recursion(self, func_name: str, func_symbol: Function):
        if not self.config.enable_recursion:  # 未启用递归
            current = self.current_scope
            while current:
                if (current.get_name() == func_name
                        and current.type == StructureType.FUNCTION
                        and current.get_parent().find_symbol(func_name) is func_symbol):
                    raise CompileRecursionError(
                        f"函数 '{func_name}' 检测到递归调用，但递归支持未启用，启用递归请使用参数--enable-recursion",
                        line=self._get_current_line(),
                        column=self._get_current_column(),
                        filename=self.filename
                    )
                current = current.parent

    @staticmethod
    def _parse_fstring(s: str) -> tuple[str, ...]:
        parts: list[str] = []  # 存储解析结果（交替为文本和变量）
        current_text = ''  # 当前累积的普通文本
        i = 0  # 当前字符索引

        while i < len(s):
            # 处理双花括号转义
            if i + 1 < len(s) and s[i] == '{' and s[i + 1] == '{':
                current_text += '{'
                i += 2
            elif i + 1 < len(s) and s[i] == '}' and s[i + 1] == '}':
                current_text += '}'
                i += 2
            elif s[i] == '{':
                # 遇到单花括号，开始变量解析
                parts.append(current_text)
                current_text = ''
                start = i + 1
                end = start
                while end < len(s) and s[end] != '}':
                    end += 1
                variable = s[start:end]
                parts.append(variable)
                i = end + 1
            else:
                # 普通字符，添加到 current_text
                current_text += s[i]
                i += 1

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

    def _create_temp_var(self, dtype: DataType | Class, prefix: str) -> Variable:
        """创建带唯一编号的临时变量"""
        temp_var = Variable(f"{prefix}_{next(self.cnt)}", dtype)
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
        var_symbol = self.current_scope.resolve_symbol(var_name)
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
        if_id = next(self.cnt)

        result_var = self._create_temp_var(DataType.NULL, "ternary")  # 此处数据类型需要根据后文得出
        self._add_ir_instruction(IRDeclare(result_var))
        with self.scoped_environment(f"ternary_{if_id}_a", StructureType.CONDITIONAL) as a_scope:
            a_ref = self.visit(a).value
            self._add_ir_instruction(IRAssign(result_var, a_ref))

        with self.scoped_environment(f"ternary_{if_id}_b", StructureType.CONDITIONAL) as b_scope:
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
            >>> MCGenerator.check_subset(['苹果', '香蕉'], ['苹果', '香蕉', '橙子'])
            (True, set())

            >>> MCGenerator.check_subset(['苹果', '葡萄'], ['苹果', '香蕉'])
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
        dtype: DataType | Class = self._get_type_definition(ctx.type_().getText()) if ctx.type_() else DataType.NULL
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
        dtype: DataType | Class = self._get_type_definition(ctx.type_().getText()) if ctx.type_() else DataType.NULL
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

        with self.scoped_environment(class_name, StructureType.CLASS):
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

        with self.scoped_environment(class_name, StructureType.CLASS):
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
        left: Reference = self.visit(ctx.expr(0)).value
        right: Reference = self.visit(ctx.expr(1)).value
        op = ctx.getChild(1).getText()
        if left.get_data_type() != right.get_data_type():
            raise TypeMismatchError(
                expected_type=left.get_data_type(),
                actual_type=right.get_data_type(),
                line=self._get_current_line(),
                column=self._get_current_column(),
                filename=self.filename
            )
        # 生成唯一结果变量
        result_var = self._create_temp_var(DataType.BOOLEAN, "bool")

        self._add_ir_instruction(IRDeclare(result_var))
        self._add_ir_instruction(IRCompare(result_var, CompareOps(op), left, right))

        return Result(Reference(ValueType.VARIABLE, result_var))

    def visitLogicalAndExpr(self, ctx: transpilerParser.LogicalAndExprContext):
        left: Reference = self.visit(ctx.expr(0)).value
        right: Reference = self.visit(ctx.expr(1)).value

        if left.get_data_type() != DataType.BOOLEAN or right.get_data_type() != DataType.BOOLEAN:
            raise TypeMismatchError(
                expected_type="boolean与boolean",
                actual_type=f"{left.get_data_type().value}和{right.get_data_type().value}",
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
                actual_type=f"{left.get_data_type().value}和{right.get_data_type().value}",
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
        if isinstance(instance_type, DataType):
            raise PrimitiveTypeOperationError(
                "修改属性",
                instance_type.name,
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
        if isinstance(array_type, DataType):
            raise PrimitiveTypeOperationError(
                "数组修改",
                array_type.name,
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
        op = BinaryOps(ctx.getChild(1).getText())

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
        if left.value.get_data_type() == DataType.STRING and op != BinaryOps.ADD:
            raise InvalidOperatorError(
                str(op.value),
                line=self._get_current_line(),
                column=self._get_current_column(),
                filename=self.filename
            )

        # 生成唯一结果变量
        result_var = self._create_temp_var(left.value.get_data_type(), "calc")

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
        method_name = ctx.ID().getText()
        if isinstance(instance_type, DataType):
            raise PrimitiveTypeOperationError(
                "方法调用",
                instance_type.name,
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
        if isinstance(instance_type, DataType):
            raise PrimitiveTypeOperationError(
                "成员访问",
                instance_type.name,
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
        if isinstance(array_type, DataType):
            raise PrimitiveTypeOperationError(
                "数组访问",
                array_type.name,
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
        loop_id = next(self.cnt)
        with self.scoped_environment(f"while_{loop_id}_check", StructureType.LOOP_CHECK) as loop_check:
            with self.scoped_environment(f"while_{loop_id}_body", StructureType.LOOP_BODY) as loop_body:
                self.visit(ctx.block())

            # 从检查函数调用循环体
            condition_ref = self.visit(ctx.condition()).value

            self._add_ir_instruction(IRCondJump(condition_ref.value, loop_body.name))
            self._add_ir_instruction(IRCondJump(condition_ref.value, loop_check.name))
        self._add_ir_instruction(IRJump(loop_check.name))

    def visitForStmt(self, ctx: transpilerParser.ForStmtContext):
        for_control: transpilerParser.ForControlContext = ctx.forControl()
        if for_control:  # 传统for循环
            loop_id = next(self.cnt)
            if for_control.forInit():
                # 处理初始化表达式
                if for_control.forInit().varDecl():
                    self.visit(for_control.forInit().varDecl())
                else:
                    self.visit(for_control.forInit().expr())
            # 创建循环检查作用域
            with self.scoped_environment(f"for_{loop_id}_check", StructureType.LOOP_CHECK) as loop_check:
                with self.scoped_environment(f"for_{loop_id}_body", StructureType.LOOP_BODY) as loop_body:

                    # 处理循环体
                    self.visit(ctx.block())

                    # 处理更新表达式
                    if ctx.forControl().forUpdate():
                        self.visit(ctx.forControl().forUpdate().expr())
                # 处理条件表达式
                if for_control.condition():
                    condition_ref = self.visit(for_control.condition()).value
                else:
                    condition_ref = Reference.literal(True)

                self._add_ir_instruction(IRCondJump(condition_ref.value, loop_body.name))
                self._add_ir_instruction(IRCondJump(condition_ref.value, loop_check.name))

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
        if_id = next(self.cnt)
        # 计算条件表达式
        condition_ref = self.visit(ctx.condition()).value

        # 创建if分支作用域
        with self.scoped_environment(f"if_{if_id}", StructureType.CONDITIONAL) as if_scope:
            self.visit(ctx.block(0))
        # 创建else分支作用域
        if ctx.block(1):
            with self.scoped_environment(f"else_{if_id}", StructureType.CONDITIONAL) as else_scope:
                self.visit(ctx.block(1))
            self._add_ir_instruction(IRCondJump(condition_ref.value, if_scope.name, else_scope.name))
        else:
            self._add_ir_instruction(IRCondJump(condition_ref.value, if_scope.name))
        return Result(None)

    def visitReturnStmt(self, ctx: transpilerParser.ReturnStmtContext):
        result_dtype: DataType | Class = DataType.NULL
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
            if current.type == StructureType.FUNCTION:
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
        include_path_ref: Literal = self.visit(ctx.literal()).value.value
        if include_path_ref.dtype != DataType.STRING:
            raise TypeMismatchError(
                DataType.STRING,
                include_path_ref.dtype,
                self._get_current_line(),
                self._get_current_column(),
                self.filename
            )

        include_path: Path = Path(include_path_ref.value)

        # 检查是否已经导入过
        if self.include_manager.has_path(include_path):
            return Result(None)

        # 判断是否为内置库
        if library := StdBuiltinMapping.get(include_path_ref.value, self.ir_builder):
            self._load_library(library)
            self.include_manager.add_include_path(include_path)
            return Result(None)

        if not include_path.exists():
            if (self.config.lib_path / include_path_ref.value).exists():
                include_path = self.config.lib_path / include_path_ref.value
                self.include_manager.add_include_path(include_path)
            else:
                raise CompilerIncludeError(
                    include_path.absolute(),
                    "找不到文件",
                    line=self._get_current_line(),
                    column=self._get_current_column(),
                    filename=self.filename
                )

        # 处理导入的文件
        try:
            old_filename = self.filename
            self.filename = str(include_path.absolute())
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
                str(include_path.absolute()),
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
