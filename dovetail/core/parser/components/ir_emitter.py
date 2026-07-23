# coding=utf-8
"""
IR 发射器模块

提供高级 IR 生成接口，封装常用模式，但保持底层灵活性。
"""
import itertools
from contextlib import contextmanager
from typing import Optional

from lark.tree import Meta

from dovetail.core.enums import StructureType, BinaryOps, CompareOps, PrimitiveDataType
from dovetail.core.enums.datatypes import DataTypeBase
from dovetail.core.errors import Errors
from dovetail.core.instructions import (
    IRInstruction, IRDeclare, IRScopeBegin, IRScopeEnd,
    IRBinaryOp, IRCompare, IRAssign
)
from dovetail.core.ir_builder import IRBuilder
from dovetail.core.parser.components.error_reporter import ErrorReporter
from dovetail.core.parser.components.type_checker import TypeChecker
from dovetail.core.parser.components.symbol_resolver import SymbolResolver
from dovetail.core.symbols import Variable, Reference, Function
from dovetail.utils.naming import NameNormalizer


class IREmitter:
    """
    IR 发射器 - 提供高级 IR 生成接口

    设计原则：
    1. 不包装所有指令 - 保持 emit() 的通用性
    2. 只封装高频模式 - 如"声明+赋值"
    3. 提供工具方法 - 如生成唯一名称
    """

    def __init__(
            self,
            builder: IRBuilder,
            error_reporter: ErrorReporter,
            type_checker: TypeChecker,
            symbol_resolver: SymbolResolver
    ):
        self.symbol_resolver = symbol_resolver
        self.builder = builder
        self.error_reporter = error_reporter
        self.type_checker = type_checker
        self.temp_counter = itertools.count()
        self.label_counter = itertools.count()

    # ==================== 核心方法 ====================

    def emit(self, *instrs: IRInstruction) -> None:
        """
        发射一个或多个 IR 指令

        用法:
            emitter.emit(IRDeclare(var))
            emitter.emit(IRDeclare(var), IRAssign(var, value))

        Args:
            *instrs: 一个或多个 IR 指令
        """
        for instr in instrs:
            self.builder.insert(instr)

    def emit_list(self, instrs: list[IRInstruction]) -> None:
        """
        发射指令列表

        Args:
            instrs: IR 指令列表
        """
        self.emit(*instrs)

    # ==================== 高频模式封装 ====================


    def declare_variable(
            self,
            name: str,
            dtype: DataTypeBase,
            value: Optional[Reference],
            meta: Meta,
            mutable: bool = True
    ) -> Optional[Reference]:
        """
        声明变量或常量

        Args:
            name: 变量名
            dtype: 数据类型
            value: 初始值（可选）
            meta: 元数据
            mutable: 是否可变（True=变量，False=常量）

        Returns:
            变量引用，声明失败则返回 None
        """

        # 检查类型可定义性
        if not self.type_checker.check_definable(dtype, meta):
            return None

        # 检查初始值类型匹配
        if value and not self.type_checker.check_type_match(
                dtype,
                value.get_dtype(),
                context=f"初始化{'变量' if mutable else '常量'} {name}",
                meta=meta
        ):
            return None

        # 检查常量必须初始化
        if not mutable and value is None:
            self.error_reporter.report(
                Errors.ConstantRequiresInitialization,
                name,
                meta=meta
            )
            return None

        # 创建并注册符号
        variable = Variable(NameNormalizer.normalize(name), dtype, mutable=mutable)
        if not self.symbol_resolver.add_symbol(variable, meta):
            return None

        # 生成 IR
        self.emit(IRDeclare(variable))
        if value:
            self.emit(IRAssign(variable, value))
        return Reference(variable)


    # ==================== 工具方法 ====================

    def create_temp_var(
            self,
            dtype: DataTypeBase,
            prefix: str = "temp"
    ) -> Variable:
        """
        创建临时变量（不自动声明）

        Args:
            dtype: 变量类型
            prefix: 变量名前缀

        Returns:
            新创建的临时变量
        """
        return Variable(f"{prefix}_{next(self.temp_counter)}_", dtype)

    def create_temp_var_declared(
            self,
            dtype: DataTypeBase,
            prefix: str = "temp"
    ) -> Variable:
        """
        创建临时变量并自动声明

        Args:
            dtype: 变量类型
            prefix: 变量名前缀

        Returns:
            已声明的临时变量
        """
        var = self.create_temp_var(dtype, prefix)
        self.emit(IRDeclare(var))
        return var

    def generate_label(self, prefix: str) -> str:
        """
        生成唯一标签名

        Args:
            prefix: 标签前缀

        Returns:
            唯一标签名，格式为 "prefix_序号_"
        """
        return f"{prefix}_{next(self.label_counter)}_"

    @contextmanager
    def scope(self, name: str, scope_type: StructureType):
        """
        作用域上下文管理器（自动生成配对的 ScopeBegin/ScopeEnd）

        用法:
            with ir_emitter.scope("loop_body", StructureType.LOOP_BODY):
                ir_emitter.emit(...)  # 这些指令在作用域内

        Args:
            name: 作用域名称
            scope_type: 作用域类型

        Yields:
            作用域名称
        """
        self.emit(IRScopeBegin(name, scope_type))
        try:
            yield name
        finally:
            self.emit(IRScopeEnd(name, scope_type))

    # ==================== 快捷方法 ====================

    def emit_binary_calc(
            self,
            left: Reference,
            op: BinaryOps,
            right: Reference,
            result_type: DataTypeBase,
            result_prefix: str = "calc"
    ) -> Variable:
        """
        二元运算的完整流程：创建临时变量 → 声明 → 执行运算

        Args:
            left: 左操作数
            op: 运算符
            right: 右操作数
            result_type: 结果类型
            result_prefix: 结果变量名前缀

        Returns:
            包含运算结果的临时变量（已声明和赋值）
        """
        result_var = self.create_temp_var_declared(result_type, result_prefix)
        self.emit(IRBinaryOp(result_var, op, left, right))
        return result_var

    def emit_comparison(
            self,
            left: Reference,
            op: CompareOps,
            right: Reference,
            result_prefix: str = "cmp_result"
    ) -> Variable:
        """
        比较运算的完整流程

        Args:
            left: 左操作数
            op: 比较运算符
            right: 右操作数
            result_prefix: 结果变量名前缀

        Returns:
            包含比较结果的布尔型临时变量
        """
        result_var = self.create_temp_var_declared(PrimitiveDataType.BOOLEAN, result_prefix)
        self.emit(IRCompare(result_var, op, left, right))
        return result_var

    def emit_call_function(
            self,
            func: Function,
            args: list[tuple[Reference, bool]],
            meta: Meta
    ):
        ...
