# coding=utf-8
"""
IRFunction 指令处理器
"""
from dovetail.core.backend import ir_processor, IRProcessor, GenerationContext
from dovetail.core.instructions import IRInstruction, IROpCode
from dovetail.core.symbols import Function
from ..backend import JE1215Backend
from ..output_writers import StubFunction, InitializerFunctionWriter


@ir_processor(JE1215Backend, IROpCode.FUNCTION)
class IRFunctionProcessor(IRProcessor):

    def process(self, instruction: IRInstruction, context: GenerationContext):
        function: Function = instruction.operands[0]  # NOQA

        function_path = f"{context.current_scope.get_absolute_path('/')}/{function.name}"

        # 打标签
        for name, attachment in function.annotations.items():
            # 更标准的做法是查函数的flags和metadata，但是性能较差，而且架构很乱
            if name == "init":
                InitializerFunctionWriter.init_functions.append(function_path)
            elif name == "tick":
                InitializerFunctionWriter.tick_functions.append(function_path)
            elif name == "export":
                # 记录需要导出的函数的信息
                JE1215Backend.stub_functions.append(
                    StubFunction(
                        function,
                        f"{context.current_scope.get_absolute_path()}.{function.name}",
                        str(function.all_metadata().get("path")),
                        str(function.all_metadata().get("abi")),
                        str(function.all_metadata().get("objective"))
                    )
                )

        context.current_scope.add_symbol(function)
