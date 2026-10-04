# coding=utf-8
"""
桩函数写入器

根据函数签名生成桩函数
"""
import hashlib

from attrs import define

from backend.commands import Copy, DataPath, StorageLocation, FunctionBuilder
from dovetail.core.backend import OutputWriter, GenerationContext
from dovetail.core.symbols import Function
from dovetail.utils.logger import get_logger

logger = get_logger(__name__)


@define
class StubFunction:
    """一个需要生成桩函数的函数"""

    func: Function
    func_path: str  # 点分路径，如 "math.sqrt"
    stub_func_path: str  # 命名空间路径，如 "mymod:stub/math/sqrt"
    abi: str
    objective: str

    @property
    def name(self) -> str:
        return self.func.name

    @property
    def stub_hash(self) -> str:
        """stub_func_path 的 MD5 摘要"""
        return hashlib.md5(self.stub_func_path.encode()).hexdigest()

    @property
    def func_hash(self) -> str:
        """func_path 的 MD5 摘要"""
        return hashlib.md5(self.func_path.encode()).hexdigest()


class StubFunctionWriter(OutputWriter):

    def __init__(self, stub_functions: list[StubFunction]):
        self.stub_functions = stub_functions

    def write(self, context: GenerationContext):
        for stub_func in self.stub_functions:
            if stub_func.abi == "dovetail":
                self._write_dovetail(stub_func, context)
            else:
                logger.warning(f"Unknown ABI: {stub_func.abi}, skipped.")

    def _write_dovetail(self, stub_func: StubFunction, context: GenerationContext):
        """写入一个 dovetail 协议的桩函数"""
        namespace, path = stub_func.stub_func_path.split(":")
        func_file = (
                context.target / context.namespace / "data" / namespace / "function" / path
        ).with_suffix(".mcfunction")
        func_file.parent.mkdir(parents=True, exist_ok=True)

        commands: list[str] = []
        sf_hash = stub_func.stub_hash

        # 复制形参
        for param in stub_func.func.params:
            storage = StorageLocation.get_storage(param.dtype)
            commands.append(Copy.copy(
                DataPath(f"{stub_func.func_path}.{param.get_name()}", context.objective, storage),
                DataPath(f"{sf_hash}.{param.get_name()}", stub_func.objective, storage),
            ))

        # 调用实际函数
        commands.append(FunctionBuilder.run(
            f"{context.namespace}:{stub_func.func_path.replace('.', '/')}"
        ))

        # 复制返回值
        ret_storage = StorageLocation.get_storage(stub_func.func.return_type)
        commands.append(Copy.copy(
            DataPath(f"return_{sf_hash}", stub_func.objective, ret_storage),
            DataPath(f"return_{stub_func.func_hash}", context.objective, ret_storage),
        ))

        with open(func_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(commands))

    def get_name(self) -> str:
        return "stub_function_writer"