# coding=utf-8
from ..base import CommandRegistry, TemplateCommandHandler
from ..template import TemplateParameter, ParameterBuilder


@CommandRegistry.register("to_integer")
class ToIntegerCommand(TemplateCommandHandler):
    no_size_effects = True
    template_name = "to_integer"

    def build_params(self, result, context, args, template):
        assert result is not None
        builder = ParameterBuilder(context.current_scope, context.objective)
        params = builder.build_all(args, ["value"])
        params["path"] = TemplateParameter.literal(
            "path", context.current_scope.get_symbol_path(result))
        params["objective"] = TemplateParameter.literal(
            "objective", context.objective)
        return params