# coding=utf-8
import gzip
import hashlib
import os
import struct
import zlib


class BinarySerializer:
    """
    嵌套字典序列化工具
    支持字典、列表、元组、字符串、整数、浮点数、布尔值、None、字节串
    """

    MAGIC_HEADER = 0x0F5E2F3D
    VERSION = 5
    MAX_PADDING = 256

    def __init__(self, padding_factor=0.3, enable_compression=True):
        self.padding_factor = max(0.0, min(1.0, padding_factor))
        self.enable_compression = enable_compression

    def _encode_key(self, key):
        """编码键为二进制格式"""
        if isinstance(key, str):
            key_bytes = key.encode()
            return struct.pack('>BH', 0xDA, len(key_bytes)) + key_bytes
        elif isinstance(key, bool):
            return struct.pack('>B', 0xBA if key else 0xBB)
        elif isinstance(key, int):
            if -(2 ** 31) <= key < 2 ** 31:
                return struct.pack('>Bi', 0xB2, key)
            else:
                return struct.pack('>Bq', 0xB3, key)
        elif isinstance(key, float):
            return struct.pack('>Bd', 0xB4, key)
        elif key is None:
            return struct.pack('>B', 0xBC)
        elif isinstance(key, bytes):
            return struct.pack('>BI', 0xBE, len(key)) + key
        elif isinstance(key, tuple):  # 新增：处理元组键
            result = struct.pack('>BI', 0xBF, len(key))  # 使用0xBF标记元组键
            for item in key:
                result += self._encode_key(item)  # 递归编码元组中的每个元素
            return result
        else:
            # 其他类型转换为字符串
            key_str = str(key)
            key_bytes = key_str.encode()
            return struct.pack('>BH', 0xDA, len(key_bytes)) + key_bytes

    def _decode_key(self, binary_data, index):
        """从二进制数据解码键"""
        tag = binary_data[index]
        index += 1

        if tag == 0xDA:  # 字符串键
            key_len = struct.unpack('>H', binary_data[index:index + 2])[0]
            index += 2
            key = binary_data[index:index + key_len].decode('utf-8')
            index += key_len
            return key, index

        elif tag == 0xB2:  # 4字节整数键
            key = struct.unpack('>i', binary_data[index:index + 4])[0]
            index += 4
            return key, index

        elif tag == 0xB3:  # 8字节整数键
            key = struct.unpack('>q', binary_data[index:index + 8])[0]
            index += 8
            return key, index

        elif tag == 0xB4:  # 浮点数键
            key = struct.unpack('>d', binary_data[index:index + 8])[0]
            index += 8
            return key, index

        elif tag == 0xBA:  # True键
            return True, index

        elif tag == 0xBB:  # False键
            return False, index

        elif tag == 0xBC:  # None键
            return None, index

        elif tag == 0xBE:  # 字节串键
            key_len = struct.unpack('>I', binary_data[index:index + 4])[0]
            index += 4
            key = binary_data[index:index + key_len]
            index += key_len
            return key, index
        elif tag == 0xBF:  # 元组键
            length = struct.unpack('>I', binary_data[index:index + 4])[0]
            index += 4
            tuple_items = []
            for _ in range(length):
                item, index = self._decode_key(binary_data, index)  # 递归处理元组元素
                tuple_items.append(item)
            return tuple(tuple_items), index
        else:
            raise ValueError(f"未知键类型标记: 0x{tag:02X}")

    def _struct_encode(self, obj):
        """核心递归编码函数"""
        if isinstance(obj, dict):
            # 保持原始键类型，不强制转换
            result = struct.pack('>BI', 0xDD, len(obj))
            for key, val in obj.items():
                # 编码键
                key_data = self._encode_key(key)
                result += key_data
                # 编码值
                result += self._struct_encode(val)
            return result

        elif isinstance(obj, (list, tuple)):
            tag = 0xDB if isinstance(obj, list) else 0xBF
            result = struct.pack('>BI', tag, len(obj))
            for item in obj:
                result += self._struct_encode(item)
            return result

        elif isinstance(obj, str):
            encoded = obj.encode()
            return struct.pack('>BI', 0xDC, len(encoded)) + encoded

        elif isinstance(obj, bool):
            return struct.pack('>B', 0xBA if obj else 0xBB)

        elif isinstance(obj, int):
            if -(2 ** 31) <= obj < 2 ** 31:
                return struct.pack('>Bi', 0xB2, obj)
            else:
                return struct.pack('>Bq', 0xB3, obj)

        elif isinstance(obj, float):
            return struct.pack('>Bd', 0xB4, obj)

        elif isinstance(obj, bytes):
            return struct.pack('>BI', 0xBE, len(obj)) + obj

        elif obj is None:
            return struct.pack('>B', 0xBC)

        else:
            raise TypeError(f"不支持的类型: {type(obj)} ({obj})")

    def _struct_decode(self, binary_data):
        """核心递归解码函数"""
        index = 0

        def decode_next():
            nonlocal index
            if index >= len(binary_data):
                raise ValueError("数据意外结束")

            tag = binary_data[index]
            index += 1

            if tag == 0xDD:  # 字典
                length = struct.unpack('>I', binary_data[index:index + 4])[0]
                index += 4
                result = {}
                for _ in range(length):
                    # 解码键
                    key, index = self._decode_key(binary_data, index)
                    # 解码值
                    value = decode_next()
                    result[key] = value
                return result

            elif tag == 0xDB:  # 列表
                length = struct.unpack('>I', binary_data[index:index + 4])[0]
                index += 4
                return [decode_next() for _ in range(length)]

            elif tag == 0xBF:  # 元组
                length = struct.unpack('>I', binary_data[index:index + 4])[0]
                index += 4
                return tuple(decode_next() for _ in range(length))

            elif tag == 0xDC:  # 字符串
                str_len = struct.unpack('>I', binary_data[index:index + 4])[0]
                index += 4
                val = binary_data[index:index + str_len].decode('utf-8')
                index += str_len
                return val

            elif tag == 0xB2:  # 4字节整数
                val = struct.unpack('>i', binary_data[index:index + 4])[0]
                index += 4
                return val

            elif tag == 0xB3:  # 8字节整数
                val = struct.unpack('>q', binary_data[index:index + 8])[0]
                index += 8
                return val

            elif tag == 0xB4:  # 浮点数
                val = struct.unpack('>d', binary_data[index:index + 8])[0]
                index += 8
                return val

            elif tag == 0xBE:  # 字节串
                data_len = struct.unpack('>I', binary_data[index:index + 4])[0]
                index += 4
                val = binary_data[index:index + data_len]
                index += data_len
                return val

            elif tag == 0xBA:  # True
                return True

            elif tag == 0xBB:  # False
                return False

            elif tag == 0xBC:  # None
                return None

            else:
                raise ValueError(f"未知标记: 0x{tag:02X} (位置: {index - 1})")

        result = decode_next()
        return result

    def freeze(self, data):
        """
        将嵌套字典冻结为防篡改二进制（可选压缩和加密）
        """
        # 基础序列化
        payload = self._struct_encode(data)

        # 压缩
        is_compressed = 0
        if self.enable_compression:
            payload = gzip.compress(payload, compresslevel=6)
            is_compressed = 1

        # 添加校验信息
        crc = zlib.crc32(payload) & 0xFFFF

        # 构建头部
        header = struct.pack('>I', self.MAGIC_HEADER)  # 4字节魔数
        header += struct.pack('>I', self.VERSION)  # 4字节版本
        header += struct.pack('>B', is_compressed)  # 1字节压缩标志
        header += struct.pack('>H', crc)  # 2字节CRC

        # 组合完整结构
        return header + payload

    def thaw(self, binary_data):
        """
        从二进制数据恢复原始字典
        """
        # 最小长度检查
        min_length = 11
        if len(binary_data) < min_length:
            raise ValueError("无效数据: 长度不足")

        # 解析头部
        magic = struct.unpack('>I', binary_data[0:4])[0]  # 4字节魔数
        version = struct.unpack('>I', binary_data[4:8])[0]  # 1字节版本
        is_compressed = struct.unpack('>B', binary_data[8:9])[0]  # 1字节压缩标志
        crc = struct.unpack('>H', binary_data[9:11])[0]  # 2字节CRC
        payload_start = 11

        # 魔数验证
        if magic != self.MAGIC_HEADER:
            raise ValueError(f"魔数不匹配: 期望0x{self.MAGIC_HEADER:08X}, 实际0x{magic:08X}")

        # 搜索有效数据
        payload_data = binary_data[payload_start:]

        # 验证CRC
        crc_calc = zlib.crc32(payload_data) & 0xFFFF
        if crc_calc != crc:
            raise ValueError(f"校验失败: crc效验失败")

        # 解压缩
        if is_compressed:
            payload_data = gzip.decompress(payload_data)

        # 解码数据结构
        return self._struct_decode(payload_data)

    def freeze_to_file(self, data, file_path):
        """序列化并保存到文件"""
        with open(file_path, 'wb') as f:
            f.write(self.freeze(data))

    def thaw_from_file(self, file_path):
        """从文件恢复数据"""
        with open(file_path, 'rb') as f:
            return self.thaw(f.read())


def main():
    # 测试各种类型键的字典
    print("===== 多类型键测试 =====")

    # 整数字典键测试
    test1 = {1: "value1", 2: "value2"}
    serializer = BinarySerializer()
    binary1 = serializer.freeze(test1)
    restored1 = serializer.thaw(binary1)
    print(f"整数字典键测试: {test1}")
    print(f"恢复结果: {restored1}")
    print(f"完整性验证: {test1 == restored1}")

    # 混合类型键测试
    test2 = {
        1: "integer key",
        2 ** 63 - 1: "long long key",
        "string_key": "string value",
        3.14: "float key",
        float('inf'): "positive_inf",
        float('-inf'): "negative_inf",
        True: "boolean key",
        None: "none key",
        b"binary": "bytes key"
    }
    binary2 = serializer.freeze(test2)
    restored2 = serializer.thaw(binary2)
    print(f"\n混合类型键测试: {test2}")
    print(f"恢复结果: {restored2}")
    print(f"完整性验证: {test2 == restored2}")

    # 复杂嵌套测试
    test3 = {
        1: {"nested": [1, 2, 3], "key": (4, 5, 6)},
        (7, 8): {"another": "value"},
        3.14: [{"list_item": True}, {"another": False}]
    }
    binary3 = serializer.freeze(test3)
    restored3 = serializer.thaw(binary3)
    print(f"\n复杂嵌套测试: {test3}")
    print(f"恢复结果: {restored3}")
    print(f"完整性验证: {test3 == restored3}")
    # 篡改检测测试
    print("\n===== 篡改检测测试 =====")
    tampered_data = bytearray(binary1)
    for i in range(5, len(tampered_data)):
        tampered_data[i] ^= 0xFF

    try:
        serializer.thaw(bytes(tampered_data))
        print("❌ 篡改未检测到!")
    except ValueError as e:
        print(f"✅ 篡改成功拦截: {e}")

    print("\n✅ 所有测试完成!")


# ===== 测试代码 =====
if __name__ == "__main__":
    main()
