# coding=utf-8
"""IRBuilder序列化工具"""
from enum import Enum

from transpiler.core.backend.ir_builder import IRBuilder
from transpiler.core.enums import DataType
from transpiler.core.symbols import Symbol, Variable, Constant, Literal, Parameter, Reference, Class, Function
from transpiler.utils.binary_serializer import BinarySerializer

version = "1.0.0"


class IRSymbolSerializer:
    serializer = BinarySerializer(0.37, True, 0x12)

    @staticmethod
    def _extract_metadata(symbol: Symbol | DataType):
        """生成符号的序列化数据"""
        if symbol is None:
            return None
        metadata: dict[str, str | None | bool | list | dict] = {
            'symbol_type': type(symbol).__name__
        }
        if isinstance(symbol, (int, float, bool, str)):
            metadata['value'] = symbol
        elif isinstance(symbol, (list, tuple)):
            metadata['value'] = [IRSymbolSerializer._extract_metadata(i) for i in symbol]
        elif isinstance(symbol, Enum):
            metadata['value'] = symbol.value
        # 如果不是符号直接跳出，不执行后续代码
        if not isinstance(symbol, Symbol):
            return metadata

        if isinstance(symbol, (Variable, Constant)):
            # 为避免循环引用，因此dtype采用字符串记录
            metadata['dtype'] = {"type_name": symbol.dtype.name}
            metadata['var_type'] = symbol.var_type.value
        elif isinstance(symbol, Literal):
            metadata['value'] = symbol.value
        elif isinstance(symbol, Parameter):
            metadata['var'] = IRSymbolSerializer._extract_metadata(symbol.var)
            metadata['optional'] = symbol.optional
            metadata['default'] = IRSymbolSerializer._extract_metadata(symbol.default)
        elif isinstance(symbol, Reference):
            metadata['value_type'] = symbol.value_type.value
            metadata['value'] = IRSymbolSerializer._extract_metadata(symbol.value)
        elif isinstance(symbol, Function):
            metadata['params'] = [IRSymbolSerializer._extract_metadata(param_symbol) for param_symbol in symbol.params]
            metadata['return_type'] = {"type_name": symbol.return_type.name}
            metadata['function_type'] = symbol.function_type.value
        elif isinstance(symbol, Class):
            metadata['methods'] = [IRSymbolSerializer._extract_metadata(func_symbol) for func_symbol in symbol.methods]
            metadata['interface'] = IRSymbolSerializer._extract_metadata(symbol.interface)
            metadata['parent'] = IRSymbolSerializer._extract_metadata(symbol.parent)
            metadata['constants'] = [IRSymbolSerializer._extract_metadata(const_symbol) for const_symbol in
                                     symbol.constants]
            metadata['variables'] = [IRSymbolSerializer._extract_metadata(var_symbol) for var_symbol in
                                     symbol.variables]
            metadata['type'] = symbol.type.value

        metadata['symbol_name'] = symbol.get_name()
        return metadata

    @staticmethod
    def serialize(builder: IRBuilder) -> dict:
        """序列化整个IRBuilder"""
        result = {}
        symbol_id_map: dict[int, Symbol] = {}
        # 预扫描所有符号
        for instr in builder.get_instructions():
            for op in instr.get_operands():
                if id(op) not in symbol_id_map:
                    symbol_id_map[id(op)] = op

        result['metadata'] = {
            'version': version,
        }
        result['symbol'] = {
            id_: IRSymbolSerializer._extract_metadata(metadata)
            for id_, metadata in symbol_id_map.items()
        }
        result['instructions'] = [
            {
                "opcode": instr.opcode.value,
                "operands": [id(op) for op in instr.operands],
                "flags": instr.flags,
            } for instr in builder.get_instructions()
        ]
        return result

    @staticmethod
    def dump(builder:IRBuilder) -> bytes:
        data = IRSymbolSerializer.serialize(builder)
        return IRSymbolSerializer.serializer.freeze(data)

    @staticmethod
    def load(data: bytes) -> dict:
        return IRSymbolSerializer.serializer.thaw(data)
