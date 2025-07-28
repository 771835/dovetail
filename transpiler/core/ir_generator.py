# coding=utf-8
from __future__ import annotations

import os.path
import re
import uuid
from contextlib import contextmanager
from itertools import count
from typing import Callable

from antlr4 import FileStream, CommonTokenStream

from transpiler.core.backend.ir_builder import IRBuilder
from transpiler.core.errors import TypeMismatchError, UnexpectedError, CompilerSyntaxError, UndefinedTypeError, \
    CompilerImportError, UndefinedVariableError, InvalidSyntaxError, DuplicateDefinitionError, \
    ArgumentTypeMismatchError, InvalidControlFlowError, MissingImplementationError, RecursionError, NotCallableError, \
    InvalidOperatorError, SymbolCategoryError
from transpiler.core.generator_config import GeneratorConfig
from transpiler.core.include_manager import IncludeManager
from transpiler.core.instructions import *
from transpiler.core.language_enums import StructureType, DataType, ValueType, VariableType, FunctionType, ClassType
from transpiler.core.lib.library import Library
from transpiler.core.lib.std_builtin_mapping import StdBuiltinMapping
from transpiler.core.parser.transpilerLexer import transpilerLexer
from transpiler.core.parser.transpilerParser import transpilerParser
from transpiler.core.parser.transpilerVisitor import transpilerVisitor
from transpiler.core.result import Result
from transpiler.core.scope import Scope
from transpiler.core.symbols import *
from transpiler.test import print_all_attributes


class MCGenerator(transpilerVisitor):
    _INT_PATTERN = re.compile(r'^[-+]?\d+$')

    def __init__(self, config: GeneratorConfig):
        self._current_ctx = None
        self.config = config
        self.top_scope = Scope(
            "global",
            None,
            StructureType.GLOBAL)
        self.current_scope = self.top_scope
        self.include_manager = IncludeManager()  # 包含管理器
        self.builtin_func_table: dict[str, Callable[..., Variable | Constant | Literal]] = {}
        self.uuid_namespace = uuid.uuid4()
        self.scope_stack = [self.top_scope]
        self.cnt = count()  # 保证for loop和if else唯一性
        self.filename = "<main>"
        self.ir_builder: IRBuilder = IRBuilder()

        #  加载内置库
        self.load_library(StdBuiltinMapping.get("builtins", self.ir_builder))
        if self.config.enable_experimental:
            self.load_library(StdBuiltinMapping.get("experimental", self.ir_builder))

    def load_library(self, library: Library):
        library.load()
        for function, handler in library.get_functions().items():
            self.current_scope.add_symbol(function)
            self.builtin_func_table[function.get_name()] = handler
        for constant, value in library.get_constants().items():
            self.current_scope.add_symbol(constant)
            self._add_ir_instruction(IRDeclare(constant))
            self._add_ir_instruction(IRAssign(constant, value))
        # TODO: 实现其他加载

    @contextmanager
    def scoped_environment(self, name: str, scope_type: StructureType):
        scope = self._enter_scope(name, scope_type)
        try:
            yield scope
        finally:
            self._exit_scope()

    # 作用域管理辅助方法
    def _enter_scope(self, name: str, scope_type: StructureType):
        new_scope = self.current_scope.create_child(name, scope_type)
        self.current_scope = new_scope
        self.scope_stack.append(new_scope)
        if len(self.scope_stack) > 100:
            for i in self.scope_stack:
                print(f"at {i.name}, in {i.parent.name}")
            raise RecursionError(
                f"作用域嵌套过深 (超过100层)\n作用域路径: {self.current_scope.get_unique_name()}",
                line=self._get_current_line(),
                column=self._get_current_column(),
                filename=self.filename
            )
        self._add_ir_instruction(IRScopeBegin(name=name, stype=scope_type))
        return new_scope

    def _exit_scope(self):
        if self.current_scope.exist_parent():
            self.current_scope = self.current_scope.get_parent()
            self.scope_stack.pop()
            self._add_ir_instruction(IRScopeEnd())

    def _add_ir_instruction(
            self, instructions: IRInstruction | list[IRInstruction]):
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

    def get_generate_ir(self) -> IRBuilder:
        return self.ir_builder

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

    def _create_temp_var(self, dtype: DataType, prefix: str) -> Variable:
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
                                      Reference(ValueType.LITERAL,
                                                Literal(DataType.STRING, text))))
        return new_var

    def _append_variable_to_result(self, current_var: Variable, var_name: str) -> Variable:
        """将变量内容追加到结果字符串"""
        try:
            # 解析变量符号
            var_symbol = self.current_scope.resolve_symbol(var_name)
            if not isinstance(var_symbol, (Variable, Constant)):
                raise UndefinedVariableError(var_name, self._get_current_line(), self._get_current_column())
        except ValueError:
            raise UndefinedVariableError(var_name, self._get_current_line(), self._get_current_column())

        # 创建类型转换临时变量
        cast_var = self._create_temp_var(DataType.STRING, "cast")
        self._add_ir_instruction(IRDeclare(cast_var))
        self._add_ir_instruction(IRCast(cast_var, DataType.STRING,
                                        Reference(ValueType.VARIABLE, var_symbol)))

        # 拼接字符串
        new_var = self._create_temp_var(DataType.STRING, "fstring")
        self._add_ir_instruction(IRDeclare(new_var))
        self._add_ir_instruction(IROp(new_var, BinaryOps.ADD,
                                      Reference(ValueType.VARIABLE, current_var),
                                      Reference(ValueType.VARIABLE, cast_var)))
        return new_var

    def _resolve_type_symbol(self, type_name: str) -> Class | None:
        """解析类型名称对应的符号（仅限类/类型定义）"""
        try:
            symbol = self.current_scope.resolve_symbol(type_name)
            if isinstance(symbol, Class):
                return symbol
            return None
        except ValueError:
            return None

    def _get_type_definition(
            self,
            type_name: str,
            allow_void=False) -> DataType | Class:
        """获取类型的具体定义（内置类型返回DataType，类返回Class实例）void特殊处理"""
        try:
            if builtin_type := DataType.get_by_value(type_name):
                if builtin_type == DataType.VOID and not allow_void:
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

    # 检查类型是否存在
    def _type_exists(self, type_):
        if isinstance(type_, DataType):
            return True
        return self._get_type_definition(type_) is not None

    def _is_number(self, s):
        return bool(self._INT_PATTERN.match(s))

    def _get_current_line(self):
        if self._current_ctx:
            return self._current_ctx.start.line
        return -1

    def _get_current_column(self):
        if self._current_ctx:
            return self._current_ctx.start.column
        return -1

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
        if not isinstance(result, Result) and not isinstance(
                tree, transpilerParser.ProgramContext):
            print_all_attributes(tree)
            raise UnexpectedError(f"意外的错误:result结果为{type(result)},需要{Result}")
        self._current_ctx = previous_ctx
        return result

    # 处理变量声明
    def visitVarDeclaration(
            self,
            ctx: transpilerParser.VarDeclarationContext):
        var_name = ctx.ID().getText()
        var_type = self._get_type_definition(ctx.type_().getText())
        var_value: Reference | None = None
        if ctx.expr():  # 如果存在初始值
            result = self.visit(ctx.expr())  # 处理初始化表达式
            # 类型检查
            if var_type != result.value.get_data_type():
                raise TypeMismatchError(
                    expected_type=var_type,
                    actual_type=result.value.get_data_type(),
                    line=self._get_current_line(),
                    column=self._get_current_column(),
                    filename=self.filename
                )

            var_value = result.value

        if not self._type_exists(var_type):  # 判断所给类型是否存在
            raise UndefinedTypeError(
                var_type.name,
                line=self._get_current_line(),
                column=self._get_current_column(),
                filename=self.filename
            )

        var = Variable(
            var_name,
            var_type
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
        name = ctx.ID().getText()
        dtype = self._get_type_definition(ctx.type_().getText())
        result = self.visit(ctx.expr())  # 处理初始化表达式
        # 类型检查
        if dtype != result.value.get_data_type():
            raise TypeMismatchError(
                expected_type=dtype,
                actual_type=result.value.get_data_type(),
                line=self._get_current_line(),
                column=self._get_current_column(),
                filename=self.filename
            )

        value = result.value
        if not self._type_exists(dtype):  # 判断所给类型是否存在
            raise UndefinedTypeError(
                dtype.name,
                line=self._get_current_line(),
                column=self._get_current_column()
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

    # 处理函数定义
    def visitFunctionDecl(
            self,
            ctx: transpilerParser.FunctionDeclContext):
        func_name = ctx.ID().getText()
        return_type = self._get_type_definition(ctx.type_().getText(), True)

        if self.current_scope.has_symbol(func_name):
            raise DuplicateDefinitionError(
                func_name,
                line=self._get_current_line(),
                column=self._get_current_column(),
                filename=self.filename
            )

        if not self.config.enable_same_name_function_nesting:
            current = self.current_scope
            while current:
                if current.get_name() == func_name:
                    raise  # TODO
                current = current.parent

        params_list: list[Variable] = []
        params: transpilerParser.ParamListContext = ctx.paramList()
        if params.paramDecl():
            for param in params.paramDecl():
                param_name = param.ID().getText()
                param_type = self._get_type_definition(param.type_().getText())
                var = Variable(
                    param_name,
                    param_type,
                    VariableType.ARGUMENT
                )
                params_list.append(var)

        func = Function(
            func_name,
            params_list,
            return_type
        )

        if not self.current_scope.add_symbol(func):
            raise DuplicateDefinitionError(
                func_name,
                line=self._get_current_line(),
                column=self._get_current_column(),
                filename=self.filename
            )
        self._add_ir_instruction(IRFunction(func))

        with self.scoped_environment(func_name, StructureType.FUNCTION) as scope:
            for i in params_list:
                if not self.current_scope.add_symbol(i):
                    raise DuplicateDefinitionError(
                        i.get_name(),
                        line=self._get_current_line(),
                        column=self._get_current_column(),
                        filename=self.filename
                    )
                self._add_ir_instruction(IRDeclare(i))

            # 处理函数体
            self.visit(ctx.block())

        return Result(Reference(ValueType.FUNCTION, func))

    def visitMethodDecl(self, ctx: transpilerParser.MethodDeclContext):
        func_name = ctx.ID().getText()
        return_type = self._get_type_definition(ctx.type_().getText(), True)

        if self.current_scope.has_symbol(func_name):
            raise DuplicateDefinitionError(
                func_name,
                line=self._get_current_line(),
                column=self._get_current_column(),
                filename=self.filename
            )

        params_list: list[Variable] = []
        params: transpilerParser.ParamListContext = ctx.paramList()
        if params.paramDecl():
            for param in params.paramDecl():
                param_name = param.ID().getText()
                param_type = self._get_type_definition(param.type_().getText())
                var = Variable(
                    param_name,
                    param_type,
                    VariableType.ARGUMENT
                )
                params_list.append(var)

        func = Function(
            func_name,
            params_list,
            return_type,
            FunctionType.METHOD
        )

        if not self.current_scope.add_symbol(func):
            raise DuplicateDefinitionError(
                func_name,
                line=self._get_current_line(),
                column=self._get_current_column(),
                filename=self.filename
            )
        self._add_ir_instruction(IRFunction(func))

        with self.scoped_environment(func_name, StructureType.FUNCTION) as scope:
            for i in params_list:
                if not self.current_scope.add_symbol(i):
                    raise DuplicateDefinitionError(
                        i.get_name(),
                        line=self._get_current_line(),
                        column=self._get_current_column(),
                        filename=self.filename
                    )
                self._add_ir_instruction(IRDeclare(i))

            # 处理函数体
            self.visit(ctx.block())

        return Result(Reference(ValueType.FUNCTION, func))

    def visitClassDecl(
            self,
            ctx: transpilerParser.ClassDeclContext):
        class_name = ctx.ID().getText()
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
        constants: set[Reference[Constant]] = set()
        variables: list[Reference[Variable]] = []
        methods: list[Function] = []

        class_ = Class(class_name,
                       methods=methods,
                       interface=interface,
                       parent=parent,
                       constants=constants,
                       variables=variables)

        if not self.current_scope.add_symbol(class_):
            raise DuplicateDefinitionError(
                class_name,
                line=self._get_current_line(),
                column=self._get_current_column(),
                filename=self.filename
            )
        self._add_ir_instruction(IRClass(class_))

        with self.scoped_environment(class_name, StructureType.CLASS) as class_scope:
            # 处理继承
            if parent:
                raise MissingImplementationError(
                    "类继承",
                    line=self._get_current_line(),
                    column=self._get_current_column(),
                    filename=self.filename
                )  # TODO:处理继承

            # 处理字段和方法

            for const in ctx.constDecl():
                constants.add(self.visit(const).value)

            for var in ctx.varDecl():
                variables.append(self.visit(var).value)

            for method in ctx.methodDecl():
                methods.append(self.visit(method).value.value)

            if interface:
                current_interface = interface
                interfaces_method = []
                while interface:
                    interfaces_method += interface.methods
                    interface = interface.interface

                pending_implementation_methods = self.check_subset(interfaces_method, [m.get_name() for m in methods])
                if len(pending_implementation_methods[1])!=0:
                    raise # TODO:报错有接口的方法未实现

        return Result(Reference(ValueType.CLASS, class_))

    def visitInterfaceDecl(self, ctx: transpilerParser.InterfaceDeclContext):
        class_name = ctx.ID().getText()
        extends = self._get_type_definition(ctx.type_().getText())
        constants: set[Reference[Constant]] = set()
        variables: list[Reference[Variable]] = []
        methods: list[Function] = []

        class_ = Class(class_name,
                       methods=methods,
                       interface=None,
                       parent=extends,
                       constants=constants,
                       variables=variables,
                       type=ClassType.INTERFACE)

        if not self.current_scope.add_symbol(class_):
            raise DuplicateDefinitionError(
                class_name,
                line=self._get_current_line(),
                column=self._get_current_column(),
                filename=self.filename
            )
        self._add_ir_instruction(IRClass(class_))

        with self.scoped_environment(class_name, StructureType.CLASS) as class_scope:
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
                methods.append(self.visit(method).value.value)

        return Result(Reference(ValueType.CLASS, class_))

    # 处理代码块
    def visitBlock(self, ctx: transpilerParser.BlockContext):
        # 遍历子节点
        self.visitChildren(ctx)
        return Result(None)

    def visitLiteral(
            self,
            ctx: transpilerParser.LiteralContext):
        value = ctx.getText()
        if value == 'true' or value == 'false':
            return Result.from_literal(bool(value), DataType.BOOLEAN)
        elif value == 'null':
            return Result.from_literal(None, DataType.NULL)
        elif value[0] == 'f':

            return Result(self._process_fstring(value))
        elif self._is_number(value):
            return Result.from_literal(int(value), DataType.INT)
        else:
            return Result.from_literal(value[1:-1], DataType.STRING)

    def visitWhileStmt(
            self,
            ctx: transpilerParser.WhileStmtContext):
        loop_id = next(self.cnt)
        cond: transpilerParser.CompareExprContext = ctx.expr()
        with self.scoped_environment(f"while_{loop_id}_check", StructureType.LOOP_CHECK) as loop_check:
            with self.scoped_environment(f"while_{loop_id}_body", StructureType.LOOP_BODY) as loop_body:
                self.visit(ctx.block())
            # 评估条件表达式
            if not isinstance(cond, (transpilerParser.CompareExprContext, transpilerParser.LogicalOrExprContext,
                                     transpilerParser.LogicalAndExprContext, transpilerParser.LogicalNotExprContext)):
                raise InvalidSyntaxError(
                    ctx.expr().getText(),
                    line=self._get_current_line(),
                    column=self._get_current_column(),
                    filename=self.filename
                )

            # 从检查函数调用循环体
            condition_expr = self.visit(cond)
            condition_var = condition_expr.value

            self._add_ir_instruction(
                IRCondJump(
                    condition_var.value,
                    loop_body.name))
            self._add_ir_instruction(
                IRCondJump(
                    condition_var.value,
                    loop_check.name))
        self._add_ir_instruction(IRJump(loop_check.name))

    def visitForStmt(self, ctx: transpilerParser.ForStmtContext):
        for_control: transpilerParser.ForControlContext = ctx.forControl()
        if for_control:  # 传统for循环
            loop_id = next(self.cnt)
            with self.scoped_environment(f"for_{loop_id}", StructureType.LOOP) as loop:
                for_control_init: transpilerParser.ForLoopVarDeclContext = for_control.forLoopVarDecl()
                for_control_cond: transpilerParser.CompareExprContext = for_control.expr()
                # 处理初始化表达式
                if for_control_init:
                    self.visit(for_control_init)
                # 创建循环检查作用域
                with self.scoped_environment(f"for_{loop_id}_check", StructureType.LOOP_CHECK) as loop_check:

                    # 创建循环体作用域
                    with self.scoped_environment(f"for_{loop_id}_body", StructureType.LOOP_BODY) as loop_body:

                        # 处理循环体
                        self.visit(ctx.block())

                        # 处理更新表达式
                        if ctx.forControl().assignment():
                            self.visit(ctx.forControl().assignment())

                        # 添加返回检查的递归调用
                        self._add_ir_instruction(IRJump(loop_check.name))

                    # 评估条件表达式
                    if for_control_cond:
                        if isinstance(for_control_cond,
                                      (transpilerParser.CompareExprContext, transpilerParser.LogicalOrExprContext,
                                       transpilerParser.LogicalAndExprContext, transpilerParser.LogicalNotExprContext)):
                            # 从检查函数调用循环体
                            condition_expr = self.visit(for_control_cond)
                            condition_var = condition_expr.value
                        else:
                            raise InvalidSyntaxError(
                                ctx.expr().getText(),
                                line=self._get_current_line(),
                                column=self._get_current_column()
                            )
                    else:
                        condition_var = Reference(
                            ValueType.LITERAL, Literal(
                                DataType.BOOLEAN, True))
                    self._add_ir_instruction(
                        IRCondJump(
                            condition_var.value,
                            loop_body.name))
                    self._add_ir_instruction(
                        IRCondJump(
                            condition_var.value,
                            loop_check.name))
                self._add_ir_instruction(
                    IRJump(loop_check.name)
                )
            self._add_ir_instruction(IRJump(loop.name))
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
        if isinstance(  # 判断expr是否为CompareExpr
                ctx.expr(),
                (transpilerParser.CompareExprContext, transpilerParser.LogicalOrExprContext,
                 transpilerParser.LogicalAndExprContext, transpilerParser.LogicalNotExprContext)):
            # 计算条件表达式
            condition_expr = self.visit(ctx.expr())
        elif isinstance(
                ctx.expr(),
                transpilerParser.PrimaryExprContext):
            condition_expr = self.visit(ctx.expr())
            if condition_expr.value.get_data_type() != DataType.BOOLEAN:
                raise TypeMismatchError(
                    expected_type=DataType.BOOLEAN,
                    actual_type=condition_expr.value.get_data_type(),
                    line=self._get_current_line(),
                    column=self._get_current_column(),
                    filename=self.filename
                )
        else:
            raise InvalidSyntaxError(
                ctx.expr().getText(),
                line=self._get_current_line(),
                column=self._get_current_column(),
                filename=self.filename
            )

        # 创建if分支作用域
        with self.scoped_environment(f"if_{if_id}", StructureType.CONDITIONAL) as if_scope:
            self.visit(ctx.block(0))
        # 创建else分支作用域
        if ctx.block(1):
            with self.scoped_environment(f"else_{if_id}", StructureType.CONDITIONAL) as else_scope:
                self.visit(ctx.block(1))
            self._add_ir_instruction(
                IRCondJump(
                    condition_expr.value.value,
                    if_scope.name,
                    else_scope.name))
        else:
            self._add_ir_instruction(
                IRCondJump(
                    condition_expr.value.value,
                    if_scope.name))
        return Result(None)

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
        result_var_name = f"bool_{next(self.cnt)}"
        result_var = Variable(result_var_name,
                              DataType.BOOLEAN)
        self._add_ir_instruction(IRDeclare(result_var))
        self._add_ir_instruction(IRCompare(result_var, CompareOps(op), left, right))

        return Result(Reference(ValueType.VARIABLE, result_var))

    def visitLogicalAndExpr(self, ctx: transpilerParser.LogicalAndExprContext):
        left: Reference = self.visit(ctx.expr(0)).value
        right: Reference = self.visit(ctx.expr(1)).value

        if left.get_data_type() != DataType.BOOLEAN or right.get_data_type() != DataType.BOOLEAN:
            raise TypeMismatchError(
                DataType.BOOLEAN,
                left.get_data_type(),
                line=ctx.expr(0).start.line,
                column=ctx.expr(0).start.column,
                filename=self.filename
            )
        # 生成唯一结果变量
        result_var_name = f"bool_{next(self.cnt)}"
        result_var = Variable(result_var_name,
                              DataType.BOOLEAN)
        temp_var = Variable(uuid.uuid5(self.uuid_namespace, result_var_name).hex,
                            DataType.INT)

        self._add_ir_instruction(IRDeclare(temp_var))
        self._add_ir_instruction(IROp(temp_var, BinaryOps.MUL, left, right))
        self._add_ir_instruction(IRDeclare(result_var))
        self._add_ir_instruction(IRCompare(result_var, CompareOps.EQ, Reference(ValueType.VARIABLE, temp_var),
                                           Reference(ValueType.LITERAL, Literal(DataType.INT, 1))))
        return Result(Reference(ValueType.VARIABLE, result_var))

    def visitLogicalOrExpr(self, ctx: transpilerParser.LogicalOrExprContext):
        left: Reference = self.visit(ctx.expr(0)).value
        right: Reference = self.visit(ctx.expr(1)).value

        if left.get_data_type() != DataType.BOOLEAN or right.get_data_type() != DataType.BOOLEAN:
            raise TypeMismatchError(
                DataType.BOOLEAN,
                left.get_data_type(),
                line=ctx.expr(0).start.line,
                column=ctx.expr(0).start.column,
                filename=self.filename
            )
        # 生成唯一结果变量
        result_var_name = f"bool_{next(self.cnt)}"
        result_var = Variable(result_var_name,
                              DataType.BOOLEAN)
        temp_var = Variable(uuid.uuid5(self.uuid_namespace, result_var_name).hex,
                            DataType.INT)

        self._add_ir_instruction(IRDeclare(temp_var))
        self._add_ir_instruction(IROp(temp_var, BinaryOps.ADD, left, right))
        self._add_ir_instruction(IRDeclare(result_var))
        self._add_ir_instruction(IRCompare(result_var, CompareOps.LT,
                                           Reference(ValueType.LITERAL, Literal(DataType.INT, 0)),
                                           Reference(ValueType.VARIABLE, temp_var)))
        return Result(Reference(ValueType.VARIABLE, result_var))

    def visitVarExpr(
            self,
            ctx: transpilerParser.VarExprContext):
        var_name = ctx.ID().getText()
        try:
            symbol: NewSymbol = self.current_scope.resolve_symbol(var_name)
            if not isinstance(symbol, (Variable, Constant)):
                raise SymbolCategoryError(
                    f"符号 '{var_name}' 必须是变量或常量",
                    expected="Variable/Constant",
                    actual=symbol.__class__.__name__,
                    line=self._get_current_line(),
                    column=self._get_current_column(),
                    filename=self.filename
                )
        except ValueError:
            raise UndefinedVariableError(
                var_name,
                line=self._get_current_line(),
                column=self._get_current_column(),
                filename=self.filename
            )
        return Result(Reference(ValueType.VARIABLE, symbol))

    def visitAssignment(
            self,
            ctx: transpilerParser.AssignmentContext):
        var_name = ctx.ID().getText()
        expr_result = self.visit(ctx.expr())

        try:
            var: NewSymbol = self.current_scope.resolve_symbol(var_name)
            if isinstance(var, Constant):
                raise CompilerSyntaxError(
                    f"不能修改常量 '{var_name}'",
                    line=self._get_current_line(),
                    column=self._get_current_column(),
                    filename=self.filename
                )
            elif not isinstance(var, Variable):
                raise SymbolCategoryError(
                    f"符号 '{var_name}' 必须是变量才能赋值",
                    expected="Variable",
                    actual=var.__class__.__name__,
                    line=self._get_current_line(),
                    column=self._get_current_column(),
                    filename=self.filename
                )

            # 类型检查
            if var.dtype != expr_result.value.get_data_type():
                raise TypeMismatchError(
                    expected_type=var.dtype,
                    actual_type=expr_result.value.get_data_type(),
                    line=self._get_current_line(),
                    column=self._get_current_column(),
                    filename=self.filename
                )
        except ValueError:
            raise UndefinedVariableError(
                var_name,
                line=self._get_current_line(),
                column=self._get_current_column()
            )

        self._add_ir_instruction(IRAssign(var, expr_result.value))

        return Result(Reference(ValueType.VARIABLE, var))

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

    def visitTermExpr(
            self,
            ctx: transpilerParser.TermExprContext):
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
        self._add_ir_instruction(IROp(result_var, op, left.value, right.value))
        return Result(Reference(ValueType.VARIABLE, result_var))

    def visitDirectFuncCall(
            self,
            ctx: transpilerParser.DirectFuncCallContext):
        func_name: str = ctx.ID().getText()

        # 调用函数
        func_symbol: NewSymbol = self.current_scope.resolve_symbol(func_name)
        if isinstance(func_symbol, Function):
            if not self.config.enable_recursion:  # 未启用递归
                current = self.current_scope
                while current:
                    if current.get_name() == func_name and current.type == StructureType.FUNCTION and current.get_parent().find_symbol(
                            func_name) is func_symbol:
                        raise RecursionError(
                            f"函数 '{func_name}' 检测到递归调用，但递归支持未启用，启用递归请使用参数--enable-recursion",
                            line=self._get_current_line(),
                            column=self._get_current_column(),
                            filename=self.filename
                        )
                    current = current.parent

            args: list[Reference] = []
            if ctx.argumentList().exprList():
                for i, (arg_expr, param) in enumerate(
                        zip(ctx.argumentList().exprList().expr(), func_symbol.params)):
                    arg_result = self.visit(arg_expr)
                    args.append(arg_result.value)
                    if param.dtype != arg_result.value.get_data_type():
                        raise ArgumentTypeMismatchError(
                            param_name=param.name,
                            expected=param.dtype.name,
                            actual=arg_result.value.get_data_type().name,
                            line=arg_expr.start.line,
                            column=arg_expr.start.column,
                            filename=self.filename
                        )
                if len(ctx.argumentList().exprList().expr()) != len(func_symbol.params):
                    raise InvalidSyntaxError(
                        f"参数数量不匹配: 期望 {len(func_symbol.params)} 个参数，实际 {len(ctx.argumentList().exprList().expr())} 个",
                        line=self._get_current_line(),
                        column=self._get_current_column(),
                        filename=self.filename
                    )
            else:
                if len(func_symbol.params) != 0:
                    raise InvalidSyntaxError(
                        f"意外的实参",
                        line=self._get_current_line(),
                        column=self._get_current_column(),
                        filename=self.filename
                    )
            if func_symbol.function_type != FunctionType.BUILTIN:
                result_var = self._create_temp_var(func_symbol.return_type, "result")
                self._add_ir_instruction(IRDeclare(result_var))
                self._add_ir_instruction(IRCall(result_var, func_symbol, args))
            else:
                result_var = self.builtin_func_table[func_symbol.get_name()](*args)
        else:
            raise NotCallableError(
                func_name,
                func_symbol.__class__.__name__,
                line=self._get_current_line(),
                column=self._get_current_column(),
                filename=self.filename
            )

        return Result(Reference(ValueType.VARIABLE, result_var))

    def visitReturnStmt(
            self,
            ctx: transpilerParser.ReturnStmtContext):
        result_var = self.visit(ctx.expr()).value
        if isinstance(result_var.value, (Constant, Variable)):
            result_var.value.var_type = VariableType.RETURN
        self._add_ir_instruction(IRReturn(result_var))
        return Result(None)

    def visitIncludeStmt(
            self,
            ctx: transpilerParser.IncludeStmtContext):
        # TODO:更完善的错误处理
        include_path: Reference[Literal] = self.visit(ctx.literal()).value
        if include_path.get_data_type() != DataType.STRING:
            raise TypeMismatchError(DataType.STRING,
                                    include_path.get_data_type(),
                                    self._get_current_line(),
                                    self._get_current_column(),
                                    self.filename)
        include_path: str = include_path.value.value
        # 检查是否已经导入过
        if self.include_manager.has_imported(include_path):
            return Result(None)

        # 标记已导入
        self.include_manager.execute_import(include_path)

        # 处理导入的文件
        try:
            o_filename = self.filename
            self.filename = os.path.abspath(include_path)
            input_stream = FileStream(include_path, encoding='utf-8')
            lexer = transpilerLexer(input_stream)
            stream = CommonTokenStream(lexer)
            parser = transpilerParser(stream)
            tree = parser.program()

            # 访问并处理导入的文件
            self.visit(tree)
            self.filename = o_filename
        except Exception as e:
            raise CompilerImportError(
                include_path,
                e.__repr__(),
                line=self._get_current_line(),
                column=self._get_current_column(),
                filename=self.filename)

        return Result(None)

    def visitContinueStmt(self, ctx: transpilerParser.ContinueStmtContext):
        loop_scope_name = self._get_loop_check_scope_name()
        if loop_scope_name is None:
            raise InvalidControlFlowError(
                "break 语句只能在循环结构中使用",
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
