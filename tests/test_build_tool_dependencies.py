# coding=utf-8
"""
依赖解析测试
"""
from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path


# ── 辅助函数 ──────────────────────────────────────────────────

def _git(*args, cwd=None):
    """调用 git"""
    result = subprocess.run(
        ["git", *args],
        cwd=cwd,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed: {result.stderr}")
    return result.stdout.strip()


def _make_git_repo(path, files=None, tag=None, branch=None):
    """
    创建一个 git 仓库

    Args:
        path: 仓库路径
        files: {文件名: 内容}
        tag: 打的标签
        branch: 额外创建的分支名（在默认分支基础上）
    """
    path.mkdir(parents=True, exist_ok=True)
    _git("init", cwd=path)

    if files:
        for name, content in files.items():
            f = path / name
            f.parent.mkdir(parents=True, exist_ok=True)
            f.write_text(content, encoding="utf-8")

    _git("add", ".", cwd=path)
    _git("commit", "-m", "init", cwd=path)

    if tag:
        _git("tag", tag, cwd=path)

    if branch:
        _git("checkout", "-b", branch, cwd=path)


# 工具函数
def _git_path(path: Path) -> str:
    """转为 git 可接受的正斜杠路径（修复 Windows 反斜杠在 TOML 中被当转义符的问题）"""
    return path.as_posix()


# ── 导入被测模块 ──────────────────────────────────────────────

_project_root = Path(__file__).resolve().parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

from dovetail.build.dependencies import (
    DependencyFormatError,
    DependencyNetworkError,
    DependencyRepoError,
    DependencyResolveError,
    DependencySpec,
    ResolvedDependency,
    parse_dependencies,
    resolve_all,
    resolve_dependency,
    _read_dep_dependencies,
    _resolve_include_paths,
)
from dovetail.build.lockfile import load_lock, write_lock, LOCK_FILENAME


# ── 测试类 ────────────────────────────────────────────────────

class TestParseDependenciesBasic(unittest.TestCase):
    """parse_dependencies 基本解析"""

    def test_tag(self):
        specs = parse_dependencies({
            "my-lib": {"git": "https://example.com/lib.git", "tag": "v1.0"}
        })
        self.assertEqual(len(specs), 1)
        self.assertEqual(specs[0].name, "my-lib")
        self.assertEqual(specs[0].git, "https://example.com/lib.git")
        self.assertEqual(specs[0].tag, "v1.0")
        self.assertEqual(specs[0].ref, "v1.0")
        self.assertFalse(specs[0].is_mutable)
        self.assertEqual(specs[0].ref_type, "tag")

    def test_branch(self):
        specs = parse_dependencies({
            "my-lib": {"git": "https://example.com/lib.git", "branch": "main"}
        })
        self.assertEqual(specs[0].branch, "main")
        self.assertTrue(specs[0].is_mutable)
        self.assertEqual(specs[0].ref_type, "branch")

    def test_rev(self):
        specs = parse_dependencies({
            "my-lib": {"git": "https://example.com/lib.git", "rev": "a1b2c3d"}
        })
        self.assertEqual(specs[0].rev, "a1b2c3d")
        self.assertFalse(specs[0].is_mutable)
        self.assertEqual(specs[0].ref_type, "rev")

    def test_multiple(self):
        specs = parse_dependencies({
            "lib-a": {"git": "https://a.git", "tag": "v1"},
            "lib-b": {"git": "https://b.git", "branch": "dev"},
        })
        self.assertEqual(len(specs), 2)


class TestParseDependenciesErrors(unittest.TestCase):
    """parse_dependencies 格式错误"""

    def test_missing_git(self):
        with self.assertRaises(DependencyFormatError):
            parse_dependencies({"bad": {"tag": "v1"}})

    def test_missing_ref(self):
        with self.assertRaises(DependencyFormatError):
            parse_dependencies({"bad": {"git": "https://example.com/repo.git"}})

    def test_multiple_refs(self):
        with self.assertRaises(DependencyFormatError):
            parse_dependencies({
                "bad": {"git": "https://example.com/repo.git", "tag": "v1", "branch": "main"}
            })

    def test_not_dict(self):
        with self.assertRaises(DependencyFormatError):
            parse_dependencies({"bad": "just-a-string"})


class TestResolveTag(unittest.TestCase):
    """resolve_dependency — tag 引用"""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.repo = self.tmp / "repos" / "my-lib"
        self.project = self.tmp / "project"
        self.project.mkdir()
        self.deps_dir = self.project / "lib"

        _make_git_repo(
            self.repo,
            {"hello.mcdl": 'fn hello() { print("hi") }'},
            tag="v1.0.0",
        )

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_first_clone(self):
        spec = DependencySpec(name="my-lib", git=str(self.repo), tag="v1.0.0")
        r = resolve_dependency(spec, self.deps_dir)

        self.assertTrue(r.local_path.exists())
        self.assertTrue((r.local_path / "hello.mcdl").exists())
        self.assertGreater(len(r.resolved), 0)
        self.assertFalse(r.is_mutable)
        self.assertTrue(len(r.include_paths) > 0)

    def test_lock_hit_skip_network(self):
        """lock 命中 + 不可变引用 → 跳过网络请求"""
        spec = DependencySpec(name="my-lib", git=str(self.repo), tag="v1.0.0")
        r1 = resolve_dependency(spec, self.deps_dir)

        # 用 r1 的 resolved 作为 locked_commit 再次解析
        r2 = resolve_dependency(spec, self.deps_dir, locked_commit=r1.resolved)
        self.assertTrue(r2.local_path.exists())
        self.assertEqual(r1.resolved, r2.resolved)


class TestResolveBranch(unittest.TestCase):
    """resolve_dependency — branch 引用"""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.repo = self.tmp / "repos" / "my-lib"
        self.project = self.tmp / "project"
        self.project.mkdir()
        self.deps_dir = self.project / "lib"

        _make_git_repo(
            self.repo,
            {"hello.mcdl": 'fn hello() { print("hi") }'},
            branch="dev",
        )

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_clone_checkout_branch(self):
        spec = DependencySpec(name="my-lib", git=str(self.repo), branch="dev")
        r = resolve_dependency(spec, self.deps_dir)

        self.assertTrue(r.local_path.exists())
        self.assertTrue(r.is_mutable)
        self.assertEqual(r.ref_type, "branch")

    def test_branch_changed_warning(self):
        """branch 前进 + lock 存在 → 应产生警告，resolved 更新"""
        spec = DependencySpec(name="my-lib", git=str(self.repo), branch="dev")
        r1 = resolve_dependency(spec, self.deps_dir)

        # 在 dev 分支推新 commit
        _git("checkout", "dev", cwd=self.repo)
        (self.repo / "new_file.mcdl").write_text("fn new() {}", encoding="utf-8")
        _git("add", ".", cwd=self.repo)
        _git("commit", "-m", "update", cwd=self.repo)
        new_commit = _git("rev-parse", "HEAD", cwd=self.repo)

        # 用旧 commit 作为 lock，应检测到变化
        r2 = resolve_dependency(spec, self.deps_dir, locked_commit=r1.resolved)
        self.assertEqual(r2.resolved, new_commit)


class TestResolveRev(unittest.TestCase):
    """resolve_dependency — rev 引用"""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.repo = self.tmp / "repos" / "my-lib"
        self.project = self.tmp / "project"
        self.project.mkdir()
        self.deps_dir = self.project / "lib"

        _make_git_repo(self.repo, {"hello.mcdl": 'fn hello() { print("hi") }'})
        self.commit = _git("rev-parse", "HEAD", cwd=self.repo)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_clone_checkout_rev(self):
        spec = DependencySpec(name="my-lib", git=str(self.repo), rev=self.commit)
        r = resolve_dependency(spec, self.deps_dir)

        self.assertTrue(r.local_path.exists())
        self.assertEqual(r.resolved, self.commit)
        self.assertEqual(r.ref_type, "rev")
        self.assertFalse(r.is_mutable)


class TestResolveRefNotFound(unittest.TestCase):
    """resolve_dependency — 引用不存在"""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.repo = self.tmp / "repos" / "my-lib"
        self.project = self.tmp / "project"
        self.project.mkdir()
        self.deps_dir = self.project / "lib"

        _make_git_repo(self.repo, {"hello.mcdl": "content"}, tag="v1.0.0")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_tag_not_found(self):
        spec = DependencySpec(name="my-lib", git=str(self.repo), tag="v99.0.0")
        with self.assertRaises(DependencyFormatError):
            resolve_dependency(spec, self.deps_dir)

    def test_branch_not_found(self):
        spec = DependencySpec(name="my-lib", git=str(self.repo), branch="nonexistent")
        with self.assertRaises(DependencyFormatError):
            resolve_dependency(spec, self.deps_dir)


class TestResolveNetworkError(unittest.TestCase):
    """resolve_dependency — 网络错误"""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.project = self.tmp / "project"
        self.project.mkdir()
        self.deps_dir = self.project / "lib"

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_nonexistent_host(self):
        """不存在的域名 → 抛出网络/仓库/解析异常之一"""
        spec = DependencySpec(
            name="bad-lib",
            git="https://this-domain-does-not-exist-12345.example/repo.git",
            tag="v1.0",
        )
        with self.assertRaises((DependencyNetworkError, DependencyRepoError, DependencyResolveError)):
            resolve_dependency(spec, self.deps_dir)


class TestTransitiveDependencies(unittest.TestCase):
    """resolve_all — 传递依赖"""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        repos = self.tmp / "repos"
        self.project = self.tmp / "project"
        self.project.mkdir()

        # C: 无依赖的底层库
        repo_c = repos / "lib-c"
        _make_git_repo(repo_c, {
            "dovetail.toml": textwrap.dedent("""\
                [package]
                name = "lib-c"
                version = "1.0.0"
                [build]
                entry = "src/main.mcdl"
                [paths]
                sources = ["src"]
            """),
            "src/c.mcdl": "fn c_func() {}",
        }, tag="v1.0.0")

        # B: 依赖 C
        repo_b = repos / "lib-b"
        _make_git_repo(repo_b, {
            "dovetail.toml": textwrap.dedent(f"""\
                [package]
                name = "lib-b"
                version = "1.0.0"
                [build]
                entry = "src/main.mcdl"
                [paths]
                sources = ["src"]
                [dependencies]
                lib-c = {{ git = "{_git_path(repo_c)}", tag = "v1.0.0" }}
            """),
            "src/b.mcdl": "fn b_func() {}",
        }, tag="v1.0.0")

        # A: 依赖 B
        repo_a = repos / "lib-a"
        _make_git_repo(repo_a, {
            "dovetail.toml": textwrap.dedent(f"""\
                [package]
                name = "lib-a"
                version = "1.0.0"
                [build]
                entry = "src/main.mcdl"
                [paths]
                sources = ["src"]
                [dependencies]
                lib-b = {{ git = "{_git_path(repo_b)}", tag = "v1.0.0" }}
            """),
            "src/a.mcdl": "fn a_func() {}",
        }, tag="v1.0.0")

        self.repo_a = repo_a

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_transitive_a_b_c(self):
        """A → B → C 三层传递"""
        specs = parse_dependencies({
            "lib-a": {"git": str(self.repo_a), "tag": "v1.0.0"},
        })
        resolved = resolve_all(specs, self.project, deps_dir_name="lib")

        self.assertEqual(len(resolved), 3)
        names = {r.name for r in resolved}
        self.assertIn("lib-a", names)
        self.assertIn("lib-b", names)
        self.assertIn("lib-c", names)

    def test_transitive_files_exist(self):
        """传递依赖的文件确实存在"""
        specs = parse_dependencies({
            "lib-a": {"git": str(self.repo_a), "tag": "v1.0.0"},
        })
        resolve_all(specs, self.project, deps_dir_name="lib")

        lib_c_dir = self.project / "lib" / "lib-c"
        self.assertTrue(lib_c_dir.exists())
        self.assertTrue((lib_c_dir / "src" / "c.mcdl").exists())


class TestConflictDetection(unittest.TestCase):
    """resolve_all — 冲突检测"""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        repos = self.tmp / "repos"
        self.project = self.tmp / "project"
        self.project.mkdir()

        # 两个不同源的 lib-c
        repo_c_v1 = repos / "lib-c-v1"
        _make_git_repo(repo_c_v1, {"c.mcdl": "fn c_v1() {}"}, tag="v1.0.0")

        repo_c_v2 = repos / "lib-c-v2"
        _make_git_repo(repo_c_v2, {"c.mcdl": "fn c_v2() {}"}, tag="v2.0.0")

        # A 依赖 C v1（来自 repo_c_v1）
        repo_a = repos / "lib-a"
        _make_git_repo(repo_a, {
            "dovetail.toml": textwrap.dedent(f"""\
                [package]
                name = "lib-a"
                version = "1.0.0"
                [build]
                entry = "src/main.mcdl"
                [dependencies]
                lib-c = {{ git = "{_git_path(repo_c_v1)}", tag = "v1.0.0" }}
            """),
        }, tag="v1.0.0")

        # B 依赖 C v2（来自 repo_c_v2，不同 git 源）
        repo_b = repos / "lib-b"
        _make_git_repo(repo_b, {
            "dovetail.toml": textwrap.dedent(f"""\
                [package]
                name = "lib-b"
                version = "1.0.0"
                [build]
                entry = "src/main.mcdl"
                [dependencies]
                lib-c = {{ git = "{_git_path(repo_c_v2)}", tag = "v2.0.0" }}
            """),
        }, tag="v1.0.0")

        self.repo_a = repo_a
        self.repo_b = repo_b

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_conflict_different_source(self):
        """同名不同源 → 冲突"""
        specs = parse_dependencies({
            "lib-a": {"git": str(self.repo_a), "tag": "v1.0.0"},
            "lib-b": {"git": str(self.repo_b), "tag": "v1.0.0"},
        })
        with self.assertRaises(DependencyFormatError):
            resolve_all(specs, self.project, "lib")


class TestSameDepDedup(unittest.TestCase):
    """resolve_all — 同名同源去重"""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        repos = self.tmp / "repos"
        self.project = self.tmp / "project"
        self.project.mkdir()

        repo_c = repos / "lib-c"
        _make_git_repo(repo_c, {"c.mcdl": "fn c() {}"}, tag="v1.0.0")

        # A 和 B 都依赖同一个 C
        repo_a = repos / "lib-a"
        _make_git_repo(repo_a, {
            "dovetail.toml": textwrap.dedent(f"""\
                [package]
                name = "lib-a"
                version = "1.0.0"
                [build]
                entry = "src/main.mcdl"
                [dependencies]
                lib-c = {{ git = "{_git_path(repo_c)}", tag = "v1.0.0" }}
            """),
        }, tag="v1.0.0")

        repo_b = repos / "lib-b"
        _make_git_repo(repo_b, {
            "dovetail.toml": textwrap.dedent(f"""\
                [package]
                name = "lib-b"
                version = "1.0.0"
                [build]
                entry = "src/main.mcdl"
                [dependencies]
                lib-c = {{ git = "{_git_path(repo_c)}", tag = "v1.0.0" }}
            """),
        }, tag="v1.0.0")

        self.repo_a = repo_a
        self.repo_b = repo_b

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_dedup_same_source(self):
        """A→C + B→C (同版本) → C 只出现一次"""
        specs = parse_dependencies({
            "lib-a": {"git": str(self.repo_a), "tag": "v1.0.0"},
            "lib-b": {"git": str(self.repo_b), "tag": "v1.0.0"},
        })
        resolved = resolve_all(specs, self.project, "lib")

        self.assertEqual(len(resolved), 3)  # A, B, C
        c_count = sum(1 for r in resolved if r.name == "lib-c")
        self.assertEqual(c_count, 1)


class TestResolveIncludePaths(unittest.TestCase):
    """_resolve_include_paths — 源码路径"""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_with_toml_and_sources(self):
        """有 toml → 解析 paths.sources"""
        repo = self.tmp / "with-toml"
        repo.mkdir(parents=True)
        (repo / "dovetail.toml").write_text(textwrap.dedent("""\
            [package]
            name = "lib"
            version = "1.0.0"
            [build]
            entry = "src/main.mcdl"
            [paths]
            sources = ["src", "lib"]
        """), encoding="utf-8")
        (repo / "src").mkdir()
        (repo / "lib").mkdir()

        paths = _resolve_include_paths(repo)
        self.assertEqual(len(paths), 2)
        self.assertIn(repo / "src", paths)
        self.assertIn(repo / "lib", paths)

    def test_without_toml(self):
        """无 toml → 退回根目录"""
        repo = self.tmp / "no-toml"
        repo.mkdir(parents=True)

        paths = _resolve_include_paths(repo)
        self.assertEqual(len(paths), 1)
        self.assertEqual(paths[0], repo)


class TestReadDepDependencies(unittest.TestCase):
    """_read_dep_dependencies — 传递依赖读取"""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_with_dependencies(self):
        """有 [dependencies] → 返回 specs"""
        repo = self.tmp / "has-deps"
        repo.mkdir(parents=True)
        (repo / "dovetail.toml").write_text(textwrap.dedent("""\
            [package]
            name = "lib"
            version = "1.0.0"
            [build]
            entry = "src/main.mcdl"
            [dependencies]
            other = { git = "https://example.com/other.git", tag = "v1" }
        """), encoding="utf-8")

        specs = _read_dep_dependencies(repo)
        self.assertEqual(len(specs), 1)
        self.assertEqual(specs[0].name, "other")

    def test_without_dependencies(self):
        """无 [dependencies] → 空列表"""
        repo = self.tmp / "no-deps"
        repo.mkdir(parents=True)
        (repo / "dovetail.toml").write_text(textwrap.dedent("""\
            [package]
            name = "lib"
            version = "1.0.0"
            [build]
            entry = "src/main.mcdl"
        """), encoding="utf-8")

        specs = _read_dep_dependencies(repo)
        self.assertEqual(len(specs), 0)

    def test_without_toml(self):
        """无 dovetail.toml → 空列表"""
        repo = self.tmp / "no-toml"
        repo.mkdir(parents=True)

        specs = _read_dep_dependencies(repo)
        self.assertEqual(len(specs), 0)


class TestLockfile(unittest.TestCase):
    """lock 文件读写"""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.project = self.tmp / "project"
        self.project.mkdir()

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_empty_lock(self):
        """首次 → 空 lock"""
        lock = load_lock(self.project)
        self.assertEqual(len(lock), 0)

    def test_write_and_read(self):
        """写入后读回一致"""
        resolved = [
            ResolvedDependency(
                name="my-lib",
                git="https://example.com/lib.git",
                tag="v1.0.0",
                resolved="a1b2c3d4e5f6789012345678abcdef1234567890",
                local_path=Path("/tmp/lib"),
            ),
        ]
        write_lock(self.project, resolved)
        self.assertTrue((self.project / LOCK_FILENAME).exists())

        lock = load_lock(self.project)
        self.assertEqual(lock.get("my-lib"), "a1b2c3d4e5f6789012345678abcdef1234567890")

    def test_write_empty_skipped(self):
        """空依赖列表不写入 lock"""
        write_lock(self.project, [])
        self.assertFalse((self.project / LOCK_FILENAME).exists())

    def test_branch_in_lock(self):
        """branch 引用写入 lock"""
        resolved = [
            ResolvedDependency(
                name="my-lib",
                git="https://example.com/lib.git",
                branch="main",
                resolved="a1b2c3d4e5f6789012345678abcdef1234567890",
                local_path=Path("/tmp/lib"),
            ),
        ]
        write_lock(self.project, resolved)

        lock = load_lock(self.project)
        self.assertIn("my-lib", lock)


class TestResolvedDependencyProperties(unittest.TestCase):
    """ResolvedDependency 属性"""

    def test_tag_ref(self):
        r = ResolvedDependency(name="x", git="url", tag="v1", resolved="abc")
        self.assertEqual(r.ref, "v1")
        self.assertEqual(r.ref_type, "tag")
        self.assertFalse(r.is_mutable)

    def test_branch_ref(self):
        r = ResolvedDependency(name="x", git="url", branch="main", resolved="abc")
        self.assertEqual(r.ref, "main")
        self.assertEqual(r.ref_type, "branch")
        self.assertTrue(r.is_mutable)

    def test_rev_ref(self):
        r = ResolvedDependency(name="x", git="url", rev="a1b2c3", resolved="a1b2c3")
        self.assertEqual(r.ref, "a1b2c3")
        self.assertEqual(r.ref_type, "rev")
        self.assertFalse(r.is_mutable)

    def test_to_lock_entry_tag(self):
        r = ResolvedDependency(name="x", git="url", tag="v1", resolved="abc")
        entry = r.to_lock_entry()
        self.assertEqual(entry["name"], "x")
        self.assertEqual(entry["git"], "url")
        self.assertEqual(entry["tag"], "v1")
        self.assertEqual(entry["resolved"], "abc")
        self.assertNotIn("branch", entry)
        self.assertNotIn("rev", entry)

    def test_to_lock_entry_branch(self):
        r = ResolvedDependency(name="x", git="url", branch="main", resolved="abc")
        entry = r.to_lock_entry()
        self.assertIn("branch", entry)
        self.assertNotIn("tag", entry)

    def test_to_lock_entry_rev(self):
        r = ResolvedDependency(name="x", git="url", rev="a1b2", resolved="abc")
        entry = r.to_lock_entry()
        self.assertIn("rev", entry)
        self.assertNotIn("tag", entry)


class TestEmptyDependencies(unittest.TestCase):
    """resolve_all — 空依赖"""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.project = self.tmp / "project"
        self.project.mkdir()

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_empty_list(self):
        result = resolve_all([], self.project, "lib")
        self.assertEqual(len(result), 0)


# ── 入口 ──────────────────────────────────────────────────────

if __name__ == "__main__":
    unittest.main()
