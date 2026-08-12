# coding=utf-8
from ..base import CommandRegistry, TemplateCommandHandler
from ..template import TemplateParameter, ParameterBuilder


@CommandRegistry.register("data_get_block")
class DataGetBlock(TemplateCommandHandler):
    no_size_effects = True
    template_name = "data_get_block"

    def build_params(self, result, context, args, template):
        assert result is not None
        builder = ParameterBuilder(context.current_scope, context.objective)
        params = builder.build_all(args, ["x", "y", "z", "path"])
        params["target_path"] = TemplateParameter.literal(
            "target_path", context.current_scope.get_symbol_path(result))
        params["target"] = TemplateParameter.literal("target", context.objective)
        return params


@CommandRegistry.register("data_get_entity")
class DataGetEntity(TemplateCommandHandler):
    no_size_effects = True
    template_name = "data_get_entity"

    def build_params(self, result, context, args, template):
        assert result is not None
        builder = ParameterBuilder(context.current_scope, context.objective)
        params = builder.build_all(args, ["source", "path"])
        params["target_path"] = TemplateParameter.literal(
            "target_path", context.current_scope.get_symbol_path(result))
        params["target"] = TemplateParameter.literal("target", context.objective)
        return params


@CommandRegistry.register("data_get_storage")
class DataGetStorage(TemplateCommandHandler):
    no_size_effects = True
    template_name = "data_get_storage"

    def build_params(self, result, context, args, template):
        assert result is not None
        builder = ParameterBuilder(context.current_scope, context.objective)
        params = builder.build_all(args, ["source", "path"])
        params["target_path"] = TemplateParameter.literal(
            "target_path", context.current_scope.get_symbol_path(result))
        params["target"] = TemplateParameter.literal("target", context.objective)
        return params


@CommandRegistry.register("data_get_block_int")
class DataGetBlockInt(TemplateCommandHandler):
    no_size_effects = True
    template_name = "data_get_block_int"

    def build_params(self, result, context, args, template):
        assert result is not None
        builder = ParameterBuilder(context.current_scope, context.objective)
        params = builder.build_all(args, ["x", "y", "z", "path", "scale"])
        params["target"] = TemplateParameter.literal(
            "target", context.current_scope.get_symbol_path(result))
        params["objective"] = TemplateParameter.literal("objective", context.objective)
        return params


@CommandRegistry.register("data_get_entity_int")
class DataGetEntityInt(TemplateCommandHandler):
    no_size_effects = True
    template_name = "data_get_entity_int"

    def build_params(self, result, context, args, template):
        assert result is not None
        builder = ParameterBuilder(context.current_scope, context.objective)
        params = builder.build_all(args, ["source", "path", "scale"])
        params["target"] = TemplateParameter.literal(
            "target", context.current_scope.get_symbol_path(result))
        params["objective"] = TemplateParameter.literal("objective", context.objective)
        return params


@CommandRegistry.register("data_get_storage_int")
class DataGetStorageInt(TemplateCommandHandler):
    no_size_effects = True
    template_name = "data_get_storage_int"

    def build_params(self, result, context, args, template):
        assert result is not None
        builder = ParameterBuilder(context.current_scope, context.objective)
        params = builder.build_all(args, ["source", "path", "scale"])
        params["target"] = TemplateParameter.literal(
            "target", context.current_scope.get_symbol_path(result))
        params["objective"] = TemplateParameter.literal("objective", context.objective)
        return params
