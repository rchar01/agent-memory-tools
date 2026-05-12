from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from .markdown import parse_entry_file
from .models import MemoryEntry
from .paths import atomic_write, entries_dir, index_path


@dataclass
class IndexRecord:
    id: str
    file: str
    project: str
    tags: list[str]
    importance: float
    summary: str


def active_entries(memory_dir: Path) -> list[MemoryEntry]:
    result = []
    for path in sorted(entries_dir(memory_dir).glob("*.md")):
        entry = parse_entry_file(path)
        if entry.status == "active":
            result.append(entry)
    return result


def regenerate_index(memory_dir: Path) -> None:
    atomic_write(index_path(memory_dir), render_index(active_entries(memory_dir)))


def render_index(entries: list[MemoryEntry]) -> str:
    lines = ["# Memory Index", "", "## Active Memories", ""]
    for entry in sorted(entries, key=lambda item: (item.project, item.id)):
        summary = one_line(entry.summary, 180)
        lines.extend(
            [
                f"### {entry.id}",
                "",
                f"File: `entries/{entry.filename}`  ",
                f"Project: `{entry.project}`  ",
                f"Tags: `{', '.join(entry.tags)}`  ",
                f"Importance: `{entry.importance:g}`  ",
                f"Summary: {summary}",
                "",
                "---",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def parse_index(memory_dir: Path) -> list[IndexRecord]:
    path = index_path(memory_dir)
    if not path.exists():
        return []
    text = path.read_text(encoding="utf-8")
    records: list[IndexRecord] = []
    blocks = re.split(r"^###\s+", text, flags=re.M)[1:]
    for block in blocks:
        lines = block.splitlines()
        if not lines:
            continue
        ident = lines[0].strip()
        data = {"id": ident, "file": "", "project": "", "tags": [], "importance": 0.0, "summary": ""}
        for line in lines[1:]:
            if ":" not in line:
                continue
            key, value = line.split(":", 1)
            key = key.strip().lower()
            value = value.strip().strip("`").rstrip("  ").strip()
            value = value.replace("`", "")
            if key == "file":
                data["file"] = value
            elif key == "project":
                data["project"] = value
            elif key == "tags":
                data["tags"] = [tag.strip() for tag in value.split(",") if tag.strip()]
            elif key == "importance":
                try:
                    data["importance"] = float(value)
                except ValueError:
                    data["importance"] = 0.0
            elif key == "summary":
                data["summary"] = value
        records.append(IndexRecord(**data))
    return records


def one_line(text: str, limit: int) -> str:
    compact = " ".join((text or "").split())
    if len(compact) <= limit:
        return compact
    return compact[: max(0, limit - 3)].rstrip() + "..."
