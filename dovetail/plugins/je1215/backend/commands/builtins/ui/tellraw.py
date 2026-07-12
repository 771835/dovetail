# coding=utf-8
from ..base import CommandRegistry, TemplateCommandHandler
from ..template import TemplateParameter, ParameterBuilder
from ...tools import LiteralPoolTools


@CommandRegistry.register('tellraw_text')
class TellrawTextCommand(TemplateCommandHandler):
    """Tellraw 文本命令"""

    template_name = "tellraw_nbt"

    def build_params(self, result, context, args, template):
        builder = ParameterBuilder(context.current_scope, context.objective)
        params = builder.build_all(args, ["target"])

        msg_param = builder.build("msg", args["msg"])
        if msg_param.is_literal():
            path = LiteralPoolTools.get_literal_path_str(msg_param.value)
        else:
            path = msg_param.storage_path

        params["path"] = TemplateParameter.literal("path", path)
        params["objective"] = TemplateParameter.literal("objective", context.objective)
        return params


@CommandRegistry.register('tellraw_json')
class TellrawJsonCommand(TemplateCommandHandler):
    """Tellraw JSON 命令"""

    template_name = "tellraw"

    def build_params(self, result, context, args, template):
        builder = ParameterBuilder(context.current_scope, context.objective)
        return builder.build_all(args, ["target", "json"])