# coding=utf-8
from dataclasses import dataclass, field
from typing import Callable, Any
from pathlib import Path
import json
from functools import lru_cache


@dataclass
class CommandTemplate:
    """
    命令模板定义
    """
    name: str
    template: str  # Minecraft 命令模板字符串
    function_path: str  # 宏函数路径
    param_names: list[str]  # 必需参数列表
    optional_params: dict[str, Any] = field(default_factory=dict)  # 可选参数及默认值
    validator: Callable | None = None  # 参数验证器
    description: str = ""  # 模板描述
    tags: list[str] = field(default_factory=list) # 命令分类标签

    def validate_params(self, params: dict[str, Any]) -> tuple[bool, str]:
        """
        验证参数完整性

        Returns:
            (是否有效, 错误信息)
        """
        # 检查必需参数
        missing = set(self.param_names) - set(params.keys())
        if missing:
            return False, f"Missing required parameters: {missing}"

        # 自定义验证器
        if self.validator:
            return self.validator(params)

        return True, ""

    def get_all_params(self, provided_params: dict[str, Any]) -> dict[str, Any]:
        """合并提供的参数和默认参数"""
        return {**self.optional_params, **provided_params}

    @classmethod
    def from_dict(cls, data: dict) -> 'CommandTemplate':
        """从字典创建模板"""
        return cls(
            name=data['name'],
            template=data['template'],
            function_path=data['function_path'],
            param_names=data.get('param_names', []),
            optional_params=data.get('optional_params', {}),
            description=data.get('description', ''),
            tags=data.get('tags', [])
        )

    def to_dict(self) -> dict:
        """导出为字典"""
        return {
            'name': self.name,
            'template': self.template,
            'function_path': self.function_path,
            'param_names': self.param_names,
            'optional_params': self.optional_params,
            'description': self.description,
            'tags': self.tags,
        }


class TemplateRegistry:
    """
    模板注册中心
    """

    _templates: dict[str, CommandTemplate] = {}
    _template_dir: Path | None = None

    @classmethod
    def set_template_dir(cls, path: str | Path):
        """设置模板目录"""
        cls._template_dir = Path(path)

    @classmethod
    def register(cls, template: CommandTemplate):
        """注册单个模板"""
        cls._templates[template.name] = template

    @classmethod
    def register_from_file(cls, file_path: str | Path):
        """从 JSON 文件加载模板"""
        path = Path(file_path)
        if not path.is_absolute() and cls._template_dir:
            path = cls._template_dir / path

        with open(path, encoding='utf-8') as f:
            data = json.load(f)

        if isinstance(data, list):
            # 批量加载
            for item in data:
                template = CommandTemplate.from_dict(item)
                cls.register(template)
        else:
            # 单个模板
            template = CommandTemplate.from_dict(data)
            cls.register(template)

    @classmethod
    def register_from_directory(cls, dir_path: str | Path):
        """从目录批量加载所有 .json 模板文件"""
        path = Path(dir_path)
        if not path.is_absolute() and cls._template_dir:
            path = cls._template_dir / path

        for json_file in path.glob('**/*.json'):
            try:
                cls.register_from_file(json_file)
            except Exception as e:
                print(f"Warning: Failed to load template from {json_file}: {e}")

    @classmethod
    @lru_cache(maxsize=256)
    def get(cls, name: str) -> CommandTemplate | None:
        """通过名称获取模板（带缓存）"""
        return cls._templates.get(name)
    @classmethod
    def has(cls, name: str) -> bool:
        return name in cls._templates

    @classmethod
    def get_by_path(cls, function_path: str) -> CommandTemplate | None:
        """通过函数路径获取模板"""
        for template in cls._templates.values():
            if template.function_path == function_path:
                return template
        return None

    @classmethod
    def all(cls) -> dict[str, CommandTemplate]:
        """获取所有模板"""
        return cls._templates.copy()

    @classmethod
    def clear(cls):
        """清空注册表"""
        cls._templates.clear()
        cls.get.cache_clear()