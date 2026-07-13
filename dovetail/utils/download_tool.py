# coding=utf-8
import hashlib
import json
import os
import time
from pathlib import Path
from typing import Optional, Callable

from dovetail.utils.logger import get_logger

# 设置日志
logger = get_logger(__name__)

# GitHub 镜像站列表，按优先级排序
GITHUB_MIRRORS = [
    "",  # 原始地址优先
    "https://gh-proxy.org/",
    "https://ghproxy.net/",
    "https://gh.llkk.cc/",
    "https://gh.ddlc.top/",
]


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
        return self._cache_table  # NOQA

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

def _get_system_proxies() -> dict:
    """
    自动读取系统代理环境变量
    支持 HTTP_PROXY / HTTPS_PROXY / ALL_PROXY
    """
    proxies = {}
    for key in ("HTTP_PROXY", "http_proxy"):
        val = os.environ.get(key)
        if val:
            proxies["http"] = val
            break
    for key in ("HTTPS_PROXY", "https_proxy"):
        val = os.environ.get(key)
        if val:
            proxies["https"] = val
            break
    for key in ("ALL_PROXY", "all_proxy"):
        val = os.environ.get(key)
        if val:
            proxies.setdefault("http", val)
            proxies.setdefault("https", val)
            break
    return proxies


def _is_github_url(url: str) -> bool:
    return "github.com" in url or "githubusercontent.com" in url


def _build_mirror_urls(url: str) -> list[str]:
    """为 GitHub URL 生成带镜像前缀的候选列表"""
    if not _is_github_url(url):
        return [url]

    use_cn_mirror = os.environ.get("USED_MIRROR_GITHUB_CN", "").strip() == "1"

    if use_cn_mirror:
        logger.info("USED_MIRROR_GITHUB_CN=1 detected, using CN mirror directly.")
        return [GITHUB_MIRRORS[1] + url]  # 直接返回，不做回退

    return [
        (mirror + url if mirror else url)
        for mirror in GITHUB_MIRRORS
    ]


def _get_file_size_from_head(url: str, headers: dict, timeout: tuple, proxies: dict, verify_ssl: bool) -> int:
    import requests
    try:
        r = requests.head(url, headers=headers, timeout=timeout, proxies=proxies, verify=verify_ssl)
        r.raise_for_status()
        return int(r.headers.get("content-length", 0))
    except Exception:
        return 0


def _should_retry_on_error(status_code: Optional[int]) -> bool:
    if status_code is None:
        return True
    return status_code not in [400, 401, 403, 404, 410]


def verify_file_hash(filepath: Path, expected_hash: str) -> bool:
    sha256 = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            for block in iter(lambda: f.read(65536), b""):
                sha256.update(block)
        return sha256.hexdigest() == expected_hash.lower()
    except Exception as e:
        logger.error(f"Hash verification failed: {e}")
        return False


def download_file(
        url: str,
        filepath: Path,
        timeout: tuple[float, float] = (10.0, 60.0),  # (connect_timeout, read_timeout)
        max_retries: int = 3,
        retry_delay: float = 2.0,
        chunk_size: int = 65536,
        expected_sha256: Optional[str] = None,
        headers: Optional[dict] = None,
        verify_ssl: bool = True,
        progress_callback: Optional[Callable[[int, int], None]] = None,
        proxies: Optional[dict] = None,
        user_agent: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        enable_resume: bool = True,
        try_mirrors: bool = True,
) -> bool:
    """
    健壮的文件下载函数。

    新增特性：
    - 自动读取系统代理（兼容 Stream++/Clash）
    - 分离连接超时与读取超时
    - 断点续传（Range 请求）
    - GitHub 镜像自动回退
    - 真指数退避重试
    """
    import requests
    from requests.exceptions import RequestException, Timeout, HTTPError, ConnectionError

    filepath.parent.mkdir(parents=True, exist_ok=True)

    # 代理：优先使用调用方传入的，否则读取系统环境变量
    effective_proxies = proxies if proxies is not None else _get_system_proxies()
    if effective_proxies:
        logger.info(f"Using proxy: {effective_proxies}")

    default_headers = {
        "User-Agent": user_agent,
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
    }
    if headers:
        default_headers.update(headers)

    # 构建候选 URL 列表（支持镜像回退）
    candidate_urls = _build_mirror_urls(url) if try_mirrors else [url]

    for url_candidate in candidate_urls:
        should_try_next_mirror = False
        logger.info(f"Trying URL: {url_candidate or url}")

        for attempt in range(max_retries):
            if attempt > 0:
                delay = retry_delay * (2 ** (attempt - 1))  # 真指数退避
                logger.info(f"Retry {attempt + 1}/{max_retries}, waiting {delay:.1f}s...")
                time.sleep(delay)

            try:
                # 断点续传：检查已下载的字节数
                resume_pos = 0
                req_headers = dict(default_headers)
                if enable_resume and filepath.exists():
                    resume_pos = filepath.stat().st_size
                    if resume_pos > 0:
                        req_headers["Range"] = f"bytes={resume_pos}-"
                        logger.info(f"Resuming from byte {resume_pos}")

                # 获取文件总大小
                total_size = _get_file_size_from_head(
                    url_candidate, req_headers, timeout, effective_proxies, verify_ssl
                )

                response = requests.get(
                    url_candidate,
                    stream=True,
                    headers=req_headers,
                    timeout=timeout,
                    verify=verify_ssl,
                    proxies=effective_proxies,
                )
                response.raise_for_status()

                if total_size == 0:
                    total_size = int(response.headers.get("content-length", 0))

                # 支持 206 Partial Content（断点续传成功）
                write_mode = "ab" if response.status_code == 206 else "wb"
                if write_mode == "wb":
                    resume_pos = 0  # 服务器不支持 Range，从头写

                downloaded = resume_pos
                with open(filepath, write_mode) as f:
                    for chunk in response.iter_content(chunk_size=chunk_size):
                        if chunk:
                            f.write(chunk)
                            downloaded += len(chunk)
                            if progress_callback and total_size > 0:
                                progress_callback(downloaded, max(total_size + resume_pos, downloaded))

                logger.info(f"Downloaded successfully -> {filepath}")

                if expected_sha256:
                    if not verify_file_hash(filepath, expected_sha256):
                        raise ValueError("SHA256 mismatch! File corrupted or tampered.")

                return True

            except Timeout:
                logger.warning(f"Timeout on attempt {attempt + 1} ({url_candidate})")
            except ConnectionError as e:
                logger.warning(f"Connection error on attempt {attempt + 1}: {e}")
                # SSL / 连接失败：重试无意义，直接换镜像
                should_try_next_mirror = True
                break  # ← 跳出重试循环
            except HTTPError as e:
                code = e.response.status_code
                logger.warning(f"HTTP {code} on attempt {attempt + 1}")
                if not _should_retry_on_error(code):
                    break  # 跳过当前 URL 的剩余重试
            except ValueError as e:
                logger.error(str(e))
                raise
            except RequestException as e:
                logger.warning(f"Request failed on attempt {attempt + 1}: {e}")
            except Exception as e:
                logger.error(f"Unexpected error: {e}")
                break

        if should_try_next_mirror:
            logger.info(f"Switching to next mirror due to connection error...")
            continue  # ← 外层循环换下一个镜像

        logger.warning(f"All retries failed for {url_candidate}, trying next mirror...")
        break

    logger.error(f"All URLs exhausted. Download failed: {url}")
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
            logger.info(f"文件已经存在于缓存中且有效: {filepath}")
            # 确保缓存表中有记录
            if not cache_manager.get_cache_info(filepath):
                cache_manager.update_cache_info(filepath, url, sha256)
            return filepath
        else:
            logger.warning("缓存文件无效，重新下载")
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
