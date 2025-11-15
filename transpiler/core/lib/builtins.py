# coding=utf-8
import uuid
from typing import Callable

from transpiler.core.enums.operations import BinaryOps
from transpiler.core.enums.types import FunctionType, DataType, ValueType
from transpiler.core.errors import ASTSyntaxError, InvalidControlFlowError
from transpiler.core.instructions import IRInstruction, IRCast, IRDeclare, IROp, IRScopeBegin, \
    IRJump, IRCall
from transpiler.core.ir_builder import IRBuilder
from transpiler.core.lib.library import Library
from transpiler.core.symbols import Constant, Class, Function, Reference, Variable, Literal, Parameter
from transpiler.utils.naming import NameNormalizer


class Builtins(Library):

    def __init__(self, builder: IRBuilder):
        self.builder = builder
        self._constants = {}
        self._functions: dict[Function, Callable[..., Variable | Constant | Literal]] = {
            Function(
                "int",
                [
                    Parameter(Variable("value", DataType.STRING))
                ],
                DataType.INT,
                FunctionType.LIBRARY
            ): self._int,
            Function(
                "str",
                [
                    Parameter(Variable("value", DataType.INT))
                ],
                DataType.STRING,
                FunctionType.LIBRARY
            ): self._str,
            Function(
                NameNormalizer.normalize("str_i"),
                [
                    Parameter(Variable("value", DataType.INT))
                ],
                DataType.STRING,
                FunctionType.LIBRARY
            ): self._str,
            Function(
                NameNormalizer.normalize("str_b"),
                [
                    Parameter(Variable("value", DataType.BOOLEAN))
                ],
                DataType.STRING,
                FunctionType.LIBRARY
            ): self._str,
            Function(
                "print",
                [
                    Parameter(Variable("msg", DataType.STRING))
                ],
                DataType.INT,
                FunctionType.LIBRARY
            ): self._print,
            Function(
                "strcat",
                [
                    Parameter(Variable("dest", DataType.STRING)),
                    Parameter(Variable("src", DataType.STRING))
                ],
                DataType.STRING,
                FunctionType.LIBRARY
            ): self._strcat,
            Function(
                "__call",
                [
                    Parameter(Variable("scope", DataType.STRING)),
                ],
                DataType.INT,
                FunctionType.LIBRARY
            ): self._call,
            Function(
                "exec",
                [
                    Parameter(Variable("command", DataType.STRING))
                ],
                DataType.NULL,
                FunctionType.BUILTIN
            ): None,
            Function(
                "tellraw_text",
                [
                    Parameter(Variable("target", DataType.STRING)),
                    Parameter(Variable("msg", DataType.STRING)),
                ],
                DataType.NULL,
                FunctionType.BUILTIN
            ): None,
            Function(
                "tellraw_json",
                [
                    Parameter(Variable("target", DataType.STRING)),
                    Parameter(Variable("json", DataType.STRING)),
                ],
                DataType.NULL,
                FunctionType.BUILTIN
            ): None,
            Function(
                "setblock",
                [
                    Parameter(Variable("x", DataType.INT)),
                    Parameter(Variable("y", DataType.INT)),
                    Parameter(Variable("z", DataType.INT)),
                    Parameter(Variable("block_id", DataType.STRING)),
                    Parameter(Variable("mode", DataType.STRING), optional=True, default=Reference.literal("destroy")),
                ],
                DataType.INT,
                FunctionType.BUILTIN
            ): None,
        }
        """
        
            Function(
                "item_spawn",
                [
                    Parameter(Variable("x", DataType.INT)),
                    Parameter(Variable("y", DataType.INT)),
                    Parameter(Variable("z", DataType.INT)),
                    Parameter(Variable("item_id", DataType.STRING)),
                    Parameter(Variable("count", DataType.INT), True)
                ],
                DataType.INT,
                FunctionType.BUILTIN
            ): None,
            Function(
                "tp",
                [
                    Parameter(Variable("player", DataType.STRING)),
                    Parameter(Variable("x", DataType.INT)),
                    Parameter(Variable("y", DataType.INT)),
                    Parameter(Variable("z", DataType.INT))
                ],
                DataType.INT,
                FunctionType.BUILTIN
            ): None,
            Function(
                "give",
                [
                    Parameter(Variable("player", DataType.STRING)),
                    Parameter(Variable("item_id", DataType.STRING)),
                    Parameter(Variable("count", DataType.INT), True)
                ],
                DataType.INT,
                FunctionType.BUILTIN
            ): None,
            Function(
                "summon",
                [
                    Parameter(Variable("entity_id", DataType.STRING)),
                    Parameter(Variable("x", DataType.INT)),
                    Parameter(Variable("y", DataType.INT)),
                    Parameter(Variable("z", DataType.INT)),
                    Parameter(Variable("nbt", DataType.STRING), True)
                ],
                DataType.INT,
                FunctionType.BUILTIN
            ): None,
            Function(
                "kill",
                [Parameter(Variable("target", DataType.STRING))],
                DataType.INT,
                FunctionType.BUILTIN
            ): None,
            Function(
                "time_set",
                [Parameter(Variable("value", DataType.INT))],
                DataType.INT,
                FunctionType.BUILTIN
            ): None,
            Function(
                "weather",
                [Parameter(Variable("type", DataType.STRING))],
                DataType.INT,
                FunctionType.BUILTIN
            ): None,
            Function(
                "difficulty",
                [Parameter(Variable("level", DataType.STRING))],
                DataType.INT,
                FunctionType.BUILTIN
            ): None,
            Function(
                "gamerule",
                [
                    Parameter(Variable("rule", DataType.STRING)),
                    Parameter(Variable("value", DataType.STRING))
                ],
                DataType.INT,
                FunctionType.BUILTIN
            ): None,
            Function(
                "fill",
                [
                    Parameter(Variable("x1", DataType.INT)),
                    Parameter(Variable("y1", DataType.INT)),
                    Parameter(Variable("z1", DataType.INT)),
                    Parameter(Variable("x2", DataType.INT)),
                    Parameter(Variable("y2", DataType.INT)),
                    Parameter(Variable("z2", DataType.INT)),
                    Parameter(Variable("block", DataType.STRING))
                ],
                DataType.INT,
                FunctionType.BUILTIN
            ): None,
            Function(
                "effect",
                [
                    Parameter(Variable("target", DataType.STRING)),
                    Parameter(Variable("effect", DataType.STRING)),
                    Parameter(Variable("duration", DataType.INT), True),
                    Parameter(Variable("amplifier", DataType.INT), True)
                ],
                DataType.INT,
                FunctionType.BUILTIN
            ): None,
            Function(
                "attribute",
                [
                    Parameter(Variable("target", DataType.STRING)),
                    Parameter(Variable("attr", DataType.STRING)),
                    Parameter(Variable("value", DataType.STRING), True)
                ],
                DataType.INT,
                FunctionType.BUILTIN
            ): None,
            Function(
                "tag",
                [
                    Parameter(Variable("target", DataType.STRING)),
                    Parameter(Variable("action", DataType.STRING)),
                    Parameter(Variable("tag", DataType.STRING))
                ],
                DataType.INT,
                FunctionType.BUILTIN
            ): None,
            Function(
                "damage",
                [
                    Parameter(Variable("target", DataType.STRING)),
                    Parameter(Variable("amount", DataType.INT)),
                    Parameter(Variable("source", DataType.STRING), True)
                ],
                DataType.INT,
                FunctionType.BUILTIN
            ): None,
            Function(
                "scoreboard",
                [
                    Parameter(Variable("op", DataType.STRING)),
                    Parameter(Variable("target", DataType.STRING)),
                    Parameter(Variable("objective", DataType.STRING)),
                    Parameter(Variable("value", DataType.STRING), True)
                ],
                DataType.INT,
                FunctionType.BUILTIN
            ): None,
            Function(
                "bossbar",
                [
                    Parameter(Variable("op", DataType.STRING)),
                    Parameter(Variable("id", DataType.STRING)),
                    Parameter(Variable("value", DataType.STRING), True)
                ],
                DataType.INT,
                FunctionType.BUILTIN
            ): None,
            """

    def _int(self, value: Reference[Variable | Constant | Literal]) -> Variable:
        result: Variable = Variable(uuid.uuid4().hex, DataType.INT)
        self.builder.insert(IRDeclare(result))
        self.builder.insert(IRCast(result, DataType.INT, value))
        return result

    def _str(self, value: Reference[Variable | Constant | Literal]) -> Variable:
        result: Variable = Variable(uuid.uuid4().hex, DataType.STRING)
        self.builder.insert(IRDeclare(result))
        self.builder.insert(IRCast(result, DataType.STRING, value))
        return result

    def _print(self, msg: Reference[Variable | Constant | Literal]) -> Literal:
        self.builder.insert(
            IRCall(
                None,
                next((function for function in self._functions if function.name == "tellraw_text"), None),
                {
                    "target": Reference.literal("@a"),
                    "msg": msg
                }
            )
        )
        return Literal(DataType.NULL, None)

    def _strcat(self, dest: Reference[Variable | Constant | Literal],
                src: Reference[Variable | Constant | Literal]) -> Variable:
        var = Variable(uuid.uuid4().hex, DataType.STRING)
        self.builder.insert(IRDeclare(var))
        self.builder.insert(IROp(var, BinaryOps.ADD, dest, src))
        return var

    def _call(self, scope: Reference[Literal]):
        if scope.value_type != ValueType.LITERAL:
            raise ASTSyntaxError(
                "跳转目标必须是字面量字符串"
            )
        exist = False
        for instr in reversed(self.builder.get_instructions()):
            if isinstance(instr, IRScopeBegin):
                if instr.get_operands()[0] == scope.value.value:
                    exist = True
        if exist:
            self.builder.insert(IRJump(scope.value.value))
        else:
            raise InvalidControlFlowError(
                f"跳转目标作用域 '{scope.value.value}' 不存在"
            )
        return Literal(DataType.INT, 1)

    def _type_of(self, value: Reference[Variable | Constant | Literal]):
        return Literal(DataType.STRING, str(value.get_data_type()))

    def __str__(self) -> str:
        return "built-in"

    def load(self) -> list[IRInstruction]:
        return []

    def get_functions(self) -> dict[Function, Callable[..., Variable | Constant | Literal]]:
        return self._functions

    def get_constants(self) -> dict[Constant, Reference]:
        return self._constants

    def get_classes(self) -> dict[Class, dict[str, Callable[..., Variable | Constant | Literal]]]:
        return {}
