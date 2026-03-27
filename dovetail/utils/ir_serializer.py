# coding=utf-8
"""IRBuilder序列化工具"""
import time
import uuid
from enum import Enum
from typing import Any, Dict, Union

from dovetail.core.config import PROJECT_VERSION
from dovetail.core.enums.types import DataTypeBase, DataType
from dovetail.core.ir_builder import IRBuilder
from dovetail.core.symbols import Symbol, Literal, Parameter, Reference, Class, Function, Variable
from dovetail.utils.binary_serializer import BinarySerializer


class IRSymbolSerializer:
    """序列化 IRBuilder 中的符号信息。

    将 IR（中间表示）中的所有符号及其结构关系打包成字典，并最终序列化为字节流，
    便于持久化存储。

    Attributes:
        builder (IRBuilder): 要被序列化的 IRBuilder 对象。
        symbol_id_map (dict): 存储已分配ID的符号到其对应对象的映射。
    """
    serializer = BinarySerializer()

    def __init__(self, builder: IRBuilder):
        """初始化 IRSymbolSerializer 实例。

        Args:
            builder (IRBuilder): 要被序列化的 IRBuilder 实例。
        """
        self.builder = builder
        self.symbol_id_map: Dict[int, Union[Symbol, str, int, Enum]] = {}

    @staticmethod
    def _extract_metadata(symbol: Symbol | DataType | list | int | float | bool | str | Enum | dict | tuple | set) -> \
            dict[str, Any] | None:
        """生成符号的序列化数据。

        Args:
            symbol (Any): 待提取元数据的符号对象。

        Returns:
            dict[str, Any] | None: 包含符号类型、名称和值等信息的元数据字典。
        """
        metadata: dict[str, ...] = {
            'symbol_type': type(symbol).__name__,
            'symbol_name': symbol.get_name() if isinstance(symbol, Symbol) else None,
        }
        if isinstance(symbol, (int, float, bool, str)) or symbol is None:
            metadata['value'] = symbol
        elif isinstance(symbol, (list, tuple, set)):
            metadata['value'] = [id(i) for i in symbol]
        elif isinstance(symbol, dict):
            metadata['value'] = {}
            for key, value in symbol.items():
                metadata['value'][id(key)] = id(value)
        elif isinstance(symbol, Enum):
            metadata['value'] = symbol.value
        elif isinstance(symbol, Literal):
            metadata['value'] = symbol.value
        elif isinstance(symbol, Parameter):
            metadata['var'] = id(symbol.var)
            metadata['default'] = id(symbol.default)
        elif isinstance(symbol, Reference):
            metadata['value_type'] = symbol.value_type.value
            metadata['value'] = id(symbol.value)
        elif isinstance(symbol, Function):
            metadata['params'] = {param_symbol.get_name(): id(param_symbol) for param_symbol in symbol.params}
            metadata['return_type'] = id(symbol.return_type)
            metadata['function_type'] = id(symbol.function_type)
        elif isinstance(symbol, Variable):
            metadata['dtype'] = id(symbol.dtype)
            metadata['var_type'] = symbol.var_type.value
            metadata['mutable'] = symbol.mutable
        elif isinstance(symbol, Class):
            metadata['methods'] = [id(func_symbol) for func_symbol in symbol.methods]
            metadata['interface'] = id(symbol.interface)
            metadata['parent'] = id(symbol.parent)
            metadata['properties'] = [id(var_symbol) for var_symbol in symbol.properties]
            metadata['type'] = id(symbol.type)
        else:
            print(symbol.__class__.__name__, type(symbol))

        return metadata

    def _add_symbol_id_map(self, symbol: Symbol | Enum | list | dict | bool | set | DataTypeBase | tuple):
        """递归地将符号加入全局 ID 映射表中。

        若当前符号为容器类型（如list、dict），将遍历其子元素也将其载入映射表。
        这是为后续序列化的符号ID索引做准备。

        Args:
            symbol (Any): 当前处理的符号对象。
        """
        # 将自身加入映射表
        if id(symbol) not in self.symbol_id_map:
            self.symbol_id_map[id(symbol)] = symbol
        else:
            return
        # 将符号中所有子符号也加入其中
        if isinstance(symbol, Reference):
            self._add_symbol_id_map(symbol.value)
            self._add_symbol_id_map(symbol.value_type)
        elif isinstance(symbol, Function):
            for param_symbol in symbol.params:
                self._add_symbol_id_map(param_symbol)
            self._add_symbol_id_map(symbol.return_type)
            self._add_symbol_id_map(symbol.function_type)
        elif isinstance(symbol, Parameter):
            self._add_symbol_id_map(symbol.var)
            self._add_symbol_id_map(symbol.default)
        elif isinstance(symbol, Class):
            self._add_symbol_id_map(symbol.properties)
            self._add_symbol_id_map(symbol.methods)
            self._add_symbol_id_map(symbol.type)
            self._add_symbol_id_map(symbol.interface)
            self._add_symbol_id_map(symbol.parent)
        elif isinstance(symbol, (list, tuple, set)):
            for i in symbol:
                self._add_symbol_id_map(i)
        elif isinstance(symbol, dict):
            for key, value in symbol.items():
                self._add_symbol_id_map(key)
                self._add_symbol_id_map(value)

    def serialize(self) -> dict:
        """将整个 IRBuilder 序列化为一个可嵌套的字典格式。

        包含元数据、符号信息、以及指令列表。优先扫描所有涉及的符号并建立映射表，
        然后对每条指令提取 byte 表示及依赖符号ID。

        Returns:
            dict: 包含 version、time、instructions 等字段的完整描述符。
        """
        result = {}

        # 预扫描所有符号
        for instr in self.builder.get_instructions():
            for op in instr.get_operands():
                self._add_symbol_id_map(op)

        result['metadata'] = {
            'version': PROJECT_VERSION,
            'time': time.time_ns(),
            'uuid': uuid.uuid4().hex,
        }
        result['symbol'] = {
            id_: self._extract_metadata(metadata)
            for id_, metadata in self.symbol_id_map.items()
        }
        result['instructions'] = [
            {
                "opcode": instr.opcode.value[0],
                "operands": [id(op) for op in instr.operands],
            } for instr in self.builder.get_instructions()
        ]
        return result

    @staticmethod
    def restore(data: bytes) -> IRBuilder:
        """从字节数据反序列化为 IRBuilder 对象。

        Args:
            data (bytes): 序列化的字节数据。

        Returns:
            IRBuilder: 恢复的 IRBuilder 实例。
        """
        serialized = IRSymbolSerializer.load(data)

        # 第一阶段：创建所有符号的占位映射
        id_to_symbol: dict[int, Any] = {}

        # 先处理所有基础类型和简单对象
        for symbol_id_str, metadata in serialized['symbol'].items():
            symbol_id = int(symbol_id_str)
            symbol_type = metadata['symbol_type']

            # 基础类型直接恢复
            if symbol_type in ('int', 'float', 'bool', 'str'):
                id_to_symbol[symbol_id] = metadata['value']
            elif symbol_type == 'NoneType':
                id_to_symbol[symbol_id] = None
            elif symbol_type in ('list', 'tuple', 'set'):
                # 占位，稍后填充
                id_to_symbol[symbol_id] = []
            elif symbol_type == 'dict':
                id_to_symbol[symbol_id] = {}
            elif symbol_type in 'DataType':
                # 枚举类型
                id_to_symbol[symbol_id] = DataType.from_literal(metadata['value'])
            else:
                # 复杂符号类型，先占位
                id_to_symbol[symbol_id] = None

        # 第二阶段：构造复杂对象（按依赖顺序）
        # 优先构造无依赖或依赖少的对象

        # 2.1 构造 Literal 和枚举
        for symbol_id_str, metadata in serialized['symbol'].items():
            symbol_id = int(symbol_id_str)
            if metadata['symbol_type'] == 'Literal':
                dtype = id_to_symbol.get(metadata['value'], DataType.UNDEFINED)
                id_to_symbol[symbol_id] = Literal(
                    dtype=dtype,
                    value=metadata['value']
                )

        # 2.2 构造 Variable
        for symbol_id_str, metadata in serialized['symbol'].items():
            symbol_id = int(symbol_id_str)
            if metadata['symbol_type'] == 'Variable':
                dtype_id = metadata.get('dtype')
                var_type_id = metadata.get('var_type')
                id_to_symbol[symbol_id] = Variable(
                    name=metadata['symbol_name'],
                    dtype=id_to_symbol.get(dtype_id) if dtype_id else DataType.UNDEFINED,
                    var_type=id_to_symbol.get(var_type_id) if var_type_id else None,
                    mutable=metadata.get('mutable', True)
                )

        # 2.3 构造 Reference（依赖 value）
        for symbol_id_str, metadata in serialized['symbol'].items():
            symbol_id = int(symbol_id_str)
            if metadata['symbol_type'] == 'Reference':
                # 需要等待 value 被构造
                pass  # 延后处理

        # 2.4 构造 Parameter（依赖 var 和 default）
        for symbol_id_str, metadata in serialized['symbol'].items():
            symbol_id = int(symbol_id_str)
            if metadata['symbol_type'] == 'Parameter':
                var_id = metadata['var']
                default_id = metadata.get('default')
                id_to_symbol[symbol_id] = Parameter(
                    var=id_to_symbol[var_id],
                    mutable=metadata.get('mutable', False),
                    default=id_to_symbol.get(default_id) if default_id else None
                )

        # 2.5 构造 Function（依赖 params, return_type, function_type）
        for symbol_id_str, metadata in serialized['symbol'].items():
            symbol_id = int(symbol_id_str)
            if metadata['symbol_type'] == 'Function':
                params = [id_to_symbol[pid] for pid in metadata['params'].values()]
                return_type_id = metadata.get('return_type')
                function_type_id = metadata.get('function_type')

                id_to_symbol[symbol_id] = Function(
                    name=metadata['symbol_name'],
                    params=params,
                    return_type=id_to_symbol.get(return_type_id) if return_type_id else DataType.VOID,
                    function_type=id_to_symbol.get(function_type_id) if function_type_id else None,
                    annotations={}  # 注解信息需要单独处理
                )

        # 2.6 构造 Class（依赖 methods, properties, interface, parent, type）
        for symbol_id_str, metadata in serialized['symbol'].items():
            symbol_id = int(symbol_id_str)
            if metadata['symbol_type'] == 'Class':
                methods = {id_to_symbol[mid] for mid in metadata.get('methods', [])}
                properties = {id_to_symbol[pid] for pid in metadata.get('properties', [])}
                interface_id = metadata.get('interface')
                parent_id = metadata.get('parent')
                type_id = metadata.get('type')

                id_to_symbol[symbol_id] = Class(
                    name=metadata['symbol_name'],
                    methods=methods,
                    interface=id_to_symbol.get(interface_id) if interface_id else None,
                    parent=id_to_symbol.get(parent_id) if parent_id else None,
                    properties=properties,
                    type=id_to_symbol.get(type_id) if type_id else None,
                    annotations=[]
                )

        # 2.7 现在构造 Reference（所有依赖已就绪）
        for symbol_id_str, metadata in serialized['symbol'].items():
            symbol_id = int(symbol_id_str)
            if metadata['symbol_type'] == 'Reference':
                value_id = metadata['value']
                id_to_symbol[symbol_id] = Reference(
                    value=id_to_symbol[value_id]
                )

        # 第三阶段：填充容器类型
        for symbol_id_str, metadata in serialized['symbol'].items():
            symbol_id = int(symbol_id_str)
            symbol_type = metadata['symbol_type']

            if symbol_type == 'list':
                id_to_symbol[symbol_id] = [id_to_symbol[i] for i in metadata['value']]
            elif symbol_type == 'tuple':
                id_to_symbol[symbol_id] = tuple(id_to_symbol[i] for i in metadata['value'])
            elif symbol_type == 'set':
                id_to_symbol[symbol_id] = {id_to_symbol[i] for i in metadata['value']}
            elif symbol_type == 'dict':
                id_to_symbol[symbol_id] = {
                    id_to_symbol[int(k)]: id_to_symbol[v]
                    for k, v in metadata['value'].items()
                }

        # 第四阶段：重建 IRBuilder
        builder = IRBuilder()

        for instr_data in serialized['instructions']:
            opcode_value = instr_data['opcode']
            operands = [id_to_symbol[op_id] for op_id in instr_data['operands']]

            from dovetail.core.__future__.instructions import IRInstruction, IROpCode

            # 如果 IROpcode 有 value 到枚举的映射
            opcode = IROpCode.find(opcode_value)

            instruction = IRInstruction(opcode, *operands)
            builder.insert(instruction)

        return builder

    @staticmethod
    def dump(builder: IRBuilder) -> bytes:
        """将 IRBuilder 序列化并冻结为字节数据。

        Args:
            builder (IRBuilder): 要序列化的 IRBuilder 实例。

        Returns:
            bytes: 序列化后的字节数据。
        """
        return IRSymbolSerializer.serializer.freeze(IRSymbolSerializer(builder).serialize())

    @staticmethod
    def load(data: bytes) -> dict:
        """将字节数据解冻为可读的数据结构。

        Args:
            data (bytes): 需要解析的字节数据。

        Returns:
            dict: 解析后的字典数据。
        """
        return IRSymbolSerializer.serializer.thaw(data)
