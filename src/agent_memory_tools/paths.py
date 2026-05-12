from __future__ import annotations

import os
import tempfile
from contextlib import contextmanager
from pathlib import Path

try:
    import fcntl
except ImportError:  # pragma: no cover - Linux is the target platform.
    fcntl = None


DEFAULT_MEMORY_DIR = Path.home() / ".local" / "share" / "agent-memory-tools" / "memory"


def resolve_memory_dir(value: str | None = None) -> Path:
    raw = value or os.environ.get("AGENT_MEMORY_DIR")
    return Path(raw).expanduser().resolve() if raw else DEFAULT_MEMORY_DIR


def entries_dir(memory_dir: Path) -> Path:
    return memory_dir / "entries"


def archive_dir(memory_dir: Path) -> Path:
    return memory_dir / "archive"


def index_path(memory_dir: Path) -> Path:
    return memory_dir / "INDEX.md"


def readme_path(memory_dir: Path) -> Path:
    return memory_dir / "README.md"


def ensure_memory_tree(memory_dir: Path) -> None:
    memory_dir.mkdir(parents=True, exist_ok=True)
    entries_dir(memory_dir).mkdir(parents=True, exist_ok=True)
    archive_dir(memory_dir).mkdir(parents=True, exist_ok=True)


@contextmanager
def memory_lock(memory_dir: Path):
    ensure_memory_tree(memory_dir)
    lock_path = memory_dir / ".memory.lock"
    with open(lock_path, "a+", encoding="utf-8") as lock_file:
        if fcntl is not None:
            fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX)
        try:
            yield
        finally:
            if fcntl is not None:
                fcntl.flock(lock_file.fileno(), fcntl.LOCK_UN)


def atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=str(path.parent))
    tmp_path = Path(tmp_name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            fh.write(content)
            fh.flush()
            os.fsync(fh.fileno())
        os.replace(tmp_path, path)
    except BaseException:
        try:
            tmp_path.unlink()
        except OSError:
            pass
        raise
