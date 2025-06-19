from __future__ import annotations

import os
import re
import uuid

from antlr4 import FileStream, CommonTokenStream

from mcfdsl.McFuncDSLParser import McFuncDSLParser, McFuncDSLLexer
from mcfdsl.McFuncDSLParser.McFuncDSLVisitor import McFuncDSLVisitor
from mcfdsl.core._interfaces import IScope, ISymbol
from mcfdsl.core.class_ import Class
from mcfdsl.core.command_builder._execute import Execute
from mcfdsl.core.command_builder._scoreboard import Scoreboard
from mcfdsl.core.command_builder.base import BasicCommands
from mcfdsl.core.command_builder.composite import Composite
from mcfdsl.core.errors import TypeMismatchError, UnexpectedError, CompilerSyntaxError
from mcfdsl.core.import_manager import ImportManager
from mcfdsl.core.language_types import SymbolType, StructureType, DataType, ValueType
from mcfdsl.core.result import Result
from mcfdsl.core.scope import Scope
from mcfdsl.core.symbol import Symbol
from mcfdsl.core.utils.type_utils import TypeUtils
from mcfdsl.test import print_all_attributes


class MCGenerator(McFuncDSLVisitor):
    _INT_PATTERN = re.compile(r'^[-+]?\d+$')

    def __init__(self, namespace: str = "mc_func_dsl"):
        self.namespace = namespace
        self.top_scope = Scope(
            "global",
            None,
            StructureType.GLOBAL,
            self.namespace)
        self.current_scope = self.top_scope
        self.import_manager = ImportManager()  # 引用管理器
        self.scope_stack = [self.top_scope]
        self.cnt = 0  # 保证for loop和if else唯一性
        self.uuid_namespace = uuid.uuid4()
        self.var_objective = "var"
        self.loop_objective = "loop"
        self.return_objective = "return"
        self._add_command(BasicCommands.comment("Scoreboard initialization"))
        self._add_command(
            Scoreboard.add_objective(
                self.var_objective,
                "dummy",
                "Variables"))
        self._add_command(
            Scoreboard.add_objective(
                self.loop_objective,
                "dummy",
                "Loop Counters"))
        self._add_command(
            Scoreboard.add_objective(
                self.return_objective,
                "dummy",
                "Function Returns"))

    def visit(self, tree) -> Result:
        result = tree.accept(self)
        if not isinstance(result, Result) and not isinstance(
                tree, McFuncDSLParser.McFuncDSLParser.ProgramContext):
            print_all_attributes(tree)
            raise UnexpectedError(f"意外的错误:result结果为{type(result)},需要{Result}")

        return result

    # 作用域管理辅助方法
    def _enter_scope(self, name: str, scope_type: StructureType):
        new_scope = self.current_scope.create_child(name, scope_type)
        self.current_scope = new_scope
        self.scope_stack.append(new_scope)
        if len(self.scope_stack) > 1000:
            for i in self.scope_stack:
                print(f"at {i.name}, in {i.parent.name}")
            raise RecursionError("maximum recursion depth exceeded")

        return new_scope

    def _exit_scope(self):
        if self.current_scope.is_exist_parent():
            self.current_scope = self.current_scope.get_parent()
            self.scope_stack.pop()

    def _process_fstring(self, text: str) -> str:
        """
        安全替换字符串中的 ${...} 占位符
        特性：

        1. 自动处理转义（$$ → $）
        2. 支持多级路径（user.name）
        """
        # 先处理转义符 $$
        processed_text = re.sub(r'\$\$', '\x00', text)  # 临时替换

        # 定义替换逻辑
        def replacer(match):
            key = match.group(1)
            try:
                if '.' not in key:
                    symbol = self.current_scope.resolve_symbol(key)
                    if symbol.value is not None and (
                            symbol.symbol_type == SymbolType.VARIABLE or symbol.symbol_type == SymbolType.CONSTANT):
                        return symbol.value
                    else:
                        raise NameError(
                            f"{symbol.name} has not been assigned a value, or cannot resolve its value")
                else:
                    raise NameError(
                        "fstring does not support non-constant results")
            except (KeyError, TypeError):
                return f'${{{key}}}'  # 保留原占位符

        # 执行替换
        result = re.sub(r'\$\{([^}]+)}', replacer, processed_text)
        # 恢复转义符
        return result.replace('\x00', '$')

    def _add_command(self, cmds: str | list[str], scope: IScope | None = None):
        if scope is None:
            scope = self.current_scope
        if isinstance(cmds, str):
            cmds = [cmds]
        for cmd in cmds:
            if cmd is None:
                raise UnexpectedError(f"试图添加一条为None的指令")
            scope.commands.append(cmd)

    def _generate_commands(self):
        """遍历作用域树生成文件"""
        output_dir = "target"
        stack: list[IScope] = [self.top_scope]

        while stack:
            current: IScope = stack.pop()
            if current.commands:
                path = os.path.join(output_dir, current.get_file_path())
                os.makedirs(os.path.dirname(path), exist_ok=True)
                with open(path, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(current.commands))
            stack.extend(reversed(current.children))

    # 检查类型是否存在
    def _type_exists(self, type_):
        if isinstance(type_, DataType):
            return True
        try:
            resolve_symbol_result = self.current_scope.resolve_symbol(type_)
            if resolve_symbol_result.symbol_type == SymbolType.CLASS:
                return True
        except NameError:
            return False
        return False

    def _is_number(self, s):
        return bool(self._INT_PATTERN.match(s))

    def visitCmdExpr(
            self,
            ctx: McFuncDSLParser.McFuncDSLParser.CmdExprContext):

        fstring = ctx.FSTRING().getText()[2:-1]  # 去掉f""
        command = self._process_fstring(fstring)
        self._add_command(scope=None, cmds=command)
        return Result.from_literal(command, DataType.STRING)

    def visitCmdBlockExpr(
            self,
            ctx: McFuncDSLParser.McFuncDSLParser.CmdBlockExprContext):
        command = []
        for fstring in ctx.FSTRING():
            fstring = fstring.getText()[2:-1]
            command += self._process_fstring(fstring)
            self._add_command(scope=None, cmds=command[-1])
        return Result.from_literal("\n".join(command), DataType.STRING)

    # 处理变量声明
    def visitVarDeclaration(
            self,
            ctx: McFuncDSLParser.McFuncDSLParser.VarDeclarationContext):
        var_name = ctx.ID().getText()
        try:
            var_type: DataType = DataType(
                ctx.type_().getText()) if ctx.type_() else DataType.ANY
        except ValueError:
            try:
                type_symbol = self.current_scope.resolve_symbol(ctx.type_().getText())
            except NameError:
                raise TypeMismatchError(f"不存在的类型{ctx.type_().getText()}")

            if type_symbol.symbol_type == SymbolType.CLASS:
                var_type: Class = type_symbol.value  # TODO:实现class的实例定义
            else:
                raise TypeMismatchError(f"不存在的类型{ctx.type_().getText()}")

        result: Result | None = None
        result_type: DataType | None = None
        # 创建符号
        symbol: Symbol = Symbol(
            var_name,
            SymbolType.VARIABLE,
            self.current_scope,
            var_type,
            self.var_objective)

        if ctx.expr():
            result = self.visit(ctx.expr())  # 处理初始化表达式
            result_type = result.data_type

            if var_type == DataType.ANY:
                var_type = result.data_type
                symbol.data_type = var_type

            if var_type != result.data_type:
                raise TypeMismatchError(f"需要{var_type}却设置了{result.data_type}")

            elif result.value_type == ValueType.VARIABLE:
                if result.value:
                    symbol.value = result.value
                symbol.value_type = ValueType.VARIABLE
            elif result.value_type == ValueType.LITERAL:
                symbol.value = result.value
                symbol.value_type = ValueType.LITERAL

            self._add_command(BasicCommands.comment(f"变量{var_name}:{var_type}初始化值: {symbol.value}"))
            print(f"变量{var_name}:{var_type}初始化值: {symbol.value}")
            print_all_attributes(symbol)
        else:  # 没有初始值
            if var_type == DataType.ANY:
                raise TypeMismatchError(
                    f"Variable '{var_name}' must be initialized as type cannot be inferred")

        if not self._type_exists(var_type):
            raise TypeMismatchError(f"The type {var_type} does not exist.")

        self.current_scope.add_symbol(symbol)

        if result:
            cmd = Composite.var_assignment(symbol, result)
            if cmd is None:
                raise CompilerSyntaxError(f"未知的赋值操作")
            self._add_command(cmd,
                              self.current_scope)

        return Result.from_variable(symbol)

    # 处理函数定义
    def visitFunctionDecl(
            self,
            ctx: McFuncDSLParser.McFuncDSLParser.FunctionDeclContext):
        func_name = ctx.ID().getText()
        return_type = ctx.type_().getText()
        symbol = Symbol(
            func_name,
            SymbolType.FUNCTION,
            self.current_scope,
            DataType(return_type),  # TODO: 实现返回值系统
            None,
            None,
            ValueType.OTHER)
        self.current_scope.add_symbol(symbol)
        scope = self._enter_scope(func_name, StructureType.FUNCTION)

        # 处理参数
        params: McFuncDSLParser.McFuncDSLParser.ParamListContext = ctx.paramList()
        if params.paramDecl():
            for param in params.paramDecl():
                param_name = param.ID().getText()
                param_type = param.type_().getText()
                self.current_scope.add_symbol(
                    Symbol(
                        param_name,
                        SymbolType.VARIABLE,
                        self.current_scope,
                        param_type,
                        self.var_objective))

        # 处理函数体
        self.visit(ctx.block())

        self._exit_scope()
        symbol.value = scope
        return Result(ValueType.OTHER, DataType.ANY, symbol, False)

    # 处理代码块
    def visitBlock(self, ctx: McFuncDSLParser.McFuncDSLParser.BlockContext):
        # 遍历子节点
        self.visitChildren(ctx)
        return Result(
            ValueType.VARIABLE,
            DataType.ANY,
            self.current_scope,
            False)

    def visitLiteral(
            self,
            ctx: McFuncDSLParser.McFuncDSLParser.LiteralContext):
        value = ctx.getText()
        if value == 'true':
            return Result.from_literal(True, DataType.BOOLEAN)
        elif value == 'false':
            return Result.from_literal(False, DataType.BOOLEAN)
        elif value[0] == 'f':
            return Result.from_literal(
                self._process_fstring(value[2:-1]), DataType.FSTRING)
        elif self._is_number(value):
            return Result.from_literal(int(value), DataType.INT)
        else:
            return Result.from_literal(value[1:-1], DataType.STRING)

    def visitClassDecl(
            self,
            ctx: McFuncDSLParser.McFuncDSLParser.ClassDeclContext):
        class_name = ctx.ID().getText()
        class_scope = self._enter_scope(class_name, StructureType.CLASS)
        interfaces: McFuncDSLParser.McFuncDSLParser.TypeListContext = ctx.typeList()
        class_symbol = Symbol(
            class_name,
            SymbolType.CLASS,
            self.current_scope,
            None,
            None,
            None,
            ValueType.OTHER)
        class_scope.add_symbol(class_symbol)
        class_symbol.value = Class(
            methods=[
                method.ID() for method in ctx.methodDecl()],
            constructor=ctx.constructorDecl(),
            interfaces=interfaces.type_(),
            scope=class_scope,
            consts=[
                const.ID() for const in ctx.constDecl()])
        # 处理继承
        if ctx.type_():
            base_class = ctx.type_().getText()
            base_class_symbol = class_scope.resolve_symbol(base_class)
            if base_class_symbol is None or base_class_symbol.symbol_type != SymbolType.CLASS:
                raise NameError(f"基类 {base_class} 未定义")
            # TODO:处理继承

        if interfaces.type_():  # TODO:接口实现
            pass

        # 处理字段和方法
        for member in ctx.varDecl() + ctx.constDecl() + \
                      ctx.methodDecl() + ctx.constructorDecl():
            self.visit(member)

        self._exit_scope()
        return Result(ValueType.OTHER, DataType.ANY, class_symbol, False)

    def visitForStmt(self, ctx: McFuncDSLParser.McFuncDSLParser.ForStmtContext):  # TODO:需修改
        if ctx.forControl():  # 传统for循环
            loop_id = self.cnt
            self.cnt += 1

            # 处理初始化表达式
            if ctx.forControl().forLoopVarDecl():
                self.visit(ctx.forControl().forLoopVarDecl())

            # 创建循环检查作用域
            check_scope = self._enter_scope(
                f"for_{loop_id}_check", StructureType.FUNCTION)

            # 评估条件表达式
            condition_expr = self.visit(ctx.forControl().expr(0))
            condition_var = condition_expr.value
            # TODO: return 必须特殊处理！
            # 条件检查 - 如果条件为假则返回
            self._add_command(
                f"execute unless score {condition_var} var matches 1 run return",
                check_scope)

            # 创建循环体作用域
            body_scope = self._enter_scope(
                f"for_{loop_id}_body", StructureType.LOOP)

            # 访问循环体
            self.visit(ctx.block())

            # 处理更新表达式
            if ctx.forControl().assignment():
                self.visit(ctx.forControl().assignment())
            elif len(ctx.forControl().expr()) > 1:
                self.visit(ctx.forControl().expr(1))

            # 添加返回检查的递归调用
            self._add_command(
                f"function {check_scope.get_minecraft_function_path()}",
                body_scope)

            # 从检查函数调用循环体
            self._add_command(
                f"function {body_scope.get_minecraft_function_path()}",
                check_scope)

            self._exit_scope()  # 退出body作用域
            self._exit_scope()  # 退出check作用域

            # 在当前作用域中调用检查函数开始循环
            self._add_command(
                f"function {check_scope.get_minecraft_function_path()}",
                self.current_scope)

        else:  # 增强for循环
            selector: Result = self.visit(ctx.expr())
            if selector.data_type != DataType.SELECTOR:
                raise TypeError(
                    f"增强for循环需要{DataType.SELECTOR}而不是{selector.data_type}")

            self._enter_scope(str(self.cnt), StructureType.LOOP)
            block: Result = self.visit(ctx.block())
            self._exit_scope()
            # 在主作用域添加初始化+首次调用
            self._add_command(
                Execute.execute().
                as_(selector.value).
                run(f"function {block.value.get_minecraft_function_path()}"),
                self.current_scope)
        return Result(ValueType.OTHER, DataType.ANY, None)

    # 选择器生成
    def visitNewSelectorExpr(
            self,
            ctx: McFuncDSLParser.McFuncDSLParser.NewSelectorExprContext):
        selector_args = ctx.STRING().getText()[1:-1]

        # 支持更复杂的选择器参数解析
        selector_predicates = []
        for pred in selector_args.split(','):
            pred = pred.strip()
            if '=' in pred:
                key, value = pred.split('=')
                selector_predicates.append(f"{key}={value}")

        # 构建更灵活的选择器
        final_selector = f"@e[{','.join(selector_predicates)}]"

        return Result.from_literal(final_selector, DataType.SELECTOR)

    def visitIfStmt(self, ctx: McFuncDSLParser.McFuncDSLParser.IfStmtContext):
        # 生成唯一ID
        if_id = self.cnt
        self.cnt += 1

        # 判断expr是否为CompareExpr
        if not isinstance(ctx.expr(), McFuncDSLParser.McFuncDSLParser.CompareExprContext):
            raise CompilerSyntaxError(f"expr 需要为 CompareExpr")

        # 计算条件表达式
        condition_expr: Result = self.visit(ctx.expr())
        if condition_expr.value_type == ValueType.VARIABLE:
            condition_var: ISymbol = condition_expr.value
            # 创建if分支作用域
            if_scope: Scope = self._enter_scope(
                f"if_{if_id}", StructureType.FUNCTION)
            self.visit(ctx.block(0))
            self._exit_scope()

            self._add_command(BasicCommands.comment(f"创建if分支{if_scope.name}"))

            # 处理else分支(如果存在)
            if len(ctx.block()) > 1:
                # 创建else分支作用域
                else_scope: Scope = self._enter_scope(
                    f"else_{if_id}", StructureType.FUNCTION)
                self.visit(ctx.block(1))
                self._exit_scope()

                self._add_command(BasicCommands.comment(f"创建else分支{else_scope.name}"))

                # 根据条件执行不同分支
                self._add_command(
                    Execute.execute().if_score_matches(condition_var.get_unique_name(), condition_var.objective,
                                                       "1").run(f"function {if_scope.get_minecraft_function_path()}"),
                    self.current_scope)
                self._add_command(
                    Execute.execute().unless_score_matches(condition_var.get_unique_name(), condition_var.objective,
                                                           "1").run(
                        f"function {else_scope.get_minecraft_function_path()}"), self.current_scope)
            else:
                # 只有if分支的情况
                self._add_command(
                    Execute.execute().if_score_matches(condition_var.get_unique_name(), condition_var.objective,
                                                       "1").run(f"function {if_scope.get_minecraft_function_path()}"),
                    self.current_scope)
        elif condition_expr.value_type == ValueType.LITERAL:
            if condition_expr.data_type == DataType.BOOLEAN or condition_expr.data_type == DataType.INT:
                if int(condition_expr.value) == 1:
                    self.visit(ctx.block(0))
                elif int(condition_expr.value) == 0 and len(ctx.block()) > 1:  # 如果存在else分支
                    self.visit(ctx.block(1))
                else:
                    assert "奇奇怪怪的东西又增加了"
            else:
                raise CompilerSyntaxError(f"不支持的类型{condition_expr.data_type}")
        else:
            assert "不是哥们，怎么什么鬼东西都能传进来啊"
        return Result(ValueType.OTHER, DataType.ANY, None)

    # 在visitCompareExpr中生成比较指令
    def visitCompareExpr(self, ctx):
        left = self.visit(ctx.expr(0))
        right = self.visit(ctx.expr(1))
        op = ctx.getChild(1).getText()

        # 生成唯一结果变量
        result_var_name = f"bool_{self.cnt}"
        result_var = Symbol(result_var_name, SymbolType.VARIABLE, self.current_scope, DataType.BOOLEAN,
                            self.var_objective, False, ValueType.LITERAL)
        self.cnt += 1

        # 初始化结果为假(0)
        self._add_command(
            f"scoreboard players set {result_var_name} var 0",
            self.current_scope)

        self._add_command(Composite.var_compare(left, op, right, result_var))
        return Result(ValueType.VARIABLE, DataType.BOOLEAN, result_var, False)

    def visitVarExpr(
            self,
            ctx: McFuncDSLParser.McFuncDSLParser.VarExprContext):
        var_name = ctx.ID().getText()
        symbol = self.current_scope.resolve_symbol(var_name)
        return Result.from_variable(
            symbol
        )

    def visitAssignment(
            self,
            ctx: McFuncDSLParser.McFuncDSLParser.AssignmentContext):
        var_name = ctx.ID().getText()
        expr_result = self.visit(ctx.expr())

        try:
            symbol = self.current_scope.resolve_symbol(var_name)
        except NameError:
            raise NameError(f"变量 '{var_name}' 未定义")

        # 正确的类型检查
        expr_result_type = TypeUtils.infer(expr_result.value)

        if symbol.data_type != expr_result_type:
            raise TypeMismatchError(
                f"错误的类型，需要{symbol.data_type},实际为{expr_result_type}")

        cmd = Composite.var_assignment(symbol, expr_result)
        if cmd is None:
            raise CompilerSyntaxError(f"未知的赋值操作")
        self._add_command(cmd,
                          self.current_scope)

        # 更新符号表中的值
        symbol.value = expr_result.value

        return Result.from_variable(symbol)

    def visitAddSubExpr(self, ctx: McFuncDSLParser.McFuncDSLParser.AddSubExprContext):
        left = self.visit(ctx.expr(0))
        right = self.visit(ctx.expr(1))
        op = ctx.getChild(1).getText()

        # 生成唯一结果变量
        result_name = f"calc_{self.cnt}"
        result_var = Symbol(result_name, SymbolType.VARIABLE, None, DataType.INT,
                            self.var_objective)  # TODO:根据具体类型实现而非INT
        self.cnt += 1

        # 处理变量与变量的运算
        if left.value_type == ValueType.VARIABLE and right.value_type == ValueType.VARIABLE:
            assert isinstance(left.value, ISymbol)
            assert isinstance(right.value, ISymbol)
            # 两个变量相加减
            self._add_command(
                Scoreboard.set_op(result_var.get_unique_name(), result_var.objective, left.value.get_unique_name(),
                                  left.value.objective))
            if op == '+':
                self._add_command(
                    Scoreboard.add_op(result_var.get_unique_name(), result_var.objective, right.value.get_unique_name(),
                                      right.value.objective))
            else:  # '-'
                self._add_command(
                    Scoreboard.sub_op(result_var.get_unique_name(), result_var.objective, right.value.get_unique_name(),
                                      right.value.objective))
            result_var.value_type = ValueType.VARIABLE
            return Result.from_variable(result_var)

        # 处理常量与常量的运算
        elif left.value_type == ValueType.LITERAL and right.value_type == ValueType.LITERAL:
            value = left.value

            if op == '+':
                value += right.value
            else:  # '-'
                value -= right.value
            self._add_command(
                Scoreboard.set_score(result_var.get_unique_name(), result_var.objective, value))
            result_var.value_type = ValueType.LITERAL
            return Result.from_literal(value, DataType.INT)

        # 处理变量与常量的运算
        else:
            if left.value_type == ValueType.LITERAL:
                left, right = right, left  # 直接交换

            self._add_command(
                Scoreboard.set_op(result_var.get_unique_name(), result_var.objective, left.value.get_unique_name(),
                                  left.value.objective))

            if op == '+':
                self._add_command(Scoreboard.add_score(result_var.get_unique_name(), result_var.objective, right.value))
            else:  # '-'
                self._add_command(Scoreboard.sub_score(result_var.get_unique_name(), result_var.objective, right.value))
            result_var.value_type = ValueType.VARIABLE
            return Result.from_variable(result_var)

    def visitDirectFuncCall(self, ctx: McFuncDSLParser.McFuncDSLParser.DirectFuncCallContext):
        func_name = ctx.ID()

        # 处理参数
        args = []
        if ctx.argumentList().exprList():
            for arg_expr in ctx.argumentList().exprList():
                args.append(self.visit(arg_expr))

        # 生成参数传递命令
        for i, arg in enumerate(args):
            pass  # TODO:生成参数传递命令
            """
            if arg.type_ == ValueType.VARIABLE:
                self._add_command(
                    f"scoreboard players operation arg{i} var = {arg.value} var", self.current_scope)
            else:
                value = arg.value
                if arg.type_ == DataType.BOOLEAN:
                    value = 1 if value else 0
                self._add_command(
                    f"scoreboard players set arg{i} var {value}",
                    self.current_scope)"""

        # 调用函数
        result_name = f"result_{self.cnt}"
        self.cnt += 1

        func_symbol = self.current_scope.resolve_symbol(func_name)
        assert isinstance(func_symbol.value, IScope)
        result_var = Symbol(result_name, SymbolType.VARIABLE, self.current_scope, func_symbol.data_type,
                            self.return_objective, None,
                            ValueType.VARIABLE)
        if func_symbol.symbol_type != SymbolType.FUNCTION:
            return TypeMismatchError(f"找不到函数{func_name}")
        self._add_command(
            f"function {func_symbol.value.get_minecraft_function_path()}",
            self.current_scope)

        # TODO:实现返回值系统
        self._add_command(
            f"# scoreboard players operation {result_name} var = return var",
            self.current_scope)

        return Result.from_variable(result_var)

    def visitWhileStmt(self, ctx):
        raise CompilerSyntaxError("while暂未实现，请使用for")

    def visitReturnStmt(self, ctx):
        if ctx.expr():
            expr = self.visit(ctx.expr())
            # TODO:使用更好的方法处理返回result来使调用处正常处理
            result = Symbol(f"return_{uuid.uuid5(self.uuid_namespce, self.current_scope.name)}", SymbolType.VARIABLE,None,
                            expr.data_type, self.return_objective, None, ValueType.VARIABLE)
            self._add_command(Composite.var_assignment(result, expr))
            self._add_command("return", self.current_scope)
            return Result.from_variable(result)

        # 结束函数执行
        self._add_command("return", self.current_scope)
        return Result.from_literal(None, DataType.VOID)

    def visitImportStmt(self, ctx: McFuncDSLParser.McFuncDSLParser.ImportStmtContext):
        import_path = ctx.STRING().getText()[1:-1]  # 去除引号

        # 检查是否已经导入过
        if self.import_manager.has_imported(import_path):
            return Result(ValueType.OTHER, DataType.STRING, import_path)

        # 标记已导入
        self.import_manager.execute_import(import_path)

        # 处理导入的文件
        try:
            input_stream = FileStream(import_path, encoding='utf-8')
            lexer = McFuncDSLLexer.McFuncDSLLexer(input_stream)
            stream = CommonTokenStream(lexer)
            parser = McFuncDSLParser.McFuncDSLParser(stream)
            tree = parser.program()

            # 访问并处理导入的文件
            self.visit(tree)
        except Exception as e:
            raise ImportError(e)

        return Result(ValueType.OTHER, DataType.STRING, import_path)
