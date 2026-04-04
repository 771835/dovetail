# coding=utf-8
"""
后端工厂
"""
from pathlib import Path
from typing import Dict, Type

from dovetail.core.backend.base import Backend
from dovetail.core.compile_config import CompileConfig
from dovetail.core.config import get_project_logger
from dovetail.core.errors import report, Errors, CompilationError
from dovetail.core.ir_builder import IRBuilder


class BackendNotFoundError(CompilationError):
    """后端未找到"""
    pass


class BackendFactory:
    """后端工厂"""

    _backends: Dict[str, Type[Backend]] = {}

    @classmethod
    def register(cls, backend_class: Type[Backend]):
        """注册后端"""
        name = backend_class.get_name()
        cls._backends[name] = backend_class
        get_project_logger().info(f"Registered backend: {name}")

    @classmethod
    def create(cls, name: str, ir_builder: IRBuilder, target: Path, config: CompileConfig) -> Backend | None:
        """
        创建后端实例

        Args:
            name: 后端名称
            ir_builder: IR构建器
            target: 输出目标路径
            config: 编译配置

        Returns:
            后端实例

        Raises:
            BackendNotFoundError: 未找到后端时
        """
        backend_class = cls._backends.get(name)
        if not backend_class:
            report(
                Errors.ConfigurationError,
                f"后端 {name} 不存在。",
            )
            raise BackendNotFoundError(f"后端 {name} 不存在。")
        return backend_class(ir_builder, target, config)

    @classmethod
    def auto_select(cls, config: CompileConfig, backend_name: str = None) -> type[Backend] | None:
        """
        自动选择合适的后端

        Args:
            config: 编译配置
            backend_name: 后端名(不填时自动选择)

        Returns:
            后端类

        Raises:
            BackendNotFoundError: 没有合适的后端
        """
        if backend_name:
            backend = cls._backends.get(backend_name, None)
            if backend is not None:
                return backend
            report(
                Errors.UnsupportedTargetVersion,
                "没有找到适合该配置的合适后端",
            )
            raise BackendNotFoundError("没有找到适合该配置的合适后端")
        else:
            for name, backend in cls._backends.items():
                if backend.is_support(config):
                    get_project_logger().info(f"Selected backend '{name}' ({id(backend)}).")
                    return backend

        report(
            Errors.UnsupportedTargetVersion,
            "没有找到适合该配置的合适后端",
        )
        raise BackendNotFoundError("没有找到适合该配置的合适后端")

    @classmethod
    def get_available_backends(cls) -> list[str]:
        """获取所有可用后端名称"""
        return list(cls._backends.keys())
