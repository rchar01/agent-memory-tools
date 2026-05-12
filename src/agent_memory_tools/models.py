from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Any


VALID_STATUSES = {"active", "superseded", "archived"}
ID_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


@dataclass
class MemoryEntry:
    id: str
    project: str
    tags: list[str]
    importance: float
    summary: str
    title: str
    status: str = "active"
    created: str = field(default_factory=lambda: date.today().isoformat())
    updated: str = field(default_factory=lambda: date.today().isoformat())
    decisions: list[str] = field(default_factory=list)
    impact: list[str] = field(default_factory=list)
    related_projects: list[str] = field(default_factory=list)
    important_files: list[str] = field(default_factory=list)
    retrieve_when: list[str] = field(default_factory=list)
    notes: str = ""
    superseded_by: str = ""
    path: Path | None = None

    @property
    def filename(self) -> str:
        return f"{self.id}.md"

    @property
    def relative_path(self) -> str:
        if self.status == "archived" and self.path is not None:
            return str(self.path)
        return f"entries/{self.filename}"

    @classmethod
    def from_mapping(cls, data: dict[str, Any]) -> "MemoryEntry":
        tags = normalize_list(data.get("tags"))
        return cls(
            id=str(data.get("id", "")).strip(),
            project=str(data.get("project", "")).strip(),
            tags=tags,
            importance=float(data.get("importance", 0)),
            summary=str(data.get("summary", "")).strip(),
            title=str(data.get("title") or data.get("heading") or data.get("summary", "")).strip(),
            status=str(data.get("status", "active")).strip() or "active",
            created=str(data.get("created") or date.today().isoformat()).strip(),
            updated=str(data.get("updated") or date.today().isoformat()).strip(),
            decisions=plain_list(data.get("decisions")),
            impact=plain_list(data.get("impact")),
            related_projects=plain_list(data.get("related_projects") or data.get("related projects")),
            important_files=plain_list(data.get("important_files") or data.get("important files")),
            retrieve_when=plain_list(data.get("retrieve_when") or data.get("when_to_retrieve") or data.get("when to retrieve")),
            notes=str(data.get("notes", "")).strip(),
            superseded_by=str(data.get("superseded_by", "")).strip(),
        )

    def validation_errors(self, *, require_active_file: bool = False) -> list[str]:
        errors: list[str] = []
        if not ID_RE.match(self.id):
            errors.append("id must be stable kebab-case")
        if not self.project:
            errors.append("project is required")
        if not self.tags:
            errors.append("at least one tag is required")
        if any(not ID_RE.match(tag) for tag in self.tags):
            errors.append("tags must be lowercase kebab-case values")
        if not 0 <= self.importance <= 1:
            errors.append("importance must be between 0 and 1")
        if self.status not in VALID_STATUSES:
            errors.append("status must be active, superseded, or archived")
        if not self.summary:
            errors.append("summary is required")
        if not self.title:
            errors.append("title is required")
        if require_active_file and self.status == "active" and self.path and self.path.name != self.filename:
            errors.append("active entry filename must match id")
        return errors


def normalize_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        if not value.strip():
            return []
        if "," in value:
            items = value.split(",")
        else:
            items = [value]
    elif isinstance(value, (list, tuple, set)):
        items = list(value)
    else:
        items = [value]
    normalized = []
    for item in items:
        text = str(item).strip().lower().replace("_", "-")
        text = re.sub(r"[^a-z0-9-]+", "-", text)
        text = re.sub(r"-+", "-", text).strip("-")
        if text and text not in normalized:
            normalized.append(text)
    return normalized


def plain_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        items = [value]
    elif isinstance(value, (list, tuple, set)):
        items = list(value)
    else:
        items = [value]
    result = []
    for item in items:
        text = str(item).strip()
        if text and text not in result:
            result.append(text)
    return result
