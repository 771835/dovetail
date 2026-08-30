# coding=utf-8
"""
依赖解析与下载

从 [dependencies] 声明 → git clone/fetch → 本地缓存 → 传给编译器
支持三种 git 引用: tag（不可变）、branch（可变）、rev（不可变）
可变引用依赖 dovetail.lock 锁定精确 commit 以保证可复现性。
"""
from __future__ import annotations

import subprocess
from dataclasses import dataclass, field
from pathlib import Path

from dovetail.build.lockfile import load_lock
from dovetail.utils.logger import get_logger

logger = get_logger(__name__)


# ── 异常 ──────────────────────────────────────────────────────

class DependencyFormatError(ValueError):
    """依赖声明格式错误（dovetail.toml 中 [dependencies] 写法有误 / 引用不存在）"""
    pass


class DependencyGitNotFoundError(RuntimeError):
    """git 命令不可用"""
    pass


class DependencyNetworkError(RuntimeError):
    """网络错误（无法连接远程仓库）"""
    pass


class DependencyRepoError(RuntimeError):
    """仓库错误（不存在、无权限等）"""
    pass


class DependencyResolveError(RuntimeError):
    """依赖解析失败（兜底）"""
    pass


# ── 数据结构 ─────────────────────────────────────────────────

@dataclass
class DependencySpec:
    """依赖声明（来自 dovetail.toml [dependencies]）"""

    name: str
    git: str
    tag: str | None = None
    branch: str | None = None
    rev: str | None = None

    @property
    def ref(self) -> str:
        """当前指定的 git 引用"""
        if self.rev:
            return self.rev
        if self.tag:
            return self.tag
        if self.branch:
            return self.branch
        raise ValueError(f"依赖 {self.name} 未指定 tag/branch/rev")

    @property
    def is_mutable(self) -> bool:
        """是否为可变引用（branch 可变，tag 和 rev 不可变）"""
        return self.branch is not None

    @property
    def ref_type(self) -> str:
        """引用类型，用于日志"""
        if self.rev:
            return "rev"
        if self.tag:
            return "tag"
        if self.branch:
            return "branch"
        return "unknown"


@dataclass
class ResolvedDependency:
    """已解析的依赖（带精确 commit hash）"""

    name: str
    git: str
    tag: str | None = None
    branch: str | None = None
    rev: str | None = None
    resolved: str = ""  # 精确 commit hash
    local_path: Path = field(default_factory=Path)

    def to_lock_entry(self) -> dict:
        """序列化为 lock 文件条目"""
        entry = {
            "name": self.name,
            "git": self.git,
            "resolved": self.resolved,
        }
        if self.tag:
            entry["tag"] = self.tag
        if self.branch:
            entry["branch"] = self.branch
        if self.rev:
            entry["rev"] = self.rev
        return entry


# ── git stderr 分类 ──────────────────────────────────────────

_NETWORK_PATTERNS = (
    "could not resolve host",
    "connection timed out",
    "operation timed out",
    "network is unreachable",
    "failed to connect",
    "ssl connection error",
)

_REPO_PATTERNS = (
    "repository not found",
    "could not read from remote repository",
    "remote: not found",
    "access denied",
    "authentication failed",
)


def _classify_git_error(stderr: str) -> type:
    """根据 git stderr 内容分类错误"""
    lower = stderr.lower()
    for pattern in _NETWORK_PATTERNS:
        if pattern in lower:
            return DependencyNetworkError
    for pattern in _REPO_PATTERNS:
        if pattern in lower:
            return DependencyRepoError
    return DependencyResolveError


# ── git 子命令调用 ───────────────────────────────────────────

def _git(*args: str, cwd: Path | None = None, check: bool = True) -> str:
    """调用 git 子命令"""
    result = subprocess.run(
        ["git", *args],
        cwd=cwd,
        capture_output=True,
        text=True,
    )
    if check and result.returncode != 0:
        stderr = result.stderr.strip()
        error_cls = _classify_git_error(stderr)

        if error_cls is DependencyNetworkError:
            raise DependencyNetworkError(
                f"网络错误: git {' '.join(args)}\n"
                f"  {stderr}\n"
                f"  提示: 如果在国内访问 GitHub，可设置代理:\n"
                f"    git config --global http.proxy http://127.0.0.1:7890\n"
                f"  或设置环境变量:\n"
                f"    set HTTPS_PROXY=http://127.0.0.1:7890"
            )
        elif error_cls is DependencyRepoError:
            raise DependencyRepoError(
                f"仓库错误: git {' '.join(args)}\n"
                f"  {stderr}\n"
                f"  提示: 检查仓库地址拼写，以及是否有访问权限（私有仓库需要 SSH key）"
            )
        else:
            raise DependencyResolveError(
                f"git {' '.join(args)} 失败: {stderr}"
            )
    return result.stdout.strip()


# ── 解析 ─────────────────────────────────────────────────────

def parse_dependencies(deps_data: dict) -> list[DependencySpec]:
    """
    解析 dovetail.toml [dependencies] 段

    Args:
        deps_data: [dependencies] 下的原始字典

    Returns:
        依赖声明列表

    Raises:
        DependencyFormatError: 声明格式错误
    """
    specs = []
    for name, info in deps_data.items():
        if not isinstance(info, dict) or "git" not in info:
            raise DependencyFormatError(
                f"依赖 {name!r} 格式无效，需要指定 git 地址，例如:\n"
                f'  {name} = {{ git = "https://...", tag = "v1.0" }}'
            )

        tag = info.get("tag")
        branch = info.get("branch")
        rev = info.get("rev")

        ref_count = sum(x is not None for x in (tag, branch, rev))
        if ref_count == 0:
            raise DependencyFormatError(
                f"依赖 {name!r} 必须指定 tag、branch 或 rev 其一"
            )
        if ref_count > 1:
            raise DependencyFormatError(
                f"依赖 {name!r} 只能指定 tag、branch 或 rev 其一，不能同时指定多个"
            )

        specs.append(DependencySpec(
            name=name,
            git=info["git"],
            tag=tag,
            branch=branch,
            rev=rev,
        ))
    return specs


def resolve_dependency(
        spec: DependencySpec,
        deps_dir: Path,
        locked_commit: str | None = None,
) -> ResolvedDependency:
    """
    解析单个依赖

    Args:
        spec: 依赖声明
        deps_dir: 依赖缓存目录（.deps/）
        locked_commit: lock 文件中记录的精确 commit（可选）

    Returns:
        已解析的依赖

    Raises:
        DependencyNetworkError: 网络错误
        DependencyRepoError: 仓库错误
        DependencyFormatError: 引用不存在（配置错误）
        DependencyResolveError: 其他解析错误
    """
    target = deps_dir / spec.name

    # ── 不可变引用 + lock 命中 → 跳过网络请求 ────────────
    if locked_commit and not spec.is_mutable:
        if target.exists() and (target / ".git").exists():
            current = _git("rev-parse", "HEAD", cwd=target)
            if current == locked_commit:
                logger.info(f"依赖 {spec.name}: 已缓存 ({locked_commit[:12]})")
                return ResolvedDependency(
                    name=spec.name,
                    git=spec.git,
                    tag=spec.tag,
                    branch=spec.branch,
                    rev=spec.rev,
                    resolved=locked_commit,
                    local_path=target,
                )

    # ── 需要网络请求 ──────────────────────────────────────
    if target.exists() and (target / ".git").exists():
        logger.info(f"更新依赖: {spec.name} ({spec.ref_type}={spec.ref})")
        _git("fetch", "--tags", cwd=target)
    else:
        logger.info(f"下载依赖: {spec.name} ({spec.ref_type}={spec.ref})")
        target.parent.mkdir(parents=True, exist_ok=True)
        _git("clone", spec.git, str(target))

    # checkout 到目标引用
    try:
        if spec.rev:
            _git("checkout", spec.rev, cwd=target)
        elif spec.tag:
            _git("checkout", f"tags/{spec.tag}", cwd=target)
        elif spec.branch:
            _git("checkout", spec.branch, cwd=target)
    except DependencyResolveError as e:
        # checkout 失败多半是引用不存在 → 升为配置错误
        raise DependencyFormatError(
            f"依赖 {spec.name} 的 {spec.ref_type}={spec.ref!r} 不存在于仓库中\n"
            f"  提示: 检查 {spec.ref_type} 拼写，或确认该 {spec.ref_type} 已推送到远程"
        ) from e

    resolved = _git("rev-parse", "HEAD", cwd=target)

    # 可变引用校验：lock 存在但 commit 变了 → 警告
    if spec.is_mutable and locked_commit and resolved != locked_commit:
        logger.warning(
            f"依赖 {spec.name} 的 {spec.branch} 分支已变化: "
            f"{locked_commit[:12]} → {resolved[:12]}，dovetail.lock 将更新"
        )

    return ResolvedDependency(
        name=spec.name,
        git=spec.git,
        tag=spec.tag,
        branch=spec.branch,
        rev=spec.rev,
        resolved=resolved,
        local_path=target,
    )


def resolve_all(
        specs: list[DependencySpec],
        project_root: Path,
        deps_dir_name: str = "lib",
) -> list[ResolvedDependency]:
    """
    解析全部依赖，结合 lock 文件加速

    Args:
        specs: 依赖声明列表
        project_root: 项目根目录
        deps_dir_name: 第三方库存放目录

    Returns:
        已解析依赖列表

    Raises:
        DependencyGitNotFoundError: git 不可用
        DependencyNetworkError: 网络错误
        DependencyRepoError: 仓库错误
        DependencyFormatError: 引用不存在
        DependencyResolveError: 其他解析错误
    """
    if not specs:
        return []

    deps_dir = project_root / deps_dir_name

    # 检查 git 是否可用
    try:
        _git("--version")
    except FileNotFoundError:
        raise DependencyGitNotFoundError(
            "依赖解析需要 git，但未检测到 git 命令\n"
            "  提示: 请安装 git: https://git-scm.com/downloads"
        )
    except RuntimeError as e:
        raise DependencyGitNotFoundError(f"git 检查失败: {e}")

    # 读取 lock 文件
    lock = load_lock(project_root)

    resolved = []
    for spec in specs:
        try:
            r = resolve_dependency(spec, deps_dir, locked_commit=lock.get(spec.name))
            resolved.append(r)
            logger.debug(f"依赖 {spec.name}: {r.resolved[:12]}")
        except (
                DependencyNetworkError,
                DependencyRepoError,
                DependencyFormatError,
        ):
            raise  # 直接上抛，已有清晰错误信息
        except Exception as e:
            raise DependencyResolveError(
                f"依赖 {spec.name} 解析失败: {e}"
            ) from e

    return resolved
