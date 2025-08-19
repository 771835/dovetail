# coding=utf-8
"""IRBuilder序列化工具"""
import time
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
        metadata: dict[str, str | None | bool | list | dict] = {
            'symbol_type': type(symbol).__name__,
            'symbol_name': symbol.get_name() if isinstance(symbol, Symbol) else None,
        }
        if isinstance(symbol, (int, float, bool, str)):
            metadata['value'] = symbol
        elif isinstance(symbol, (list, tuple)):
            metadata['value'] = [
                {'ref': id(i)} for i in symbol
            ]
        elif isinstance(symbol, dict):
            metadata['value'] = {}
            for key, value in symbol.items():
                metadata['value'][id(key)] = id(value)
        elif isinstance(symbol, Enum):
            metadata['value'] = symbol.value
        elif isinstance(symbol, (Variable, Constant)):
            metadata['dtype'] = {"ref": id(symbol.dtype)}
            metadata['var_type'] = {"ref": id(symbol.var_type)}
        elif isinstance(symbol, Literal):
            metadata['value'] = symbol.value
        elif isinstance(symbol, Parameter):
            metadata['var'] = {'ref': id(symbol.var)}
            metadata['optional'] = symbol.optional
            metadata['default'] = {'ref': id(symbol.default)}
        elif isinstance(symbol, Reference):
            metadata['value_type'] = symbol.value_type.value
            metadata['value'] = {'ref': id(symbol.value)}
        elif isinstance(symbol, Function):
            metadata['params'] = {param_symbol.get_name(): id(param_symbol) for param_symbol in symbol.params}
            metadata['return_type'] = {'type_name': symbol.return_type.name}
            metadata['function_type'] = {'ref': id(symbol.function_type)}
        elif isinstance(symbol, Class):
            metadata['methods'] = [{'ref': id(func_symbol)} for func_symbol in symbol.methods]
            metadata['interface'] = {'ref': id(symbol.interface)}
            metadata['parent'] = {'ref': id(symbol.parent)}
            metadata['constants'] = [{'ref': id(const_symbol)} for const_symbol in symbol.constants]
            metadata['variables'] = [{'ref': id(var_symbol)} for var_symbol in symbol.variables]
            metadata['type'] = {'ref': id(symbol.type)}

        return metadata

    def _add_symbol_id_map(self, symbol: Symbol):
        # 将自身加入映射表
        if id(symbol) not in self.symbol_id_map:
            self.symbol_id_map[id(symbol)] = symbol
        # 将符号中所有符号也加入其中
        if isinstance(symbol, Reference):
            self._add_symbol_id_map(symbol.value)
            self._add_symbol_id_map(symbol.get_data_type())
        elif isinstance(symbol, Function):
            for param_symbol in symbol.params:
                self._add_symbol_id_map(param_symbol)
            self._add_symbol_id_map(symbol.return_type)
        elif isinstance(symbol, Parameter):
            self._add_symbol_id_map(symbol.var)
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
            'time': time.time(),
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
