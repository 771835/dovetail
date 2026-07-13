# coding=utf-8
from typing import cast

from ..base import TemplateCommandHandler, CommandRegistry, CommandHandler
from ..template import CommandTemplate, TemplateParameter, ParameterBuilder
from dovetail.core.backend import GenerationContext
from dovetail.core.symbols import Variable, Reference, Literal
from ... import DataBuilder


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
        params["source"] = TemplateParameter.literal("source", context.objective)
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
        params["source"] = TemplateParameter.literal("source", context.objective)
        params["source_path"] = TemplateParameter.literal("source_path", context.current_scope.get_symbol_path(array))
        return params


@CommandRegistry.register("malloc")
class MallocCommand(CommandHandler):
    no_size_effects = False

    def handle(self, result: Variable | None, context: GenerationContext, args: dict[str, Reference]) -> None:
        array: Variable = args["array"].value
        size: Variable | Literal = args["size"].value

        if isinstance(size, Literal):
            size_t = int(cast(int, size.value))
            context.current_scope.add_command(
                DataBuilder.modify_storage_set_value(
                    context.objective,
                    "temp_array",
                    f"[{'0,'*size_t}]"
                )
            )
            context.current_scope.add_command(
                DataBuilder.modify_storage_append_from_storage(
                    context.objective,
                    context.current_scope.get_symbol_path(array),
                    context.objective,
                    "temp_array[]"
                )
            )
        else:
            pass # TODO: 实现对编译期未知的情况下的数组槽位分配
