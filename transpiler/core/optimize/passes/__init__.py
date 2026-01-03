# coding=utf-8
"""
内置优化 Pass 模块

提供所有内置的优化 Pass 实现。
"""
from .constant_folding import ConstantFoldingPass
from .dead_code_elimination import DeadCodeEliminationPass
from .declare_cleanup import DeclareCleanupPass
from .empty_scope import EmptyScopeRemovalPass
from .unreachable_code import UnreachableCodeRemovalPass
from .unused_function import UnusedFunctionEliminationPass
from .useless_scope import UselessScopeRemovalPass

__all__ = [
    'ConstantFoldingPass',
    'DeadCodeEliminationPass',
    'DeclareCleanupPass',
    'UnreachableCodeRemovalPass',
    'UnusedFunctionEliminationPass',
    'UselessScopeRemovalPass',
    'EmptyScopeRemovalPass',
]