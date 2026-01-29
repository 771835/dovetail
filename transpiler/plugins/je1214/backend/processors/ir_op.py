# coding=utf-8
"""
IROp 指令处理器
"""
from transpiler.core.backend import ir_processor, IRProcessor, GenerationContext
from transpiler.core.enums import BinaryOps, DataType
from transpiler.core.instructions import IRInstruction, IROpCode
from transpiler.core.symbols import Constant, Literal, Variable, Reference
from ..backend import JE1214Backend
from ..commands.binary_op import BinaryOp
from ..commands.tools import DataPath, StorageLocation


@ir_processor(JE1214Backend, IROpCode.BINARY_OP)
class IROpProcessor(IRProcessor):
    def process(self, instruction: IRInstruction, context: GenerationContext):
        result: Variable | Constant = instruction.get_operands()[0]
        op: BinaryOps = instruction.get_operands()[1]
        left_ref: Reference[Variable | Constant | Literal] = instruction.get_operands()[2]
        right_ref: Reference[Variable | Constant | Literal] = instruction.get_operands()[3]
        # 对类的运算应在AST阶段解析为方法调用
        assert isinstance(result.dtype, DataType), "不支持的运算"
        assert isinstance(left_ref.get_data_type(), DataType), "不支持的运算"
        assert isinstance(right_ref.get_data_type(), DataType), "不支持的运算"
        context.add_commands(
            BinaryOp.op_all(
                DataPath(
                    context.current_scope.get_symbol_path(result.name),
                    context.objective,
                    StorageLocation.get_storage(result.dtype)
                ),
                op,
                DataPath(
                    context.current_scope.get_symbol_path(left_ref.get_name()),
                    context.objective,
                    StorageLocation.get_storage(left_ref.get_data_type())
                ),
                DataPath(
                    context.current_scope.get_symbol_path(left_ref.get_name()),
                    context.objective,
                    StorageLocation.get_storage(left_ref.get_data_type())
                )
            )
        )
