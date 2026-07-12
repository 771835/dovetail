# coding=utf-8
from ..base import CommandRegistry, TemplateCommandHandler
from ..template import TemplateParameter, ParameterBuilder
from ... import Copy, DataPath, StorageLocation


@CommandRegistry.register("randint")
class RandintCommand(TemplateCommandHandler):
    no_size_effects = True
    template_name = "randint"

    def build_params(self, result, context, args, template):
        builder = ParameterBuilder(context.current_scope, context.objective)
        params = builder.build_all(args, ["min", "max"])
        params["objective"] = TemplateParameter.literal("objective", context.objective)
        return params

    def _post_process(self, result, context, args):
        # 为了简化模板的产生，
        assert result is not None
        context.current_scope.add_command(
            Copy.copy(
                DataPath(
                    context.current_scope.get_symbol_path(result),
                    context.objective,
                    StorageLocation.get_storage(result.dtype)
                ),
                DataPath("output_randint", context.objective)
            )
        )

@CommandRegistry.register("randint_fast")
class RandintCommand(TemplateCommandHandler):
    no_size_effects = True
    template_name = "randint_fast"

    def build_params(self, result, context, args, template):
        assert result is not None
        builder = ParameterBuilder(context.current_scope, context.objective)
        params = builder.build_all(args, ["min", "max"])
        params["objective"] = TemplateParameter.literal("objective", context.objective)
        params["path"] = TemplateParameter.literal("path", context.current_scope.get_symbol_path(result))
        return params

    def _post_process(self, result, context, args):
        # 为了简化模板的产生，
        assert result is not None
        context.current_scope.add_command(
            Copy.copy(
                DataPath(
                    context.current_scope.get_symbol_path(result),
                    context.objective,
                    StorageLocation.get_storage(result.dtype)
                ),
                DataPath("output_randint", context.objective)
            )
        )