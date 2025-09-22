# coding=utf-8
"""
生成1.20.4版本最终指令
"""
import uuid
from datetime import datetime
from pathlib import Path
from typing import Callable

from transpiler.core.enums import *
from transpiler.core.generator_config import MinecraftEdition, GeneratorConfig, MinecraftVersion
from transpiler.core.instructions import IROpCode, IRInstruction
from transpiler.core.ir_builder import IRBuilder, IRBuilderIterator, IRBuilderReversibleIterator
from transpiler.core.specification import CodeGeneratorSpec
from transpiler.core.symbols import *
from .builtins import builtin_func, BuiltinFuncMapping
from .code_generator_scope import CodeGeneratorScope
from .command_builder import *


class CodeGenerator(CodeGeneratorSpec):
    """
    je1.20.4指令生成后端
    """

    def __init__(self, builder: IRBuilder, target: Path, config: GeneratorConfig):
        self.target = target
        self.config = config
        self.builder = builder
        self.namespace = config.namespace
        self.iterator: IRBuilderIterator | None = None
        self.uuid_namespace = uuid.uuid4()
        self.top_scope = CodeGeneratorScope(
            "global",
            None,
            StructureType.GLOBAL,
            self.namespace
        )
        # 作用域堆栈
        self.scope_stack = [self.top_scope]
        self.current_scope = self.top_scope
        # 变量记分板名
        self.var_objective = "var"
        # 语句记分板
        self.statement_objective = "stmt"
        self.init_functions = [self.top_scope.get_minecraft_function_path()]
        self.tick_functions = []
        # 生成初始化指令
        self._generate_init_code()

    def _generate_init_code(self):
        """
        初始化记分板
        """
        self.current_scope.add_command(
            ScoreboardBuilder.add_objective(
                self.var_objective,
                "dummy",
                "Variables"
            )
        )
        self.current_scope.add_command(
            ScoreboardBuilder.add_objective(
                self.statement_objective,
                "dummy",
                "Statement"
            )
        )
        # 保证类id累加器被初始化,同时保证0为null唯一使用(但是每次重新启动都将使id缺失一个)
        self.current_scope.add_command(
            ScoreboardBuilder.add_score(
                "#new_obj_id",
                self.statement_objective,
                1
            )
        )

    @staticmethod
    def is_support(config: GeneratorConfig) -> bool:
        version = config.minecraft_version
        if version != MinecraftVersion(1, 20, 4, MinecraftEdition.JAVA_EDITION):
            return False
        if config.enable_recursion or config.enable_experimental:
            return False
        return True

    def _process_instruction(
            self,
            instr: IRInstruction,
            handlers: dict[IROpCode, Callable[[IRInstruction], None]]
    ):
        """处理单个IR指令"""
        handler = handlers.get(instr.opcode, self._fallback_handler)

        if self.config.debug:
            # 添加调试注释
            if instr.opcode not in (IROpCode.SCOPE_BEGIN, IROpCode.SCOPE_END,
                                    IROpCode.FUNCTION, IROpCode.CLASS):
                self.current_scope.add_command(
                    BasicCommands.comment(f"{self.current_scope.name}:{instr}")
                )

        # 处理指令
        handler(instr)

    def _fallback_handler(self, instr: IRInstruction):
        """后备指令处理器"""
        opcode_name = instr.opcode.name
        if hasattr(self, "_" + opcode_name):
            handler = getattr(self, "_" + opcode_name)
            if callable(handler):
                handler(instr.opcode)
            else:
                self.current_scope.add_command(f"# Fucking {opcode_name} exists but isn't callable!")
        else:
            self.current_scope.add_command(f"# Fucking {opcode_name} doesn't exist!")

    def _get_scope_block(self, name: str):
        iterable: IRBuilderIterator = self.iterator or self.builder
        reversed_iterable: IRBuilderReversibleIterator = iterable.__reversed__()

        for instr in reversed_iterable:
            if instr.opcode == IROpCode.SCOPE_BEGIN and instr.get_operands()[0] == name:
                break
        else:
            raise Exception(f"作用域结构错误")
        scope_block = []
        for instr in reversed(reversed_iterable):
            scope_block.append(instr)
            if instr.opcode == IROpCode.SCOPE_END and instr.get_operands()[0] == name:
                break
        return scope_block

    def _write_commands(self):
        """遍历作用域树生成文件"""
        stack: list[CodeGeneratorScope] = [self.top_scope]

        while stack:
            current: CodeGeneratorScope = stack.pop()
            if current.get_commands():
                file_path = self.target / self.namespace / "data" / current.get_file_path()
                file_path.parent.mkdir(parents=True, exist_ok=True)
                with open(file_path, 'w', encoding='utf-8') as f:
                    if self.config.debug:
                        # 写入文件位置及信息
                        f.write(
                            f"# {current.get_file_path()} time:{datetime.now()} version:{self.config.minecraft_version}\n")
                    # 写入实际指令
                    f.write('\n'.join(current.get_commands()))
            stack.extend(reversed(current.children))

    def _write_builtin_functions(self):
        """写入内置函数库"""
        for file_path, content in builtin_func.items():
            full_path = self.target / self.namespace / "data" / self.namespace / "functions" / f"{file_path}.mcfunction"
            full_path.parent.mkdir(parents=True, exist_ok=True)
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)

    def _write_minecraft_tags(self):
        """写入内置函数标签 init/tick"""
        function_tags_path = self.target / self.namespace / "data" / "minecraft" / "tags" / "functions"
        function_tags_path.mkdir(parents=True, exist_ok=True)
        if self.init_functions:
            init_tag_path = function_tags_path / "load.json"
            with open(init_tag_path, 'w', encoding='utf-8') as f:
                f.write(f"""{{"values": ["{'","'.join(self.init_functions)}"]}}""")
        if self.tick_functions:
            tick_tag_path = function_tags_path / "tick.json"
            with open(tick_tag_path, 'w', encoding='utf-8') as f:
                f.write(f"""{{"values": ["{'","'.join(self.tick_functions)}"]}}""")

    def _write_datapack_meta(self):
        """写入数据包元数据"""
        datapack_meta_path = self.target / self.namespace / "pack.mcmeta"
        with open(datapack_meta_path, 'w', encoding='utf-8') as f:
            f.write(f"""{{"pack": {{"pack_format": 26,"description": "{self.namespace}"}}}}""")

    def _get_opcode_handler(self) -> dict[IROpCode, Callable[[IRInstruction], None]]:
        return {
            # ===== 控制流指令 (0x00-0x1F) =====
            IROpCode.JUMP: self._jump,
            IROpCode.COND_JUMP: self._cond_jump,
            IROpCode.FUNCTION: self._function,
            IROpCode.CALL: self._call,
            IROpCode.RETURN: self._return,
            IROpCode.SCOPE_BEGIN: self._scope_begin,
            IROpCode.SCOPE_END: self._scope_end,
            IROpCode.BREAK: self._break,
            IROpCode.CONTINUE: self._continue,

            # ===== 变量操作指令 (0x20-0x3F) =====
            IROpCode.DECLARE: self._declare,
            IROpCode.ASSIGN: self._assign,
            IROpCode.UNARY_OP: self._unary_op,
            IROpCode.OP: self._op,
            IROpCode.COMPARE: self._compare,
            IROpCode.CAST: self._cast,

            # ===== 面向对象指令 (0x40-0x5F) =====
            IROpCode.CLASS: self._class,
            IROpCode.NEW_OBJ: self._new_object,
            IROpCode.GET_FIELD: self._get_property,
            IROpCode.SET_FIELD: self._set_property,
            IROpCode.CALL_METHOD: self._method_call,

            # ===== 命令生成指令 (0x60-0x7F) =====
        }

    def generate_commands(self):
        self.iterator = self.builder.__iter__()
        for instr in self.iterator:
            self._process_instruction(instr, self._get_opcode_handler())
        # 写入实际指令
        self._write_commands()
        # 写入宏函数
        self._write_builtin_functions()
        # 写入init/tick标签
        self._write_minecraft_tags()
        # 写入元数据
        self._write_datapack_meta()
        self.iterator = None

    def _handle_jump_flags(self, scope_name: str, jump_instr: IRInstruction):
        # FIXME:这函数执行一次要30ms+纯纯性能刺客，我当时写下这函数是人我吃
        # 反向搜索
        iterator = self.iterator.__reversed__()
        # 向前搜索到需要跳转到的作用域的头部
        depth = 0
        for instr in iterator:
            if instr.opcode == IROpCode.SCOPE_END:
                depth += 1
                continue
            elif instr.opcode == IROpCode.SCOPE_BEGIN:
                depth -= 1
                if depth == 0 and instr.operands[0] == scope_name:
                    break
                continue
        # 再次反转，重新正向扫描作用域块的内容，处理 flag
        depth = 0
        flag_name_set = set()
        for instr in reversed(iterator):
            if instr.opcode == IROpCode.SCOPE_BEGIN:
                depth += 1
                continue
            elif instr.opcode == IROpCode.SCOPE_END:
                depth -= 1
                if depth == 0:
                    break
                continue

            # 当搜索到开始搜索位置时返回
            if instr is jump_instr:
                break
            # 无视作用域深度过大的位置
            if depth == 1:
                for flag_name, i in instr.get_flags().items():
                    # flag_name重复出现的情况下不生成指令
                    if flag_name in flag_name_set:
                        continue
                    if flag_name.startswith("return") and i > 0:
                        jump_instr.add_flag(flag_name, i - 1)
                        self.current_scope.add_command(
                            Execute.execute()
                            .if_score_matches(
                                flag_name.split(';')[1],
                                self.statement_objective,
                                '1'
                            )
                            .run(
                                "return 0"
                            )
                        )

    def _handle_annotation(self, function: Function, annotation: str):
        if annotation == "init":
            self.init_functions.append(f"{self.current_scope.get_minecraft_function_path()}/{function.name}")
        elif annotation == "tick":
            self.tick_functions.append(f"{self.current_scope.get_minecraft_function_path()}/{function.name}")

    def _scope_begin(self, instr: IRInstruction):
        name: str = instr.get_operands()[0]
        stype: StructureType = instr.get_operands()[1]

        if stype == StructureType.LOOP_CHECK:
            break_name = f"#break_{self.current_scope.get_unique_name('.')}.{name}"
            self.current_scope.add_command(
                ScoreboardBuilder.set_score(
                    break_name,
                    self.statement_objective,
                    0
                )
            )

        self.current_scope = self.current_scope.create_child(name, stype)
        self.scope_stack.append(self.current_scope)
        if stype == StructureType.FUNCTION:
            name = "#return_" + self.current_scope.get_unique_name(".")
            self.current_scope.add_command(
                ScoreboardBuilder.set_score(
                    name,
                    self.statement_objective,
                    0
                )
            )

    def _scope_end(self, instr: IRInstruction):
        stype: StructureType = instr.get_operands()[1]
        if stype == StructureType.LOOP_CHECK:
            continue_name = "#continue_" + self.current_scope.get_unique_name(".")
            self.current_scope.add_command(
                ScoreboardBuilder.set_score(
                    continue_name,
                    self.statement_objective,
                    0
                )
            )

        self.current_scope = self.current_scope.parent
        self.scope_stack.pop()

    def _break(self, instr: IRInstruction):
        loop_check_scope = self.current_scope.resolve_scope(instr.get_operands()[0])
        name = "#break_" + loop_check_scope.get_unique_name(".")
        instr.add_flag(
            f"return;{name}",
            self.current_scope.get_unique_name(".").count(".") -
            loop_check_scope.get_unique_name(".").count(".")
        )
        self.current_scope.add_command(
            ScoreboardBuilder.set_score(
                name,
                self.statement_objective,
                1
            )
        )
        self.current_scope.add_command(
            "return 0"
        )

    def _continue(self, instr: IRInstruction):
        loop_check_scope = self.current_scope.resolve_scope(instr.get_operands()[0])
        name = "#continue_" + loop_check_scope.get_unique_name(".")
        instr.add_flag(
            f"return;{name}",
            self.current_scope.get_unique_name(".").count(".") -
            loop_check_scope.get_unique_name(".").count(".")
        )
        self.current_scope.add_command(
            ScoreboardBuilder.set_score(
                name,
                self.statement_objective,
                1
            )
        )
        self.current_scope.add_command(
            "return 0"
        )

    def _function(self, instr: IRInstruction):
        function: Function = instr.get_operands()[0]
        for annotation in function.annotations:
            self._handle_annotation(function, annotation)

    def _class(self, instr: IRInstruction):
        pass

    def _return(self, instr: IRInstruction):
        value: Reference[Variable | Constant | Literal] = instr.get_operands()[0]
        function_scope = self.current_scope.find_parent_scope_by_type(StructureType.FUNCTION)

        if value:  # 如果存在返回值
            return_var = Variable(
                "return_" + uuid.uuid5(
                    self.uuid_namespace,
                    function_scope.get_unique_name('.')
                ).hex[:8],
                value.get_data_type()
            )
            function_scope.add_symbol(return_var, force=True)

            self.current_scope.add_command(
                BasicCommands.Copy.copy(
                    return_var,
                    self.current_scope,
                    self.var_objective,
                    value.value,
                    self.current_scope,
                    self.var_objective
                )
            )

        name = "#return_" + function_scope.get_unique_name(".")
        instr.add_flag(
            f"return;{name}",
            self.current_scope.get_unique_name(".").count(".") -
            function_scope.get_unique_name(".").count(".")
        )
        self.current_scope.add_command(
            ScoreboardBuilder.set_score(
                name,
                self.statement_objective,
                1
            )
        )
        self.current_scope.add_command(
            "return 0"
        )

    def _jump(self, instr: IRInstruction):
        scope_name: str = instr.get_operands()[0]
        jump_scope = self.current_scope.resolve_scope(scope_name)
        self.current_scope.add_command(
            FunctionBuilder.run(
                jump_scope.get_minecraft_function_path()
            )
        )
        self._handle_jump_flags(scope_name, instr)

    def _cond_jump(self, instr: IRInstruction):
        cond_var: Variable = instr.get_operands()[0]
        true_scope_name: str = instr.get_operands()[1]
        false_scope_name: str = instr.get_operands()[2]
        if true_scope_name:
            true_jump_scope = self.current_scope.resolve_scope(true_scope_name)
            self.current_scope.add_command(
                Execute.execute()
                .if_score_matches(
                    self.current_scope.get_symbol_path(
                        cond_var.get_name()
                    ),
                    self.var_objective,
                    "1"
                )
                .run(
                    FunctionBuilder.run(
                        true_jump_scope.get_minecraft_function_path()
                    )
                )
            )

            self._handle_jump_flags(true_scope_name, instr)
        if false_scope_name:
            false_jump_scope = self.current_scope.resolve_scope(false_scope_name)
            self.current_scope.add_command(
                Execute.execute()
                .unless_score_matches(
                    self.current_scope.get_symbol_path(
                        cond_var.get_name()
                    ),
                    self.var_objective,
                    "1"
                )
                .run(
                    FunctionBuilder.run(
                        false_jump_scope.get_minecraft_function_path()
                    )
                )
            )

            self._handle_jump_flags(false_scope_name, instr)

    def _call(self, instr: IRInstruction):
        result: Variable | Constant = instr.get_operands()[0]
        func: Function = instr.get_operands()[1]
        args: dict[str, Reference[Variable | Constant | Literal]] = instr.get_operands()[2]
        if func.function_type == FunctionType.BUILTIN:
            BuiltinFuncMapping.get(func.get_name())(result, self, args)
            return
        jump_scope = self.current_scope.resolve_scope(func.name)
        for (param_name, arg), param in zip(args.items(), func.params):
            self.current_scope.add_command(
                BasicCommands.Copy.copy(
                    param.var,
                    jump_scope,
                    self.var_objective,
                    arg.value,
                    self.current_scope,
                    self.var_objective
                )
            )
        self.current_scope.add_command(
            FunctionBuilder.run(
                jump_scope.get_minecraft_function_path()
            )
        )
        if func.return_type != DataType.NULL and result is not None:
            self.current_scope.add_command(
                BasicCommands.Copy.copy_variable_base_type(
                    result,
                    self.current_scope,
                    self.var_objective,
                    Variable(
                        "return_" +
                        uuid.uuid5(
                            self.uuid_namespace,
                            jump_scope.get_unique_name('.')
                        ).hex[:8],
                        func.return_type
                    ),
                    jump_scope,
                    self.var_objective
                )
            )

    def _method_call(self, instr: IRInstruction):
        result: Variable | Constant = instr.get_operands()[0]
        class_: Class = instr.get_operands()[1]
        func: Function = instr.get_operands()[2]
        args: dict[str, Reference[Variable | Constant | Literal]] = instr.get_operands()[3]
        if func.function_type == FunctionType.BUILTIN:
            BuiltinFuncMapping.get(f"{class_.get_name()}:{func.get_name()}")(result, self, args)
            return
        jump_scope = self.current_scope.resolve_scope(class_.name).find_scope(func.name)
        for (param_name, arg), param in zip(args.items(), func.params):
            self.current_scope.add_command(
                BasicCommands.Copy.copy(
                    param.var,
                    jump_scope,
                    self.var_objective,
                    arg.value,
                    self.current_scope,
                    self.var_objective
                )
            )
        self.current_scope.add_command(
            FunctionBuilder.run(
                jump_scope.get_minecraft_function_path()
            )
        )
        if func.return_type != DataType.NULL and result is not None:
            self.current_scope.add_command(
                BasicCommands.Copy.copy(
                    result,
                    self.current_scope,
                    self.var_objective,
                    Variable(
                        "return_" +
                        uuid.uuid5(
                            self.uuid_namespace,
                            jump_scope.get_unique_name('.')
                        ).hex[:8],
                        func.return_type
                    ),
                    jump_scope,
                    self.var_objective
                )
            )

    def _assign(self, instr: IRInstruction):
        target: Variable | Constant = instr.get_operands()[0]
        source: Reference[Variable | Constant | Literal] = instr.get_operands()[1]

        self.current_scope.add_command(
            BasicCommands.Copy.copy(
                target,
                self.current_scope,
                self.var_objective,
                source.value,
                self.current_scope,
                self.var_objective
            )
        )

    def _unary_op(self, instr: IRInstruction):
        result: Variable | Constant = instr.get_operands()[0]
        op: UnaryOps = instr.get_operands()[1]
        operand: Reference[Variable | Constant | Literal] = instr.get_operands()[2]
        if op == UnaryOps.NOT:
            self.current_scope.add_command(
                Composite.unary_op_not(
                    result,
                    self.current_scope,
                    self.var_objective,
                    operand,
                    self.current_scope,
                    self.var_objective
                )
            )
        else:
            pass  # 因该dsl内不存在直接性的位运算，故不实现

    def _op(self, instr: IRInstruction):
        result: Variable | Constant = instr.get_operands()[0]
        op: BinaryOps = instr.get_operands()[1]
        left_ref: Reference[Variable | Constant | Literal] = instr.get_operands()[2]
        right_ref: Reference[Variable | Constant | Literal] = instr.get_operands()[3]
        if isinstance(result.dtype, DataType):
            self.current_scope.add_command(
                Composite.op_base_type(
                    result,
                    self.current_scope,
                    self.var_objective,
                    op,
                    left_ref,
                    self.current_scope,
                    self.var_objective,
                    right_ref,
                    self.current_scope,
                    self.var_objective,
                    self.namespace
                )
            )
        else:
            assert False, "不支持的比较"

    def _compare(self, instr: IRInstruction):
        result: Variable | Constant = instr.get_operands()[0]
        op: CompareOps = instr.get_operands()[1]
        left: Reference[Variable | Constant | Literal] = instr.get_operands()[2]
        right: Reference[Variable | Constant | Literal] = instr.get_operands()[3]
        if isinstance(left.get_data_type(), DataType):
            self.current_scope.add_command(
                Composite.compare_base_type(
                    left,
                    self.current_scope,
                    self.var_objective,
                    op,
                    right,
                    self.current_scope,
                    self.var_objective,
                    result,
                    self.current_scope,
                    self.var_objective
                )
            )

    def _cast(self, instr: IRInstruction):
        result: Variable | Constant = instr.get_operands()[0]
        dtype: DataType | Class = instr.get_operands()[1]
        value: Reference[Variable | Constant | Literal] = instr.get_operands()[2]
        if value.value_type == Literal:
            raise
        # int -> string
        if dtype == DataType.STRING and value.get_data_type() in (DataType.INT, DataType.BOOLEAN):
            temp_path = uuid.uuid4().hex
            self.current_scope.add_command(
                Execute.execute()
                .store_result_storage(
                    self.var_objective,
                    temp_path,
                    "int",
                    1.0
                )
                .run(
                    ScoreboardBuilder.get_score(
                        self.current_scope.get_symbol_path(
                            value.get_name()
                        ),
                        self.var_objective
                    )
                )
            )
            self.current_scope.add_command(
                DataBuilder.modify_storage_set_string_storage(
                    self.var_objective,
                    self.current_scope.get_symbol_path(
                        result.get_name()
                    ),
                    self.var_objective,
                    temp_path
                )
            )
        elif dtype in (DataType.INT, DataType.BOOLEAN) and value.get_data_type() == DataType.STRING:  # string -> int
            temp_path = uuid.uuid4().hex
            self.current_scope.add_command(
                Execute.execute()
                .store_result_storage(
                    self.var_objective,
                    temp_path,
                    "int",
                    1.0
                )
                .run(
                    ScoreboardBuilder.get_score(
                        self.current_scope.get_symbol_path(
                            value.get_name()
                        ),
                        self.var_objective
                    )
                )
            )
            self.current_scope.add_command(
                BasicCommands.call_macros_function(
                    f"{self.namespace}:builtins/str2int",
                    self.var_objective,
                    {
                        "objective": (
                            False,
                            self.var_objective,
                            None
                        ),
                        "target_path": (
                            False,
                            self.current_scope.get_symbol_path(result.get_name()),
                            None
                        ),
                        "value": (
                            True,
                            temp_path,
                            self.var_objective
                        )
                    }
                )
            )

    def _declare(self, instr: IRInstruction):
        self.current_scope.add_symbol(instr.get_operands()[0])

    def _new_object(self, instr: IRInstruction):
        result: Variable = instr.get_operands()[0]
        # 为新建的对象分配id
        self.current_scope.add_command(
            ScoreboardBuilder.set_op(
                BasicCommands.get_symbol_path(
                    self.current_scope,
                    result
                ),
                self.var_objective,
                "#new_obj_id",
                self.statement_objective
            )
        )
        # 增加id值
        self.current_scope.add_command(
            ScoreboardBuilder.add_score(
                "#new_obj_id",
                self.statement_objective,
                1
            )
        )

    def _get_property(self, instr: IRInstruction):
        result: Variable = instr.get_operands()[0]
        obj: Variable | Constant = instr.get_operands()[1]
        property_name: str = instr.get_operands()[2]
        if result is None:
            return
        self.current_scope.add_command(
            OOP.get_property(
                result,
                self.current_scope,
                self.var_objective,
                obj,
                self.current_scope,
                self.var_objective,
                property_name
            )
        )

    def _set_property(self, instr: IRInstruction):
        obj: Variable | Constant = instr.get_operands()[0]
        property_name: str = instr.get_operands()[1]
        value: Reference[Variable | Constant | Literal] = instr.get_operands()[2]
        if value is None:
            return
        self.current_scope.add_command(
            OOP.set_property(
                obj,
                self.current_scope,
                self.var_objective,
                value,
                self.current_scope,
                self.var_objective,
                property_name
            )
        )
