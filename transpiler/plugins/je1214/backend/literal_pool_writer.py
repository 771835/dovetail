# coding=utf-8
"""
常量池写入器

用于收集字面量并将字面量加载
"""
import uuid

from transpiler.core.backend import OutputWriter, GenerationContext
from transpiler.core.enums import ValueType
from transpiler.core.symbols import Reference, Literal
from .commands import ReturnBuilder, Execute, ScoreboardBuilder
from .commands.copy import MCCopy


class LiteralPoolWriter(OutputWriter):
    def write(self, context: GenerationContext):
        function_dir_path = context.target / context.namespace / "data" / context.namespace / "function"
        literal_pool_path = function_dir_path / "literal_pool_init.mcfunction"
        function_dir_path.mkdir(parents=True, exist_ok=True)
        commands = []
        # 记录标志以保证仅加载一次
        flag = uuid.uuid4().hex[:5]

        commands.append(
            Execute.execute().if_score_matches(
                f"literal_pool.flag.{flag}",
                context.objective,
                "1.."
            ).run(ReturnBuilder.return_value("0"))
        )
        commands.append(ScoreboardBuilder.set_score(f"literal_pool.flag.{flag}", context.objective, 9999))

        for literal in self._collect_literals(context):
            commands.append(
                MCCopy.copy_literal_base_type(
                    self.get_literal_path(
                        literal
                    ),
                    context.objective,
                    literal
                )
            )
        with open(literal_pool_path, "w") as f:
            f.write("\n".join(commands))

    @staticmethod
    def _collect_literals(context: GenerationContext):
        literals = set()
        for instr in context.ir_builder:
            for operand in instr.operands:
                if isinstance(operand, Reference) and operand.value_type == ValueType.LITERAL:
                    literals.add(operand.value.value)
                if isinstance(operand, Literal):
                    literals.add(operand.value)
        return literals

    @staticmethod
    def get_literal_path(literal):
        if isinstance(literal, str):
            return f"literal_pool.str.{hash(literal)}"
        elif isinstance(literal, int):
            return f"literal_pool.int.{'n' if literal < 0 else ''}{abs(literal)}"
        else:
            raise TypeError(f"literal type {type(literal)} is not supported")

    def get_name(self) -> str:
        return "LiteralPoolWriter"
