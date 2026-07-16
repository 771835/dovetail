# coding=utf-8
"""
类型检查器模块

负责所有类型相关的验证、推导和兼容性检查。
"""
from lark.tree import Meta

from dovetail.core.enums import PrimitiveDataType
from dovetail.core.enums.datatypes import DataTypeBase, UnionType
from dovetail.core.errors import Errors
from dovetail.core.parser.components.error_reporter import ErrorReporter
from dovetail.core.symbols import Function


class TypeChecker:
    """类型检查器 - 处理类型验证逻辑"""

    def __init__(self, error_reporter: ErrorReporter):
        self.error_reporter = error_reporter

    def check_type_match(
            self,
            expected: DataTypeBase,
            actual: DataTypeBase,
            context: str,
            meta: Meta | None
    ) -> bool:
        """
        检查类型是否匹配

        Args:
            expected: 期望类型
            actual: 实际类型
            context: 上下文描述（如"初始化变量 x"）
            meta: 元数据

        Returns:
            True 表示类型匹配，False 表示不匹配
        """
        if isinstance(expected, UnionType):
            if not any(self._check_a_type_match(i, actual) for i in expected.types):
                self.error_reporter.report(
                    Errors.TypeMismatch,
                    repr(expected),
                    actual.get_name(),
                    meta=meta,
                    suggestion=f"在 {context} 时发生类型不匹配"
                )
                return False
            return True
        else:
            if not self._check_a_type_match(expected, actual):
                self.error_reporter.report(
                    Errors.TypeMismatch,
                    expected.get_name(),
                    actual.get_name(),
                    meta=meta,
                    suggestion=f"在 {context} 时发生类型不匹配"
                )
                return False
            return True

    def _check_a_type_match(
            self,
            expected: DataTypeBase | type,
            actual: DataTypeBase
    ):
        """
        检查单个类型是否匹配

        Args:
            expected: 期望类型
            actual: 实际类型

        Returns:
            True 表示类型匹配，False 表示不匹配
        """
        if isinstance(expected, type) and isinstance(actual, expected):
            return True
        elif isinstance(expected, DataTypeBase) and actual.is_subclass_of(expected):
            return True
        return False

    def check_definable(
            self,
            dtype: DataTypeBase,
            meta: Meta | None
    ) -> bool:
        """
        检查类型是否可定义

        Args:
            dtype: 待检查的类型
            meta: 元数据

        Returns:
            True 表示可定义，False 表示不可定义
        """
        if not dtype.is_definable():
            self.error_reporter.report(
                Errors.TypeMismatch,
                "可定义类型",
                dtype.get_name(),
                meta=meta,
                suggestion=f"{dtype.get_name()} 不可作为变量类型定义"
            )
            return False
        return True

    def check_compatible_for_comparison(
            self,
            left: DataTypeBase,
            right: DataTypeBase,
            meta: Meta
    ) -> bool:
        """
        检查两个类型是否可以比较

        Args:
            left: 左操作数类型
            right: 右操作数类型
            meta: 元数据

        Returns:
            True 表示可以比较，False 表示不能比较
        """
        if not (left.is_subclass_of(right) or right.is_subclass_of(left)):
            self.error_reporter.report(
                Errors.TypeMismatch,
                left.get_name(),
                right.get_name(),
                meta=meta,
                suggestion="比较运算要求两侧类型兼容"
            )
            return False
        return True

    def check_binary_op_compatibility(
            self,
            left: DataTypeBase,
            right: DataTypeBase,
            op: str,
            meta: Meta
    ) -> bool:
        """
        检查二元运算的类型兼容性

        Args:
            left: 左操作数类型
            right: 右操作数类型
            op: 运算符
            meta: 元数据

        Returns:
            True 表示兼容，False 表示不兼容
        """
        # 检查类型兼容性
        if not (left.is_subclass_of(right) or right.is_subclass_of(left)):
            self.error_reporter.report(
                Errors.TypeMismatch,
                left.get_name(),
                right.get_name(),
                meta=meta,
                suggestion=f"运算符 '{op}' 要求两侧类型兼容"
            )
            return False

        # 检查字符串只能用于加法
        if left == PrimitiveDataType.STRING and op != "+":
            self.error_reporter.report(
                Errors.InvalidOperator,
                op,
                meta=meta,
                suggestion="字符串只支持 '+' 运算符"
            )
            return False

        return True

    def infer_binary_op_type(
            self,
            left: DataTypeBase,
            right: DataTypeBase,
    ) -> DataTypeBase:
        """
        推导二元运算的结果类型

        Args:
            left: 左操作数类型
            right: 右操作数类型

        Returns:
            运算结果类型
        """
        # 布尔类型参与运算时提升为 int
        if left == PrimitiveDataType.BOOLEAN or right == PrimitiveDataType.BOOLEAN:
            return PrimitiveDataType.INT

        # 其他情况返回左操作数类型
        return left

    def check_function_type(
            self,
            func: Function,
            param_types: list[DataTypeBase],
            return_value_type: DataTypeBase,
            meta: Meta
    ) -> Function | None:
        """
        检查函数的签名类型

        Args:
            func: 方法
            param_types: 形参类型
            return_value_type: 返回值类型
            meta: 元数据

        Returns:
            当找不到符号时返回 None
        """

        min_args: int = sum(not param.is_optional() for param in func.params)
        max_args: int = len(func.params)

        # 检查参数数量是否在有效范围内
        if not min_args <= len(param_types) <= max_args:
            self.error_reporter.report(
                Errors.ArgumentNumberMismatch,
                func.name,
                f"{min_args}-{max_args}",
                str(len(param_types)),
                meta=meta
            )
            return None

        # 检查类型
        for expected_type, actual_type in zip(param_types, (param.get_dtype() for param in func.params)):
            if not actual_type.is_subclass_of(expected_type):
                self.error_reporter.report(
                    Errors.ArgumentTypeMismatch,
                    func.name,
                    str(expected_type),
                    str(actual_type),
                    meta=meta
                )

        # 检查返回值类型
        if return_value_type.is_subclass_of(func.get_dtype()):
            self.error_reporter.report(
                Errors.ArgumentTypeMismatch,
                func.name,
                str(return_value_type),
                str(func.get_dtype()),
                meta=meta
            )

        return func
