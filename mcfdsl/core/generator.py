# coding=utf-8
from __future__ import annotations

import os.path
import re
import uuid
from contextlib import contextmanager
from itertools import count

from antlr4 import FileStream, CommonTokenStream

from mcfdsl.core.DSLParser.McFuncDSLLexer import McFuncDSLLexer
from mcfdsl.core.DSLParser.McFuncDSLParser import McFuncDSLParser
from mcfdsl.core.DSLParser.McFuncDSLVisitor import McFuncDSLVisitor
from mcfdsl.core.errors import TypeMismatchError, UnexpectedError, CompilerSyntaxError, UndefinedTypeError, \
    CompilerImportError, UndefinedVariableError, InvalidSyntaxError, DuplicateDefinitionError, \
    ArgumentTypeMismatchError, InvalidControlFlowError, MissingImplementationError, RecursionError, NotCallableError
from mcfdsl.core.import_manager import ImportManager
from mcfdsl.core.ir.instructions import *
from mcfdsl.core.ir.ir_builder import IRBuilder
from mcfdsl.core.language_enums import StructureType, DataType, ValueType
from mcfdsl.core.result import Result
from mcfdsl.core.scope import Scope
from mcfdsl.core.symbols import *
from mcfdsl.test import print_all_attributes


class MCGenerator(McFuncDSLVisitor):
    _INT_PATTERN = re.compile(r'^[-+]?\d+$')

    def __init__(self, namespace: str = "mc_func_dsl"):
        self._current_ctx = None
        self.namespace = namespace
        self.top_scope = Scope(
            "global",
            None,
            StructureType.GLOBAL,
            self.namespace)
        self.current_scope = self.top_scope
        self.import_manager = ImportManager()  # 引用管理器
        self.uuid_namespace = uuid.uuid4()
        self.scope_stack = [self.top_scope]
        self.cnt = count()  # 保证for loop和if else唯一性
        self.filename = "<main>"
        self.ir_builder: IRBuilder = IRBuilder()

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

    def _is_in_loop(self) -> bool:
        current = self.current_scope
        while current:
            if current.type == StructureType.LOOP_BODY:
                return True
            elif current.type == StructureType.CONDITIONAL:
                current = current.parent
            else:
                break
        return False

    def get_generate_ir(self) -> IRBuilder:
        return self.ir_builder

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
            type_name: str) -> DataType | Class:
        """获取类型的具体定义（内置类型返回DataType，类返回Class实例）"""
        try:
            if builtin_type := DataType.get_by_value(type_name):
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

    def visit(self, tree) -> Result:
        self._current_ctx = tree
        result = tree.accept(self)
        if not isinstance(result, Result) and not isinstance(
                tree, McFuncDSLParser.ProgramContext):
            print_all_attributes(tree)
            raise UnexpectedError(f"意外的错误:result结果为{type(result)},需要{Result}")

        return result

    def visitCommandExpr(self, ctx: McFuncDSLParser.CommandExprContext):
        argument_list: McFuncDSLParser.ArgumentListContext = ctx.argumentList()
        expr_list: McFuncDSLParser.ExprListContext = argument_list.exprList()
        if expr_list:
            for i in expr_list.expr():
                expr = self.visit(i)
                # TODO:考虑未来改为标准库实现(exec)而非语法解析
                self._add_ir_instruction(IRRawCmd(expr.value))

        return Result.from_literal(None, DataType.NULL)

    # 处理变量声明
    def visitVarDeclaration(
            self,
            ctx: McFuncDSLParser.VarDeclarationContext):
        var_name = ctx.ID().getText()
        var_type = self._get_type_definition(ctx.type_().getText())
        var_value: Reference | None = None
        if ctx.expr():
            result = self.visit(ctx.expr())  # 处理初始化表达式
            # 类型推断
            if var_type == DataType.ANY:
                var_type = result.value.get_data_type()
            # 类型检查
            if var_type != result.value.get_data_type():
                raise TypeMismatchError(
                    expected_type=var_type,
                    actual_type=result.value.get_data_type(),
                    line=ctx.start.line,
                    column=ctx.start.column,
                    filename=self.filename
                )

            var_value = result.value

        else:  # 没有初始值
            if var_type == DataType.ANY:
                raise CompilerSyntaxError(
                    f"Variable '{var_name}' must be initialized as type cannot be inferred",
                    line=ctx.start.line,
                    column=ctx.start.column,
                    filename=self.filename
                )

        if not self._type_exists(var_type):  # 判断所给类型是否存在
            raise UndefinedTypeError(
                var_type.name,
                line=ctx.start.line,
                column=ctx.start.column
            )

        var = Variable(
            var_name,
            var_type,
        )

        self.current_scope.add_symbol(var)

        self._add_ir_instruction(IRDeclare(var))
        self._add_ir_instruction(IRAssign(var, var_value))

        return Result(Reference(ValueType.VARIABLE, var))

    def visitConstDecl(self, ctx: McFuncDSLParser.ConstDeclContext):
        name = ctx.ID().getText()
        dtype = self._get_type_definition(ctx.type_().getText())
        result = self.visit(ctx.expr())  # 处理初始化表达式
        # 类型推断
        if dtype == DataType.ANY:
            dtype = result.value.get_data_type()
        # 类型检查
        if dtype != result.value.get_data_type():
            raise TypeMismatchError(
                expected_type=dtype,
                actual_type=result.value.get_data_type(),
                line=ctx.start.line,
                column=ctx.start.column,
                filename=self.filename
            )

        value = result.value
        if not self._type_exists(dtype):  # 判断所给类型是否存在
            raise UndefinedTypeError(
                dtype.name,
                line=ctx.start.line,
                column=ctx.start.column
            )

        constant = Constant(
            name,
            dtype
        )

        self.current_scope.add_symbol(constant)

        self._add_ir_instruction(IRDeclare(constant))
        self._add_ir_instruction(IRAssign(constant, value))
        return Result(Reference(ValueType.CONSTANT, constant))

    # 处理函数定义
    def visitFunctionDecl(
            self,
            ctx: McFuncDSLParser.FunctionDeclContext):
        func_name = ctx.ID().getText()
        return_type = self._get_type_definition(ctx.type_().getText())

        if self.current_scope.has_symbol(func_name):
            raise DuplicateDefinitionError(
                func_name,
                line=ctx.start.line,
                column=ctx.start.column,
                filename=self.filename
            )

        params_list: list[Variable] = []
        params: McFuncDSLParser.ParamListContext = ctx.paramList()
        if params.paramDecl():
            for param in params.paramDecl():
                param_name = param.ID().getText()
                param_type = self._get_type_definition(param.type_().getText())
                params_list.append(
                    Variable(
                        param_name,
                        param_type
                    )
                )

        func = Function(
            func_name,
            params_list,
            return_type
        )
        self.current_scope.add_symbol(func)
        self._add_ir_instruction(IRFunction(func))

        with self.scoped_environment(func_name, StructureType.FUNCTION) as scope:
            for i in params_list:
                self.current_scope.add_symbol(i)

            # 处理函数体
            self.visit(ctx.block())

        return Result(Reference(ValueType.FUNCTION, func))

    # 处理代码块
    def visitBlock(self, ctx: McFuncDSLParser.BlockContext):
        # 遍历子节点
        self.visitChildren(ctx)
        return Result(None)

    def visitLiteral(
            self,
            ctx: McFuncDSLParser.LiteralContext):
        value = ctx.getText()
        if value == 'true' or value == 'false':
            return Result.from_literal(bool(value), DataType.BOOLEAN)
        elif value == 'null':
            return Result.from_literal(None, DataType.NULL)
        elif value[0] == 'f':
            temp_var = Variable(uuid.uuid4().hex, DataType.FSTRING)
            self._add_ir_instruction(IRDeclare(temp_var))
            self._add_ir_instruction(
                IRFstring(temp_var, Reference(ValueType.LITERAL, value[2:-1])))
            return Result(Reference(ValueType.VARIABLE, temp_var))
        elif self._is_number(value):
            return Result.from_literal(int(value), DataType.INT)
        else:
            return Result.from_literal(value[1:-1], DataType.STRING)

    def visitClassDecl(
            self,
            ctx: McFuncDSLParser.ClassDeclContext):
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
                       interfaces=interface,
                       parent=parent,
                       constants=constants,
                       variables=variables)

        self.current_scope.add_symbol(class_)
        with self.scoped_environment(class_name, StructureType.CLASS) as class_scope:
            # 处理继承
            if parent:
                raise MissingImplementationError(
                    "类继承",
                    line=ctx.start.line,
                    column=ctx.start.column,
                    filename=self.filename
                )  # TODO:处理继承

            if interface:
                raise MissingImplementationError(
                    "接口实现",
                    line=ctx.start.line,
                    column=ctx.start.column,
                    filename=self.filename
                )  # TODO:接口实现

            # 处理字段和方法

            for const in ctx.constDecl():
                constants.add(self.visit(const).value)

            for var in ctx.varDecl():
                variables.append(self.visit(var).value)

            for method in ctx.methodDecl():
                methods.append(self.visit(method).value.value)

        return Result(Reference(ValueType.CLASS, class_))

    def visitWhileStmt(
            self,
            ctx: McFuncDSLParser.WhileStmtContext):
        loop_id = next(self.cnt)
        cond: McFuncDSLParser.CompareExprContext = ctx.expr()
        with self.scoped_environment(f"while_{loop_id}_check", StructureType.LOOP_CHECK) as loop_check:
            with self.scoped_environment(f"while_{loop_id}_body", StructureType.LOOP_BODY) as loop_body:
                self.visit(ctx.block())
            # 评估条件表达式
            if not isinstance(cond, (McFuncDSLParser.CompareExprContext, McFuncDSLParser.LogicalOrExprContext,
                                     McFuncDSLParser.LogicalAndExprContext, McFuncDSLParser.LogicalNotExprContext)):
                raise InvalidSyntaxError(
                    ctx.expr().getText(),
                    line=ctx.start.line,
                    column=ctx.start.column,
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

    def visitForStmt(self, ctx: McFuncDSLParser.ForStmtContext):
        for_control: McFuncDSLParser.ForControlContext = ctx.forControl()
        if for_control:  # 传统for循环
            loop_id = next(self.cnt)
            with self.scoped_environment(f"for_{loop_id}", StructureType.LOOP) as loop:
                for_control_init: McFuncDSLParser.ForLoopVarDeclContext = for_control.forLoopVarDecl()
                for_control_cond: McFuncDSLParser.CompareExprContext = for_control.expr()
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
                                      (McFuncDSLParser.CompareExprContext, McFuncDSLParser.LogicalOrExprContext,
                                       McFuncDSLParser.LogicalAndExprContext, McFuncDSLParser.LogicalNotExprContext)):
                            # 从检查函数调用循环体
                            condition_expr = self.visit(for_control_cond)
                            condition_var = condition_expr.value
                        else:
                            raise InvalidSyntaxError(
                                ctx.expr().getText(),
                                line=ctx.start.line,
                                column=ctx.start.column
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

            self._add_ir_instruction(IRJump(loop.name))
        else:  # 增强for循环
            raise MissingImplementationError(
                "增强for循环",
                line=ctx.start.line,
                column=ctx.start.column,
                filename=self.filename
            )  # TODO:增强for循环实现
        return Result(None)

    def visitIfStmt(self, ctx: McFuncDSLParser.IfStmtContext):
        # 生成唯一ID
        if_id = next(self.cnt)
        condition_expr: Result | None = None
        if isinstance(  # 判断expr是否为CompareExpr
                ctx.expr(),
                (McFuncDSLParser.CompareExprContext, McFuncDSLParser.LogicalOrExprContext,
                 McFuncDSLParser.LogicalAndExprContext, McFuncDSLParser.LogicalNotExprContext)):
            # 计算条件表达式
            condition_expr = self.visit(ctx.expr())
        elif isinstance(
                ctx.expr(),
                McFuncDSLParser.PrimaryExprContext):
            condition_expr = self.visit(ctx.expr())
            if condition_expr.value.get_data_type() != DataType.BOOLEAN:
                raise TypeMismatchError(
                    expected_type=DataType.BOOLEAN,
                    actual_type=condition_expr.value.get_data_type(),
                    line=ctx.start.line,
                    column=ctx.start.column,
                    filename=self.filename
                )
        else:
            raise InvalidSyntaxError(
                ctx.expr().getText(),
                line=ctx.start.line,
                column=ctx.start.column,
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
                line=ctx.start.line,
                column=ctx.start.column,
                filename=self.filename
            )
        # 生成唯一结果变量
        result_var_name = f"bool_{next(self.cnt)}"
        result_var = Variable(result_var_name,
                              DataType.BOOLEAN)
        self._add_ir_instruction(IRDeclare(result_var))
        self._add_ir_instruction(IRCompare(result_var, CompareOps(op), left, right))

        return Result(Reference(ValueType.VARIABLE, result_var))

    def visitLogicalAndExpr(self, ctx: McFuncDSLParser.LogicalAndExprContext):
        left: Reference = self.visit(ctx.expr(0)).value
        right: Reference = self.visit(ctx.expr(1)).value

        if left.value_type not in (ValueType.VARIABLE, ValueType.CONSTANT) or right.value_type not in (
                ValueType.VARIABLE, ValueType.CONSTANT):
            raise TypeMismatchError(
                expected_type=DataType.BOOLEAN,
                actual_type=left.get_data_type() if left.value_type not in (ValueType.VARIABLE, ValueType.CONSTANT)
                else right.get_data_type(),
                line=ctx.expr(0).start.line,
                column=ctx.expr(0).start.column,
                filename=self.filename
            )
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

    def visitLogicalOrExpr(self, ctx: McFuncDSLParser.LogicalOrExprContext):
        left: Reference = self.visit(ctx.expr(0)).value
        right: Reference = self.visit(ctx.expr(1)).value

        if left.value_type not in (ValueType.VARIABLE, ValueType.CONSTANT) or right.value_type not in (
                ValueType.VARIABLE, ValueType.CONSTANT):
            raise TypeMismatchError(
                expected_type=DataType.BOOLEAN,
                actual_type=left.get_data_type() if left.value_type not in (ValueType.VARIABLE, ValueType.CONSTANT)
                else right.get_data_type(),
                line=ctx.expr(0).start.line,
                column=ctx.expr(0).start.column,
                filename=self.filename
            )
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
            ctx: McFuncDSLParser.VarExprContext):
        var_name = ctx.ID().getText()
        try:
            symbol: NewSymbol = self.current_scope.resolve_symbol(var_name)
            if not isinstance(symbol, (Variable, Constant)):
                raise UnexpectedError(
                    f"符号 '{var_name}' 不是变量或常量",
                    line=ctx.start.line,
                    column=ctx.start.column,
                    filename=self.filename
                )
        except ValueError:
            raise UndefinedVariableError(
                var_name,
                line=ctx.start.line,
                column=ctx.start.column,
                filename=self.filename
            )
        return Result(Reference(ValueType.VARIABLE, symbol))

    def visitAssignment(
            self,
            ctx: McFuncDSLParser.AssignmentContext):
        var_name = ctx.ID().getText()
        expr_result = self.visit(ctx.expr())

        try:
            var: NewSymbol = self.current_scope.resolve_symbol(var_name)
            if isinstance(var, Constant):
                raise CompilerSyntaxError(
                    f"不能修改常量 '{var_name}'",
                    line=ctx.start.line,
                    column=ctx.start.column,
                    filename=self.filename
                )
            elif not isinstance(var, Variable):
                raise UnexpectedError(
                    f"符号 '{var_name}' 不是变量",
                    line=ctx.start.line,
                    column=ctx.start.column,
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
                line=ctx.start.line,
                column=ctx.start.column
            )

        self._add_ir_instruction(IRAssign(var, expr_result.value))

        return Result(Reference(ValueType.VARIABLE, var))

    def visitMulDivExpr(self, ctx: McFuncDSLParser.MulDivExprContext):
        left = self.visit(ctx.expr(0))
        right = self.visit(ctx.expr(1))
        op = ctx.getChild(1).getText()

        # 生成唯一结果变量
        result_name = f"calc_{next(self.cnt)}"
        result_var = Variable(result_name,
                              left.value.get_data_type() or right.value.get_data_type())

        self._add_ir_instruction(IRDeclare(result_var))
        self._add_ir_instruction(IROp(result_var, BinaryOps(op), left.value, right.value))
        return Result(Reference(ValueType.VARIABLE, result_var))

    def visitAddSubExpr(
            self,
            ctx: McFuncDSLParser.AddSubExprContext):
        left = self.visit(ctx.expr(0))
        right = self.visit(ctx.expr(1))
        op = ctx.getChild(1).getText()

        # 生成唯一结果变量
        result_name = f"calc_{next(self.cnt)}"
        result_var = Variable(result_name,
                              left.value.get_data_type() or right.value.get_data_type())

        self._add_ir_instruction(IRDeclare(result_var))
        self._add_ir_instruction(IROp(result_var, BinaryOps(op), left.value, right.value))
        return Result(Reference(ValueType.VARIABLE, result_var))

    def visitDirectFuncCall(
            self,
            ctx: McFuncDSLParser.DirectFuncCallContext):
        func_name = ctx.ID().getText()

        # 调用函数
        result_name = f"result_{next(self.cnt)}"

        func_symbol: NewSymbol = self.current_scope.resolve_symbol(func_name)
        if isinstance(func_symbol, Function):
            result_var = Variable(result_name, func_symbol.return_type)

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
                if  len(ctx.argumentList().exprList().expr()) != len(func_symbol.params):
                    raise InvalidSyntaxError(
                        f"参数数量不匹配: 期望 {len(func_symbol.params)} 个参数，实际 {len(ctx.argumentList().exprList().expr())} 个",
                        line=ctx.start.line,
                        column=ctx.start.column,
                        filename=self.filename
                    )
            else:
                if len(func_symbol.params) != 0:
                    raise InvalidSyntaxError(
                        f"意外的实参",
                        line=ctx.start.line,
                        column=ctx.start.column,
                        filename=self.filename
                    )
            self._add_ir_instruction(IRCall(result_var, func_symbol, args))
        else:
            raise NotCallableError(
                func_name,
                func_symbol.__class__.__name__,
                line=ctx.start.line,
                column=ctx.start.column,
                filename=self.filename
            )

        return Result(Reference(ValueType.VARIABLE, result_var))

    def visitReturnStmt(
            self,
            ctx: McFuncDSLParser.ReturnStmtContext):
        result_var = self.visit(ctx.expr()).value
        self._add_ir_instruction(IRReturn(result_var))
        return Result(None)

    def visitIncludeStmt(
            self,
            ctx: McFuncDSLParser.IncludeStmtContext):

        import_path: Reference[Literal] = self.visit(ctx.literal()).value
        if import_path.get_data_type() != DataType.STRING:
            raise TypeMismatchError(DataType.STRING,
                                    import_path.get_data_type(),
                                    self._get_current_line(),
                                    self._get_current_column(),
                                    self.filename)
        import_path: str = import_path.value.value
        # 检查是否已经导入过
        if self.import_manager.has_imported(import_path):
            return Result(None)

        # 标记已导入
        self.import_manager.execute_import(import_path)

        # 处理导入的文件
        try:
            o_filename = self.filename
            self.filename = os.path.abspath(import_path)
            input_stream = FileStream(import_path, encoding='utf-8')
            lexer = McFuncDSLLexer(input_stream)
            stream = CommonTokenStream(lexer)
            parser = McFuncDSLParser(stream)
            tree = parser.program()

            # 访问并处理导入的文件
            self.visit(tree)
            self.filename = o_filename
        except Exception as e:
            raise CompilerImportError(
                import_path,
                e.__repr__(),
                line=self._get_current_line(),
                column=self._get_current_column(),
                filename=self.filename)

        return Result(None)

    def visitContinueStmt(self, ctx: McFuncDSLParser.ContinueStmtContext):
        if not self._is_in_loop():
            raise InvalidControlFlowError(
                "break 语句只能在循环结构中使用",
                line=ctx.start.line,
                column=ctx.start.column,
                filename=self.filename
            )
        self._add_ir_instruction(IRContinue())
        return Result(None)

    def visitBreakStmt(self, ctx: McFuncDSLParser.ContinueStmtContext):
        if not self._is_in_loop():
            raise InvalidControlFlowError(
                "break 语句只能在循环结构中使用",
                line=ctx.start.line,
                column=ctx.start.column,
                filename=self.filename
            )
        self._add_ir_instruction(IRBreak())
        return Result(None)
