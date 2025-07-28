# coding=utf-8
from __future__ import annotations

import os
import uuid
from pathlib import Path
from typing import Callable

from transpiler.core.backend.ir_builder import IRBuilder
from transpiler.core.backend.specification import CodeGeneratorSpec
from transpiler.core.generator_config import MinecraftEdition, GeneratorConfig
from transpiler.core.instructions import IROpCode, IRInstruction
from transpiler.core.language_enums import StructureType, ValueType, DataType, CompareOps, BinaryOps
from transpiler.core.symbols import Variable, Constant, Function, Literal, Reference, Class
from .builtins_func import builtins_func
from .code_generator_scope import CodeGeneratorScope
from .command_builder import FunctionBuilder, BasicCommands, Execute, \
    ScoreboardBuilder, DataBuilder
from .command_builder.composite import Composite


class CodeGenerator(CodeGeneratorSpec):
    def __init__(self, builder: IRBuilder, target: Path, config: GeneratorConfig):
        self.target = target
        self.config = config
        self.builder = builder
        self.namespace = config.namespace
        self.uuid_namespace = uuid.uuid4()
        self.top_scope = CodeGeneratorScope(
            "global",
            None,
            StructureType.GLOBAL,
            self.namespace)
        self.scope_stack = [self.top_scope]
        self.current_scope = self.top_scope
        self.var_objective = "var"  # 存储变量记分板
        self.statement_objective = "stmt"  # 存储变量记分板
        self.current_scope.add_command(ScoreboardBuilder.add_objective(self.var_objective, "dummy", "Variables"))
        self.current_scope.add_command(ScoreboardBuilder.add_objective(self.statement_objective, "dummy", "Statement"))
        self.function_table: dict[Function, CodeGeneratorScope] = {}

    @staticmethod
    def is_support(config: GeneratorConfig) -> bool:
        version = config.minecraft_version
        if version.major == 1 and version.minor == 20 and version.patch == 4 and version.edition == MinecraftEdition.JAVA_EDITION:
            pass
        else:
            return False
        if config.enable_recursion or config.enable_experimental:
            return False
        return True

    def generate_commands(self):
        iterator = self.builder.__iter__()
        handlers: dict[IROpCode, Callable[[IRInstruction], None]] = {
            # ===== 控制流指令 (0x00-0x1F) =====
            IROpCode.JUMP: self._jump,  # 0x00
            IROpCode.COND_JUMP: self._cond_jump,  # 0x01
            IROpCode.FUNCTION: self._function,  # 0x02
            IROpCode.CALL: self._call,  # 0x03
            IROpCode.RETURN: self._return,  # 0x04
            IROpCode.SCOPE_BEGIN: self._scope_begin,  # 0x05
            IROpCode.SCOPE_END: self._scope_end,  # 0x06
            IROpCode.BREAK: self._break,  # 0x07
            IROpCode.CONTINUE: self._continue,  # 0x08

            # ===== 变量操作指令 (0x20-0x3F) =====
            IROpCode.DECLARE: self._declare,  # 0x20
            IROpCode.VAR_RELEASE: self._var_release,  # 0x21
            IROpCode.ASSIGN: self._assign,  # 0x22
            IROpCode.UNARY_OP: self._unary_op,  # 0x23
            IROpCode.OP: self._op,  # 0x24
            IROpCode.COMPARE: self._compare,  # 0x25
            IROpCode.CAST: self._cast,  ## 0x26

            # ===== 面向对象指令 (0x40-0x5F) =====
            # IROpCode.CLASS: self._class_def,  # 0x40
            # IROpCode.NEW_OBJ: self._new_object,  # 0x41
            # IROpCode.GET_FIELD: self._get_field,  # 0x42
            # IROpCode.SET_FIELD: self._set_field,  # 0x43
            # IROpCode.CALL_METHOD: self._call_method,  # 0x44

            # ===== 命令生成指令 (0x60-0x7F) =====
            IROpCode.RAW_CMD: self._raw_command,  # 0x60
            IROpCode.DEBUG_INFO: self._debug_info,  # 0x61
        }
        for instr in iterator:
            handler = handlers.get(instr.opcode, lambda i: None)
            if handler:
                handler(instr)
            else:
                if hasattr(self, "_" + instr.opcode.name):
                    if callable(getattr(self, "_" + instr.opcode.name)):
                        getattr(self, "_" + instr.opcode.name)(instr.opcode)
                        continue

        def _generate_commands(output_dir: str, top_scope):
            """遍历作用域树生成文件"""
            stack: list[CodeGeneratorScope] = [top_scope]

            while stack:
                current: CodeGeneratorScope = stack.pop()
                path = os.path.join(output_dir, current.get_file_path())
                os.makedirs(os.path.dirname(path), exist_ok=True)
                with open(path, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(current.commands))
                stack.extend(reversed(current.children))

        _generate_commands(self.target.__str__(), self.top_scope)
        for file_path in builtins_func:
            path = os.path.join(self.target, self.namespace, "functions", f"{file_path}.mcfunction")
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(builtins_func[file_path])

    def _scope_begin(self, instr: IRInstruction):
        name: str = instr.get_operands()[0]
        stype: StructureType = instr.get_operands()[1]
        self.current_scope = self.current_scope.create_child(name, stype)
        self.scope_stack.append(self.current_scope)

    def _scope_end(self, instr: IRInstruction):
        self.current_scope = self.current_scope.parent
        self.scope_stack.pop()

    def _break(self, instr: IRInstruction):
        loop_check_scope = self.current_scope.resolve_scope(instr.get_operands()[0])
        name = "#break_" + self.current_scope.get_unique_name(".")
        self.current_scope.add_command(ScoreboardBuilder.set_score(name, self.statement_objective, 1))
        current = self.current_scope
        while True:
            current.add_command(
                Execute.execute().if_score_matches(name, self.statement_objective, "1").run("return"))
            if current == loop_check_scope:
                break
            current = current.parent

    def _continue(self, instr: IRInstruction):
        loop_check_scope = self.current_scope.resolve_scope(instr.get_operands()[0])
        name = "#continue_" + self.current_scope.get_unique_name(".")
        self.current_scope.add_command(ScoreboardBuilder.set_score(name, self.statement_objective, 1))
        current = self.current_scope
        while True:
            if current == loop_check_scope:
                break
            current.add_command(
                Execute.execute().if_score_matches(name, self.statement_objective, "1").run("return"))
            current = current.parent

    def _function(self, instr: IRInstruction):
        ...

    def _return(self, instr: IRInstruction):
        value: Reference[Variable | Constant | Literal] = instr.get_operands()[0]
        current = self.current_scope
        while True:
            current = current.parent
            if current.type == StructureType.FUNCTION:
                break

        return_var = Variable("return_" + uuid.uuid5(uuid.uuid4(), current.get_unique_name(".")).hex,
                              value.get_data_type())
        current.add_symbol(return_var)

        if value:  # 如果存在返回值
            if isinstance(value.get_data_type(), DataType):
                if value.value_type == ValueType.LITERAL:
                    self.current_scope.add_command(
                        BasicCommands.Copy.copy_literal_base_type(return_var, self.current_scope, self.var_objective,
                                                                  value.value))
                elif value.value_type in (ValueType.VARIABLE, ValueType.CONSTANT):
                    self.current_scope.add_command(
                        BasicCommands.Copy.copy_variable_base_type(return_var, self.current_scope, self.var_objective,
                                                                   value.value,
                                                                   self.current_scope, self.var_objective)
                    )
            else:  # Class
                assert isinstance(value.get_data_type(), Class)
                pass  # TODO:实现类的赋值

        name = "#return_" + self.current_scope.get_unique_name(".")
        self.current_scope.add_command(ScoreboardBuilder.set_score(name, self.statement_objective, 1))
        current = self.current_scope
        while True:
            current.add_command(
                Execute.execute().if_score_matches(name, self.statement_objective, "1").run("return"))
            current = current.parent
            if current.type == StructureType.FUNCTION:
                break

    def _var_release(self, instr: IRInstruction):
        pass  # 懒得清理，反正不清理也占不了多少内存

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

        for i, (arg, param) in enumerate(zip(args, func.params)):
            if isinstance(arg.get_data_type(), DataType):
                if arg.value_type == ValueType.LITERAL:
                    self.current_scope.add_command(
                        BasicCommands.Copy.copy_literal_base_type(param, jump_scope, self.var_objective,
                                                                  arg.value))
                elif arg.value_type in (ValueType.VARIABLE, ValueType.CONSTANT):
                    BasicCommands.Copy.copy_variable_base_type(param, jump_scope, self.var_objective, arg.value,
                                                               self.current_scope, self.var_objective)
            else:  # Class
                assert isinstance(arg.get_data_type(), Class)
                pass  # TODO:实现类的赋值
        if isinstance(func.return_type, DataType):
            BasicCommands.Copy.copy_variable_base_type(result, self.current_scope, self.var_objective, Variable(
                "return_" + uuid.uuid5(uuid.uuid4(), jump_scope.get_unique_name(".")).hex, func.return_type),
                                                       self.current_scope, self.var_objective)
        else:  # Class
            assert isinstance(func.return_type, Class)
            pass  # TODO:实现类的赋值
        self.current_scope.add_command(FunctionBuilder.run(jump_scope.get_minecraft_function_path()))

    def _assign(self, instr: IRInstruction):
        target: Variable | Constant = instr.get_operands()[0]
        source: Reference[Variable | Constant | Literal] = instr.get_operands()[1]
        if isinstance(target.dtype, DataType):
            if source.value_type == ValueType.LITERAL:
                self.current_scope.add_command(
                    BasicCommands.Copy.copy_literal_base_type(target, self.current_scope, self.var_objective,
                                                              source.value))
            elif source.value_type in (ValueType.VARIABLE, ValueType.CONSTANT):
                self.current_scope.add_command(
                    BasicCommands.Copy.copy_variable_base_type(target, self.current_scope, self.var_objective,
                                                               source.value, self.current_scope, self.var_objective))
        else:  # Class
            assert isinstance(target.dtype, Class)
            pass  # TODO:实现类的赋值

    def _unary_op(self, instr: IRInstruction):
        pass  # 因该dsl内不存在直接性的位运算，故不实现

    def _op(self, instr: IRInstruction):
        result: Variable | Constant = instr.get_operands()[0]
        op: BinaryOps = instr.get_operands()[1]
        left_ref: Reference[Variable | Constant | Literal] = instr.get_operands()[2]
        right_ref: Reference[Variable | Constant | Literal] = instr.get_operands()[3]
        if isinstance(result.dtype, DataType):
            self.current_scope.add_command(
                Composite.op_base_type(result, self.current_scope, self.var_objective, op, left_ref, self.current_scope,
                                       self.var_objective, right_ref, self.current_scope, self.var_objective,
                                       self.namespace))
        else:  # TODO:实现类的比较？
            assert isinstance(result.dtype, Class)
            pass

    def _compare(self, instr: IRInstruction):
        result: Variable | Constant = instr.get_operands()[0]
        op: CompareOps = instr.get_operands()[1]
        left: Reference[Variable | Constant | Literal] = instr.get_operands()[2]
        right: Reference[Variable | Constant | Literal] = instr.get_operands()[3]
        if isinstance(left.get_data_type(), DataType):
            self.current_scope.add_command(
                Composite.var_compare_base_type(left, self.current_scope, self.var_objective, op, right,
                                                self.current_scope, self.var_objective, result, self.current_scope,
                                                self.var_objective))

    def _cast(self, instr: IRInstruction):
        result: Variable | Constant = instr.get_operands()[0]
        dtype: DataType | Class = instr.get_operands()[1]
        value: Reference[Variable | Constant | Literal] = instr.get_operands()[2]
        if value.value_type == Literal:
            raise
        # int -> string
        if dtype == DataType.STRING and value.get_data_type() == DataType.INT:
            args_path = f"builtins.int2str.args" + uuid.uuid4().hex

            self.current_scope.add_command(
                DataBuilder.modify_storage_set_value(self.var_objective, args_path + ".target",
                                                     self.var_objective))
            self.current_scope.add_command(
                DataBuilder.modify_storage_set_value(self.var_objective, args_path + ".target_path",
                                                     self.current_scope.get_symbol_path(result.get_name())))
            self.current_scope.add_command(
                Execute.execute().store_result_storage(self.var_objective, args_path + ".value", "int", 1.0).run(
                    ScoreboardBuilder.get_score(self.current_scope.get_symbol_path(value.get_name()),
                                                self.var_objective)))
            self.current_scope.add_command(
                FunctionBuilder.run_with_source(f"{self.namespace}:builtins/int2str", "storage",
                                                f"{self.var_objective} {args_path}"))
        elif dtype == DataType.INT and value.get_data_type() == DataType.STRING:  # string -> int
            args_path = f"builtins.str2int.args" + uuid.uuid4().hex
            self.current_scope.add_command(
                DataBuilder.modify_storage_set_value(self.var_objective, args_path + ".objective",
                                                     self.var_objective))
            self.current_scope.add_command(
                DataBuilder.modify_storage_set_value(self.var_objective, args_path + ".target_path",
                                                     self.current_scope.get_symbol_path(result.get_name())))
            self.current_scope.add_command(
                Execute.execute().store_result_storage(self.var_objective, args_path + ".value", "int", 1.0).run(
                    ScoreboardBuilder.get_score(self.current_scope.get_symbol_path(value.get_name()),
                                                self.var_objective)))
            self.current_scope.add_command(
                FunctionBuilder.run_with_source(f"{self.namespace}:builtins/str2int", "storage",
                                                f"{self.var_objective} {args_path}"))

    def _declare(self, instr: IRInstruction):
        self.current_scope.add_symbol(instr.get_operands()[0])

    def _raw_command(self, instr: IRInstruction):
        command: Reference[Variable | Constant | Literal] = instr.get_operands()[0]
        if command.value_type == ValueType.LITERAL:
            self.current_scope.add_command(str(command.value.value))
        else:
            args_path = f"builtins.exec.args" + uuid.uuid4().hex

            self.current_scope.add_command(
                DataBuilder.modify_storage_set_from_storage(self.var_objective, args_path + ".command",
                                                            self.var_objective,
                                                            self.current_scope.get_symbol_path(command.get_name())))
            self.current_scope.add_command(
                FunctionBuilder.run_with_source(f"{self.namespace}:builtins/exec", "storage",
                                                f"{self.var_objective} " + args_path))  # TODO:内置函数实现

    def _debug_info(self, instr: IRInstruction):
        self.current_scope.add_command(f'tellraw @a "{".".join(i.name for i in self.scope_stack)}"')
