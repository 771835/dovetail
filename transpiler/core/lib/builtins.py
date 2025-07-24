# coding=utf-8
import uuid
from typing import Callable

from transpiler.core.backend.ir_builder import IRBuilder
from transpiler.core.errors import CompilerSyntaxError, InvalidControlFlowError
from transpiler.core.instructions import IRInstruction, IRRawCmd, IRCast, IRDeclare, IRAssign, IROp, IRScopeBegin, \
    IRJump
from transpiler.core.language_enums import DataType, ValueType, BinaryOps, FunctionType
from transpiler.core.lib.lib_base import Library
from transpiler.core.symbols import Constant, Class, Function, Reference, Variable, Literal


class Builtins(Library):

    def __init__(self, builder: IRBuilder):
        self.builder = builder

        self._constants = {
            Constant("INT_MAX", DataType.INT): Reference(ValueType.LITERAL, Literal(DataType.INT, 2147483647)),
            Constant("INT_MIN", DataType.INT): Reference(ValueType.LITERAL, Literal(DataType.INT, -2147483648)),
        }
        self._functions: dict[Function, Callable[..., Variable | Constant | Literal]] = {
            Function(
                "exec",
                [
                    Variable("command", DataType.STRING)
                ],
                DataType.INT,
                FunctionType.BUILTIN
            ): self._exec,
            Function(
                "int",
                [
                    Variable("value", DataType.STRING)
                ],
                DataType.INT,
                FunctionType.BUILTIN
            ): self._int,
            Function(
                "str",
                [
                    Variable("value", DataType.INT)
                ],
                DataType.STRING,
                FunctionType.BUILTIN
            ): self._exec,
            Function(
                "print",
                [
                    Variable("msg", DataType.STRING)
                ],
                DataType.INT,
                FunctionType.BUILTIN
            ): self._print,
            Function(
                "strcat",
                [
                    Variable("dest", DataType.STRING),
                    Variable("src", DataType.STRING)
                ],
                DataType.STRING,
                FunctionType.BUILTIN
            ): self._strcat,
            Function(
                "_call",
                [
                    Variable("scope", DataType.STRING),
                ],
                DataType.INT,
                FunctionType.BUILTIN
            ): self._call,

        }

    def _exec(self, command: Reference[Variable | Constant | Literal]) -> Literal:
        self.builder.insert(IRRawCmd(command))
        return Literal(DataType.INT, 0)

    def _int(self, value: Reference[Variable | Constant | Literal]) -> Variable:
        result: Variable = Variable(uuid.uuid4().hex, DataType.INT)
        self.builder.insert(IRCast(result, DataType.INT, value))
        return result

    def _str(self, value: Reference[Variable | Constant | Literal]) -> Variable:
        result: Variable = Variable(uuid.uuid4().hex, DataType.STRING)
        self.builder.insert(IRCast(result, DataType.STRING, value))
        return result

    def _print(self, msg: Reference[Variable | Constant | Literal]) -> Literal:

        if msg.value_type == ValueType.LITERAL:
            self.builder.insert(
                IRRawCmd(Reference(ValueType.LITERAL, Literal(DataType.STRING, f"tellraw @a \"{msg.value.value}\""))))
        else:
            temp_var = Variable(uuid.uuid4().hex, DataType.STRING)
            self.builder.insert(IRDeclare(temp_var))
            self.builder.insert(
                IRAssign(temp_var, Reference(ValueType.LITERAL, Literal(DataType.STRING, "tellraw @a \""))))
            temp_var2 = Variable(uuid.uuid4().hex, DataType.STRING)
            self.builder.insert(IRDeclare(temp_var2))
            self.builder.insert(
                IROp(temp_var2, BinaryOps.ADD, Reference(ValueType.VARIABLE, temp_var), msg))
            temp_var3 = Variable(uuid.uuid4().hex, DataType.STRING)
            self.builder.insert(IRDeclare(temp_var3))
            self.builder.insert(
                IROp(temp_var3, BinaryOps.ADD, Reference(ValueType.VARIABLE, temp_var2),
                     Reference(ValueType.LITERAL, Literal(DataType.STRING, "\""))))
            self.builder.insert(IRRawCmd(Reference(ValueType.VARIABLE, temp_var3)))

        return Literal(DataType.INT, 0)

    def _strcat(self, dest: Reference[Variable | Constant | Literal],
                src: Reference[Variable | Constant | Literal]) -> Variable:
        var = Variable(uuid.uuid4().hex, DataType.STRING)
        self.builder.insert(IRDeclare(var))
        self.builder.insert(IROp(var, BinaryOps.ADD, dest, src))
        return var

    def _call(self, scope: Reference[Literal]):
        if scope.value_type != ValueType.LITERAL:
            raise CompilerSyntaxError(
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

    def _type_of(self, value):
        return Literal(DataType.STRING, repr(value))
    def __str__(self) -> str:
        return "built-in"

    def load(self) -> list[IRInstruction]:
        return []

    def get_functions(self) -> dict[Function, Callable[..., Variable | Constant | Literal]]:
        return self._functions

    def get_constants(self) -> dict[Constant, Reference]:
        return self._constants

    def get_events(self) -> dict[str, Callable[..., list[IRInstruction]]]:
        """获取事件及其处理函数的映射"""
        return {}

    def get_annotations(self) -> dict[str, Callable[..., list[IRInstruction]]]:
        """获取注解及其处理函数的映射"""
        return {}

    def get_classes(self) -> list[Class]:
        """获取库中定义的所有类"""
        return []
