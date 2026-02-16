# coding=utf-8
"""
后端生成处理器
"""
from .ir_assign import IRAssignProcessor
from .ir_break import IRBreakProcessor
from .ir_call import IRCallProcessor
from .ir_cast import IRCastProcessor
from .ir_class import IRClassProcessor
from .ir_compare import IRCompareProcessor
from .ir_cond_jump import IRCondJumpProcessor
from .ir_continue import IRContinueProcessor
from .ir_declare import IRDeclareProcessor
from .ir_function import IRFunctionProcessor
from .ir_jump import IRJumpProcessor
from .ir_binary_op import IROpProcessor
from .ir_return import IRReturnProcessor
from .ir_scope_begin import IRScopeBeginProcessor
from .ir_scope_end import IRScopeEndProcessor
from .ir_unary_op import IRUnaryOpProcessor
__all__ = []
