# coding=utf-8
"""
后端生成处理器
"""
from .ir_class import IRClassProcessor
from .ir_function import IRFunctionProcessor
from .ir_op import IROpProcessor
from .ir_scope_begin import IRScopeBeginProcessor
from .ir_scope_end import IRScopeEndProcessor
from .ir_compare import IRCompareProcessor
from .ir_declare import IRDeclareProcessor
__all__ = [
    'IROpProcessor',
    'IRClassProcessor',
    'IRFunctionProcessor',
    'IRScopeBeginProcessor',
    'IRScopeEndProcessor',
    'IRCompareProcessor',
    'IRDeclareProcessor',
]
