# coding=utf-8
"""
常量池写入器

用于收集字面量并将字面量加载
"""
import uuid

from transpiler.core.backend import OutputWriter, GenerationContext
from transpiler.core.config import get_project_logger
from transpiler.core.enums import ValueType
from transpiler.core.symbols import Reference, Literal
from .commands import ReturnBuilder, Execute, ScoreboardBuilder
from .commands.copy import Copy
from .commands.tools import LiteralPoolTools


class LiteralPoolWriter(OutputWriter):
    builtin_literals = {1, -1}

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
                Copy.copy_literals(
                    LiteralPoolTools.get_literal_path(literal, context.objective),
                    literal
                )
            )
        with open(literal_pool_path, "w", encoding='utf-8') as f:
            f.write("\n".join(commands))

    @staticmethod
    def _collect_literal(value, literals):
        if isinstance(value, Reference) and value.value_type == ValueType.LITERAL:
            literals.add(value.value.value)
        elif isinstance(value, Literal):
            literals.add(value.value)
        elif isinstance(value, list):
            for item in value:
                LiteralPoolWriter._collect_literal(item, literals)
        elif isinstance(value, dict):
            for key, value in value.items():
                LiteralPoolWriter._collect_literal(value, literals)
        elif value is None:
            literals.add(0)
        else:
            # get_project_logger().warning(f"Unsupported literal '{value}'({type(value)})")
            return

    @staticmethod
    def _collect_literals(context: GenerationContext):
        literals = set()
        for instr in context.ir_builder:
            for operand in instr.operands:
                LiteralPoolWriter._collect_literal(operand, literals)

        # 收集特殊常量以支持编译器的功能
        literals.add(context.objective)
        literals.update(LiteralPoolWriter.builtin_literals)

        return literals

    def get_name(self) -> str:
        return "LiteralPoolWriter"
