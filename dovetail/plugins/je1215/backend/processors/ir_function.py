# coding=utf-8
"""
IRFunction 指令处理器
"""
from dovetail.core.backend import ir_processor, IRProcessor, GenerationContext
from dovetail.core.instructions import IRInstruction, IROpCode
from dovetail.core.symbols import Function
from ..backend import JE1214Backend
from ..initializer_function_writer import InitializerFunctionWriter


@ir_processor(JE1214Backend, IROpCode.FUNCTION)
class IRFunctionProcessor(IRProcessor):


    def process(self, instruction: IRInstruction, context: GenerationContext):
        function: Function = instruction.operands[0]  # NOQA

        for annotation in function.annotations:
            function_path = f"{context.current_scope.get_absolute_path('/')}/{function.name}"
            if annotation.name == "init":
                InitializerFunctionWriter.init_functions.append(function_path)
            elif annotation.name == "tick":
                InitializerFunctionWriter.tick_functions.append(function_path)

        context.current_scope.add_symbol(function)
