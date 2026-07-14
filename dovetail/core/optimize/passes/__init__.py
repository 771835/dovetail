# coding=utf-8
"""
内置优化 Pass 模块

此包的 import 会触发各 Pass 的 @register_pass 装饰器，
将 Pass 类注册到全局注册表。
由 optimizer.ensure_passes_registered() 统一调用，不应在其他地方直接 import *。
"""
from .chain_assign import ChainAssignEliminationPass # bug
from .constant_folding import ConstantFoldingPass
from .dead_code_elimination import DeadCodeEliminationPass
from .declare_cleanup import DeclareCleanupPass
from .empty_scope import EmptyScopeRemovalPass
from .unreachable_code import UnreachableCodeRemovalPass
from .unused_function import UnusedFunctionEliminationPass # 可能能用，不确定
from .useless_scope import UselessScopeRemovalPass
from .function_inling import FunctionInliningPass
__all__ = []