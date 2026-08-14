# coding=utf-8
from dovetail.plugins.plugin_api.plugin import Plugin  # noqa
from .v2 import *  # noqa

def compiler_version() -> str:
    from dovetail.core.config import PROJECT_VERSION
    return PROJECT_VERSION


def api_version() -> str:
    return "2.1"
