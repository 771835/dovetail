# coding=utf-8
"""IRBuilder序列化工具"""
import time
import uuid
from enum import Enum

from transpiler.core.backend.ir_builder import IRBuilder
from transpiler.core.enums import DataType
from transpiler.core.symbols import Symbol, Variable, Constant, Literal, Parameter, Reference, Class, Function
from transpiler.utils.binary_serializer import BinarySerializer

version = "1.0.0"


class IRSymbolSerializer:
    serializer = BinarySerializer(0.37, obf_key=0x12)

    def __init__(self, builder: IRBuilder):
        self.builder = builder
        self.symbol_id_map: dict[int, Symbol | str | int | Enum] = {}

    @staticmethod
    def _extract_metadata(symbol: Symbol | DataType | list):
        """生成符号的序列化数据"""
        if symbol is None:
            return None
        metadata: dict[str, str | None | bool | list | dict | int] = {
            'symbol_type': type(symbol).__name__,
            'symbol_name': symbol.get_name() if isinstance(symbol, Symbol) else None,
        }
        if isinstance(symbol, (int, float, bool, str)):
            metadata['value'] = symbol
        elif isinstance(symbol, (list, tuple)):
            metadata['value'] = [id(i) for i in symbol]
        elif isinstance(symbol, dict):
            metadata['value'] = {}
            for key, value in symbol.items():
                metadata['value'][id(key)] = id(value)
        elif isinstance(symbol, Enum):
            metadata['value'] = symbol.value
        elif isinstance(symbol, (Variable, Constant)):
            metadata['dtype'] = id(symbol.dtype)
            metadata['var_type'] = id(symbol.var_type)
        elif isinstance(symbol, Literal):
            metadata['value'] = symbol.value
        elif isinstance(symbol, Parameter):
            metadata['var'] = id(symbol.var)
            metadata['optional'] = symbol.optional
            metadata['default'] = id(symbol.default)
        elif isinstance(symbol, Reference):
            metadata['value_type'] = symbol.value_type.value
            metadata['value'] = id(symbol.value)
        elif isinstance(symbol, Function):
            metadata['params'] = {param_symbol.get_name(): id(param_symbol) for param_symbol in symbol.params}
            metadata['return_type'] = id(symbol.return_type)
            metadata['function_type'] = id(symbol.function_type)
        elif isinstance(symbol, Class):
            metadata['methods'] = [id(func_symbol) for func_symbol in symbol.methods]
            metadata['interface'] = id(symbol.interface)
            metadata['parent'] = id(symbol.parent)
            metadata['constants'] = [id(const_symbol) for const_symbol in symbol.constants]
            metadata['variables'] = [id(var_symbol) for var_symbol in symbol.variables]
            metadata['type'] = id(symbol.type)

        return metadata

    def _add_symbol_id_map(self, symbol: Symbol | Enum | list | dict | bool):
        # 将自身加入映射表
        if id(symbol) not in self.symbol_id_map:
            self.symbol_id_map[id(symbol)] = symbol
        # 将符号中所有符号也加入其中
        if isinstance(symbol, Reference):
            self._add_symbol_id_map(symbol.value)
            self._add_symbol_id_map(symbol.value_type)
        elif isinstance(symbol, (Variable, Constant)):
            self._add_symbol_id_map(symbol.dtype)
            self._add_symbol_id_map(symbol.var_type)
        elif isinstance(symbol, Function):
            for param_symbol in symbol.params:
                self._add_symbol_id_map(param_symbol)
            self._add_symbol_id_map(symbol.return_type)
            self._add_symbol_id_map(symbol.function_type)
        elif isinstance(symbol, Parameter):
            self._add_symbol_id_map(symbol.var)
            self._add_symbol_id_map(symbol.optional)
            self._add_symbol_id_map(symbol.default)
        elif isinstance(symbol, (list, tuple)):
            for i in symbol:
                self._add_symbol_id_map(i)
        elif isinstance(symbol, dict):
            for key, value in symbol.items():
                self._add_symbol_id_map(key)
                self._add_symbol_id_map(value)

    def serialize(self) -> dict:
        """序列化整个IRBuilder"""
        result = {}

        # 预扫描所有符号
        for instr in self.builder.get_instructions():
            for op in instr.get_operands():
                self._add_symbol_id_map(op)

        result['metadata'] = {
            'version': version,
            'time': time.time_ns(),
            'minecraft_version': '2.0',
            uuid.uuid4().hex: uuid.uuid4().hex,
        }
        result['symbol'] = {
            id_: self._extract_metadata(metadata)
            for id_, metadata in self.symbol_id_map.items()
        }
        result['instructions'] = [
            {
                "opcode": instr.opcode.value,
                "operands": [id(op) for op in instr.operands],
                "flags": instr.flags,
            } for instr in self.builder.get_instructions()
        ]
        return result

    @staticmethod
    def dump(builder: IRBuilder, password=None) -> bytes:
        return IRSymbolSerializer.serializer.freeze(IRSymbolSerializer(builder).serialize(), password)

    @staticmethod
    def load(data: bytes, password=None) -> dict:
        return IRSymbolSerializer.serializer.thaw(data, password)
