from __future__ import annotations

import re


SECRET_PATTERNS = [
    (re.compile(r"-----BEGIN (?:RSA |OPENSSH |EC |DSA )?PRIVATE KEY-----"), "private key"),
    (re.compile(r"\b(?:api[_-]?key|token|secret|password)\s*[:=]\s*['\"]?[A-Za-z0-9_./+=-]{16,}", re.I), "credential assignment"),
    (re.compile(r"\b[A-Za-z0-9_]{20,}\.[A-Za-z0-9_]{20,}\.[A-Za-z0-9_/-]{20,}\b"), "jwt-like token"),
    (re.compile(r"\b(?:sk|pk|ghp|github_pat|xoxb|xoxp|AKIA)[A-Za-z0-9_/-]{16,}\b"), "api token"),
]

INJECTION_PATTERNS = [
    (re.compile(r"ignore\s+(?:previous|all|above|prior)\s+instructions", re.I), "prompt injection"),
    (re.compile(r"disregard\s+(?:your|all|any)\s+(?:instructions|rules|guidelines)", re.I), "prompt injection"),
    (re.compile(r"you\s+are\s+now\s+", re.I), "role hijack"),
    (re.compile(r"system\s+prompt\s+override", re.I), "system prompt override"),
]

INVISIBLE_CHARS = {"\u200b", "\u200c", "\u200d", "\u2060", "\ufeff", "\u202a", "\u202b", "\u202c", "\u202d", "\u202e"}


def scan_text(text: str) -> list[str]:
    issues: list[str] = []
    for char in INVISIBLE_CHARS:
        if char in text:
            issues.append(f"contains invisible unicode U+{ord(char):04X}")
    for pattern, label in SECRET_PATTERNS:
        if pattern.search(text):
            issues.append(f"possible secret: {label}")
    for pattern, label in INJECTION_PATTERNS:
        if pattern.search(text):
            issues.append(f"possible prompt attack: {label}")
    if _looks_like_giant_diff(text):
        issues.append("appears to contain a large diff")
    if _looks_like_giant_log(text):
        issues.append("appears to contain a large terminal log")
    return issues


def _looks_like_giant_diff(text: str) -> bool:
    lines = text.splitlines()
    if len(lines) < 40:
        return False
    diffish = sum(1 for line in lines if line.startswith(("+", "-", "@@", "diff --git")))
    return diffish >= 25


def _looks_like_giant_log(text: str) -> bool:
    lines = text.splitlines()
    if len(lines) < 80:
        return False
    noisy = sum(1 for line in lines if re.search(r"\b(?:traceback|error|warning|debug|info|npm|pytest|stack)\b", line, re.I))
    return noisy >= 30
