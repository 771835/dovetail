from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from McFuncDSL import McFuncDSLParser, McFuncDSLLexer
from McFuncDSL.McFuncDSLVisitor import *
from antlr4 import *
import os, re
from enum import Enum

from Scope import Scope


class ScopeType(Enum):
    GLOBAL = "global"
    FUNCTION = "function"
    CLASS = "class"
    LOOP = "loop"
    #CONDITIONAL_BLOCK = "conditional_block"
    INTERFACE = 'interface'


class FunctionType(Enum):
    NORMAL = "function"
    METHOD = "method"
    CONSTRUCTOR = "constructor"


class SymbolType(Enum):
    VARIABLE = "variable"
    CONST = 'const'
    FUNCTION = "function"
    CLASS = "class"
    INTERFACE = 'interface'


class BaseType(Enum):
    TYPE_INT = 'int'
    TYPE_STRING = 'string'
    TYPE_FSTRING = 'fstring'
    TYPE_BOOLEAN = 'boolean'
    TYPE_VOID = 'void'
    TYPE_ANY = 'any'
    TYPE_SELECTOR = 'Selector'


class Type(Enum):
    TYPE = 'type'
    TYPE_ANY = 'any'

    # 仅字面量或常量为以下几个参数，其他均为TYPE_VARIABLE，boolean拟成0/1，string/fstring仅限编译期使用，void仅编译器模拟
    TYPE_INT = 'int'  # 存储具体数值
    TYPE_STRING = 'string'  # 存储字符串
    TYPE_FSTRING = 'fstring'  # 该类型将会在解析后转为string
    TYPE_BOOLEAN = 'boolean'  # 存储bool
    TYPE_VOID = 'void'  # 存储None

    TYPE_SELECTOR = 'Selector'  # 特殊常量，存储选择器

    TYPE_VARIABLE = "variable"  # 变量，存储变量的unique_name
    TYPE_INTERFACE = 'interface'
    TYPE_FUNCTION = 'function'
    TYPE_CLASS = 'class'
    TYPE_BLOCK = 'block'
    TYPE_IMPORT = 'import'
    TYPE_ERROR = 'error'


@dataclass
class Result:
    type_: Type | None
    value: Any
    Error: bool

    def OK(self, function):
        if not self.Error:
            function(self.type_, self.value)

    def ERR(self, function):
        if self.Error:
            function(self.type_, self.value)

    def __str__(self):
        return str(self.value)


class TypeInferencer:
    @staticmethod
    def infer(expr_result: Result) -> Type | None:
        if expr_result is None:
            return None
        if expr_result.type_ != Type.TYPE_ANY:
            return expr_result.type_
        # 根据表达式结果的具体值推断
        if isinstance(expr_result.value, int):
            return Type.TYPE_INT
        elif isinstance(expr_result.value, str):
            return Type.TYPE_STRING
        elif isinstance(expr_result.value, bool):
            return Type.TYPE_BOOLEAN
        elif expr_result.value is None:
            return Type.TYPE_VOID
        else:
            return None


class Symbol:
    def __init__(self, name: str, symbol_type: SymbolType, data_type: Type = None):
        self.name = name
        self.type = symbol_type
        self.data_type = data_type
        self.value = None  # 用于存储初始值或记录代码中指定的值

    def get_unique_name(self, scope: Scope):
        return scope.get_name() + "_" + self.name


class ImportManager:
    def __init__(self):
        self.imported = set()  # 已导入文件

    def resolve_path(self, import_path: str):
        return os.path.abspath(import_path)

    def add_import(self, import_path: str) -> None:
        self.imported.add(self.resolve_path(import_path))
        return

    def is_exist(self, import_path: str):
        return self.resolve_path(import_path) in self.imported


class MCGenerator(McFuncDSLVisitor):
    def __init__(self, namespace: str = "mcfdsl"):
        self.namespace = namespace
        self.top_scope = Scope(name="global", scope_type=ScopeType.GLOBAL, namespace=self.namespace)
        self.current_scope = self.top_scope
        self.import_manager = ImportManager()  # 引用管理器
        self.scope_stack = [self.top_scope]
        self.cnt = 0  # 保证for loop和if else唯一性

        self._add_command("# Scoreboard initialization", self.top_scope)
        self._add_command("scoreboard objectives add var dummy \"Variables\"", self.top_scope)
        self._add_command("scoreboard objectives add loop dummy \"Loop Counters\"", self.top_scope)
        self._add_command("scoreboard objectives add return dummy \"Function Returns\"", self.top_scope)

    # 作用域管理辅助方法
    def _enter_scope(self, name: str, scope_type: ScopeType):
        new_scope = self.current_scope.create_child(name, scope_type)
        self.current_scope = new_scope
        self.scope_stack.append(new_scope)
        if (len(self.scope_stack) > 1000):
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
                            symbol.type == SymbolType.VARIABLE or symbol.type == SymbolType.CONST):
                        return symbol.value
                    else:
                        raise NameError(f"{symbol.name} has not been assigned a value, or cannot resolve its value")
                else:
                    raise NameError("fstring does not support non-constant results")
            except (KeyError, TypeError):
                return f'${{{key}}}'  # 保留原占位符

        # 执行替换
        result = re.sub(r'\$\{([^}]+)}', replacer, processed_text)
        # 恢复转义符
        return result.replace('\x00', '$')

    def _add_command(self, cmd, scope: Scope | None):
        if scope is None:
            scope = self.current_scope
        scope.cmd.append(cmd)

    def _generate_commands(self):
        """遍历作用域树生成文件"""
        output_dir = "target"
        stack: list[Scope] = [self.top_scope]

        while stack:
            current = stack.pop()
            if current.cmd:
                path = os.path.join(output_dir, current.get_file_path())
                os.makedirs(os.path.dirname(path), exist_ok=True)
                with open(path, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(current.cmd))
            stack.extend(reversed(current.children))

    # 检查类型是否存在
    def _type_exists(self, type_name):
        if isinstance(type_name, Type):
            return True
        try:
            resolve_symbol_result = self.current_scope.resolve_symbol(type_name)
            if resolve_symbol_result.type == SymbolType.CLASS:
                return True
        except NameError:
            if type_name in BaseType:
                return True
        return False

    def _is_number(self, s):
        try:
            int(s)
            return True
        except ValueError:
            return False

    def visitCmdExpr(self, ctx: McFuncDSLParser.CmdExprContext):
        fstring = ctx.FSTRING().getText()[2:-1]  # 去掉f""
        command = self._process_fstring(fstring)
        self._add_command(scope=None, cmd=command)
        return Result(Type.TYPE_STRING, command, False)

    # 处理变量声明
    def visitVarDeclaration(self, ctx: McFuncDSLParser.VarDeclarationContext):
        var_name = ctx.ID().getText()
        var_type = Type(ctx.type_().getText()) if ctx.type_() else Type.TYPE_ANY

        # 创建符号
        symbol = Symbol(var_name, SymbolType.VARIABLE, var_type)
        if ctx.primary():
            result = self.visit(ctx.primary())  # 处理初始化表达式
            if var_type == TypeInferencer.infer(result):
                symbol.value = result.value
            else:
                raise TypeError(f"需要{var_type}却设置了{TypeInferencer.infer(result.value)}")
            print(f"变量{var_name}:{var_type}初始化值: {symbol.value}  完整:{symbol}")

        if var_type == Type.TYPE_ANY and symbol.value is None:
            raise TypeError(f"Variable '{var_name}' must be initialized as type cannot be inferred")
        if not self._type_exists(var_type):
            raise TypeError(f"The type {var_type} does not exist.")
        self.current_scope.add_symbol(symbol)
        self._add_command(cmd=f"scoreboard players set {symbol.get_unique_name(self.current_scope)} var 0",
                          scope=self.current_scope)
        return Result(Type.TYPE_VARIABLE, symbol.value, False)

    # 处理函数定义
    def visitFunctionDecl(self, ctx: McFuncDSLParser.FunctionDeclContext):
        func_name = ctx.ID().getText()
        scope = self._enter_scope(func_name, ScopeType.FUNCTION)
        # 处理参数
        params = ctx.paramList()
        if params:
            for param in params.paramDecl():
                param_name = param.ID().getText()
                param_type = param.type_().getText()
                self.current_scope.add_symbol(Symbol(param_name, SymbolType.VARIABLE, param_type))

        # 处理函数体
        self.visit(ctx.block())

        self._exit_scope()
        return Result(Type.TYPE_FUNCTION, scope.get_minecraft_function_path(), False)

    # 处理代码块
    def visitBlock(self, ctx: McFuncDSLParser.BlockContext):
        # 遍历子节点
        self.visitChildren(ctx)
        return Result(Type.TYPE_FUNCTION, self.current_scope.get_minecraft_function_path(), False)

    def visitLiteral(self, ctx: McFuncDSLParser.LiteralContext):
        value = ctx.getText()
        if value == 'true':
            return Result(Type.TYPE_BOOLEAN, True, False)
        elif value == 'false':
            return Result(Type.TYPE_BOOLEAN, False, False)
        elif value[0] == 'f':
            return Result(Type.TYPE_FSTRING, self._process_fstring(value[2:-1]), False)
        elif self._is_number(value):
            return Result(Type.TYPE_INT, int(value), False)
        else:
            return Result(Type.TYPE_STRING, value[1:-1], False)

    def visitClassDecl(self, ctx: McFuncDSLParser.ClassDeclContext):
        class_name = ctx.ID().getText()
        class_scope = self._enter_scope(class_name, ScopeType.CLASS)
        class_symbol = Symbol(class_name, SymbolType.CLASS, Type.TYPE_CLASS)
        class_scope.add_symbol(class_symbol)

        # 处理继承
        if ctx.type_():
            base_class = ctx.type_().getText()
            base_class_symbol = class_scope.resolve_symbol(base_class)
            if base_class_symbol is None or base_class_symbol.type != SymbolType.CLASS:
                raise NameError(f"基类 {base_class} 未定义")
        if ctx.type_(1):  # 接口实现
            pass

        # 处理字段和方法
        for member in ctx.varDecl() + ctx.methodDecl():
            self.visit(member)

        self._exit_scope()
        return Result(Type.TYPE_CLASS, class_name, False)

    def visitForStmt(self, ctx: McFuncDSLParser.ForStmtContext):  # 需修改

        if ctx.forControl():  # 传统for循环
            loop_id = self.cnt
            self.cnt += 1

            # 处理初始化表达式
            if ctx.forControl().forLoopVarDecl():
                self.visit(ctx.forControl().forLoopVarDecl())

            # 创建循环检查作用域
            check_scope = self._enter_scope(f"for_{loop_id}_check", ScopeType.FUNCTION)

            # 评估条件表达式
            condition_expr = self.visit(ctx.forControl().expr(0))
            condition_var = condition_expr.value

            # 条件检查 - 如果条件为假则返回
            self._add_command(f"execute unless score {condition_var} var matches 1 run return", check_scope)

            # 创建循环体作用域
            body_scope = self._enter_scope(f"for_{loop_id}_body", ScopeType.LOOP)

            # 访问循环体
            self.visit(ctx.block())

            # 处理更新表达式
            if ctx.forControl().assignment():
                self.visit(ctx.forControl().assignment())
            elif len(ctx.forControl().expr()) > 1:
                self.visit(ctx.forControl().expr(1))

            # 添加返回检查的递归调用
            self._add_command(f"function {check_scope.get_minecraft_function_path()}", body_scope)

            # 从检查函数调用循环体
            self._add_command(f"function {body_scope.get_minecraft_function_path()}", check_scope)

            self._exit_scope()  # 退出body作用域
            self._exit_scope()  # 退出check作用域

            # 在当前作用域中调用检查函数开始循环
            self._add_command(f"function {check_scope.get_minecraft_function_path()}", self.current_scope)


        else:  # 增强for循环
            scope = self._enter_scope(str(self.cnt), ScopeType.LOOP)
            selector: Result = self.visit(ctx.expr())
            if selector.type_ != Type.TYPE_SELECTOR:
                raise TypeError(f"增强for循环需要{Type.TYPE_SELECTOR}而不是{selector.type_}")
            self._add_command(f"execute as {selector} run {self.visit(ctx.block()).value}",
                              self.current_scope.get_parent())
            self._exit_scope()
            # 在主作用域添加初始化+首次调用
            self._add_command("function " + scope.get_minecraft_function_path(), self.current_scope)
        return Result(Type.TYPE_VOID, None, False)

    # 选择器生成
    def visitNewSelectorExpr(self, ctx: McFuncDSLParser.NewSelectorExprContext):
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

        return Result(Type.TYPE_SELECTOR, final_selector, False)

    def visitIfStmt(self, ctx: McFuncDSLParser.IfStmtContext):
        # 生成唯一ID
        if_id = self.cnt
        self.cnt += 1

        # 计算条件表达式
        condition_expr = self.visit(ctx.expr())
        condition_var = condition_expr.value

        # 创建if分支作用域
        if_scope = self._enter_scope(f"if_{if_id}", ScopeType.FUNCTION)
        self.visit(ctx.block(0))
        self._exit_scope()

        # 处理else分支(如果存在)
        if len(ctx.block()) > 1:
            else_scope = self._enter_scope(f"else_{if_id}", ScopeType.FUNCTION)
            self.visit(ctx.block(1))
            self._exit_scope()

            # 根据条件执行不同分支
            self._add_command(
                f"execute if score {condition_var} var matches 1 run function {if_scope.get_minecraft_function_path()}",
                self.current_scope)
            self._add_command(
                f"execute unless score {condition_var} var matches 1 run function {else_scope.get_minecraft_function_path()}",
                self.current_scope)
        else:
            # 只有if分支的情况
            self._add_command(
                f"execute if score {condition_var} var matches 1 run function {if_scope.get_minecraft_function_path()}",
                self.current_scope)

        return Result(Type.TYPE_VOID, None, False)

    # 在visitCompareExpr中生成比较指令
    def visitCompareExpr(self, ctx):
        left = self.visit(ctx.expr(0))
        right = self.visit(ctx.expr(1))
        op = ctx.getChild(1).getText()

        # 生成唯一结果变量
        result_var = f"bool_{self.cnt}"
        self.cnt += 1

        # 初始化结果为假(0)
        self._add_command(f"scoreboard players set {result_var} var 0", self.current_scope)

        # 变量与变量比较
        if left.type_ == Type.TYPE_VARIABLE and right.type_ == Type.TYPE_VARIABLE:
            if op == '<':
                self._add_command(
                    f"execute if score {left.value} var < {right.value} var run scoreboard players set {result_var} var 1",
                    self.current_scope)
            elif op == '>':
                self._add_command(
                    f"execute if score {left.value} var > {right.value} var run scoreboard players set {result_var} var 1",
                    self.current_scope)
            elif op == '<=':
                self._add_command(
                    f"execute if score {left.value} var <= {right.value} var run scoreboard players set {result_var} var 1",
                    self.current_scope)
            elif op == '>=':
                self._add_command(
                    f"execute if score {left.value} var >= {right.value} var run scoreboard players set {result_var} var 1",
                    self.current_scope)
            elif op == '==':
                self._add_command(
                    f"execute if score {left.value} var = {right.value} var run scoreboard players set {result_var} var 1",
                    self.current_scope)
            elif op == '!=':
                self._add_command(
                    f"execute if score {left.value} var != {right.value} var run scoreboard players set {result_var} var 1",
                    self.current_scope)

        # 变量与常量比较
        elif left.type_ == Type.TYPE_VARIABLE and right.type_ == Type.TYPE_INT:
            if op == '<':
                self._add_command(
                    f"execute if score {left.value} var < {right.value} run scoreboard players set {result_var} var 1",
                    self.current_scope)
            elif op == '>':
                self._add_command(
                    f"execute if score {left.value} var > {right.value} run scoreboard players set {result_var} var 1",
                    self.current_scope)
            elif op == '<=':
                self._add_command(
                    f"execute if score {left.value} var <= {right.value} run scoreboard players set {result_var} var 1",
                    self.current_scope)
            elif op == '>=':
                self._add_command(
                    f"execute if score {left.value} var >= {right.value} run scoreboard players set {result_var} var 1",
                    self.current_scope)
            elif op == '==':
                self._add_command(
                    f"execute if score {left.value} var = {right.value} run scoreboard players set {result_var} var 1",
                    self.current_scope)
            elif op == '!=':
                self._add_command(
                    f"execute if score {left.value} var != {right.value} run scoreboard players set {result_var} var 1",
                    self.current_scope)

        # 常量与变量比较
        elif left.type_ == Type.TYPE_INT and right.type_ == Type.TYPE_VARIABLE:
            if op == '<':
                self._add_command(
                    f"execute if score {left.value} < {right.value} var run scoreboard players set {result_var} var 1",
                    self.current_scope)
            elif op == '>':
                self._add_command(
                    f"execute if score {left.value} > {right.value} var run scoreboard players set {result_var} var 1",
                    self.current_scope)
            elif op == '<=':
                self._add_command(
                    f"execute if score {left.value} <= {right.value} var run scoreboard players set {result_var} var 1",
                    self.current_scope)
            elif op == '>=':
                self._add_command(
                    f"execute if score {left.value} >= {right.value} var run scoreboard players set {result_var} var 1",
                    self.current_scope)
            elif op == '==':
                self._add_command(
                    f"execute if score {left.value} = {right.value} var run scoreboard players set {result_var} var 1",
                    self.current_scope)
            elif op == '!=':
                self._add_command(
                    f"execute if score {left.value} != {right.value} var run scoreboard players set {result_var} var 1",
                    self.current_scope)

        # 常量与常量比较
        elif left.type_ == Type.TYPE_INT and right.type_ == Type.TYPE_INT:
            result = False
            if op == '<':
                result = left.value < right.value
            elif op == '>':
                result = left.value > right.value
            elif op == '<=':
                result = left.value <= right.value
            elif op == '>=':
                result = left.value >= right.value
            elif op == '==':
                result = left.value == right.value
            elif op == '!=':
                result = left.value != right.value

            self._add_command(f"scoreboard players set {result_var} var {1 if result else 0}", self.current_scope)

        else:
            raise TypeError(f"不支持的比较类型: {left.type_} {op} {right.type_}")

        return Result(Type.TYPE_VARIABLE, result_var, False)

    def visitVarExpr(self, ctx: McFuncDSLParser.VarExprContext):
        var_name = ctx.ID().getText()
        symbol = self.current_scope.resolve_symbol(var_name)
        return Result(
            Type.TYPE_VARIABLE,
            symbol.get_unique_name(self.current_scope),
            False
        )

    def visitAssignment(self, ctx):
        var_name = ctx.ID().getText()
        expr_result = self.visit(ctx.expr())

        try:
            symbol = self.current_scope.resolve_symbol(var_name)
        except NameError:
            raise NameError(f"变量 '{var_name}' 未定义")

        if (expr_result is None) :
            raise TypeError("意外的类型NoneType，需要Result")

        # 正确的类型检查
        expr_result_type = TypeInferencer.infer(expr_result)

        if symbol.type != expr_result_type :
            raise TypeError(f"错误的类型，需要{symbol.type},实际为{expr_result_type}")


        # 根据表达式类型生成不同的命令
        if expr_result.type_ == Type.TYPE_INT:
            # 整数常量赋值
            self._add_command(
                f"scoreboard players set {symbol.get_unique_name(self.current_scope)} var {expr_result.value}",
                self.current_scope
            )
        elif expr_result.type_ == Type.TYPE_VARIABLE:
            # 变量赋值
            self._add_command(
                f"scoreboard players operation {symbol.get_unique_name(self.current_scope)} var = {expr_result.value} var",
                self.current_scope
            )
        elif expr_result.type_ == Type.TYPE_BOOLEAN:
            # 布尔值转为0/1
            value = 1 if expr_result.value else 0
            self._add_command(
                f"scoreboard players set {symbol.get_unique_name(self.current_scope)} var {value}",
                self.current_scope
            )

        # 更新符号表中的值
        symbol.value = expr_result.value

        return Result(Type.TYPE_VARIABLE, expr_result.value, False)

    def visitAddSubExpr(self, ctx):
        left = self.visit(ctx.expr(0))
        right = self.visit(ctx.expr(1))
        op = ctx.getChild(1).getText()

        # 生成唯一结果变量
        result_var = f"calc_{self.cnt}"
        self.cnt += 1

        # 处理变量与变量的运算
        if left.type_ == Type.TYPE_VARIABLE and right.type_ == Type.TYPE_VARIABLE:
            # 两个变量相加减
            self._add_command(f"scoreboard players operation {result_var} var = {left.value} var", self.current_scope)
            if op == '+':
                self._add_command(f"scoreboard players operation {result_var} var += {right.value} var",
                                  self.current_scope)
            else:  # '-'
                self._add_command(f"scoreboard players operation {result_var} var -= {right.value} var",
                                  self.current_scope)

        # 处理变量与常量的运算
        elif left.type_ == Type.TYPE_VARIABLE and right.type_ == Type.TYPE_INT:
            # 变量与常量
            self._add_command(f"scoreboard players operation {result_var} var = {left.value} var", self.current_scope)
            if op == '+':
                self._add_command(f"scoreboard players add {result_var} var {right.value}", self.current_scope)
            else:  # '-'
                self._add_command(f"scoreboard players remove {result_var} var {right.value}", self.current_scope)

        # 处理常量与变量的运算
        elif left.type_ == Type.TYPE_INT and right.type_ == Type.TYPE_VARIABLE:
            # 常量与变量
            self._add_command(f"scoreboard players set {result_var} var {left.value}", self.current_scope)
            if op == '+':
                self._add_command(f"scoreboard players operation {result_var} var += {right.value} var",
                                  self.current_scope)
            else:  # '-'
                self._add_command(f"scoreboard players operation {result_var} var -= {right.value} var",
                                  self.current_scope)

    def visitDirectFuncCall(self, ctx: McFuncDSLParser.DirectFuncCallContext):
        func_name = ctx.ID()

        # 处理参数
        args = []
        if ctx.argumentList().exprList():
            for arg_expr in ctx.argumentList().exprList():
                args.append(self.visit(arg_expr))

        # 生成参数传递命令
        for i, arg in enumerate(args):
            if arg.type_ == Type.TYPE_VARIABLE:
                self._add_command(
                    f"scoreboard players operation arg{i} var = {arg.value} var",
                    self.current_scope
                )
            else:
                value = arg.value
                if arg.type_ == Type.TYPE_BOOLEAN:
                    value = 1 if value else 0
                self._add_command(f"scoreboard players set arg{i} var {value}", self.current_scope)

        # 调用函数
        result_var = f"result_{self.cnt}"
        self.cnt += 1

        self._add_command(f"function {self.current_scope.resolve_scope(func_name).get_minecraft_function_path()}",
                          self.current_scope)
        self._add_command(f"scoreboard players operation {result_var} var = return var", self.current_scope)

        return Result(Type.TYPE_VARIABLE, result_var, False)

    def visitWhileStmt(self, ctx):
        while_id = self.cnt
        self.cnt += 1

        check_scope = self._enter_scope(f"while_{while_id}_check", ScopeType.FUNCTION)

        # 条件检查
        condition_expr = self.visit(ctx.expr())
        condition_var = condition_expr.value

        self._add_command(f"execute unless score {condition_var} var matches 1 run return", check_scope)

        # 循环体
        body_scope = self._enter_scope(f"while_{while_id}_body", ScopeType.LOOP)
        self.visit(ctx.block())
        self._add_command(f"function {check_scope.get_minecraft_function_path()}", body_scope)

        # 启动循环
        self._add_command(f"function {body_scope.get_minecraft_function_path()}", check_scope)
        self._add_command(f"function {check_scope.get_minecraft_function_path()}", self.current_scope)

        self._exit_scope()
        self._exit_scope()

        return Result(Type.TYPE_VOID, None, False)

    def visitReturnStmt(self, ctx):
        if ctx.expr():
            expr_result = self.visit(ctx.expr())

            if expr_result.type_ == Type.TYPE_VARIABLE:
                # 变量返回
                self._add_command(f"scoreboard players operation return var = {expr_result.value} var",
                                  self.current_scope)
            else:
                # 常量返回
                value = expr_result.value
                if expr_result.type_ == Type.TYPE_BOOLEAN:
                    value = 1 if value else 0
                if isinstance(value, (int, bool)):
                    self._add_command(f"scoreboard players set return var {value}", self.current_scope)
                else:
                    raise TypeError("暂不支持非基本类型返回")

        # 结束函数执行
        self._add_command("return", self.current_scope)
        return Result(Type.TYPE_VOID, None, False)

    def visitImportStmt(self, ctx: McFuncDSLParser.ImportStmtContext):
        import_path = ctx.STRING().getText()[1:-1]  # 去除引号

        # 检查是否已经导入过
        if self.import_manager.is_exist(import_path):
            return Result(Type.TYPE_IMPORT, import_path, True)

        # 标记已导入
        self.import_manager.add_import(import_path)

        # 处理导入的文件
        try:
            input_stream = FileStream(import_path)
            lexer = McFuncDSLLexer.McFuncDSLLexer(input_stream)
            stream = CommonTokenStream(lexer)
            parser = McFuncDSLParser.McFuncDSLParser(stream)
            tree = parser.program()

            # 访问并处理导入的文件
            self.visit(tree)
        except Exception as e:
            raise ImportError(e)
            # return Result(Type.TYPE_ERROR, e, True)

        return Result(Type.TYPE_IMPORT, import_path, False)


def compile(source_path):
    input_stream = FileStream(source_path)
    lexer = McFuncDSLLexer.McFuncDSLLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = McFuncDSLParser.McFuncDSLParser(stream)
    tree = parser.program()

    generator = MCGenerator()
    try:
        generator.visit(tree)
    except Exception as e:
        # 定义作用域树打印函数
        def print_scope_tree(node, prefix="", is_tail=True):
            """递归打印作用域树结构"""
            # 节点显示：作用域名 (类型)
            type_str = f" ({node.type.value})" if node.type else ""
            line = f"{prefix}{'└── ' if is_tail else '├── '}{node.name}{type_str}"
            print(line)

            # 处理子节点
            children = node.children
            for i, child in enumerate(children):
                new_prefix = prefix + ("    " if is_tail else "│   ")
                print_scope_tree(child, new_prefix, i == len(children) - 1)

        # 打印错误信息
        print("\n⚠️ Compilation Error ⚠️")
        print("Current scope structure:")
        print_scope_tree(generator.top_scope)

        # 打印当前作用域栈（调用链）
        print("\nScope call stack:")
        for i, scope in enumerate(generator.scope_stack):
            indent = "  " * i
            type_str = f" ({scope.type.value})" if scope.type else ""
            print(f"{indent}{scope.name}{type_str}")

        # 重新抛出异常显示错误详情
        raise
    generator._generate_commands()
    # 输出到target目录


if __name__ == "__main__":
    compile("b.mcdl")
