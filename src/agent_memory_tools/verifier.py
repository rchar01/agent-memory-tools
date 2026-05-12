from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from .index import parse_index
from .markdown import parse_entry_file
from .models import MemoryEntry
from .paths import entries_dir, index_path
from .security import scan_text


@dataclass
class VerificationResult:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors


def verify_memory(memory_dir: Path) -> VerificationResult:
    result = VerificationResult()
    entries = _load_entries(memory_dir, result)
    _verify_entries(entries, result)
    _verify_index(memory_dir, entries, result)
    return result


def _load_entries(memory_dir: Path, result: VerificationResult) -> list[MemoryEntry]:
    loaded: list[MemoryEntry] = []
    for path in sorted(entries_dir(memory_dir).glob("*.md")):
        try:
            entry = parse_entry_file(path)
            loaded.append(entry)
        except Exception as exc:
            result.errors.append(f"{path}: failed to parse entry: {exc}")
    return loaded


def _verify_entries(entries: list[MemoryEntry], result: VerificationResult) -> None:
    seen: dict[str, Path] = {}
    for entry in entries:
        label = str(entry.path or entry.id)
        for error in entry.validation_errors(require_active_file=True):
            result.errors.append(f"{label}: {error}")
        if entry.id in seen:
            result.errors.append(f"{label}: duplicate id also used by {seen[entry.id]}")
        elif entry.path:
            seen[entry.id] = entry.path
        if entry.path and entry.status == "archived":
            result.errors.append(f"{label}: archived entries should be moved out of entries/")
        if entry.path:
            text = entry.path.read_text(encoding="utf-8")
            for issue in scan_text(text):
                result.errors.append(f"{label}: {issue}")
        if len(entry.summary) > 220:
            result.warnings.append(f"{label}: summary is longer than 220 chars")


def _verify_index(memory_dir: Path, entries: list[MemoryEntry], result: VerificationResult) -> None:
    path = index_path(memory_dir)
    if not path.exists():
        result.errors.append(f"{path}: INDEX.md is missing")
        return
    records = parse_index(memory_dir)
    active = {entry.id: entry for entry in entries if entry.status == "active"}
    indexed = {record.id: record for record in records}
    for ident, entry in active.items():
        if ident not in indexed:
            result.errors.append(f"INDEX.md: active entry {ident} is missing from index")
            continue
        record = indexed[ident]
        if record.file != f"entries/{entry.filename}":
            result.errors.append(f"INDEX.md: {ident} file path does not match entry filename")
        if record.project != entry.project:
            result.errors.append(f"INDEX.md: {ident} project does not match frontmatter")
        if set(record.tags) != set(entry.tags):
            result.errors.append(f"INDEX.md: {ident} tags do not match frontmatter")
        if not 0 <= record.importance <= 1:
            result.errors.append(f"INDEX.md: {ident} importance must be between 0 and 1")
    for ident, record in indexed.items():
        file_path = memory_dir / record.file
        if ident not in active:
            result.errors.append(f"INDEX.md: index row {ident} has no active entry")
        if not file_path.exists():
            result.errors.append(f"INDEX.md: {ident} points to missing file {record.file}")
