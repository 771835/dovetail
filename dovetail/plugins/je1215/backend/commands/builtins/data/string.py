# coding=utf-8
from dovetail.core.backend import GenerationContext
from dovetail.core.symbols import Variable, Reference, Literal
from ..base import CommandRegistry, CommandHandler, TemplateCommandHandler
from ..template import TemplateParameter, ParameterBuilder
from ... import Copy, DataPath, Execute, DataBuilder, LiteralPoolTools

@CommandRegistry.register("strcat_fast")
class StrcatFastCommand(TemplateCommandHandler):
    no_size_effects = True
    template_name = "strcat_fast"
    def build_params(self, result, context, args, template):
        assert result is not None
        builder = ParameterBuilder(context.current_scope, context.objective)
        params = builder.build_all(args, ["dest", "src"])
        params["target"] = TemplateParameter.literal("target", context.objective)
        params["path"] = TemplateParameter.literal("path", context.current_scope.get_symbol_path(result))
        return params


@CommandRegistry.register("strlen")
class StrlenCommand(CommandHandler):
    no_size_effects = True

    def handle(self, result: Variable | None, context: GenerationContext,
               args: dict[str, Reference]) -> None:
        assert result is not None
        s: Variable | Literal = args["s"].value
        result_path = DataPath.from_symbol(context, result)
        s_path = DataPath.from_symbol(context, s)

        if isinstance(s, Literal):
            context.add_command(Copy.copy_literals(result_path, len(str(s.value))))
        else:
            context.add_command(
                Execute.execute()
                .store_result_score(*result_path)
                .run(DataBuilder.get_storage(*reversed(s_path)))
            )


@CommandRegistry.register("substring")
class SubstringCommand(TemplateCommandHandler):
    no_size_effects = True
    template_name = "substring"

    def build_params(self, result, context, args, template):
        assert result is not None
        builder = ParameterBuilder(context.current_scope, context.objective)

        s = args["s"].value
        s_path = (LiteralPoolTools.get_literal_path_str(s.value)
                  if isinstance(s, Literal)
                  else context.current_scope.get_symbol_path(s))

        params = {
            "target": TemplateParameter.literal("target", context.objective),
            "path": TemplateParameter.literal("path", context.current_scope.get_symbol_path(result)),
            "source": TemplateParameter.literal("source", context.objective),
            "source_path": TemplateParameter.literal("source_path", s_path),
        }

        for name in ["start", "end"]:
            if name in args:
                params[name] = builder.build(name, args[name])

        return params