from __future__ import annotations

import shutil
from collections import defaultdict
from datetime import date
from pathlib import Path

from .index import regenerate_index
from .markdown import parse_entry_file, render_entry
from .paths import archive_dir, atomic_write, entries_dir, ensure_memory_tree, memory_lock


def find_duplicates(memory_dir: Path) -> list[str]:
    entries = []
    for path in sorted(entries_dir(memory_dir).glob("*.md")):
        entry = parse_entry_file(path)
        if entry.status == "active":
            entries.append(entry)
    by_summary: dict[str, list[str]] = defaultdict(list)
    for entry in entries:
        key = " ".join(entry.summary.lower().split())
        if key:
            by_summary[key].append(entry.id)
    findings = []
    for ids in by_summary.values():
        if len(ids) > 1:
            findings.append("duplicate summary: " + ", ".join(ids))
    for idx, left in enumerate(entries):
        for right in entries[idx + 1 :]:
            if left.project != right.project:
                continue
            overlap = set(left.tags) & set(right.tags)
            if len(overlap) >= 2:
                findings.append(f"possible overlap ({left.project}, tags {', '.join(sorted(overlap))}): {left.id}, {right.id}")
    return findings


def archive_memory(memory_dir: Path, memory_id: str, *, reason: str = "") -> Path:
    with memory_lock(memory_dir):
        ensure_memory_tree(memory_dir)
        source = entries_dir(memory_dir) / f"{memory_id}.md"
        if not source.exists():
            raise FileNotFoundError(f"active memory not found: {memory_id}")
        entry = parse_entry_file(source)
        entry.status = "archived"
        entry.updated = date.today().isoformat()
        if reason:
            entry.notes = (entry.notes + "\n\n" if entry.notes else "") + f"Archived: {reason}"
        month_dir = archive_dir(memory_dir) / date.today().strftime("%Y-%m")
        month_dir.mkdir(parents=True, exist_ok=True)
        target = month_dir / source.name
        if target.exists():
            raise FileExistsError(f"archive target already exists: {target}")
        atomic_write(source, render_entry(entry))
        shutil.move(str(source), str(target))
        regenerate_index(memory_dir)
        return target


def supersede_memory(memory_dir: Path, old_id: str, new_id: str) -> None:
    with memory_lock(memory_dir):
        source = entries_dir(memory_dir) / f"{old_id}.md"
        if not source.exists():
            raise FileNotFoundError(f"memory not found: {old_id}")
        if not (entries_dir(memory_dir) / f"{new_id}.md").exists():
            raise FileNotFoundError(f"superseding memory not found: {new_id}")
        entry = parse_entry_file(source)
        entry.status = "superseded"
        entry.superseded_by = new_id
        entry.updated = date.today().isoformat()
        atomic_write(source, render_entry(entry))
        regenerate_index(memory_dir)
