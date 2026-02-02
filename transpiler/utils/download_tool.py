# coding=utf-8
import hashlib
import time
from pathlib import Path
from typing import Optional, Callable

from transpiler.utils.logging_plus import get_logger

# 设置日志
logger = get_logger(__name__)


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
                logger.info(f"Retry attempt {attempt + 1}/{max_retries}")
                time.sleep(retry_delay * attempt)  # 指数退避

            # 发起HEAD请求获取文件信息（避免重复下载大文件）
            total_size = 0
            if progress_callback and attempt == 0:
                try:
                    head_response = requests.head(
                        url,
                        headers=default_headers,
                        timeout=timeout / 2,
                        verify=verify_ssl
                    )
                    head_response.raise_for_status()
                    total_size = int(head_response.headers.get('content-length', 0))
                except Exception:
                    pass  # 无法获取文件大小则跳过

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

            # 获取文件大小（如果HEAD请求失败）
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
                            progress_callback(downloaded, total_size)

            logger.info(f"File downloaded successfully to {filepath}")

            # 验证文件完整性
            if expected_sha256:
                if not verify_file_hash(filepath, expected_sha256):
                    raise ValueError("SHA256 hash verification failed! File may be corrupted or tampered with.")

            return True

        except Timeout:
            logger.warning(f"Timeout occurred on attempt {attempt + 1}")
        except ConnectionError:
            logger.warning(f"Connection error on attempt {attempt + 1}")
        except HTTPError as e:
            logger.warning(f"HTTP error {e.response.status_code} on attempt {attempt + 1}")
            if e.response.status_code in [404, 403, 401]:
                break  # 这些错误重试无意义
        except RequestException as e:
            logger.warning(f"Request failed on attempt {attempt + 1}: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error on attempt {attempt + 1}: {str(e)}")
            break

    logger.error(f"Failed to download file after {max_retries} attempts")
    return False


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
        logger.error(f"Hash verification failed: {str(e)}")
        return False


def simple_progress_callback(downloaded: int, total: int):
    """简单的进度显示回调函数"""
    if total > 0:
        percent = (downloaded / total) * 100
        print(f"Download progress: {percent:.1f}% ({downloaded}/{total} bytes)", end='\r')
        if downloaded == total:
            print()  # 换行


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
    if cache_dir.exists() and not cache_dir.is_dir():
        cache_dir.unlink(missing_ok=True)
    cache_dir.mkdir(parents=True, exist_ok=True)

    # 创建或读取缓存表文件
    cache_table_file = cache_dir / "download_cache.json"
    cache_table = {}

    # 如果缓存表文件存在，则读取现有缓存信息
    if cache_table_file.exists():
        try:
            import json
            with open(cache_table_file, encoding='utf-8') as f:
                cache_table = json.load(f)
        except Exception as e:
            logger.warning(f"Failed to read cache table: {str(e)}")
            cache_table = {}

    # 生成文件名（使用URL的哈希值作为文件名）
    url_hash = hashlib.md5(url.encode()).hexdigest()
    filename = f"{url_hash}_{Path(url).name}"
    filepath = cache_dir / filename

    # 检查文件是否已经在缓存中且完整
    if filepath.exists():
        cache_key = str(filepath)

        # 检查缓存表中是否有记录
        if cache_key in cache_table:
            cached_info = cache_table[cache_key]

            # 验证文件是否完整（如果提供了SHA256）
            if sha256:
                if verify_file_hash(filepath, sha256):
                    logger.info(f"File already exists in cache and is valid: {filepath}")
                    return filepath
                else:
                    logger.warning("Cached file hash mismatch, re-downloading")
                    filepath.unlink(missing_ok=True)  # 删除损坏的文件
            else:
                # 如果没有提供SHA256，检查文件大小是否与缓存记录一致
                actual_size = filepath.stat().st_size
                if actual_size == cached_info.get('size', 0):
                    logger.info(f"File already exists in cache: {filepath}")
                    return filepath
                else:
                    logger.warning("Cached file size mismatch, re-downloading")
                    filepath.unlink(missing_ok=True)
        else:
            # 文件存在但不在缓存表中，需要验证完整性
            if sha256:
                if verify_file_hash(filepath, sha256):
                    # 添加到缓存表
                    cache_table[str(filepath)] = {
                        'url': url,
                        'size': filepath.stat().st_size,
                        'sha256': sha256,
                        'download_time': time.time()
                    }
                    # 保存缓存表
                    try:
                        import json
                        with open(cache_table_file, 'w', encoding='utf-8') as f:
                            json.dump(cache_table, f, indent=2, ensure_ascii=False)
                    except Exception as e:
                        logger.warning(f"Failed to update cache table: {str(e)}")

                    logger.info(f"File already exists and is valid: {filepath}")
                    return filepath
                else:
                    logger.warning("Existing file hash mismatch, re-downloading")
                    filepath.unlink(missing_ok=True)
            else:
                # 没有SHA256验证，直接使用现有文件
                logger.info(f"Using existing file: {filepath}")
                return filepath

    # 下载文件
    success = download_file(
        url=url,
        filepath=filepath,
        expected_sha256=sha256,
        progress_callback=simple_progress_callback
    )

    if success:
        # 更新缓存表
        cache_table[str(filepath)] = {
            'url': url,
            'size': filepath.stat().st_size,
            'sha256': sha256,
            'download_time': time.time()
        }

        # 保存缓存表
        try:
            import json
            with open(cache_table_file, 'w', encoding='utf-8') as f:
                json.dump(cache_table, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.warning(f"Failed to update cache table: {str(e)}")

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

    cache_table_file = cache_dir / "download_cache.json"
    cache_table = {}

    # 读取缓存表
    if cache_table_file.exists():
        try:
            import json
            with open(cache_table_file, 'r', encoding='utf-8') as f:
                cache_table = json.load(f)
        except Exception as e:
            logger.warning(f"Failed to read cache table: {str(e)}")
            return

    current_time = time.time()
    max_age_seconds = max_age_days * 24 * 60 * 60
    max_size_bytes = max_size_mb * 1024 * 1024

    # 计算当前缓存总大小
    total_size = 0
    files_to_keep = []

    # 检查每个缓存文件
    for filepath_str, file_info in list(cache_table.items()):
        filepath = Path(filepath_str)

        if not filepath.exists():
            # 文件不存在，从缓存表中移除
            del cache_table[filepath_str]
            continue

        file_age = current_time - file_info.get('download_time', 0)
        file_size = filepath.stat().st_size

        if file_age > max_age_seconds:
            # 文件过期，删除
            try:
                filepath.unlink()
                del cache_table[filepath_str]
                logger.info(f"Removed expired cache file: {filepath}")
            except Exception as e:
                logger.warning(f"Failed to remove expired file {filepath}: {str(e)}")
        else:
            total_size += file_size
            files_to_keep.append((filepath_str, file_info, file_size))

    # 如果缓存大小超过限制，按LRU策略删除最旧的文件
    if total_size > max_size_bytes:
        # 按下载时间排序（最旧的文件优先删除）
        files_to_keep.sort(key=lambda x: x[1].get('download_time', 0))

        while total_size > max_size_bytes and files_to_keep:
            filepath_str, file_info, file_size = files_to_keep.pop(0)
            filepath = Path(filepath_str)

            try:
                filepath.unlink()
                del cache_table[filepath_str]
                total_size -= file_size
                logger.info(f"Removed cache file due to size limit: {filepath}")
            except Exception as e:
                logger.warning(f"Failed to remove file {filepath}: {str(e)}")

    # 保存更新后的缓存表
    try:
        import json
        with open(cache_table_file, 'w', encoding='utf-8') as f:
            json.dump(cache_table, f, indent=2, ensure_ascii=False)
    except Exception as e:
        logger.warning(f"Failed to update cache table: {str(e)}")
