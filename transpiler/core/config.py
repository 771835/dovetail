# coding=utf-8
"""
项目全局配置/常量
"""
import fastjsonschema

from transpiler.utils.logging_plus import ThreadSafeLogger

PROJECT_NAME = "Dovetail"
PROJECT_WEBSITE = "https://github.com/771835/dovetail"
PROJECT_VERSION = "1.0.1"
FILE_PREFIX = ".mcdl"
CACHE_FILE_PREFIX = ".mcdc"
PACK_CONFIG_VALIDATOR = fastjsonschema.compile({
    "type": "object",
    "title": "目录配置文件",
    "properties": {
        "main": {
            "type": "string",
        }
    },
    "required": ["main"]
})
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
logger: ThreadSafeLogger | None = None


def set_project_logger(new_logger: ThreadSafeLogger):
    global logger
    logger = new_logger


def get_project_logger():
    return logger
