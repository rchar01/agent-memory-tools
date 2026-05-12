from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path

from .index import IndexRecord, one_line, parse_index
from .markdown import parse_entry_file
from .models import MemoryEntry, normalize_list


@dataclass
class RetrievedMemory:
    entry: MemoryEntry
    score: float


def retrieve_memories(memory_dir: Path, *, query: str, project: str = "", tags: str = "", limit: int = 3) -> list[RetrievedMemory]:
    records = parse_index(memory_dir)
    query_terms = tokenize(query)
    requested_tags = set(normalize_list(tags))
    scored: list[tuple[float, IndexRecord]] = []
    for record in records:
        score = score_record(record, query_terms=query_terms, project=project, tags=requested_tags)
        if score > 0:
            scored.append((score, record))
    scored.sort(key=lambda item: item[0], reverse=True)
    results: list[RetrievedMemory] = []
    for score, record in scored[: max(1, min(limit, 5))]:
        path = memory_dir / record.file
        if not path.exists():
            continue
        entry = parse_entry_file(path)
        if entry.status != "active":
            continue
        score += recency_bonus(entry.updated)
        results.append(RetrievedMemory(entry=entry, score=score))
    results.sort(key=lambda item: item.score, reverse=True)
    return results[: max(1, min(limit, 5))]


def score_record(record: IndexRecord, *, query_terms: set[str], project: str, tags: set[str]) -> float:
    record_tags = set(record.tags)
    text = " ".join([record.id, record.project, record.summary, " ".join(record.tags)]).lower()
    score = record.importance * 2.0
    if project and record.project == project:
        score += 5.0
    elif project and project in record_tags:
        score += 2.5
    tag_matches = len(record_tags & tags)
    score += tag_matches * 3.0
    keyword_matches = sum(1 for term in query_terms if term in text)
    score += keyword_matches * 1.25
    if not project and not tags and not query_terms:
        return score
    return score if (tag_matches or keyword_matches or (project and (record.project == project or project in record_tags))) else 0.0


def render_brief(results: list[RetrievedMemory]) -> str:
    if not results:
        return "# Relevant Memories\n\nNo relevant active memories found.\n"
    lines = ["# Relevant Memories", ""]
    for item in results:
        entry = item.entry
        lines.extend(
            [
                f"## {entry.id}",
                "",
                f"Project: {entry.project}  ",
                f"Tags: {', '.join(entry.tags)}  ",
                f"Importance: {entry.importance:g}  ",
                f"Score: {item.score:.2f}",
                "",
                one_line(entry.summary, 300),
            ]
        )
        if entry.decisions or entry.impact:
            lines.extend(["", "Important:"])
            for value in (entry.decisions + entry.impact)[:5]:
                lines.append(f"- {value}")
        if entry.important_files:
            lines.extend(["", "Files:"])
            for value in entry.important_files[:5]:
                lines.append(f"- `{value}`")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def tokenize(query: str) -> set[str]:
    return {token for token in re.findall(r"[a-z0-9][a-z0-9-]{2,}", (query or "").lower())}


def recency_bonus(updated: str) -> float:
    try:
        days = (date.today() - date.fromisoformat(updated[:10])).days
    except Exception:
        return 0.0
    if days <= 7:
        return 0.5
    if days <= 30:
        return 0.25
    return 0.0
