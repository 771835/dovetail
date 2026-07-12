# coding=utf-8
from backend.commands.builtins.base import TemplateCommandHandler, CommandRegistry
from backend.commands.builtins.template import CommandTemplate, TemplateParameter, ParameterBuilder
from dovetail.core.backend import GenerationContext
from dovetail.core.symbols import Variable, Reference

@CommandRegistry.register("array_access_to_score")
class ArrayAccessToScoreCommand(TemplateCommandHandler):
    no_size_effects = True
    template_name = "array_access_to_score"

    def build_params(
            self,
            result: Variable | None,
            context: GenerationContext,
            args: dict[str, Reference],
            template: CommandTemplate
    ) -> dict[str, TemplateParameter]:
        assert result is not None
        array: Variable = args["array"].value
        params = (ParameterBuilder(context.current_scope, context.objective)
                  .build_all(args, ["index"]))
        params["path"] = TemplateParameter.literal("path", context.current_scope.get_symbol_path(result))
        params["objective"] = TemplateParameter.literal("objective", context.objective)
        params["score"] = TemplateParameter.literal("score", context.current_scope.get_symbol_path(result))
        params["source_path"] = TemplateParameter.literal("source_path", context.current_scope.get_symbol_path(array))
        return params


@CommandRegistry.register("array_access_to_storage")
class ArrayAccessToStorageCommand(TemplateCommandHandler):
    no_size_effects = True
    template_name = "array_access_to_storage"

    def build_params(
            self,
            result: Variable | None,
            context: GenerationContext,
            args: dict[str, Reference],
            template: CommandTemplate
    ) -> dict[str, TemplateParameter]:
        assert result is not None
        array: Variable = args["array"].value
        params = (ParameterBuilder(context.current_scope, context.objective)
                  .build_all(args, ["index"]))
        params["target_path"] = TemplateParameter.literal("target_path", context.current_scope.get_symbol_path(result))
        params["target"] = TemplateParameter.literal("target", context.objective)
        params["score"] = TemplateParameter.literal("score", context.current_scope.get_symbol_path(result))
        params["source_path"] = TemplateParameter.literal("source_path", context.current_scope.get_symbol_path(array))
        return params