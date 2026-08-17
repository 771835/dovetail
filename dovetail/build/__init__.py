# coding=utf-8
"""
Dovetail 构建工具包

独立于插件体系，负责项目级构建编排：
读取 dovetail.toml → 执行 hooks → 调用编译器
"""
from dovetail.build.builder import Builder
from dovetail.build.config import BuildConfig
from dovetail.build.hooks import run_hook

__all__ = ["Builder", "BuildConfig", "run_hook"]