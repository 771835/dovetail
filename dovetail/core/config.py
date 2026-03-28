# coding=utf-8
"""
项目全局配置/常量
"""
import fastjsonschema

from dovetail.utils.logger import ThreadSafeLogger

# 项目信息
PROJECT_NAME = "Dovetail"
PROJECT_WEBSITE = "https://github.com/771835/dovetail"
PROJECT_VERSION = "1.0.2-rc.1"

# 文件后缀
FILE_PREFIX = ".mcdl"
CACHE_FILE_PREFIX = ".mcdc"

# 杂项
MAX_FILE_SIZE = 1024 * 1024 * 1024  # 最大允许单个文件1GB大小
FAST_MODE = True  # 禁用一些编译器的类型检查以加速代码运行
USED_FUTURE_INSTRUCTIONS = True  # 临时选项: 启用新版IR指令
ENABLE_FUTURE_INSTRUCTION_VALIDATION = True  # 临时选项: 启用新版IR指令类型效验，当 FAST_MODE 开启时无效


# 目录编译配置文件
PACK_CONFIG_VALIDATOR = fastjsonschema.compile({
    "type": "object",
    "title": "目录配置文件",
    "properties": {
        "main": {
            "type": "string",
        },
        "description": {
            "type": "string",
        },
    },
    "required": ["main"]
})

# 插件元数据
PLUGIN_METADATA_VALIDATOR = fastjsonschema.compile({
    "type": "object",
    "properties": {
        "display_name": {
            "type": "string"
        },
        "plugin_main": {
            "type": "string"
        },
        "plugin_version": {
            "type": "string"
        },
        "plugin_type": {
            "type": "string",
            "enum": ["plugin", "library", "loader"]
        },
        "main_class": {
            "type": "string"
        },
        "plugin_author": {
            "type": "array",
            "items": {
                "type": "string"
            }
        }
    },
    "required": [  # 必需的字段
        "display_name",
        "plugin_main",
        "plugin_version",
        "plugin_type",
        "main_class",
        "plugin_author"
    ],
    "additionalProperties": False  # 不允许额外属性
})

# 默认错误建议列表
DEFAULT_SUGGESTIONS: list[str] = [
    "Who set us up the compile error?",
    "把错误复制到 Stack Overflow，然后祈祷",
    "All your code are belong to bugs",
    "深呼吸，然后接受现实",
    "保持冷静，假装你知道自己在干什么",
    "It works on my machine!",
    "Maybe it's your environment.",
    "Why not try other projects, suc... uh, clang-mc?",
    "The cake is a lie.",
    "机魂不悦!",
    "或许你更需要的是换一门语言而不是来这里受虐。",
    "Avada Kedavra",
    ":wq!",
    "为 MCFPP 默哀一分钟，伟大的作品胎死腹中。"
]

# 项目全局日志对象
logger: ThreadSafeLogger | None = None


def set_project_logger(new_logger: ThreadSafeLogger):
    global logger
    logger = new_logger


def get_project_logger():
    return logger
