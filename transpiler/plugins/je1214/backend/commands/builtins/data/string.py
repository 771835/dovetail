# coding=utf-8
from functools import lru_cache

from transpiler.core.backend import GenerationContext
from transpiler.core.symbols import Variable, Constant, Reference, Literal
from .. import TemplateRegistry
from ..base import CommandHandler, TemplateCommandHandler
from ..template import CommandTemplate
from ... import Copy, DataPath, StorageLocation, Execute, DataBuilder, LiteralPoolTools
from ...builtins import CommandRegistry


@CommandRegistry.register("strlen")
class StrlenCommand(CommandHandler):
    def handle(self, result: Variable | Constant | None, context: GenerationContext,
               args: dict[str, Reference]) -> None:
        if result is None:
            return
        s: Variable | Constant | Literal = args["s"].value
        result_path = DataPath(context.current_scope.get_symbol_path(result), context.objective)
        s_path = DataPath(context.current_scope.get_symbol_path(s), context.objective, StorageLocation.STORAGE)

        if isinstance(s, Literal):
            context.add_command(Copy.copy_literals(result_path, len(s.value)))
        else:
            context.add_command(
                Execute.execute()
                .store_result_score(*result_path)
                .run(
                    DataBuilder.get_storage(*reversed(s_path))
                )
            )


@CommandRegistry.register("substring")
class SubstringCommand(TemplateCommandHandler):

    def _pre_process(
            self,
            result: Variable | Constant | None,
            context: GenerationContext,
            args: dict[str, Reference]
    ) -> None:
        """处理模板前执行的处理程序"""
        s = args["s"].value

        result_path = context.current_scope.get_symbol_path(result)
        if isinstance(s, Literal):
            s_path = LiteralPoolTools.get_literal_path_str(s.value)
        else:
            s_path = context.current_scope.get_symbol_path(s)

        self.register_template_auto(context.objective, context.objective, result_path, s_path)
        self.template_name = self._get_template_name(context.objective, context.objective, result_path, s_path)

    def register_template_auto(self, target1: str, target2: str, path1: str, path2: str):
        if not TemplateRegistry.has(self._get_template_name(target1, target2, path1, path2)):
            TemplateRegistry.register(
                CommandTemplate(
                    name=self._get_template_name(target1, target2, path1, path2),
                    template=f"data modify storage {target1} {path1} set string storage {target2} {path2} $(start) $(end)",
                    function_path=f"builtins/string/{self._get_template_name(target1, target2, path1, path2)}",
                    param_names=[],
                    optional_params={"start": "0", "end": "9999"},
                    description="截取字符串切片(自动生成模板)",
                    tags=["string", "data", "shortcut"]
                )
            )

    @lru_cache(maxsize=20)
    def _get_template_name(self, target1: str, target2: str, path1: str, path2: str) -> str:
        prefix = f"{target1}_{target2}_{hash(path1)}_{hash(path2)}"
        return f"substring_{prefix}_{hash(prefix)}"
