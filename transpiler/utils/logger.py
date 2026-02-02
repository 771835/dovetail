import json
import logging
import os
import sys
import threading
from logging.handlers import RotatingFileHandler
from typing import Optional, Union


class MessageTranslator:
    """消息翻译器，支持根据键翻译消息"""

    _lock = threading.Lock()
    _instance = None
    _translations = {}

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
            return cls._instance

    def __init__(self):
        if hasattr(self, '_initialized'):
            return
        self._initialized = True

    def load_translations_from_json(self, json_file: str):
        """从JSON文件加载翻译"""
        try:
            with open(json_file, encoding='utf-8') as f:
                translations = json.load(f)
                with self._lock:
                    self._translations.update(translations)
        except FileNotFoundError:
            print(f"警告: 翻译文件 {json_file} 不存在")
        except json.JSONDecodeError as e:
            print(f"错误: 翻译文件 {json_file} 格式错误 - {e}")

    def translate(self, key: str, *args) -> str:
        """根据键翻译消息，支持参数替换"""
        with self._lock:
            template = self._translations.get(key, key)
            try:
                return template.format(*args)
            except (IndexError, KeyError) as e:
                return f"翻译错误 [{key}]: {template} (参数: {args})"


class ColoredFormatter(logging.Formatter):
    """彩色日志格式化器"""

    # ANSI颜色代码
    COLORS = {
        'DEBUG': '\033[36m',  # 青色
        'INFO': '\033[32m',  # 绿色
        'WARNING': '\033[33m',  # 黄色
        'ERROR': '\033[31m',  # 红色
        'CRITICAL': '\033[35m',  # 紫色
        'RESET': '\033[0m'  # 重置
    }

    def format(self, record):
        # 获取日志级别对应的颜色
        level_color = self.COLORS.get(record.levelname, '')
        reset_color = self.COLORS['RESET']

        # 应用颜色到整个日志消息
        record.levelname = f"{level_color}{record.levelname}{reset_color}"
        record.name = f"{level_color}{record.name}{reset_color}"

        return super().format(record)


class ThreadSafeLogger:
    """线程安全的日志记录器"""

    _lock = threading.Lock()
    _instances = {}
    _translator = MessageTranslator()

    def __new__(cls, name: str, level: Union[str, int] = logging.INFO):
        # 单例模式，确保同一名字的logger只有一个实例
        with cls._lock:
            if name not in cls._instances:
                cls._instances[name] = super().__new__(cls)
            return cls._instances[name]

    def __init__(self, name: str = 'default', level: Union[str, int] = logging.INFO):
        if hasattr(self, '_initialized'):
            return

        self._initialized = True
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        # 避免重复添加处理器
        if not self.logger.handlers:
            self._setup_handlers()

    def setLevel(self, level) -> None:
        self.logger.setLevel(level)

    def _setup_handlers(self):
        """设置日志处理器"""
        # 控制台处理器（彩色）
        console_handler = logging.StreamHandler(sys.stdout)
        console_formatter = ColoredFormatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)

    def _log(self, level: int, message: str, *args, **kwargs):
        """线程安全的日志记录方法"""
        with self._lock:
            self.logger.log(level, message, *args, **kwargs)

    def _translate_and_log(self, level: int, key: str, *args, **kwargs):
        """翻译消息并记录日志"""
        translated_message = self._translator.translate(key, *args)
        self._log(level, translated_message, **kwargs)

    def debug_t(self, key: str, *args, **kwargs):
        """翻译调试消息"""
        self._translate_and_log(logging.DEBUG, key, *args, **kwargs)

    def info_t(self, key: str, *args, **kwargs):
        """翻译信息消息"""
        self._translate_and_log(logging.INFO, key, *args, **kwargs)

    def warning_t(self, key: str, *args, **kwargs):
        """翻译警告消息"""
        self._translate_and_log(logging.WARNING, key, *args, **kwargs)

    def error_t(self, key: str, *args, **kwargs):
        """翻译错误消息"""
        self._translate_and_log(logging.ERROR, key, *args, **kwargs)

    def critical_t(self, key: str, *args, **kwargs):
        """翻译严重错误消息"""
        self._translate_and_log(logging.CRITICAL, key, *args, **kwargs)

    def debug(self, message: str, *args, **kwargs):
        """普通调试消息"""
        self._log(logging.DEBUG, message, *args, **kwargs)

    def info(self, message: str, *args, **kwargs):
        """普通信息消息"""
        self._log(logging.INFO, message, *args, **kwargs)

    def warning(self, message: str, *args, **kwargs):
        """普通警告消息"""
        self._log(logging.WARNING, message, *args, **kwargs)

    def error(self, message: str, *args, **kwargs):
        """普通错误消息"""
        self._log(logging.ERROR, message, *args, **kwargs)

    def critical(self, message: str, *args, **kwargs):
        """普通严重错误消息"""
        self._log(logging.CRITICAL, message, *args, **kwargs)

    def exception_t(self, key: str, *args, **kwargs):
        """记录翻译的异常信息"""
        translated_message = self._translator.translate(key, *args)
        with self._lock:
            self.logger.exception(translated_message, **kwargs)

    def exception(self, message: str, *args, **kwargs):
        """记录异常信息"""
        with self._lock:
            self.logger.exception(message, *args, **kwargs)


class LoggerFactory:
    """日志工厂类"""

    _lock = threading.Lock()
    _loggers = {}
    _translator = MessageTranslator()

    @classmethod
    def get_logger(cls, name: str = 'default',
                   level: Union[str, int] = logging.INFO,
                   log_file: Optional[str] = None,
                   max_bytes: int = 10485760,  # 10MB
                   backup_count: int = 5) -> ThreadSafeLogger:
        """
        获取日志记录器

        Args:
            name: 日志记录器名称
            level: 日志级别
            log_file: 日志文件路径（可选）
            max_bytes: 单个日志文件最大字节数
            backup_count: 保留的备份文件数量

        Returns:
            ThreadSafeLogger实例
        """
        with cls._lock:
            if name not in cls._loggers:
                cls._loggers[name] = cls._create_logger(
                    name, level, log_file, max_bytes, backup_count
                )
            return cls._loggers[name]

    @classmethod
    def _create_logger(cls, name: str, level: Union[str, int],
                       log_file: Optional[str], max_bytes: int, backup_count: int) -> ThreadSafeLogger:
        """创建日志记录器"""
        logger_instance = ThreadSafeLogger(name, level)

        if log_file:
            cls._add_file_handler(logger_instance, log_file, max_bytes, backup_count)

        return logger_instance

    @classmethod
    def _add_file_handler(cls, logger_instance: ThreadSafeLogger,
                          log_file: str, max_bytes: int, backup_count: int):
        """添加文件处理器（不带颜色）"""
        # 确保日志目录存在
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # 文件处理器（不带颜色）
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding='utf-8'
        )

        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_formatter)

        # 检查是否已存在文件处理器
        has_file_handler = any(
            isinstance(handler, RotatingFileHandler)
            for handler in logger_instance.logger.handlers
        )

        if not has_file_handler:
            logger_instance.logger.addHandler(file_handler)

    @classmethod
    def load_translations(cls, json_file: str):
        """加载翻译文件"""
        cls._translator.load_translations_from_json(json_file)


# 便捷函数
def get_logger(name: str = 'default',
               level: Union[str, int] = logging.INFO,
               log_file: Optional[str] = None) -> ThreadSafeLogger:
    """
    获取日志记录器的便捷函数

    Args:
        name: 日志记录器名称
        level: 日志级别 ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL')
        log_file: 日志文件路径（可选）

    Returns:
        ThreadSafeLogger实例
    """
    return LoggerFactory.get_logger(name, level, log_file)


def setup_logger(name: str = 'default',
                 level: Union[str, int] = logging.INFO,
                 log_file: Optional[str] = None) -> ThreadSafeLogger:
    """
    设置日志记录器的便捷函数

    Args:
        name: 日志记录器名称
        level: 日志级别
        log_file: 日志文件路径（可选）

    Returns:
        ThreadSafeLogger实例
    """
    return get_logger(name, level, log_file)


def load_translations(json_file: str):
    """加载翻译文件"""
    LoggerFactory.load_translations(json_file)


# 使用示例和测试代码
if __name__ == "__main__":
    # 创建日志记录器
    logger = get_logger('test_app', logging.DEBUG)

    # 测试普通日志
    logger.info("这是普通信息")
    logger.error("这是错误信息")
