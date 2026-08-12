# coding=utf-8
"""
内置优化 Pass 模块

此包的 import 会触发各 Pass 的 @register_pass 装饰器，
将 Pass 类注册到全局注册表。
由 optimizer.ensure_passes_registered() 统一调用，不应在其他地方直接 import *。
"""
from .chain_assign_elimination import ChainAssignEliminationPass
from .constant_folding import ConstantFoldingPass
from .dead_code_elimination import DeadCodeEliminationPass
from .empty_scope import EmptyScopeRemovalPass
from .function_inlining import FunctionInliningPass
from .tail_call_optimization import TailCallOptimizationPass
from .unconditional_scope_inlining import UnconditionalScopeInliningPass
from .unreachable_code import UnreachableCodeRemovalPass
from .unused_function import UnusedFunctionEliminationPass  # 可能能用，不确定
from .unreachable_scope_elimination import UselessScopeEliminationPass

__all__ = []
