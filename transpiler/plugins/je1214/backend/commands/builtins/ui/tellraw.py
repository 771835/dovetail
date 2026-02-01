from .. import TemplateRegistry
from ..base import CommandRegistry, CommandHandler
from ..template import TemplateEngine, ParameterBuilder, TemplateParameter, CommandTemplate
from ... import LiteralPoolTools


@CommandRegistry.register('tellraw_text')
class TellrawTextCommand(CommandHandler):
    """Tellraw 文本命令"""

    def handle(self, result, context, args):
        engine = TemplateEngine(context.namespace, context.objective)
        builder = ParameterBuilder(context.current_scope, context.objective)

        # 尝试注册简化模板
        self.register_template_auto(context.objective)
        params = builder.build_all(args, ["target", "msg"])
        msg = params.pop("msg")
        if msg.is_literal():
            params["path"] = TemplateParameter.literal(
                "path",
                LiteralPoolTools.get_literal_path_str(
                    msg.value
                )
            )
        else:
            params["path"] = TemplateParameter.literal("path", msg.storage_path)

        commands = engine.render_by_name(f"tellraw_nbt_{context.objective}", params)

        for cmd in commands:
            context.current_scope.add_command(cmd)

    def register_template_auto(self, objective: str):
        if not TemplateRegistry.has(f"tellraw_nbt_{objective}"):
            TemplateRegistry.register(
                CommandTemplate(
                    name=f"tellraw_nbt_{objective}",
                    template=f'tellraw $(target) {{"storage":"{objective}","nbt":"$(path)"}}',
                    function_path=f"builtins/tellraw/tellraw_nbt_{objective}",
                    param_names=["target", "path"],
                    description="向指定目标发送指定nbt路径中的文本消息(自动生成模板，提前填写objective)",
                    tags=["ui", "tellraw", "shortcut"]
                )
            )


@CommandRegistry.register('tellraw_json')
class TellrawJsonCommand(CommandHandler):
    """Tellraw JSON - 展示快捷方式优化"""

    SHORTCUTS = {
        "@a": "tellraw_json_all",
        "@s": "tellraw_json_self",
        "@e": "tellraw_json_entities",
        "@n": "tellraw_json_nearest",
        "@p": "tellraw_json_nearest_player",
        "@r": "tellraw_json_random",
    }

    def handle(self, result, context, args):
        engine = TemplateEngine(context.namespace, context.objective)
        builder = ParameterBuilder(context.current_scope, context.objective)

        target_param = builder.build("target", args["target"])
        json_param = builder.build("json", args["json"])

        # 优化：target 是快捷选择器
        if target_param.is_literal() and target_param.value in self.SHORTCUTS:
            template_name = self.SHORTCUTS[target_param.value]
            commands = engine.render_by_name(template_name, {"json": json_param})
        else:
            # 通用路径
            commands = engine.render_by_name("tellraw_json", {
                "target": target_param,
                "json": json_param
            })

        for cmd in commands:
            context.current_scope.add_command(cmd)
