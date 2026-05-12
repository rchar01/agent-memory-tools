from __future__ import annotations

from pathlib import Path

from .index import regenerate_index
from .markdown import render_entry
from .models import MemoryEntry
from .paths import atomic_write, entries_dir, ensure_memory_tree, memory_lock
from .security import scan_text
from .verifier import verify_memory


def write_memory(memory_dir: Path, entry: MemoryEntry) -> None:
    errors = entry.validation_errors()
    if errors:
        raise ValueError("invalid memory entry: " + "; ".join(errors))
    rendered = render_entry(entry)
    issues = scan_text(rendered)
    if issues:
        raise ValueError("memory entry failed safety checks: " + "; ".join(issues))
    with memory_lock(memory_dir):
        ensure_memory_tree(memory_dir)
        target = entries_dir(memory_dir) / entry.filename
        if target.exists():
            raise FileExistsError(f"memory id already exists: {entry.id}")
        atomic_write(target, rendered)
        regenerate_index(memory_dir)
        verification = verify_memory(memory_dir)
        if not verification.ok:
            raise RuntimeError("memory verification failed after write: " + "; ".join(verification.errors))
