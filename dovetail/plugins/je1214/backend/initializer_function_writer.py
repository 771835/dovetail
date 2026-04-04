# coding=utf-8
"""
初始化函数写入器

写入初始化函数
初始化函数行为:
- 初始化计分板
- 调用常量池初始化
- 对特殊位置预填充数据
- 输出项目启动信息(可选)
"""
from dovetail.core.backend import OutputWriter, GenerationContext
from .commands import FunctionBuilder, DataBuilder, ScoreboardBuilder


class InitializerFunctionWriter(OutputWriter):
    init_functions: list[str] = []
    tick_functions: list[str] = []
    def write(self, context: GenerationContext):
        function_dir_path = context.target / context.namespace / "data" / context.namespace / "function"
        function_dir_path.mkdir(parents=True, exist_ok=True)
        initializer_path = function_dir_path / "initializer.mcfunction"
        with open(initializer_path, "w") as f:
            # 初始化常量池和stringlib库
            f.write(ScoreboardBuilder.add_objective(context.objective, "dummy", "Main objective") + "\n")
            f.write(FunctionBuilder.run(f"{context.namespace}:literal_pool_init") + "\n")
            f.write(FunctionBuilder.run("stringlib:zprivate/load") + "\n")
            f.write(DataBuilder.modify_storage_set_value("stringlib:input", "concat", "['','']") + "\n")

            # 执行初始化函数
            for init_function in self.init_functions:
                f.write(FunctionBuilder.run(f"{context.namespace}:{init_function}") + "\n")

            if context.config.debug:
                f.write(f"say Datapack '{context.config.namespace}' is initialized\n")

    def get_name(self) -> str:
        return "initializer_function_writer"
