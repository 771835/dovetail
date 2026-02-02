"""
初始化函数写入器

写入初始化函数
初始化函数行为:
- 初始化计分板
- 调用常量池初始化
- 对特殊位置预填充数据
- 输出项目启动信息(可选)
"""
from transpiler.core.backend import OutputWriter, GenerationContext
from .commands import FunctionBuilder, DataBuilder, ScoreboardBuilder


class InitializerFunctionWriter(OutputWriter):
    def write(self, context: GenerationContext):
        function_dir_path = context.target / context.namespace / "data" / context.namespace / "function"
        function_dir_path.mkdir(parents=True, exist_ok=True)
        initializer_path = function_dir_path / "initializer.mcfunction"
        with open(initializer_path, "w") as f:
            f.write(ScoreboardBuilder.add_objective(context.objective, "dummy", "Main objective") + "\n")
            f.write(FunctionBuilder.run(f"{context.namespace}:literal_pool_init") + "\n")
            f.write(DataBuilder.modify_storage_set_value("stringlib:input", "concat", "['','']"))
            if context.config.debug:
                f.write(f"say Datapack '{context.config.namespace}' is initialized\n")

    def get_name(self) -> str:
        return "initializer_function_writer"
