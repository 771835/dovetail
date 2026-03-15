# coding=utf-8
import hashlib
import json
import time
from pathlib import Path
from typing import Optional, Callable

from dovetail.utils.logger import get_logger

# 设置日志
logger = get_logger(__name__)


class _CacheManager:
    """缓存管理器 - 处理缓存表的读写和验证"""

    def __init__(self, cache_dir: Path):
        self.cache_dir = cache_dir
        self.cache_table_file = cache_dir / "download_cache.json"
        self._cache_table: Optional[dict] = None

    @property
    def cache_table(self) -> dict:
        """延迟加载缓存表"""
        if self._cache_table is None:
            self._cache_table = self._load_cache_table()
        return self._cache_table

    def _load_cache_table(self) -> dict:
        """加载缓存表"""
        if not self.cache_table_file.exists():
            return {}

        try:
            with open(self.cache_table_file, encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.warning(f"Failed to read cache table: {e}")
            return {}

    def save_cache_table(self) -> bool:
        """保存缓存表"""
        try:
            with open(self.cache_table_file, 'w', encoding='utf-8') as f:
                json.dump(self._cache_table, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            logger.warning(f"Failed to save cache table: {e}")
            return False

    def get_cache_info(self, filepath: Path) -> Optional[dict]:
        """获取缓存信息"""
        return self.cache_table.get(str(filepath))

    def update_cache_info(self, filepath: Path, url: str, sha256: Optional[str] = None):
        """更新缓存信息"""
        self.cache_table[str(filepath)] = {
            'url': url,
            'size': filepath.stat().st_size,
            'sha256': sha256,
            'download_time': time.time()
        }
        self.save_cache_table()

    def remove_cache_entry(self, filepath: Path):
        """删除缓存条目"""
        cache_key = str(filepath)
        if cache_key in self.cache_table:
            del self.cache_table[cache_key]
            self.save_cache_table()

    def is_file_valid(self, filepath: Path, sha256: Optional[str] = None) -> bool:
        """验证文件是否有效"""
        if not filepath.exists():
            return False

        cached_info = self.get_cache_info(filepath)

        # 如果提供了 SHA256，进行哈希验证
        if sha256:
            return verify_file_hash(filepath, sha256)

        # 否则比较文件大小
        if cached_info:
            actual_size = filepath.stat().st_size
            return actual_size == cached_info.get('size', 0)

        # 文件存在但没有缓存记录，假定有效
        return True


def verify_file_hash(filepath: Path, expected_hash: str) -> bool:
    """验证文件的SHA256哈希值"""
    sha256_hash = hashlib.sha256()

    try:
        with open(filepath, 'rb') as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)

        actual_hash = sha256_hash.hexdigest()
        logger.debug(f"Expected hash: {expected_hash}")
        logger.debug(f"Actual hash: {actual_hash}")

        return actual_hash == expected_hash.lower()

    except Exception as e:
        logger.error(f"Hash verification failed: {e}")
        return False


def _get_file_size_from_head(url: str, headers: dict, timeout: float, verify_ssl: bool) -> int:
    """通过 HEAD 请求获取文件大小"""
    import requests

    try:
        head_response = requests.head(
            url,
            headers=headers,
            timeout=timeout / 2,
            verify=verify_ssl
        )
        head_response.raise_for_status()
        return int(head_response.headers.get('content-length', 0))
    except Exception:
        return 0


def _should_retry_on_error(status_code: Optional[int]) -> bool:
    """判断是否应该重试"""
    if status_code is None:
        return True
    # 4xx 客户端错误通常无法通过重试解决
    return status_code not in [400, 401, 403, 404, 410]


def download_file(
        url: str,
        filepath: Path,
        timeout: float = 30.0,
        max_retries: int = 3,
        retry_delay: float = 2.0,
        chunk_size: int = 8192,
        expected_sha256: Optional[str] = None,
        headers: Optional[dict[str, str]] = None,
        verify_ssl: bool = True,
        progress_callback: Optional[Callable[[int, int], None]] = None,
        user_agent: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
) -> bool:
    """
    安全下载文件的函数，支持重试机制和完整性验证

    Args:
        url: 要下载的文件URL
        filepath: 保存文件的路径
        timeout: 请求超时时间（秒）
        max_retries: 最大重试次数
        retry_delay: 重试延迟时间（秒）
        chunk_size: 分块下载大小
        expected_sha256: 预期的SHA256哈希值（可选，用于验证文件完整性）
        headers: 自定义请求头
        verify_ssl: 是否验证SSL证书
        progress_callback: 进度回调函数，参数为(已下载字节数, 总字节数)
        user_agent: 用户代理字符串

    Returns:
        bool: 下载是否成功

    Raises:
        ValueError: 当文件哈希验证失败时
        RequestException: 当所有重试都失败时
    """
    import requests
    from requests.exceptions import RequestException, Timeout, HTTPError, ConnectionError

    # 确保目录存在
    filepath.parent.mkdir(parents=True, exist_ok=True)

    # 设置默认请求头
    default_headers = {
        'User-Agent': user_agent,
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive'
    }
    if headers:
        default_headers.update(headers)

    # 重试机制
    for attempt in range(max_retries):
        try:
            if attempt > 0:
                delay = retry_delay * attempt  # 指数退避
                logger.info(f"Retry attempt {attempt + 1}/{max_retries} after {delay}s")
                time.sleep(delay)

            # 获取文件大小（仅第一次尝试）
            total_size = 0
            if progress_callback and attempt == 0:
                total_size = _get_file_size_from_head(url, default_headers, timeout, verify_ssl)

            # 发起GET请求下载文件
            logger.info(f"Downloading {url}")
            response = requests.get(
                url,
                stream=True,
                headers=default_headers,
                timeout=timeout,
                verify=verify_ssl
            )
            response.raise_for_status()

            # 从响应头获取文件大小（如果HEAD请求失败）
            if progress_callback and total_size == 0:
                total_size = int(response.headers.get('content-length', 0))

            # 分块下载文件
            downloaded = 0
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=chunk_size):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)

                        # 调用进度回调
                        if progress_callback and total_size > 0:
                            actual_total = max(total_size, downloaded)
                            progress_callback(downloaded, actual_total)

            logger.info(f"File downloaded successfully to {filepath}")

            # 验证文件完整性
            if expected_sha256:
                if not verify_file_hash(filepath, expected_sha256):
                    raise ValueError("SHA256 hash verification failed! File may be corrupted or tampered with.")

            return True

        except Timeout:
            logger.warning(f"Timeout occurred on attempt {attempt + 1}")
        except ConnectionError as e:
            logger.warning(f"Connection error on attempt {attempt + 1}: {e}")
        except HTTPError as e:
            status_code = e.response.status_code
            logger.warning(f"HTTP error {status_code} on attempt {attempt + 1}")
            if not _should_retry_on_error(status_code):
                break
        except ValueError as e:
            # 哈希验证失败，不重试
            logger.error(str(e))
            raise
        except RequestException as e:
            logger.warning(f"Request failed on attempt {attempt + 1}: {e}")
        except Exception as e:
            logger.error(f"Unexpected error on attempt {attempt + 1}: {e}")
            break

    logger.error(f"Failed to download file after {max_retries} attempts")
    return False


def simple_progress_callback(downloaded: int, total: int):
    """简单的进度显示回调函数"""
    if total > 0:
        percent = min((downloaded / total) * 100, 100.0)
        print(f"Download progress: {percent:.1f}% ({downloaded}/{total} bytes)", end='\r')
        if downloaded >= total:
            print()


def _ensure_cache_dir(cache_dir: Path):
    """确保缓存目录存在且有效"""
    if cache_dir.exists() and not cache_dir.is_dir():
        cache_dir.unlink(missing_ok=True)
    cache_dir.mkdir(parents=True, exist_ok=True)


def _generate_cache_filename(url: str) -> str:
    """生成缓存文件名"""
    url_hash = hashlib.md5(url.encode()).hexdigest()
    original_name = Path(url).name
    return f"{url_hash}_{original_name}"


def download_dependencies(
        url: str,
        sha256: Optional[str] = None
) -> Path | None:
    """
    下载依赖文件，支持缓存机制和完整性验证

    Args:
        url: 要下载的文件URL
        sha256: 预期的SHA256哈希值（可选，用于验证文件完整性）

    Returns:
        Path: 下载文件的路径，如果下载失败则返回None
    """
    cache_dir = Path(".cache")
    _ensure_cache_dir(cache_dir)

    cache_manager = _CacheManager(cache_dir)

    # 生成缓存文件路径
    filename = _generate_cache_filename(url)
    filepath = cache_dir / filename

    # 检查文件是否已在缓存中且有效
    if filepath.exists():
        if cache_manager.is_file_valid(filepath, sha256):
            logger.info(f"File already exists in cache and is valid: {filepath}")
            # 确保缓存表中有记录
            if not cache_manager.get_cache_info(filepath):
                cache_manager.update_cache_info(filepath, url, sha256)
            return filepath
        else:
            logger.warning("Cached file is invalid, re-downloading")
            filepath.unlink(missing_ok=True)
            cache_manager.remove_cache_entry(filepath)

    # 下载文件
    success = download_file(
        url=url,
        filepath=filepath,
        expected_sha256=sha256,
        progress_callback=simple_progress_callback
    )

    if success:
        # 更新缓存表
        cache_manager.update_cache_info(filepath, url, sha256)
        return filepath
    else:
        return None


def cleanup_cache(max_age_days: int = 30, max_size_mb: int = 1024):
    """
    清理过期的缓存文件

    Args:
        max_age_days: 最大保留天数
        max_size_mb: 最大缓存大小（MB）
    """
    cache_dir = Path(".cache")
    if not cache_dir.exists() or not cache_dir.is_dir():
        return

    cache_manager = _CacheManager(cache_dir)
    cache_table = cache_manager.cache_table

    current_time = time.time()
    max_age_seconds = max_age_days * 24 * 60 * 60
    max_size_bytes = max_size_mb * 1024 * 1024

    # 第一步：清理过期文件和不存在的缓存条目
    total_size = 0
    valid_files = []

    for filepath_str, file_info in list(cache_table.items()):
        filepath = Path(filepath_str)

        if not filepath.exists():
            # 文件不存在，从缓存表中移除
            cache_manager.remove_cache_entry(filepath)
            continue

        file_age = current_time - file_info.get('download_time', 0)
        file_size = filepath.stat().st_size

        if file_age > max_age_seconds:
            # 文件过期，删除
            try:
                filepath.unlink()
                cache_manager.remove_cache_entry(filepath)
                logger.info(f"Removed expired cache file: {filepath}")
            except Exception as e:
                logger.warning(f"Failed to remove expired file {filepath}: {e}")
        else:
            total_size += file_size
            valid_files.append((filepath_str, file_info, file_size))

    # 第二步：如果缓存大小超过限制，按LRU策略删除最旧的文件
    if total_size > max_size_bytes:
        # 按下载时间排序（最旧的优先）
        valid_files.sort(key=lambda x: x[1].get('download_time', 0))

        while total_size > max_size_bytes and valid_files:
            filepath_str, file_info, file_size = valid_files.pop(0)
            filepath = Path(filepath_str)

            try:
                filepath.unlink()
                cache_manager.remove_cache_entry(filepath)
                total_size -= file_size
                logger.info(f"Removed cache file due to size limit: {filepath}")
            except Exception as e:
                logger.warning(f"Failed to remove file {filepath}: {e}")

    logger.info(f"Cache cleanup completed. Current size: {total_size / (1024 * 1024):.2f} MB")