from __future__ import annotations

import tarfile
from datetime import datetime, timezone
from pathlib import Path

from .paths import ensure_memory_tree


def create_backup(memory_dir: Path, output: str | None = None) -> Path:
    """Create a gzipped tar archive of the memory directory."""
    ensure_memory_tree(memory_dir)
    target = resolve_backup_path(memory_dir, output)
    target.parent.mkdir(parents=True, exist_ok=True)
    with tarfile.open(target, "w:gz") as archive:
        archive.add(memory_dir, arcname="memory")
    return target


def resolve_backup_path(memory_dir: Path, output: str | None = None) -> Path:
    if output:
        path = Path(output).expanduser()
        if path.exists() and path.is_dir():
            return path / default_backup_name()
        if str(output).endswith(('/', '\\')):
            return path / default_backup_name()
        if path.suffix not in {".gz", ".tgz"}:
            return path / default_backup_name()
        return path
    return memory_dir.parent / "backups" / default_backup_name()


def default_backup_name() -> str:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%SZ")
    return f"agent-memory-backup-{stamp}.tar.gz"
