# coding=utf-8
"""
项目全局配置/常量
"""
import fastjsonschema

from dovetail.utils.logger import ThreadSafeLogger

# 项目数据
PROJECT_NAME = "Dovetail"
PROJECT_WEBSITE = "https://github.com/771835/dovetail"
PROJECT_VERSION = "1.0.1"

# 文件后缀
FILE_PREFIX = ".mcdl"
CACHE_FILE_PREFIX = ".mcdc"

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
DEFAULT_RANDOM_SUGGESTION: list[str] = [
    "你有试过关掉再开吗？",
    "建议：不要写有 bug 的代码",
    "这不是一个 bug，这是一个未记录的特性",
    "试试把电脑倒过来？重力可能会修复它",
    "据统计，99% 的编译错误都是因为代码写错了",
    "你知道吗？正确的代码通常不会报错",
    "建议先检查一下今天是不是星期五",
    "也许你需要的是一杯咖啡，而不是修复代码",
    "Who set us up the compile error?",
    "友情提示：Ctrl+Z 可以撤销，但不能撤销人生",
    "把错误复制到 Stack Overflow，然后祈祷",
    "如果你不理解这个错误，那说明你理解对了",
    "All your code are belong to bugs",
    "试着把代码删掉重写？至少你会感觉在做点什么",
    "编译器永远是对的，除了它错的时候",
    "深呼吸，然后接受现实",
    "据不可靠消息称，重新启动计算机可以解决 0% 的编译错误",
    "保持冷静，假装你知道自己在干什么",
    "It works on my machine!",
    "Maybe it's your environment.",
    "Why not try other projects, suc... uh, clang-mc?",
    "The cake is a lie.",
    "机魂不悦!",
    "劳动者最光荣。",
    "或许你更需要的是换一门语言而不是来这里受虐。",
    "Avada Kedavra",
    ":wq!"
]

# 项目全局日志对象
logger: ThreadSafeLogger | None = None



def set_project_logger(new_logger: ThreadSafeLogger):
    global logger
    logger = new_logger


def get_project_logger():
    return logger
