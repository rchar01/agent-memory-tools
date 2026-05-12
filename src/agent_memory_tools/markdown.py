from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from .models import MemoryEntry


def parse_input_file(path: Path) -> MemoryEntry:
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".json":
        return MemoryEntry.from_mapping(json.loads(text))
    if text.lstrip().startswith("---"):
        entry = parse_entry_text(text)
        entry.path = path
        return entry
    return MemoryEntry.from_mapping(parse_simple_mapping(text))


def parse_entry_file(path: Path) -> MemoryEntry:
    entry = parse_entry_text(path.read_text(encoding="utf-8"))
    entry.path = path
    return entry


def parse_entry_text(text: str) -> MemoryEntry:
    meta, body = split_frontmatter(text)
    sections = extract_sections(body)
    data: dict[str, Any] = dict(meta)
    title = extract_title(body)
    if title:
        data.setdefault("title", title)
    data.setdefault("summary", first_paragraph(sections.get("summary", "")))
    data.setdefault("decisions", bullets(sections.get("decisions", "")))
    data.setdefault("impact", bullets(sections.get("impact", "")))
    data.setdefault("related_projects", bullets(sections.get("related projects", "")))
    data.setdefault("important_files", bullets(sections.get("important files", "")))
    data.setdefault("retrieve_when", bullets(sections.get("when to retrieve this memory", "")))
    data.setdefault("notes", sections.get("notes", "").strip())
    return MemoryEntry.from_mapping(data)


def split_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, text
    for idx in range(1, len(lines)):
        if lines[idx].strip() == "---":
            return parse_simple_mapping("\n".join(lines[1:idx])), "\n".join(lines[idx + 1 :]).strip()
    return {}, text


def parse_simple_mapping(text: str) -> dict[str, Any]:
    data: dict[str, Any] = {}
    current_key: str | None = None
    for raw in text.splitlines():
        line = raw.rstrip()
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        stripped = line.strip()
        if current_key and stripped.startswith("- "):
            data.setdefault(current_key, []).append(parse_scalar(stripped[2:].strip()))
            continue
        if ":" not in stripped:
            current_key = None
            continue
        key, value = stripped.split(":", 1)
        key = key.strip().replace("-", "_")
        value = value.strip()
        if value == "":
            data[key] = []
            current_key = key
        else:
            data[key] = parse_scalar(value)
            current_key = None
    return data


def parse_scalar(value: str) -> Any:
    value = value.strip()
    if value in {"[]", ""}:
        return []
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        if not inner:
            return []
        return [parse_scalar(part.strip()) for part in inner.split(",")]
    if (value.startswith("'") and value.endswith("'")) or (value.startswith('"') and value.endswith('"')):
        return value[1:-1]
    if value.lower() in {"true", "false"}:
        return value.lower() == "true"
    try:
        if re.match(r"^-?\d+(?:\.\d+)?$", value):
            return float(value) if "." in value else int(value)
    except ValueError:
        pass
    return value


def render_entry(entry: MemoryEntry) -> str:
    frontmatter = [
        "---",
        f"id: {entry.id}",
        f"project: {entry.project}",
        f"tags: [{', '.join(entry.tags)}]",
        f"importance: {entry.importance:g}",
        f"created: {entry.created}",
        f"updated: {entry.updated}",
        f"status: {entry.status}",
    ]
    if entry.superseded_by:
        frontmatter.append(f"superseded_by: {entry.superseded_by}")
    frontmatter.append("---")
    parts = ["\n".join(frontmatter), "", f"# {entry.title}", "", "## Summary", "", entry.summary]
    parts.extend(render_list_section("Decisions", entry.decisions))
    parts.extend(render_list_section("Impact", entry.impact))
    parts.extend(render_list_section("Related projects", entry.related_projects))
    parts.extend(render_list_section("Important files", entry.important_files))
    parts.extend(render_list_section("When to retrieve this memory", entry.retrieve_when))
    if entry.notes:
        parts.extend(["", "## Notes", "", entry.notes])
    return "\n".join(parts).rstrip() + "\n"


def render_list_section(title: str, items: list[str]) -> list[str]:
    if not items:
        return []
    return ["", f"## {title}", "", *[f"- {item}" for item in items]]


def extract_title(body: str) -> str:
    for line in body.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return ""


def extract_sections(body: str) -> dict[str, str]:
    sections: dict[str, list[str]] = {}
    current: str | None = None
    for line in body.splitlines():
        if line.startswith("## "):
            current = line[3:].strip().lower()
            sections[current] = []
            continue
        if current:
            sections[current].append(line)
    return {key: "\n".join(value).strip() for key, value in sections.items()}


def first_paragraph(text: str) -> str:
    for block in re.split(r"\n\s*\n", text.strip()):
        block = block.strip()
        if block:
            return " ".join(block.split())
    return ""


def bullets(text: str) -> list[str]:
    items = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("- "):
            items.append(stripped[2:].strip())
    return items
