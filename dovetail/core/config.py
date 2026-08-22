# coding=utf-8
"""
项目全局配置/常量
"""

try:
    from dovetail._version import PROJECT_VERSION, COMMIT_HASH
except ImportError:
    # 开发模式下 _version.py 可能不存在
    PROJECT_VERSION = "dev"
    COMMIT_HASH = "unknown"

# 项目信息
PROJECT_NAME = "Dovetail"
PROJECT_WEBSITE = "https://github.com/771835/dovetail"
PROJECT_LICENSE = "Apache 2.0"

# 文件后缀
FILE_PREFIX = ".mcdl"
CACHE_FILE_PREFIX = ".mcdc"
IR_CACHE_FILE_PREFIX = ".mcdo"

# 杂项
MAX_FILE_SIZE = 1024 * 1024 * 1024  # 最大允许单个文件1GB大小
FAST_MODE = True  # 禁用一些编译器的内部类型检查以加速代码运行
ENABLE_INSTRUCTION_VALIDATION = True  # 启用IR指令类型效验，当 FAST_MODE 开启时无效
USE_FUTURE_IR_BUILDER = False # 启用基于链表的 IR 指令构建器，实测速度没有提高，不值得开启


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
    "审判开始",
    # "冷知识: 对着泽渡可可的照片干任何事情她都能看到，但是呢~她在魔女岛",
    # "都是汉娜干的!",
]
