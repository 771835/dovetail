from transpiler.core.backend import GenerationContext
from transpiler.core.symbols import Variable, Constant, Reference
from .. import CommandRegistry, TemplateRegistry
from ..base import TemplateCommandHandler
from ..template import CommandTemplate
from ... import Copy, DataPath, StorageLocation


@CommandRegistry.register("randint")
class RandintCommand(TemplateCommandHandler):

    def _pre_process(
            self,
            result: Variable | Constant | None,
            context: GenerationContext,
            args: dict[str, Reference]
    ) -> None:
        self.register_template_auto(context.objective)
        self.template_name = f"randint_{context.objective}"

    def _post_process(
            self,
            result: Variable | Constant | None,
            context: GenerationContext,
            args: dict[str, Reference]
    ) -> None:
        context.current_scope.add_command(
            Copy.copy(
                DataPath(
                    context.current_scope.get_symbol_path(result),
                    context.objective,
                    StorageLocation.get_storage(result.dtype)
                ),
                DataPath(
                    "output_randint",
                    context.objective
                )
            )
        )

    def register_template_auto(self, objective: str):
        if not TemplateRegistry.has(f"randint_{objective}"):
            TemplateRegistry.register(
                CommandTemplate(
                    name=f"randint_{objective}",
                    template=f"execute store result score output_randint {objective} run random value $(min)..$(max)",
                    function_path=f"builtins/random/randint_{objective}",
                    param_names=["min", "max"],
                    description="生成随机数到指定位置(自动生成模板，提前填写objective)",
                    tags=["random", "math"],
                    validator=lambda p: (
                        int(p['min']) <= int(p['max']),
                        "min must be less than or equal to max"
                    )
                )
            )
