# coding=utf-8
"""
将ir反编译回原始代码的核心
"""
import os
import shutil
from pathlib import Path

from transpiler.core.enums import StructureType, DataType, VariableType, FunctionType
from transpiler.core.generator_config import GeneratorConfig
from transpiler.core.instructions import IROpCode
from transpiler.core.ir_builder import IRBuilder
from transpiler.core.specification import CodeGeneratorSpec
from transpiler.core.symbols import Class, Reference, Function, Literal
from transpiler.utils.naming import NameNormalizer


class CodeGenerator(CodeGeneratorSpec):
    def __init__(self, builder: IRBuilder, target: Path, config: GeneratorConfig):
        self.builder = builder
        self.target = target
        self.config = config
        self.code = ['include "math"', 'include "random"']
        self.depth = 0
        self.instructions = list(builder)
        self.current_index = 0
        self.processed_instructions = set()
        self.if_else_mapping = {}  # 存储if-else配对信息

    def _indent(self):
        return "    " * self.depth

    def _add_line(self, line: str):
        if line.strip():
            self.code.append(self._indent() + line)
        else:
            self.code.append("")

    def _preprocess_if_else_structures(self):
        """预处理if-else结构，建立条件映射"""
        for i, instr in enumerate(self.instructions):
            if instr.opcode == IROpCode.COND_JUMP and len(instr.operands) >= 3:
                condition = instr.operands[0]
                true_scope = instr.operands[1]  # if_158
                false_scope = instr.operands[2]  # else_158

                # 存储if作用域的条件信息
                self.if_else_mapping[true_scope] = {
                    'condition': condition,
                    'else_scope': false_scope,
                    'cond_jump_index': i
                }

    def _format_type(self, dtype) -> str:
        """正确格式化数据类型"""
        if isinstance(dtype, DataType):
            return dtype.value
        elif isinstance(dtype, Class):
            return dtype.name
        return str(dtype).lower()

    def _format_reference(self, ref):
        """正确格式化引用"""
        if ref is None:
            return "null"

        # 如果是Reference对象，获取其target
        if isinstance(ref, Reference):
            target = ref.value
        else:
            target = ref

        # 处理字面量
        if isinstance(target, Literal):
            if target.dtype == DataType.STRING:
                return f'"{target.value}"'
            elif target.dtype == DataType.BOOLEAN:
                return str(target.value).lower()
            else:
                return str(target.value)

        # 处理变量
        if hasattr(target, 'name'):
            return target.name

        return str(target)

    def _peek_next_instructions(self, count=5):
        """查看接下来的几条指令"""
        result = []
        for i in range(1, count + 1):
            if self.current_index + i < len(self.instructions):
                result.append(self.instructions[self.current_index + i])
        return result

    def _find_matching_scope_end(self, scope_name):
        """找到匹配的作用域结束指令"""
        for i in range(self.current_index + 1, len(self.instructions)):
            instr = self.instructions[i]
            if (instr.opcode == IROpCode.SCOPE_END and
                    len(instr.operands) > 0 and
                    instr.operands[0] == scope_name):
                return i
        return None

    def get_handle_mapping(self):
        return {
            IROpCode.FUNCTION: self._handle_function,
            IROpCode.SCOPE_BEGIN: self._handle_scope_begin,
            IROpCode.SCOPE_END: self._handle_scope_end,
            IROpCode.DECLARE: self._handle_declare,
            IROpCode.ASSIGN: self._handle_assign,
            IROpCode.OP: self._handle_op,
            IROpCode.COMPARE: self._handle_compare,
            IROpCode.CALL: self._handle_call,
            IROpCode.RETURN: self._handle_return,
            IROpCode.COND_JUMP: self._handle_cond_jump,
            IROpCode.JUMP: self._handle_jump,
            IROpCode.BREAK: self._handle_break,
            IROpCode.CONTINUE: self._handle_continue,
            IROpCode.CAST: self._handle_cast,

            IROpCode.CLASS: self._handle_class,
            IROpCode.NEW_OBJ: self._handle_new_obj,
            IROpCode.GET_FIELD: self._handle_get_property,
            IROpCode.SET_FIELD: self._handle_set_property,
            IROpCode.CALL_METHOD: self._handle_call_method,
        }

    def _handle_function(self, instr):
        """处理函数定义"""
        func = instr.operands[0]

        # 处理函数注解
        if hasattr(func, 'annotations') and func.annotations:
            for annotation in func.annotations:
                self._add_line(f"@{annotation}")

        # 处理参数 - Parameter通过var字段访问变量信息
        params = []
        if hasattr(func, 'params') and func.params:
            params = [f"{p.var.name}: {self._format_type(p.var.dtype)}" for p in func.params]

        params_str = ", ".join(params)

        # 处理返回类型
        if func.return_type != DataType.NULL:
            return_type = self._format_type(func.return_type)
            self._add_line(f"func {func.name}({params_str}): {return_type} {{")
        else:
            self._add_line(f"func {func.name}({params_str}) {{")
        self.depth += 1

    def _handle_scope_begin(self, instr):
        """处理作用域开始"""
        scope_name, scope_type = instr.operands

        if scope_type == StructureType.CONDITIONAL:
            if scope_name.startswith('if_'):
                # 查找对应的条件信息
                if scope_name in self.if_else_mapping:
                    condition = self.if_else_mapping[scope_name]['condition']
                    condition_str = self._format_reference(condition)
                    self._add_line(f"if ({condition_str}) {{")
                    self.depth += 1
                    # 标记对应的条件跳转已处理
                    cond_index = self.if_else_mapping[scope_name]['cond_jump_index']
                    self.processed_instructions.add(cond_index)
            # else作用域不需要特殊处理，由scope_end处理

    def _handle_scope_end(self, instr):
        """处理作用域结束"""
        scope_name, scope_type = instr.operands

        if scope_type == StructureType.CONDITIONAL:
            if scope_name.startswith('if_'):
                # if作用域结束，检查是否有else
                if scope_name in self.if_else_mapping:
                    else_scope = self.if_else_mapping[scope_name]['else_scope']
                    if else_scope:
                        # 有else分支
                        self.depth -= 1
                        self._add_line("} else {")
                        self.depth += 1
                    else:
                        # 没有else分支
                        self.depth -= 1
                        self._add_line("}")
                else:
                    self.depth -= 1
                    self._add_line("}")
            elif scope_name.startswith('else_'):
                # else作用域结束
                self.depth -= 1
                self._add_line("}")
        elif scope_type == StructureType.FUNCTION:
            self.depth -= 1
            self._add_line("}")

    def _find_recent_condition_for_scope(self, scope_name):
        """查找最近的条件跳转指令 - 修复查找逻辑"""
        # 扩大搜索范围，因为条件计算可能在更早的位置
        for i in range(max(0, self.current_index - 20), self.current_index):
            instr = self.instructions[i]
            if (instr.opcode == IROpCode.COND_JUMP and
                    len(instr.operands) >= 2):

                true_scope = instr.operands[1]
                false_scope = instr.operands[2] if len(instr.operands) > 2 else None

                # 检查是否跳转到当前作用域或对应的else作用域
                if (true_scope == scope_name or
                        (false_scope and false_scope == scope_name) or
                        self._is_related_scope(scope_name, true_scope, false_scope)):

                    if i not in self.processed_instructions:
                        self.processed_instructions.add(i)
                        return instr
        return None

    def _is_related_scope(self, current_scope, true_scope, false_scope):
        """检查作用域是否相关"""
        if current_scope.startswith('if_'):
            struct_id = current_scope.replace('if_', '')
            else_scope = f'else_{struct_id}'
            return true_scope == current_scope or false_scope == else_scope
        elif current_scope.startswith('else_'):
            struct_id = current_scope.replace('else_', '')
            if_scope = f'if_{struct_id}'
            return true_scope == if_scope or false_scope == current_scope
        return False

    def _handle_declare(self, instr):
        """处理变量声明 - 跳过函数参数声明"""
        var = instr.operands[0]

        # 检查是否为函数参数
        if var.var_type == VariableType.PARAMETER:
            return  # 跳过参数声明

        var_type = self._format_type(var.dtype)
        self._add_line(f"{var_type} {var.name};")

    def _handle_assign(self, instr):
        """处理赋值"""
        target, source = instr.operands
        source_str = self._format_reference(source)
        self._add_line(f"{target.name} = {source_str};")

    def _handle_op(self, instr):
        """处理二元运算"""
        result, op, left, right = instr.operands
        left_str = self._format_reference(left)
        right_str = self._format_reference(right)
        op_str = op.value if hasattr(op, 'value') else str(op)
        self._add_line(f"{result.name} = {left_str} {op_str} {right_str};")

    def _handle_compare(self, instr):
        """处理比较运算"""
        result, op, left, right = instr.operands
        left_str = self._format_reference(left)
        right_str = self._format_reference(right)
        op_str = op.value if hasattr(op, 'value') else str(op)
        self._add_line(f"{result.name} = {left_str} {op_str} {right_str};")

    def _handle_call(self, instr):
        """处理函数调用"""
        result, func, args = instr.operands
        func: Function
        func_name = func.name if hasattr(func, 'name') else str(func)

        # 对于函数为内置函数的情况下反归一化函数命名
        if func.function_type == FunctionType.BUILTIN:
            func_name = NameNormalizer.denormalize(func_name)

        args_list = []
        if args:
            for arg in args.values():
                args_list.append(self._format_reference(arg))

        args_str = ", ".join(args_list)

        if result:
            self._add_line(f"{result.name} = {func_name}({args_str});")
        else:
            self._add_line(f"{func_name}({args_str});")

    def _handle_return(self, instr):
        """处理返回语句"""
        if instr.operands and instr.operands[0]:
            value = self._format_reference(instr.operands[0])
            self._add_line(f"return {value};")
        else:
            self._add_line("return;")

    def _handle_cond_jump(self, instr):
        """处理条件跳转 - 已被预处理，静默跳过"""
        pass

    def _handle_jump(self, instr):
        """处理无条件跳转"""
        # 大部分jump都是循环回跳，可以忽略
        pass

    def _handle_break(self, instr):
        self._add_line("break;")

    def _handle_continue(self, instr):
        self._add_line("continue;")

    def _handle_cast(self, instr):
        """处理类型转换 - 使用标准库函数"""
        result, target_type, value = instr.operands

        target_type_name = self._format_type(target_type)
        value_str = self._format_reference(value)

        # 根据目标类型使用相应的内置函数
        if target_type_name == "string":
            self._add_line(f"{result.name} = str({value_str});")
        elif target_type_name == "int":
            self._add_line(f"{result.name} = int({value_str});")
        else:
            # 其他类型转换，使用通用格式
            self._add_line(f"{result.name} = ({target_type_name}){value_str};")

    def _handle_class(self, instr):
        """处理类定义"""
        class_obj = instr.operands[0]
        class_name = class_obj.name if hasattr(class_obj, 'name') else str(class_obj)
        self._add_line(f"class {class_name} {{")
        self.depth += 1

    def _handle_new_obj(self, instr):
        """处理对象实例化"""
        result, class_obj = instr.operands
        class_name = class_obj.name if hasattr(class_obj, 'name') else str(class_obj)
        self._add_line(f"{result.name} = new {class_name}();")

    def _handle_get_property(self, instr):
        """处理属性获取"""
        result, obj, property_name = instr.operands
        obj_name = obj.name if hasattr(obj, 'name') else str(obj)
        self._add_line(f"{result.name} = {obj_name}.{property_name};")

    def _handle_set_property(self, instr):
        """处理属性设置"""
        obj, property_name, value = instr.operands
        obj_name = obj.name if hasattr(obj, 'name') else str(obj)
        value_str = self._format_reference(value)
        self._add_line(f"{obj_name}.{property_name} = {value_str};")

    def _handle_call_method(self, instr):
        """处理方法调用"""
        result, class_obj, method, args = instr.operands
        obj_name = class_obj.name if hasattr(class_obj, 'name') else str(class_obj)
        method_name = method.name if hasattr(method, 'name') else str(method)

        args_list = []
        if args:
            for arg in args.values():
                args_list.append(self._format_reference(arg))
        args_str = ", ".join(args_list)

        if result:
            self._add_line(f"{result.name} = {obj_name}.{method_name}({args_str});")
        else:
            self._add_line(f"{obj_name}.{method_name}({args_str});")

    def generate(self):
        # 预处理if-else结构
        self._preprocess_if_else_structures()

        while self.current_index < len(self.instructions):
            instr = self.instructions[self.current_index]

            if self.current_index not in self.processed_instructions:
                handler = self.get_handle_mapping().get(instr.opcode)
                if handler:
                    handler(instr)  # NOQA

            self.current_index += 1

        # 写入文件
        if self.target.exists():
            if self.target.is_dir():
                shutil.rmtree(self.target)
            else:
                self.target.unlink()
        self.target.write_text("\n".join(self.code), encoding='utf-8')

    @staticmethod
    def is_support(config: GeneratorConfig) -> bool:
        return bool(os.environ.get("DECOMPILER", None))

    @staticmethod
    def get_name() -> str:
        return "MCDL Decompiler"
