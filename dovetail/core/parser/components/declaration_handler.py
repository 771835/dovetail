# coding=utf-8
"""
声明处理器模块

专门处理变量、常量、函数、类等声明语句。
"""
from typing import Optional

from lark.tree import Meta

from dovetail.core.enums.types import DataTypeBase
from dovetail.core.errors import Errors
from dovetail.core.instructions import IRDeclare, IRAssign
from dovetail.core.parser.components.error_reporter import ErrorReporter
from dovetail.core.parser.components.ir_emitter import IREmitter
from dovetail.core.parser.components.symbol_resolver import SymbolResolver
from dovetail.core.parser.components.type_checker import TypeChecker
from dovetail.core.symbols import Variable, Reference
from dovetail.utils.naming import NameNormalizer

_n = NameNormalizer.normalize


class DeclarationHandler:
    """声明处理器 - 处理声明语句"""

    def __init__(
            self,
            symbol_resolver: SymbolResolver,
            type_checker: TypeChecker,
            ir_emitter: IREmitter,
            error_reporter: ErrorReporter
    ):
        self.symbol_resolver = symbol_resolver
        self.type_checker = type_checker
        self.ir_emitter = ir_emitter
        self.error_reporter = error_reporter

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
        variable = Variable(_n(name), dtype, mutable=mutable)
        if not self.symbol_resolver.add_symbol(variable, meta):
            return None

        # 生成 IR
        self.ir_emitter.emit(IRDeclare(variable))
        if value:
            self.ir_emitter.emit(IRAssign(variable, value))
        return Reference(variable)
