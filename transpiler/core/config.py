# coding=utf-8
"""
项目全局配置/常量
"""
import fastjsonschema

PROJECT_NAME = "Dovetail"
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
