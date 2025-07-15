# coding=utf-8
from __future__ import annotations

from pathlib import Path
from typing import Callable

from mcfdsl.core.backend.code_generator.c_je_1204.code_generator_scope import CodeGeneratorScope
from mcfdsl.core.backend.code_generator.c_je_1204.command_builder import FunctionBuilder, BasicCommands, Execute
from mcfdsl.core.backend.instructions import IROpCode, IRInstruction
from mcfdsl.core.backend.ir_builder import IRBuilder
from mcfdsl.core.backend.specification import CodeGeneratorSpec, MinecraftVersion, MinecraftEdition
from mcfdsl.core.language_enums import StructureType, ValueType, DataType
from mcfdsl.core.symbols import Variable, Constant, Function, Literal, Reference, Class


class CodeGenerator(CodeGeneratorSpec):
    def __init__(self, builder: IRBuilder, target: Path, debug: bool = False, namespace: str = "example"):
        self.debug = debug
        self.target = target
        self.builder = builder
        self.namespace = namespace
        self.top_scope = CodeGeneratorScope(
            "global",
            None,
            StructureType.GLOBAL,
            self.namespace)
        self.var_objective = "var"
        self.current_scope = self.top_scope

    @classmethod
    def is_support(cls, version: MinecraftVersion) -> bool:
        if version.major == 1 and version.minor == 20 and version.patch == 4 and version.edition == MinecraftEdition.JAVA_EDITION:
            return True
        else:
            return False

    def generate_commands(self):
        iterator = self.builder.__iter__()
        handlers: dict[IROpCode, Callable[[IRInstruction], None]] = {
            # ===== 控制流指令 (0x00-0x1F) =====
            IROpCode.JUMP: self._jump,  # 0x00
            IROpCode.COND_JUMP: self._cond_jump,  # 0x01
            IROpCode.FUNCTION: self._function,  # 0x02
            IROpCode.CALL: self._call,  # 0x03
            IROpCode.CALL_INLINE: self._call,  # 0x04 - 复用CALL处理
            IROpCode.RETURN: self._return,  # 0x05
            IROpCode.SCOPE_BEGIN: self._scope_begin,  # 0x06
            IROpCode.SCOPE_END: self._scope_end,  # 0x07
            IROpCode.BREAK: self._break,  # 0x08
            IROpCode.CONTINUE: self._continue,  # 0x09

            # ===== 变量操作指令 (0x20-0x3F) =====
            IROpCode.DECLARE: self._declare,  # 0x20
            IROpCode.VAR_RELEASE: self._var_release,  # 0x21
            IROpCode.ASSIGN: self._assign,  # 0x22
            IROpCode.UNARY_OP: self._unary_op,  # 0x23
            IROpCode.OP: self._op,  # 0x24
            IROpCode.COMPARE: self._compare,  # 0x25

            # ===== 面向对象指令 (0x40-0x5F) =====
            IROpCode.CLASS: self._class_def,  # 0x40
            IROpCode.NEW_OBJ: self._new_object,  # 0x41
            IROpCode.GET_FIELD: self._get_field,  # 0x42
            IROpCode.SET_FIELD: self._set_field,  # 0x43
            IROpCode.CALL_METHOD: self._call_method,  # 0x44

            # ===== 命令生成指令 (0x60-0x7F) =====
            IROpCode.RAW_CMD: self._raw_command,  # 0x60
        }
        for instr in iterator:
            handler = handlers.get(instr.opcode, lambda instr: None)
            if handler:
                handler(instr)
            else:
                if hasattr(self, "_" + instr.opcode.name):
                    if callable(getattr(self, "_" + instr.opcode.name)):
                        getattr(self, "_" + instr.opcode.name)(instr.opcode)
                        continue
                raise  # TODO:补充报错

    def _scope_begin(self, instr: IRInstruction):
        name: str = instr.get_operands()[0]
        stype: StructureType = instr.get_operands()[1]
        self.current_scope = self.current_scope.create_child(name, stype)

    def _scope_end(self, instr: IRInstruction):
        self.current_scope = self.current_scope.parent

    def _break(self, instr: IRInstruction):
        ...

    def _continue(self, instr: IRInstruction):
        ...

    def _function(self, instr: IRInstruction):
        ...

    def _return(self, instr: IRInstruction):
        ...

    def _var_release(self, instr: IRInstruction):
        ...

    def _jump(self, instr: IRInstruction):
        scope_name: str = instr.get_operands()[0]
        jump_scope = self.current_scope.resolve_scope(scope_name)
        self.current_scope.add_command(FunctionBuilder.run(jump_scope.get_minecraft_function_path()))

    def _cond_jump(self, instr: IRInstruction):
        cond_var: Variable = instr.get_operands()[0]
        true_scope_name: str = instr.get_operands()[1]
        false_scope_name: str = instr.get_operands()[2]
        if true_scope_name:
            true_jump_scope = self.current_scope.resolve_scope(true_scope_name)
            self.current_scope.add_command(
                Execute.execute().if_score_matches(self.current_scope.get_symbol_path(cond_var.get_name()),
                                                   self.var_objective, "1").run(
                    FunctionBuilder.run(true_jump_scope.get_minecraft_function_path())))
        if false_scope_name:
            false_jump_scope = self.current_scope.resolve_scope(false_scope_name)
            self.current_scope.add_command(
                Execute.execute().unless_score_matches(self.current_scope.get_symbol_path(cond_var.get_name()),
                                                       self.var_objective, "1").run(
                    FunctionBuilder.run(false_jump_scope.get_minecraft_function_path())))

    def _call(self, instr: IRInstruction):
        result: Variable | Constant = instr.get_operands()[0]
        func: Function = instr.get_operands()[1]
        args: list[Reference[Variable | Constant | Literal]] = instr.get_operands()[2]
        jump_scope = self.current_scope.resolve_scope(func.name)
        # TODO:..
        for arg in args:
            pass
        self.current_scope.add_command(FunctionBuilder.run(jump_scope.get_minecraft_function_path()))

    def _assign(self, instr: IRInstruction):
        target: Variable | Constant = instr.get_operands()[0]
        source: Reference[Variable | Constant | Literal] = instr.get_operands()[1]
        if isinstance(target.dtype, DataType):
            if source.value_type == ValueType.LITERAL:
                BasicCommands.Copy.copy_literal_base_type(target, self.current_scope, self.var_objective, source.value)
            elif source.value_type in (ValueType.VARIABLE, ValueType.CONSTANT):
                BasicCommands.Copy.copy_variable_base_type(source.value, self.current_scope, self.var_objective, target,
                                                           self.current_scope, self.var_objective)
        else:  # Class
            assert isinstance(target.dtype, Class)
            pass  # TODO:实现类的赋值

    def _unary_op(self, instr: IRInstruction):
        pass  # 因该dsl内不存在直接性的位运算，故不实现，

    def _declare(self, instr: IRInstruction):
        self.current_scope.add_symbol(instr.get_operands()[0])

    def _raw_command(self, instr: IRInstruction):
        command: Reference[Variable | Constant | Literal] = instr.get_operands()[0]
        if command.value_type == ValueType.LITERAL:
            self.current_scope.add_command(str(command.value.value))
        else:
            self.current_scope.add_command(
                FunctionBuilder.run_with_source(f"{self.namespace}:builtins/exec", "storage", ...))  # TODO
